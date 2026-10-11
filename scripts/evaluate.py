#!/usr/bin/env python3
"""Run three clean, bounded Claude Code paired composition cases using existing auth.
Optional model calls consume existing subscription/quota; never part of merge CI.
Raw execution events stay in the explicitly chosen private output directory.
"""
import argparse
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run(output,model='sonnet',timeout=240,case_ids=None,arms=None):
    output.mkdir(parents=True,exist_ok=True)
    all_cases=json.loads((ROOT/'evals/cases.json').read_text())['cases']
    cases=[x for x in all_cases if x['id'] in case_ids] if case_ids else all_cases[:3]
    arms=arms or ['without_skill','with_skill']
    summary=[]
    for case in cases:
        for arm in arms:
            with tempfile.TemporaryDirectory(prefix='promptcraft-eval-') as d:
                work=Path(d); shutil.copy(ROOT/'evals/fixtures/guidance.md',work/'guidance.md')
                args=['claude','--print','--model',model,'--output-format','stream-json','--verbose',
                      '--no-session-persistence','--setting-sources','','--strict-mcp-config',
                      '--mcp-config','{"mcpServers":{}}','--permission-mode','default',
                      '--tools','Read,Skill','--allowedTools','Read,Skill','--max-turns','12',
                      '--max-budget-usd','2']
                if arm=='with_skill': args+=['--plugin-dir',str(ROOT)]
                else: args+=['--disable-slash-commands']
                task=('This is prompt composition only; do not implement or execute the underlying task. '
                      'Use guidance.md as synthetic dated reference context. Network retrieval is unavailable. '
                      'Do not claim live official sources.\n\n'+case['prompt'])
                args.append(task)
                start=time.monotonic(); folder=output/case['id']/arm; folder.mkdir(parents=True)
                try:
                    result=subprocess.run(args,cwd=work,text=True,capture_output=True,timeout=timeout)
                    (folder/'events.jsonl').write_text(result.stdout)
                    (folder/'stderr.log').write_text(result.stderr)
                    events=[]
                    for line in result.stdout.splitlines():
                        try: events.append(json.loads(line))
                        except json.JSONDecodeError: pass
                    final=next((x for x in reversed(events) if x.get('type')=='result'),{})
                    skill_calls=[]; models=set()
                    for event in events:
                        message=event.get('message',{})
                        if message.get('model'): models.add(message['model'])
                        for block in message.get('content',[]) if isinstance(message.get('content'),list) else []:
                            if block.get('type')=='tool_use' and block.get('name')=='Skill':
                                skill_calls.append(block.get('input',{}).get('skill'))
                    row={'case':case['id'],'arm':arm,'exit_code':result.returncode,
                         'status':'RUN' if final.get('result') and not final.get('is_error') else 'ERROR',
                         'model_requested':model,'models_observed':sorted(models),
                         'duration_seconds':round(time.monotonic()-start,2),'skill_calls':skill_calls,
                         'reported_cost_usd':final.get('total_cost_usd'), 'usage':final.get('usage'),
                         'output_chars':len(final.get('result',''))}
                    (folder/'output.md').write_text(final.get('result',''))
                except subprocess.TimeoutExpired:
                    row={'case':case['id'],'arm':arm,'status':'TIMEOUT','duration_seconds':timeout}
                summary.append(row)
                (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
                print(json.dumps(row),flush=True)
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--output',type=Path,required=True)
    p.add_argument('--model',default='sonnet'); p.add_argument('--timeout',type=int,default=240)
    p.add_argument('--cases',help='Comma-separated synthetic case IDs; default first three')
    p.add_argument('--arms',choices=['paired','with_skill'],default='paired')
    a=p.parse_args(); run(a.output,a.model,a.timeout,a.cases.split(',') if a.cases else None,
                         ['with_skill'] if a.arms=='with_skill' else None)
