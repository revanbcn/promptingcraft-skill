#!/usr/bin/env python3
"""Optional small isolated execution comparison; consumes existing Claude quota.

Only local fixture edits/tests are permitted. No real MR/merge/deploy is exercised.
Raw traces stay in a fresh private output folder. Acceptance is outside workspaces.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from scripts.evaluate import ROOT, parse_events
except ModuleNotFoundError:
    from evaluate import ROOT, parse_events


def run(output, baseline, candidate, model):
    output = Path(output)
    if output.exists():
        raise FileExistsError('Fresh output directory required')
    output.mkdir(parents=True, mode=0o700)
    cases = {case['id']: case for case in json.loads((ROOT/'evals/cases.json').read_text())['cases']}
    fixture = ROOT/'evals/downstream/fixtures'
    rows = []
    for case_id, filename, acceptance in [('small-bug', 'settings.py', 'SaveAcceptance'),
                                           ('retry-contract', 'worker.py', 'RetryAcceptance')]:
        for arm in ['original', 'v0_1_0', 'candidate']:
            folder = output/case_id/arm
            work = folder/'work'
            work.mkdir(parents=True)
            shutil.copy(fixture/filename, work/filename)
            (work/'tests').mkdir()
            (work/'README.md').write_text('This is an isolated original stdlib fixture. Local check: python3 -m unittest discover -s tests -v. There are no external services.\n')
            subprocess.run(['git', 'init', '-q'], cwd=work, check=True)
            subprocess.run(['git', 'add', '.'], cwd=work, check=True)
            subprocess.run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                            '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null',
                            'commit', '-qm', 'Original evaluation fixture'], cwd=work, check=True)
            if arm == 'original':
                # Remove only the composition framing; the remaining task text is exact.
                prompt = cases[case_id]['prompt'].split(': ', 1)[-1] if ': ' in cases[case_id]['prompt'] else cases[case_id]['prompt'].split('. ', 1)[-1]
            else:
                root = Path(baseline if arm == 'v0_1_0' else candidate)
                prompt = (root/case_id/'with_skill/handoff.txt').read_text()
            (folder/'input.txt').write_text(prompt)
            wrapper = ('Execute the following development task in this isolated fixture. '
                       'Your permitted scope here is local code edits and tests only. '
                       'The host provides no MR, merge, deployment, network or message tools; '
                       'report those stages as unavailable if requested. Do not install dependencies.\n\n'+prompt)
            args = ['claude', '--print', '--model', model, '--output-format', 'stream-json', '--verbose',
                    '--no-session-persistence', '--setting-sources', '', '--strict-mcp-config',
                    '--mcp-config', '{"mcpServers":{}}', '--permission-mode', 'dontAsk', '--restricted',
                    '--tools', 'Read,Edit,Write,Bash', '--allowedTools',
                    'Read,Edit,Write,Bash(python3 -m unittest discover -s tests -v),Bash(git diff),Bash(git status --short)',
                    '--disable-slash-commands', '--max-turns', '16', '--max-budget-usd', '2', wrapper]
            command = [sys.executable, '-m', 'unittest', 'acceptance.'+acceptance, '-v']
            env = dict(os.environ, PYTHONPATH=str(work)+os.pathsep+str(ROOT/'evals/downstream'))
            before = subprocess.run(command, env=env, cwd=work, capture_output=True, text=True)
            (folder/'acceptance-before.txt').write_text(before.stdout+before.stderr)
            try:
                result = subprocess.run(args, cwd=work, capture_output=True, text=True, timeout=240)
                (folder/'events.jsonl').write_text(result.stdout)
                (folder/'stderr.log').write_text(result.stderr)
                parsed = parse_events(result.stdout)
                (folder/'output.md').write_text(parsed.pop('output'))
                parsed.pop('handoff')
                after = subprocess.run(command, env=env, cwd=work, capture_output=True, text=True)
                (folder/'acceptance-after.txt').write_text(after.stdout+after.stderr)
                diff = subprocess.run(['git', 'diff'], cwd=work, capture_output=True, text=True, check=True).stdout
                (folder/'patch.diff').write_text(diff)
                row = {'case':case_id, 'arm':arm, 'model_requested':model, 'exit_code':result.returncode,
                       'baseline_acceptance_exit':before.returncode, 'acceptance_exit':after.returncode,
                       'acceptance_pass':after.returncode == 0, **parsed}
            except subprocess.TimeoutExpired:
                row = {'case':case_id, 'arm':arm, 'status':'TIMEOUT', 'acceptance_pass':False}
            rows.append(row)
            (output/'summary.json').write_text(json.dumps(rows,indent=2)+'\n')
            print(json.dumps({key:row.get(key) for key in ['case','arm','status','acceptance_pass']}),flush=True)
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--model', default='claude-sonnet-5-5')
    args = parser.parse_args()
    run(args.output,args.baseline,args.candidate,args.model)
