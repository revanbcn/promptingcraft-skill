#!/usr/bin/env python3
"""Validate this project's constrained metadata and self-contained resources offline."""
import json
import re
import struct
import xml.etree.ElementTree as ElementTree
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
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


ATTRIBUTION='Developed by the dondego.com team.'
INTERFACE_TEXT_LIMITS={'displayName':30,'shortDescription':30,'longDescription':4000}
INTERFACE_URLS=('websiteURL','supportURL','privacyPolicyURL','termsOfServiceURL')
INTERFACE_ASSETS=('composerIcon','composerIconDark','logo','logoDark')
MIN_ASSET_SIZE=48


def https_url(value):
    parsed=urlparse(value) if isinstance(value,str) else None
    return bool(parsed and parsed.scheme=='https' and parsed.netloc and not parsed.username and not parsed.password)


def luminance(color):
    if not isinstance(color,str) or not re.fullmatch(r'#[0-9A-Fa-f]{6}',color): raise ValueError('Invalid brand color')
    channels=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    linear=[c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in channels]
    return 0.2126*linear[0]+0.7152*linear[1]+0.0722*linear[2]


def contrast(first,second):
    high,low=sorted((luminance(first),luminance(second)),reverse=True)
    return (high+0.05)/(low+0.05)


def square_asset_size(path):
    """Return the side of a square SVG viewBox or PNG image; reject anything else."""
    if path.suffix=='.png':
        data=path.read_bytes()
        if len(data)<24 or data[:8]!=b'\x89PNG\r\n\x1a\n' or data[12:16]!=b'IHDR': raise ValueError('Invalid PNG asset')
        width,height=struct.unpack('>II',data[16:24])
    elif path.suffix=='.svg':
        try: element=ElementTree.fromstring(path.read_bytes())
        except ElementTree.ParseError as error: raise ValueError('Invalid SVG asset') from error
        if element.tag!='{http://www.w3.org/2000/svg}svg': raise ValueError('Invalid SVG asset')
        if any(node.tag.rsplit('}',1)[-1] in ('script','foreignObject') for node in element.iter()):
            raise ValueError('Active SVG content')
        box=(element.get('viewBox') or '').replace(',',' ').split()
        if len(box)!=4: raise ValueError('SVG asset needs a viewBox')
        width,height=(float(value) for value in box[2:])
        for attribute in ('width','height'):
            value=element.get(attribute)
            if value is not None and value!=element.get('width' if attribute=='height' else 'height'):
                raise ValueError('SVG asset is not square')
    else:
        raise ValueError('Assets must be SVG or PNG')
    if width!=height or width<MIN_ASSET_SIZE: raise ValueError('Asset must be square and at least 48 units')
    return width


def validate_interface(root,interface):
    """Validate ChatGPT/Codex plugin listing metadata and its package-relative assets."""
    root=Path(root).resolve()
    if not isinstance(interface,dict): raise ValueError('Missing OpenAI interface metadata')
    for field,limit in INTERFACE_TEXT_LIMITS.items():
        value=interface.get(field)
        if not isinstance(value,str) or not value.strip() or len(value)>limit:
            raise ValueError(f'Invalid interface {field}')
    if not interface['longDescription'].endswith(ATTRIBUTION): raise ValueError('Missing attribution')
    for field in ('developerName','category'):
        if not isinstance(interface.get(field),str) or not interface[field].strip(): raise ValueError(f'Invalid interface {field}')
    for field in INTERFACE_URLS:
        if not https_url(interface.get(field)): raise ValueError(f'Interface {field} must be an https URL')
    if contrast(interface.get('brandColor'),'#FFFFFF')<2: raise ValueError('brandColor lacks contrast on light UI')
    if contrast(interface.get('brandColorDark'),'#212121')<2: raise ValueError('brandColorDark lacks contrast on dark UI')
    prompts=interface.get('defaultPrompt')
    if not isinstance(prompts,list) or not prompts or any(not isinstance(p,str) or not p.strip() for p in prompts):
        raise ValueError('Invalid interface defaultPrompt')
    for field in INTERFACE_ASSETS:
        value=interface.get(field)
        if not isinstance(value,str) or not value.startswith('./'): raise ValueError(f'Interface {field} must start with ./')
        path=root/value
        current=root
        for part in Path(value).parts:
            current=current/part
            if current.is_symlink(): raise ValueError('Symlinked interface asset')
        if not path.resolve().is_relative_to(root) or not path.is_file(): raise ValueError(f'Interface {field} is absent from the package')
        square_asset_size(path)


def skill_interface(skill):
    """Read the two flat string fields of agents/openai.yaml without a YAML dependency."""
    values={}
    for line in (skill/'agents/openai.yaml').read_text().splitlines():
        match=re.fullmatch(r'  (display_name|short_description): "([^"]*)"',line)
        if match: values[match.group(1)]=match.group(2)
    return values


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
    if not https_url(manifest['homepage']) or not https_url(manifest['repository']): raise ValueError('Manifest URLs must be https')
    if not manifest['description'].endswith(ATTRIBUTION) or not meta['description'].endswith(ATTRIBUTION): raise ValueError('Missing attribution')
    interface=manifest.get('extensions',{}).get('com.openai',{}).get('interface')
    validate_interface(root,interface)
    if skill_interface(skill)!={'display_name':interface['displayName'],'short_description':interface['shortDescription']}:
        raise ValueError('Skill interface metadata diverges from plugin manifest')
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
        raise ValueError('Expected one canonical PromptingCraft.com plugin')
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
