#!/usr/bin/env python3
"""With/without comparison for the installed plugin (evals/results/ab-1 was made this way).

Each case in <cases.json> runs <runs> times with the plugin enabled and <runs> times with
it disabled (`-c plugins.promptcraft@dondego-local.enabled=false`), each in a fresh empty
directory with a read-only sandbox. `skill_loaded` records whether the host read the
installed SKILL.md. The final answers are then written to a blinded file under shuffled
labels (seeded) with each case's request and contract; the key is written separately so
a grader can be given the blinded file alone (see `grader-prompt.md` in the result folder).

Usage: python3 scripts/evaluate_ab.py <cases.json> <out-dir> [runs=2] [seed=20261012]
Needs an installed, enabled `promptcraft@dondego-local` and a logged-in Codex CLI. Raw
event traces (`*.jsonl`) contain local paths; do not commit them.
"""
import json, random, re, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
cases = json.loads(Path(sys.argv[1]).read_text())
out = Path(sys.argv[2]); (out / 'outputs').mkdir(parents=True, exist_ok=True)
runs = int(sys.argv[3]) if len(sys.argv) > 3 else 2
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 20261012
SKILL = re.compile(r'skills/promptcraft/SKILL\.md')
def run(case, cond, n):
    for attempt in range(6):
        work = tempfile.mkdtemp(prefix='pc-ab-')
        cmd = ['codex', 'exec', '--json', '--skip-git-repo-check', '--ephemeral', '-s', 'read-only', '-C', work]
        if cond == 'without': cmd += ['-c', 'plugins.promptcraft@dondego-local.enabled=false']
        last = Path(work) / 'last.md'; cmd += ['-o', str(last), case['query']]
        r = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=900)
        if 'turn.failed' in r.stdout and attempt < 5: time.sleep(30 * (attempt + 1)); continue
        break
    text = last.read_text() if last.exists() else ''
    name = f"{case['id']}-{cond}-{n}"
    (out / 'outputs' / f'{name}.md').write_text(text); (out / f'{name}.jsonl').write_text(r.stdout)
    rec = {'id': case['id'], 'cond': cond, 'run': n, 'exit': r.returncode, 'skill_loaded': bool(SKILL.search(r.stdout)), 'chars': len(text)}
    print(json.dumps(rec), flush=True); return rec
jobs = [(c, cond, n) for n in range(1, runs + 1) for c in cases for cond in ('with', 'without')]
with ThreadPoolExecutor(2) as pool: results = list(pool.map(lambda a: run(*a), jobs))
(out / 'runs.json').write_text(json.dumps(results, indent=2) + '\n')
items = [(c, cond, n) for c in cases for cond in ('with', 'without') for n in range(1, runs + 1)]
random.Random(seed).shuffle(items)
key, doc = {}, ['# Blinded outputs\n']
for i, (c, cond, n) in enumerate(items, 1):
    label = f'X{i:02d}'; key[label] = {'case': c['id'], 'cond': cond, 'run': n}
    text = (out / 'outputs' / f"{c['id']}-{cond}-{n}.md").read_text().strip()
    doc.append(f"## {label} — case {c['id']}\n\nUser request:\n\n> " + c['query'].replace('\n', '\n> ')
               + '\n\nContract to check:\n' + '\n'.join('- ' + x for x in c['contract'])
               + f'\n\nAssistant output:\n\n````\n{text}\n````\n')
(out / 'blinded-outputs.md').write_text('\n'.join(doc)); (out / 'blind-key.json').write_text(json.dumps(key, indent=2) + '\n')
