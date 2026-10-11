import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from skills.promptcraft.scripts.contract_check import check


def document():
    return {
        'schema_version': 1,
        'original': 'Fix Save after a 500. Preserve the API. Edits and tests allowed. Do not deploy. Optionally check timeout errors.',
        'requirements': [
            {'id': 'goal', 'classification': 'EXPLICIT_REQUIRED', 'quote': 'Fix Save after a 500.', 'kind': 'GOAL'},
            {'id': 'api', 'classification': 'EXPLICIT_REQUIRED', 'quote': 'Preserve the API.', 'kind': 'CONSTRAINT'},
            {'id': 'authority', 'classification': 'EXPLICIT_REQUIRED', 'quote': 'Edits and tests allowed.', 'kind': 'AUTHORITY', 'actions': ['edit', 'test']},
            {'id': 'deploy', 'classification': 'FORBIDDEN', 'quote': 'Do not deploy.', 'kind': 'AUTHORITY', 'actions': ['deploy']},
            {'id': 'timeout', 'classification': 'EXPLICIT_OPTIONAL', 'quote': 'Optionally check timeout errors.', 'kind': 'GOAL'},
        ],
        'final_prompt': 'Fix Save after a 500.\nPreserve the API.\nEdits and tests allowed.\nDo not deploy.',
        'clauses': [
            {'text': 'Fix Save after a 500.', 'modality': 'REQUIRED', 'supports': ['goal'], 'relation': 'PRESERVES', 'kind': 'GOAL'},
            {'text': 'Preserve the API.', 'modality': 'REQUIRED', 'supports': ['api'], 'relation': 'PRESERVES', 'kind': 'CONSTRAINT'},
            {'text': 'Edits and tests allowed.', 'modality': 'REQUIRED', 'supports': ['authority'], 'relation': 'PRESERVES', 'kind': 'AUTHORITY'},
            {'text': 'Do not deploy.', 'modality': 'FORBIDDEN', 'supports': ['deploy'], 'relation': 'PRESERVES', 'kind': 'AUTHORITY'},
        ],
    }


def append_clause(data, text, **fields):
    data['final_prompt'] += '\n' + text
    data['clauses'].append({'text': text, 'modality': 'REQUIRED', 'supports': [],
                            'relation': 'NOVEL', 'kind': 'GOAL', **fields})


