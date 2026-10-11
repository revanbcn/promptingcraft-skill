#!/usr/bin/env python3
"""Validate this project's constrained metadata and self-contained resources offline."""
import json
import re
from pathlib import Path
try:
    from scripts.freshness import validate_registry
except ModuleNotFoundError:
    from freshness import validate_registry


def frontmatter(path):
    text=path.read_text(); parts=text.split('---',2)
    if len(parts)!=3 or parts[0].strip(): raise ValueError('Missing YAML frontmatter')
    data={}; parent=None
    for line in parts[1].strip().splitlines():
        if not line.strip(): continue
        match=re.fullmatch(r'(  )?([a-z][a-z0-9-]*):(?: (.*))?',line)
        if not match: raise ValueError('Unsupported metadata syntax')
        indent,key,value=match.groups()
        if value is None:
            if indent or key!='metadata': raise ValueError('Unexpected metadata object')
            if key in data: raise ValueError('Duplicate key')
            data[key]={}; parent=key
        else:
            value=value.strip('"')
            target=data[parent] if indent and parent else data
            if key in target: raise ValueError('Duplicate key')
            if indent and not parent: raise ValueError('Invalid indentation')
            target[key]=value
    return data,parts[2]


def validate_skill(skill):
    meta,body=frontmatter(skill/'SKILL.md')
    allowed={'name','description','license','compatibility','metadata','allowed-tools'}
    if set(meta)-allowed: raise ValueError('Unknown portable skill fields')
    name=meta.get('name','')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name) or len(name)>64 or name!=skill.name:
        raise ValueError('Invalid skill name')
    if not 1<=len(meta.get('description',''))<=1024: raise ValueError('Invalid description')
    if meta.get('compatibility') and len(meta['compatibility'])>500: raise ValueError('Compatibility too long')
    if len(body.splitlines())>=500: raise ValueError('Skill entrypoint too long')
    if 'TODO' in body: raise ValueError('Unfinished scaffold')
    for target in re.findall(r'\]\(([^)]+)\)',body):
        if target.startswith('https://'): continue
        resolved=(skill/target).resolve()
        if not resolved.is_relative_to(skill.resolve()) or not resolved.is_file():
            raise ValueError('Skill resource escapes package or is absent')
    validate_registry(json.loads((skill/'references/sources.json').read_text()))
    return meta


def validate_project(root):
    root=Path(root); skill=root/'skills/promptcraft'; meta=validate_skill(skill)
    manifest=json.loads((root/'plugin.json').read_text())
    allowed={'$schema','name','version','description','author','homepage','repository','license','keywords','extensions'}
    if set(manifest)-allowed: raise ValueError('Unknown portable manifest field')
    if manifest.get('$schema')!='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json': raise ValueError('Wrong schema')
    if manifest.get('name')!='promptcraft' or manifest.get('version')!=meta['metadata']['version']: raise ValueError('Version/name mismatch')
    for k in ('description','homepage','repository','license'):
        if not isinstance(manifest.get(k),str) or not manifest[k]: raise ValueError('Invalid manifest string')
    if manifest['author']!={'name':'DondeGo team','url':'https://dondego.com'}: raise ValueError('Author metadata mismatch')
    compatibility=json.loads((root/'.claude-plugin/plugin.json').read_text())
    if compatibility!={k:v for k,v in manifest.items() if k!='$schema'}: raise ValueError('Divergent adapter metadata')
    attribution='Developed by the dondego.com team.'
    if not manifest['description'].endswith(attribution) or not meta['description'].endswith(attribution): raise ValueError('Missing attribution')
    if (skill/'LICENSE').read_bytes()!=(root/'LICENSE').read_bytes(): raise ValueError('License mismatch')
    if (root/'.github/workflows').exists(): raise ValueError('GitHub Actions are out of scope')
    for path in skill.rglob('*'):
        if path.is_symlink(): raise ValueError('Symlink in standalone skill')
    return manifest

if __name__=='__main__':
    validate_project(Path(__file__).resolve().parents[1]); print('Project metadata, resources and source policies: PASS')
