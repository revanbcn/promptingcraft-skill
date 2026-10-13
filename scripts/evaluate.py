#!/usr/bin/env python3
"""Run all planned, bounded Claude Code composition cases using existing auth.
Optional model calls consume existing subscription/quota; never part of merge CI.
Raw execution events stay in the explicitly chosen private output directory.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def select_cases(cases, case_ids=None):
    ids = [case['id'] for case in cases]
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate case IDs')
    if case_ids is None:
        return cases
    if not case_ids or set(case_ids) - set(ids):
        raise ValueError('Empty or unknown case IDs')
    return [case for case in cases if case['id'] in case_ids]


def extract_handoff(text, preserve_whitespace=False):
    blocks, opened, body = [], None, []
    for line in text.splitlines(keepends=True):
        fence = re.fullmatch(r' {0,3}(`{3,}|~{3,})([^\r\n]*)[\r\n]*', line)
        if opened is not None:
            if (fence and fence[1][0] == opened[0][0] and len(fence[1]) >= len(opened[0])
                    and not fence[2].strip()):
                content = ''.join(body)
                if preserve_whitespace:
                    # Remove only the newline required to put the closing fence on its own line.
                    content = content[:-2] if content.endswith('\r\n') else content[:-1] if content.endswith('\n') else content
                else:
                    content = content.strip()
                blocks.append((opened[1], content))
                opened, body = None, []
            else:
                body.append(line)
        elif fence:
            opened = (fence[1], fence[2].strip())
    if opened is not None or len(blocks) != 1:
        return None
    language, content = blocks[0]
    return content if language in {'', 'text', 'plaintext', 'markdown', 'md'} and content else None


def parse_events(raw, original=None):
    events = []
    for line in raw.splitlines():
        try:
            event = json.loads(line)
            if isinstance(event, dict):
                events.append(event)
        except json.JSONDecodeError:
            pass
    final = next((event for event in reversed(events) if event.get('type') == 'result'), {})
    skill_calls, models = [], set()
    for event in events:
        message = event.get('message', {})
        if not isinstance(message, dict):
            continue
        if message.get('model'):
            models.add(message['model'])
        for block in message.get('content', []) if isinstance(message.get('content'), list) else []:
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'tool_use' and block.get('name') == 'Skill':
                skill_calls.append(block.get('input', {}).get('skill'))
    output = final.get('result', '')
    handoff = extract_handoff(output)
    marker = 'The original prompt is already suitable. No material revision is necessary.'
    outside, opened = [], None
    for line in output.splitlines():
        fence = re.fullmatch(r' {0,3}(`{3,}|~{3,})(.*)', line)
        if opened is not None:
            if fence and fence[1][0] == opened[0] and len(fence[1]) >= len(opened) and not fence[2].strip():
                opened = None
        elif fence:
            opened = fence[1]
        else:
            outside.append(line)
    paragraphs = [' '.join(p.replace('**', '').split()) for p in re.split(r'\n\s*\n', '\n'.join(outside))]
    declarations = [' '.join(line.replace('**', '').split()) for line in outside]
    unchanged = marker in paragraphs or marker in declarations
    exact_echo = extract_handoff(output, preserve_whitespace=True)
    outcome = 'REVISED' if handoff is not None else 'UNRESOLVED'
    if unchanged:
        # A reported outcome, never an automatic semantic preservation verdict.
        outcome = ('UNCHANGED' if original is not None and
                   (exact_echo == original or (handoff is None and not re.search(r'`{3,}|~{3,}', output)))
                   else 'UNRESOLVED')
        handoff = original if outcome == 'UNCHANGED' else None
    return {'status': 'RUN' if output and not final.get('is_error') else 'ERROR',
            'composition_outcome': outcome,
            'models_observed': sorted(models), 'skill_calls': skill_calls,
            'reported_cost_usd': final.get('total_cost_usd'), 'usage': final.get('usage'),
            'output_chars': len(output), 'handoff_chars': len(handoff) if handoff is not None else None,
            'handoff_words': len(handoff.split()) if handoff is not None else None,
            'output': output, 'handoff': handoff}


def skill_digest(root):
    digest = hashlib.sha256()
    for path in sorted((root/'skills/promptingcraft').rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            digest.update(path.relative_to(root).as_posix().encode())
            digest.update(b'\0' + path.read_bytes() + b'\0')
    return digest.hexdigest()


def run(output,model='claude-sonnet-5-5',timeout=240,case_ids=None,arms=None,skill_root=None,cases_file=None):
    skill_root = Path(skill_root or ROOT).resolve()
    cases_file = Path(cases_file or ROOT/'evals/cases.json').resolve()
    all_cases=json.loads(cases_file.read_text())['cases']
    cases=select_cases(all_cases,case_ids)
    arms=arms or ['without_skill','with_skill']
    if any(arm not in {'without_skill', 'with_skill'} for arm in arms):
        raise ValueError('Unknown evaluation arm')
    if not (skill_root/'skills/promptingcraft/SKILL.md').is_file():
        raise ValueError('Missing skill root')
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError('Use a fresh output directory; existing runs are never overwritten')
    output.mkdir(parents=True,exist_ok=True,mode=0o700)
    snapshot = skill_digest(skill_root)
    summary=[]
    for case in cases:
        for arm in arms:
            with tempfile.TemporaryDirectory(prefix='promptingcraft-eval-') as d:
                work=Path(d); shutil.copy(cases_file.parent/case['fixture'],work/'guidance.md')
                args=['claude','--print','--model',model,'--output-format','stream-json','--verbose',
                      '--no-session-persistence','--setting-sources','','--strict-mcp-config',
                      '--mcp-config','{"mcpServers":{}}','--permission-mode','default',
                      '--tools','Read,Skill','--allowedTools','Read,Skill','--max-turns','12',
                      '--max-budget-usd','2']
                if arm=='with_skill': args+=['--plugin-dir',str(skill_root)]
                else: args+=['--disable-slash-commands']
                task=('If the request below is prompt authoring, use the installed PromptingCraft skill and compose only; '
                      'do not implement or execute its underlying task. For other requests, answer normally. '
                      'Use guidance.md as synthetic dated reference context. Network retrieval is unavailable. '
                      'Do not claim live official sources.\n\n'+case['prompt'])
                args.append(task)
                start=time.monotonic(); folder=output/case['id']/arm; folder.mkdir(parents=True)
                (folder/'original.txt').write_text(case['prompt'])
                try:
                    result=subprocess.run(args,cwd=work,text=True,capture_output=True,timeout=timeout)
                    (folder/'events.jsonl').write_text(result.stdout)
                    (folder/'stderr.log').write_text(result.stderr)
                    parsed = parse_events(result.stdout, original=case.get('task_prompt', case['prompt']))
                    visible = parsed.pop('output'); handoff = parsed.pop('handoff')
                    row={'case':case['id'],'arm':arm,'exit_code':result.returncode,
                         'model_requested':model,'skill_tree_sha256':snapshot,
                         'duration_seconds':round(time.monotonic()-start,2), **parsed}
                    if result.returncode:
                        row['status'] = 'ERROR'
                    (folder/'output.md').write_text(visible)
                    if handoff is not None:
                        (folder/'handoff.txt').write_text(handoff)
                except subprocess.TimeoutExpired:
                    row={'case':case['id'],'arm':arm,'status':'TIMEOUT','duration_seconds':timeout,
                         'model_requested':model,'skill_tree_sha256':snapshot}
                summary.append(row)
                (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
                print(json.dumps(row),flush=True)
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--output',type=Path,required=True)
    p.add_argument('--model',default='claude-sonnet-5-5'); p.add_argument('--timeout',type=int,default=240)
    p.add_argument('--cases',help='Comma-separated case IDs; default ALL cases')
    p.add_argument('--skill-root',type=Path,help='Frozen plugin root for baseline comparison')
    p.add_argument('--cases-file',type=Path,help='Shared case file, including fixture-relative paths')
    p.add_argument('--arms',choices=['paired','with_skill'],default='paired')
    a=p.parse_args(); run(a.output,a.model,a.timeout,a.cases.split(',') if a.cases else None,
                         ['with_skill'] if a.arms=='with_skill' else None,a.skill_root,a.cases_file)
