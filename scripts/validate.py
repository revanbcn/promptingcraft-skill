#!/usr/bin/env python3
"""Validate this project's constrained metadata and self-contained resources offline."""
import json
import re
from datetime import date
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
    registry=json.loads((skill/'references/sources.json').read_text())
    validate_registry(registry)
    validate_knowledge(json.loads((skill/'references/knowledge.json').read_text()),registry)
    return meta


def validate_knowledge(knowledge,registry):
    if knowledge.get('schema_version')!=1 or not knowledge.get('recommendations'):
        raise ValueError('Invalid curated knowledge')
    sources={row['canonical_url']:row['provider'] for row in registry['sources']}
    identifiers=set()
    labels={'OFFICIAL','GENERAL','MODEL_SPECIFIC','INFERRED','EXPERIMENTAL'}
    fields=('id','provider','source_title','url','retrieval_date','applicable_model_family',
            'recommendation','evidence_or_limitation','promptcraft_applicability',
            'conflicts_with_existing_guidance','apply_when')
    for row in knowledge['recommendations']:
        if any(not isinstance(row.get(field),str) or not row[field].strip() for field in fields):
            raise ValueError('Recommendation lacks provenance, scope or limits')
        if row['id'] in identifiers: raise ValueError('Duplicate recommendation')
        identifiers.add(row['id'])
        if sources.get(row['url'].split('#')[0])!=row['provider']:
            raise ValueError('Recommendation source absent or misattributed')
        date.fromisoformat(row['retrieval_date'])
        tags=row.get('labels')
        if not isinstance(tags,list) or not tags or any(tag not in labels for tag in tags):
            raise ValueError('Invalid evidence label')
        if 'OFFICIAL' not in tags or len({'GENERAL','MODEL_SPECIFIC'} & set(tags))!=1:
            raise ValueError('Official recommendation requires one scope label')
        if row.get('mandatory_for_all_prompts') is not False:
            raise ValueError('Provider recommendations cannot be universal requirements')


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

def validate_marketplace(root, require_source=True):
    """Validate our documented single-plugin local catalog and root-relative source."""
    root = Path(root).resolve()
    catalog = root / '.agents/plugins/marketplace.json'
    for ancestor in (root / '.agents', catalog.parent, catalog):
        if ancestor.is_symlink():
            raise ValueError('Symlink in marketplace catalog path')
    data = json.loads(catalog.read_text())
    if set(data) != {'name', 'interface', 'plugins'} or data['name'] != 'dondego-local':
        raise ValueError('Invalid local marketplace metadata')
    if data['interface'] != {'displayName': 'DondeGo Local'}:
        raise ValueError('Invalid marketplace display metadata')
    plugins = data['plugins']
    if not isinstance(plugins, list) or len(plugins) != 1:
        raise ValueError('Expected one canonical PromptCraft plugin')
    plugin = plugins[0]
    if set(plugin) != {'name', 'source', 'policy', 'category'} or plugin['name'] != 'promptcraft':
        raise ValueError('Invalid marketplace plugin entry')
    if plugin['policy'] != {'installation': 'AVAILABLE', 'authentication': 'ON_USE'}:
        raise ValueError('Invalid marketplace policy')
    if plugin['category'] != 'Productivity':
        raise ValueError('Invalid marketplace category')
    source = plugin['source']
    # A constrained generated destination prevents the materializer replacing source files.
    if source != {'source': 'local', 'path': './dist/promptcraft-plugin'}:
        raise ValueError('Expected generated plugin path relative to marketplace root')
    dest = root / source['path']
    for ancestor in (dest.parent, dest):
        if ancestor.is_symlink():
            raise ValueError('Symlink in marketplace plugin path')
    if not dest.resolve().is_relative_to(root):
        raise ValueError('Plugin source escapes marketplace root')
    if require_source:
        manifest = validate_project(dest)
        if manifest['name'] != plugin['name']:
            raise ValueError('Marketplace name does not match plugin manifest')
    return dest


if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--marketplace', action='store_true', help='Also require the generated marketplace plugin')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    validate_project(root)
    validate_marketplace(root, require_source=args.marketplace)
    print('Project metadata, resources, source policies and marketplace: PASS')
