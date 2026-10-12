#!/usr/bin/env python3
"""Check a source-anchored contract against annotated final prompt clauses, offline.

Annotations are semantic judgments supplied by an author/reviewer, not trusted
proof of entailment. Clean input returns REVIEW_REQUIRED, never a semantic PASS.
No model, network, repository access or execution of prompt instructions occurs.
"""
import argparse
import json
import re
import sys
from pathlib import Path

CLASSES = {'EXPLICIT_REQUIRED', 'EXPLICIT_OPTIONAL', 'INFERRED', 'UNRESOLVED', 'FORBIDDEN'}
KINDS = {'GOAL', 'CONSTRAINT', 'AUTHORITY', 'COMPLETION', 'CONTEXT', 'FORMAT'}
MODALITIES = {'REQUIRED', 'OPTIONAL', 'FORBIDDEN', 'UNRESOLVED', 'CONTEXT'}
RELATIONS = {'PRESERVES', 'DECOMPOSES', 'CLARIFIES', 'SUGGESTS', 'CONTRADICTS', 'NOVEL', 'FORMAT'}


def _string(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be a nonempty string')
    return value


def _strings(value, label):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError(f'{label} must be a list of nonempty strings')
    if len(set(value)) != len(value):
        raise ValueError(f'{label} contains duplicate entries')
    return value


def check(document):
    if not isinstance(document, dict) or document.get('schema_version') != 1:
        raise ValueError('Expected schema_version 1 comparison object')
    original = _string(document.get('original'), 'original')
    final = _string(document.get('final_prompt'), 'final_prompt')
    outcome = document.get('outcome', 'REVISED')
    if outcome not in {'REVISED', 'UNCHANGED'}:
        raise ValueError('Invalid outcome; expected REVISED or UNCHANGED')
    requirements = document.get('requirements')
    clauses = document.get('clauses')
    if not isinstance(requirements, list) or not requirements or not isinstance(clauses, list):
        raise ValueError('requirements must be nonempty; clauses must be a list')
    by_id = {}
    for row in requirements:
        if not isinstance(row, dict):
            raise ValueError('Requirement must be an object')
        identifier = _string(row.get('id'), 'requirement id')
        if identifier in by_id or row.get('classification') not in CLASSES or row.get('kind') not in KINDS:
            raise ValueError('Duplicate id or invalid requirement classification/kind')
        quote = row.get('quote')
        if row['classification'] == 'INFERRED' and not quote:
            _string(row.get('reason'), 'inference reason')
        elif _string(quote, 'source quote') not in original:
            raise ValueError(f'Source quote for {identifier} is absent from original')
        _strings(row.get('actions', []), 'actions')
        if row.get('actions') and row['kind'] != 'AUTHORITY':
            raise ValueError('Only AUTHORITY requirements may declare actions')
        exact = row.get('preserve_exact', False)
        if not isinstance(exact, bool) or (exact and row['classification'] not in {'EXPLICIT_REQUIRED', 'FORBIDDEN'}):
            raise ValueError('preserve_exact must be boolean and anchored to an explicit invariant')
        by_id[identifier] = row

    findings = []
    covered = set()
    cursor = 0

    def flag(code, clause=None, requirement=None):
        finding = {'code': code}
        if clause is not None:
            finding['clause'] = clause
        if requirement is not None:
            finding['requirement'] = requirement
        findings.append(finding)

    if outcome == 'UNCHANGED' and final != original:
        flag('FALSE_NO_CHANGE')
    for row in requirements:
        if row.get('preserve_exact') and row['quote'] not in final:
            flag('CHANGED_IMMUTABLE_TEXT', requirement=row['id'])

    for index, clause in enumerate(clauses):
        if not isinstance(clause, dict):
            raise ValueError('Clause must be an object')
        text = _string(clause.get('text'), 'clause text')
        modality, relation, kind = (clause.get(key) for key in ('modality', 'relation', 'kind'))
        if modality not in MODALITIES or relation not in RELATIONS or kind not in KINDS:
            raise ValueError('Invalid clause modality/relation/kind')
        supports = _strings(clause.get('supports'), 'supports')
        if any(identifier not in by_id for identifier in supports):
            raise ValueError('Clause cites an unknown requirement')
        if relation in {'DECOMPOSES', 'CLARIFIES'}:
            _string(clause.get('reason'), 'decomposition/clarification reason')
        start = final.find(text, cursor)
        if start < 0:
            raise ValueError('Clause text absent, reordered or overlapping in final_prompt')
        if final[cursor:start].strip():
            flag('UNANNOTATED_TEXT', index)
        cursor = start + len(text)
        source_rows = [by_id[identifier] for identifier in supports]
        if relation == 'FORMAT':
            if kind != 'FORMAT' or modality != 'CONTEXT' or supports or clause.get('external_action') or clause.get('action'):
                raise ValueError('FORMAT is reserved for nonoperative headings/layout')
            continue

        mandatory = modality in {'REQUIRED', 'FORBIDDEN'}
        unsupported = not supports or relation in {'SUGGESTS', 'NOVEL'}
        if mandatory and unsupported:
            flag('NEW_REQUIREMENT', index)
        if kind == 'COMPLETION' and modality == 'REQUIRED':
            source_numbers = set(re.findall(r'\d+(?:\.\d+)?', ' '.join(row.get('quote') or '' for row in source_rows)))
            novel_numbers = set(re.findall(r'\d+(?:\.\d+)?', text)) - source_numbers
            if unsupported or novel_numbers:
                flag('INVENTED_COMPLETION_CRITERION', index)
        if relation == 'CONTRADICTS':
            flag('CONTRADICTORY_INSTRUCTION', index)
        if modality == 'OPTIONAL' and relation in {'SUGGESTS', 'NOVEL'}:
            # This checks an observable label, not the truth of the annotation.
            if not re.match(r'(?i)^\s*(?:[-*]\s*)?Optional(?: suggestion)?\s*:', text):
                flag('UNMARKED_SUGGESTION', index)

        for row in source_rows:
            classification = row['classification']
            if classification == 'EXPLICIT_OPTIONAL' and mandatory:
                flag('STRENGTHENED_OPTIONAL', index, row['id'])
            if classification in {'INFERRED', 'UNRESOLVED'} and mandatory:
                flag('NEW_REQUIREMENT', index, row['id'])
            if (classification == 'FORBIDDEN' and modality == 'REQUIRED') or (
                classification == 'EXPLICIT_REQUIRED' and modality == 'FORBIDDEN'
            ):
                flag('CONTRADICTORY_INSTRUCTION', index, row['id'])
            if relation in {'PRESERVES', 'DECOMPOSES', 'CLARIFIES'}:
                if classification == 'EXPLICIT_REQUIRED' and modality == 'REQUIRED':
                    covered.add(row['id'])
                if classification == 'FORBIDDEN' and modality == 'FORBIDDEN':
                    covered.add(row['id'])

        for action_field in ('action', 'external_action'):
            action = clause.get(action_field)
            if action is None:
                continue
            _string(action, action_field)
            allowed = any(row['classification'] in {'EXPLICIT_REQUIRED', 'EXPLICIT_OPTIONAL'} and row['kind'] == 'AUTHORITY'
                          and action in row.get('actions', []) for row in source_rows)
            if modality in {'REQUIRED', 'OPTIONAL'} and not allowed:
                flag('UNAUTHORIZED_EXTERNAL_ACTION' if action_field == 'external_action' else 'UNAUTHORIZED_ACTION', index)

    if final[cursor:].strip():
        flag('UNANNOTATED_TEXT')
    for row in requirements:
        if row['id'] not in covered and row['classification'] in {'EXPLICIT_REQUIRED', 'FORBIDDEN'}:
            flag('OMITTED_FORBIDDEN' if row['classification'] == 'FORBIDDEN' else 'OMITTED_REQUIRED',
                 requirement=row['id'])
    return {
        'schema_version': 1,
        'status': 'DRIFT' if findings else 'REVIEW_REQUIRED',
        'outcome': outcome,
        'semantic_validation': 'NOT_ESTABLISHED',
        'findings': findings,
        'covered_requirements': sorted(covered),
        'prompt_chars': len(final),
        'prompt_words': len(final.split()),
        'limitation': 'Review extraction completeness, clause modality, claimed entailment, action annotations and contradictions against the actual texts.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('comparison', help='Comparison JSON file, or - for stdin')
    args = parser.parse_args()
    try:
        payload = json.load(sys.stdin) if args.comparison == '-' else json.loads(Path(args.comparison).read_text())
        result = check(payload)
        exit_code = 1 if result['findings'] else 0
    except (ValueError, OSError) as error:
        result, exit_code = {'status': 'INVALID', 'error': str(error)}, 2
    print(json.dumps(result, indent=2))
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