class ContractTests(unittest.TestCase):
    def codes(self, data):
        return {x['code'] for x in check(data)['findings']}

    def test_clean_annotations_never_claim_semantic_validation(self):
        result = check(document())
        self.assertEqual(result['status'], 'REVIEW_REQUIRED')
        self.assertEqual(result['findings'], [])
        self.assertEqual(result['semantic_validation'], 'NOT_ESTABLISHED')

    def test_added_behavior_is_a_new_requirement(self):
        data = document()
        append_clause(data, 'Retain unsaved edits on every network error.')
        self.assertIn('NEW_REQUIREMENT', self.codes(data))

    def test_optional_is_not_strengthened_by_rewording(self):
        data = document()
        append_clause(data, 'Test timeout errors.', supports=['timeout'], relation='PRESERVES')
        self.assertIn('STRENGTHENED_OPTIONAL', self.codes(data))

    def test_inferred_and_unresolved_items_never_supply_authority(self):
        for classification in ['INFERRED', 'UNRESOLVED']:
            with self.subTest(classification=classification):
                data = document()
                data['requirements'].append({'id': 'assumption', 'classification': classification,
                                             'quote': 'Fix Save after a 500.', 'kind': 'GOAL'})
                append_clause(data, 'Add automatic retry.', supports=['assumption'], relation='CLARIFIES', reason='Assumed desirable')
                self.assertIn('NEW_REQUIREMENT', self.codes(data))

    def test_omitted_mandatory_constraint_and_exclusion_are_flagged(self):
        for index, code in [(1, 'OMITTED_REQUIRED'), (3, 'OMITTED_FORBIDDEN')]:
            data = document()
            del data['clauses'][index]
            data['final_prompt'] = '\n'.join(x['text'] for x in data['clauses'])
            self.assertIn(code, self.codes(data))

    def test_making_required_constraint_optional_is_an_omission(self):
        data = document()
        data['clauses'][1]['modality'] = 'OPTIONAL'
        self.assertIn('OMITTED_REQUIRED', self.codes(data))

    def test_reversed_prohibition_is_a_contradiction(self):
        data = document()
        data['clauses'][3].update(text='Deploy immediately.', modality='REQUIRED', external_action='deploy')
        data['final_prompt'] = '\n'.join(x['text'] for x in data['clauses'])
        self.assertIn('CONTRADICTORY_INSTRUCTION', self.codes(data))
        self.assertIn('UNAUTHORIZED_EXTERNAL_ACTION', self.codes(data))

    def test_explicit_semantic_contradiction_is_reported(self):
        data = document()
        append_clause(data, 'Change the API.', supports=['api'], relation='CONTRADICTS')
        self.assertIn('CONTRADICTORY_INSTRUCTION', self.codes(data))

    def test_external_action_needs_its_own_explicit_authority(self):
        data = document()
        append_clause(data, 'Send the patch to customers.', supports=['goal'], relation='DECOMPOSES',
                      reason='Customer delivery', external_action='send')
        self.assertIn('UNAUTHORIZED_EXTERNAL_ACTION', self.codes(data))

    def test_optional_suggestion_cannot_grant_external_authority(self):
        data = document()
        append_clause(data, 'Optional suggestion: deploy if useful.', modality='OPTIONAL',
                      relation='SUGGESTS', external_action='deploy')
        self.assertIn('UNAUTHORIZED_EXTERNAL_ACTION', self.codes(data))

    def test_original_optional_authority_remains_optional_and_usable(self):
        data = document()
        data['original'] += ' Optionally publish the report.'
        data['requirements'].append({'id': 'publish', 'classification': 'EXPLICIT_OPTIONAL',
                                     'quote': 'Optionally publish the report.', 'kind': 'AUTHORITY',
                                     'actions': ['publish']})
        append_clause(data, 'Optional: publish the report.', modality='OPTIONAL',
                      supports=['publish'], relation='PRESERVES', kind='AUTHORITY', external_action='publish')
        self.assertEqual(check(data)['findings'], [])

    def test_invented_completion_threshold_is_not_just_a_test(self):
        data = document()
        append_clause(data, 'Complete only when coverage is 100 percent.', kind='COMPLETION')
        self.assertIn('INVENTED_COMPLETION_CRITERION', self.codes(data))

    def test_faithful_decomposition_and_formatting_are_allowed(self):
        data = document()
        append_clause(data, 'Verify that a 500 response cannot show success.', supports=['goal'],
                      relation='DECOMPOSES', reason='Directly tests the stated failure.', kind='COMPLETION')
        append_clause(data, 'Task', modality='CONTEXT', relation='FORMAT', kind='FORMAT')
        self.assertEqual(check(data)['findings'], [])

    def test_new_suggestion_is_optional_inside_the_prompt(self):
        data = document()
        append_clause(data, 'Optional suggestion: consider timeout coverage if useful.', modality='OPTIONAL', relation='SUGGESTS')
        self.assertEqual(check(data)['findings'], [])
        data['clauses'][-1]['text'] = 'Add timeout coverage.'
        data['final_prompt'] = '\n'.join(x['text'] for x in data['clauses'])
        self.assertIn('UNMARKED_SUGGESTION', self.codes(data))

    def test_outside_note_cannot_hide_unannotated_imperatives(self):
        data = document()
        data['final_prompt'] += '\nRetain all edits after network errors.'
        self.assertIn('UNANNOTATED_TEXT', self.codes(data))

    def test_quote_must_be_present_in_original(self):
        data = document()
        data['requirements'][0]['quote'] = 'Also add retry.'
        with self.assertRaises(ValueError):
            check(data)

    def test_false_provenance_and_duplicate_identifiers_are_rejected(self):
        data = document()
        data['clauses'][0]['supports'] = ['not-a-requirement']
        with self.assertRaises(ValueError):
            check(data)
        data = document()
        data['requirements'].append(copy.deepcopy(data['requirements'][0]))
        with self.assertRaises(ValueError):
            check(data)

    def test_cli_drift_is_nonzero_and_machine_readable(self):
        script = Path(__file__).resolve().parents[1] / 'skills/promptcraft/scripts/contract_check.py'
        data = document()
        append_clause(data, 'Deploy.', external_action='deploy')
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'comparison.json'
            source.write_text(json.dumps(data))
            result = subprocess.run([sys.executable, str(script), str(source)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['status'], 'DRIFT')


if __name__ == '__main__':
    unittest.main()
