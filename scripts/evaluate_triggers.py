#!/usr/bin/env python3
"""Activation (trigger) eval for the installed plugin, following agentskills.io
"Optimizing skill descriptions": each query runs N times in a fresh empty directory
with `codex exec`; a run counts as triggered only when the host actually reads the
installed SKILL.md from the plugin cache (not when the model says it used the skill).

Usage: python3 scripts/evaluate_triggers.py evals/trigger/queries.json <out-dir> [runs=3] [workers=2]
Runs that fail on the host side (capacity, transport) are retried and, if still
failing, excluded from the rate and listed in `stops`. Needs an installed, enabled
`promptcraft@dondego-local` and a logged-in Codex CLI; uses the existing account.
"""
import json, re, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
queries = json.loads(Path(sys.argv[1]).read_text())['queries']
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
runs = int(sys.argv[3]) if len(sys.argv) > 3 else 3
SKILL = re.compile(r'plugins/cache/dondego-local/promptcraft/[^/"\\]+/skills/promptcraft/SKILL\.md')
def once(q, n):
    for attempt in range(6):
        r = attempt_once(q, n)
        if r['stop'] != 'capacity': return r
        time.sleep(30 * (attempt + 1))
    return r
def attempt_once(q, n):
    work = tempfile.mkdtemp(prefix='pc-trig-')
    cmd = ['codex', 'exec', '--json', '--skip-git-repo-check', '--ephemeral', '-s', 'read-only', '-C', work, q['query']]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, text=True, cwd=work)
    log, triggered, reason, t = [], False, 'eof', time.time()
    for line in p.stdout:
        log.append(line)
        if SKILL.search(line): triggered, reason = True, 'skill_read'; break
        if '"turn.completed"' in line: reason = 'completed'; break
        if '"turn.failed"' in line:
            reason = 'capacity' if 'capacity' in line else 'failed'; break
        if time.time() - t > 600: reason = 'timeout'; break
    p.kill(); p.wait()
    (out / f"{q['id']}-run{n}.jsonl").write_text(''.join(log))
    r = {'id': q['id'], 'run': n, 'triggered': triggered, 'stop': reason, 'seconds': round(time.time() - t)}
    print(json.dumps(r), flush=True); return r
jobs = [(q, n) for n in range(1, runs + 1) for q in queries]
with ThreadPoolExecutor(int(sys.argv[4]) if len(sys.argv) > 4 else 2) as pool:
    results = list(pool.map(lambda a: once(*a), jobs))
summary = []
for q in queries:
    rs = [r for r in results if r['id'] == q['id'] and r['stop'] in ('skill_read', 'completed')]
    rate = sum(r['triggered'] for r in rs) / len(rs) if rs else float('nan')
    summary.append({**{k: q[k] for k in ('id', 'split', 'should_trigger')}, 'triggers': sum(r['triggered'] for r in rs), 'runs': len(rs),
                    'trigger_rate': round(rate, 2), 'pass': (rate > 0.5) == q['should_trigger'], 'stops': [r['stop'] for r in results if r['id'] == q['id']]})
(out / 'summary.json').write_text(json.dumps(summary, indent=2))
for split in ('train', 'validation'):
    s = [x for x in summary if x['split'] == split]
    print(split, 'pass', sum(x['pass'] for x in s), '/', len(s))
