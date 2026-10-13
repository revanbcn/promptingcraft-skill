#!/usr/bin/env python3
"""Activation (trigger) eval in Cursor's CLI, mirroring scripts/evaluate_triggers.py.

Each query runs N times with `cursor-agent -p --mode ask` (read-only) in a fresh empty
directory, with the skill installed for the duration as a user skill at
`~/.cursor/skills/promptingcraft` (outside the workspace, so workspace search cannot find
it; the script refuses to run if that path exists and removes its copy afterwards).
A run counts as triggered only when the agent actually reads that SKILL.md (a read tool
call in the stream), not when the model says it used the skill. The model Cursor reports
in the init event is recorded per run; with the default model setting it may be Auto or
a Cursor default, so results are tied to the recorded model, not to Cursor in general.

Usage: python3 scripts/evaluate_triggers_cursor.py evals/trigger/queries.json <out-dir> [runs=3] [workers=2] [model]
Needs a logged-in Cursor CLI (`cursor-agent status`); uses the existing account. Raw
streams (`*.jsonl`) contain local paths; do not commit them.
"""
import json, shutil, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
queries = json.loads(Path(sys.argv[1]).read_text())['queries']
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
runs = int(sys.argv[3]) if len(sys.argv) > 3 else 3
model = sys.argv[5] if len(sys.argv) > 5 else None
def once(q, n):
    for attempt in range(4):
        r = attempt_once(q, n)
        if r['stop'] not in ('failed', 'timeout'): return r
        time.sleep(20 * (attempt + 1))
    return r
def reads_skill(event):
    call = event.get('tool_call') or {}
    for kind, body in call.items():
        if 'read' in kind.lower() and '.cursor/skills/promptingcraft/SKILL.md' in json.dumps(body.get('args', {})): return True
    return False
def attempt_once(q, n):
    work = Path(tempfile.mkdtemp(prefix='pc-cur-'))
    cmd = ['cursor-agent', '-p', '--output-format', 'stream-json', '--mode', 'ask', '--trust']
    if model: cmd += ['--model', model]
    cmd.append(q['query'])
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, text=True, cwd=work)
    log, triggered, reason, used, t = [], False, 'eof', None, time.time()
    for line in p.stdout:
        log.append(line)
        try: event = json.loads(line)
        except ValueError: continue
        if event.get('type') == 'system' and event.get('subtype') == 'init': used = event.get('model')
        if event.get('type') == 'tool_call' and reads_skill(event): triggered, reason = True, 'skill_read'; break
        if event.get('type') == 'result':
            reason = 'completed' if event.get('subtype') == 'success' and not event.get('is_error') else 'failed'; break
        if time.time() - t > 600: reason = 'timeout'; break
    p.kill(); p.wait()
    (out / f"{q['id']}-run{n}.jsonl").write_text(''.join(log))
    r = {'id': q['id'], 'run': n, 'triggered': triggered, 'stop': reason, 'model': used, 'seconds': round(time.time() - t)}
    print(json.dumps(r), flush=True); return r
USER_SKILL = Path.home() / '.cursor/skills/promptingcraft'
if USER_SKILL.exists() or USER_SKILL.is_symlink(): sys.exit(f'{USER_SKILL} exists; refusing to overwrite')
shutil.copytree(ROOT / 'skills/promptingcraft', USER_SKILL)
try:
    jobs = [(q, n) for n in range(1, runs + 1) for q in queries]
    with ThreadPoolExecutor(int(sys.argv[4]) if len(sys.argv) > 4 else 2) as pool:
        results = list(pool.map(lambda a: once(*a), jobs))
finally:
    shutil.rmtree(USER_SKILL)
(out / 'runs.json').write_text(json.dumps([{k: v for k, v in r.items() if k != 'seconds'} for r in results], indent=2) + '\n')
summary = []
for q in queries:
    rs = [r for r in results if r['id'] == q['id'] and r['stop'] in ('skill_read', 'completed')]
    rate = sum(r['triggered'] for r in rs) / len(rs) if rs else float('nan')
    summary.append({**{k: q[k] for k in ('id', 'split', 'should_trigger')}, 'triggers': sum(r['triggered'] for r in rs), 'valid_runs': len(rs),
                    'trigger_rate': round(rate, 2), 'pass': (rate > 0.5) == q['should_trigger'],
                    'invalid_runs': len([r for r in results if r['id'] == q['id']]) - len(rs)})
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
for split in ('train', 'validation'):
    s = [x for x in summary if x['split'] == split]
    print(split, 'pass', sum(x['pass'] for x in s), '/', len(s))
