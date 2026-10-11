#!/usr/bin/env python3
"""Copy the portable skill to an explicitly chosen project; refuse existing targets."""
import argparse
import shutil
from pathlib import Path
try:
    from scripts.validate import validate_skill
except ModuleNotFoundError:
    from validate import validate_skill


def install(source,project,host):
    source=Path(source); project=Path(project)
    validate_skill(source)
    if host not in ('codex','claude'): raise ValueError('Unsupported host')
    if not project.is_dir(): raise ValueError('Project directory must already exist')
    dest=project/('.agents' if host=='codex' else '.claude')/'skills'/'promptcraft'
    for path in (project,*dest.parents):
        if path.is_symlink(): raise ValueError('Symlink destination refused')
        if path==project.parent: break
    if dest.exists() or dest.is_symlink(): raise FileExistsError('Skill already exists; inspect and update manually')
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(source,dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    return dest

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--host',choices=['codex','claude'],required=True)
    p.add_argument('--project-dir',type=Path,required=True)
    a=p.parse_args(); print(install(Path(__file__).resolve().parents[1]/'skills/promptcraft',a.project_dir,a.host))
