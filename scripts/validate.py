#!/usr/bin/env python3
"""Validate this project's constrained metadata and self-contained resources offline."""
import json
import zipfile
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
    # Standards (agentskills.io) and agent-product docs (cursor.com) cannot back model prompting advice.
    excluded={name for name,policy in registry['policies'].items() if policy.get('classification') in ('standard','agent-product')}
    sources={row['canonical_url']:row['provider'] for row in registry['sources'] if row['provider'] not in excluded}
    identifiers=set()
    labels={'OFFICIAL','GENERAL','MODEL_SPECIFIC','INFERRED','EXPERIMENTAL'}
    fields=('id','provider','source_title','url','retrieval_date','applicable_model_family',
            'recommendation','evidence_or_limitation','promptingcraft_applicability',
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
# OpenAI Plugins Directory rules (developers.openai.com/plugins/deploy/submission-errors).
DIRECTORY_CATEGORIES=('Productivity','Creativity','Developer Tools','Business & Operations','Data & Analytics',
                      'Communication','Education & Research','Security','Finance','Healthcare','Travel',
                      'Entertainment','Other')
PORTABLE_MANIFEST_FIELDS={'$schema','name','version','description','author','homepage','repository','license','keywords','extensions'}
MAX_DEFAULT_PROMPTS=3
MAX_DEFAULT_PROMPT_LENGTH=128
MAX_CAPABILITIES=20
MAX_CAPABILITY_LENGTH=120
# Directory uploads reject app and hook configuration; the one MCP server is declared only in
# the root mcp.json (portable format), never in a Codex .mcp.json or a nested file.
EXCLUDED_CONFIG_FILES=('mcp.json','.mcp.json','.app.json','hooks.json')
MCP_SCHEMA='https://agent-plugins.org/schemas/1.0.0/mcp.schema.json'
MCP_SERVER_NAME='promptingcraft-guidance'
MCP_URL='https://mcp.promptingcraft.com/mcp'
MCP_TOOLS={'search_guidance','get_guidance','check_source_freshness'}
OPENAI_SETTINGS={'interface','review','publication'}
REVIEW_FIELDS={'test_cases','demo_recording_url','commerce','commerce_description'}
POSITIVE_CASE_FIELDS={'description','prompt','tools_triggered','expected_behavior'}
NEGATIVE_CASE_FIELDS={'description','prompt'}
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
    if interface['category'] not in DIRECTORY_CATEGORIES: raise ValueError('Unknown directory category')
    if 'screenshots' in interface: raise ValueError('Skills-only packages cannot declare screenshots')
    prompts=interface.get('defaultPrompt')
    if not isinstance(prompts,list) or not prompts or any(not isinstance(p,str) or not p.strip() for p in prompts):
        raise ValueError('Invalid interface defaultPrompt')
    normalized=[' '.join(p.split()).casefold() for p in prompts]
    if len(prompts)>MAX_DEFAULT_PROMPTS or len(set(normalized))!=len(prompts):
        raise ValueError('Directory allows at most three unique starter prompts')
    for prompt in prompts:
        if len(prompt)>MAX_DEFAULT_PROMPT_LENGTH or '\n' in prompt or '@' in prompt:
            raise ValueError('Starter prompts must be one line, at most 128 characters, without @mentions')
    capabilities=interface.get('capabilities',[])
    if not isinstance(capabilities,list) or len(capabilities)>MAX_CAPABILITIES:
        raise ValueError('Directory allows at most 20 capabilities')
    if len({' '.join(str(c).split()).casefold() for c in capabilities})!=len(capabilities):
        raise ValueError('Capabilities must be unique')
    for capability in capabilities:
        if not isinstance(capability,str) or not capability.strip() or len(capability)>MAX_CAPABILITY_LENGTH or '\n' in capability:
            raise ValueError('Capabilities must be non-empty, one line and at most 120 characters')
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


def validate_publication(openai):
    """Release notes are required with an MCP server; countries stay unrestricted."""
    if 'publication' not in openai: raise ValueError('Missing publication release notes')
    publication=openai['publication']
    if not isinstance(publication,dict) or set(publication)!={'release_notes'}: raise ValueError('Unsupported publication settings')
    notes=publication['release_notes']
    if not isinstance(notes,str) or not notes.strip() or len(notes)>4000: raise ValueError('Invalid release notes')


def validate_mcp_config(config):
    """Exactly the production guidance server: streamable HTTP, no headers, no auth settings."""
    if not isinstance(config,dict) or set(config)!={'$schema','mcpServers'} or config['$schema']!=MCP_SCHEMA:
        raise ValueError('mcp.json must use the Agent Plugins MCP schema')
    servers=config['mcpServers']
    if not isinstance(servers,dict) or list(servers)!=[MCP_SERVER_NAME]: raise ValueError('mcp.json must declare exactly one server')
    if servers[MCP_SERVER_NAME]!={'type':'streamable-http','url':MCP_URL}:
        raise ValueError('MCP server must be the production streamable HTTP endpoint without headers')


def validate_review(openai):
    """MCP review information: exactly five positive and three negative cases and a demo URL."""
    review=openai.get('review')
    if not isinstance(review,dict) or set(review)-REVIEW_FIELDS: raise ValueError('Invalid review settings')
    cases=review.get('test_cases')
    if not isinstance(cases,dict) or set(cases)!={'positive','negative'}: raise ValueError('Review needs positive and negative test cases')
    positive,negative=cases['positive'],cases['negative']
    if not isinstance(positive,list) or not isinstance(negative,list) or len(positive)!=5 or len(negative)!=3:
        raise ValueError('Review needs exactly five positive and three negative test cases')
    for case,fields in [(c,POSITIVE_CASE_FIELDS) for c in positive]+[(c,NEGATIVE_CASE_FIELDS) for c in negative]:
        if not isinstance(case,dict) or set(case)!=fields or not all(isinstance(case[f],str) and case[f].strip() for f in fields):
            raise ValueError('Incomplete review test case')
        if '@' in case['prompt']: raise ValueError('Review prompts must not mention plugins')
    for case in positive:
        tools={t.strip() for t in case['tools_triggered'].split(',')}
        if not tools or tools-MCP_TOOLS: raise ValueError('Review case names an unknown tool')
    if not https_url(review.get('demo_recording_url')): raise ValueError('Review needs an HTTPS demo recording URL')
    if review.get('commerce') is not False: raise ValueError('PromptingCraft.com declares no commerce')


def validate_project(root):
    root=Path(root); skill=root/'skills/promptingcraft'; meta=validate_skill(skill)
    manifest=json.loads((root/'plugin.json').read_text())
    if set(manifest)-PORTABLE_MANIFEST_FIELDS: raise ValueError('Unknown portable manifest field')
    if manifest.get('$schema')!='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json': raise ValueError('Wrong schema')
    if manifest.get('name')!='promptingcraft' or manifest.get('version')!=meta['metadata']['version']: raise ValueError('Version/name mismatch')
    for k in ('description','homepage','repository','license'):
        if not isinstance(manifest.get(k),str) or not manifest[k]: raise ValueError('Invalid manifest string')
    if manifest['author']!={'name':'Aleksandr Prokofyev','url':'https://promptingcraft.com'}: raise ValueError('Author metadata mismatch')
    compatibility=json.loads((root/'.claude-plugin/plugin.json').read_text())
    if compatibility!={k:v for k,v in manifest.items() if k!='$schema'}: raise ValueError('Divergent adapter metadata')
    if not https_url(manifest['homepage']) or not https_url(manifest['repository']): raise ValueError('Manifest URLs must be https')
    if not manifest['description'].endswith(ATTRIBUTION) or not meta['description'].endswith(ATTRIBUTION): raise ValueError('Missing attribution')
    openai=manifest.get('extensions',{}).get('com.openai',{})
    if set(openai)-OPENAI_SETTINGS: raise ValueError('Package declares apps, hooks or unsupported OpenAI settings')
    validate_publication(openai)
    validate_review(openai)
    validate_mcp_config(json.loads((root/'mcp.json').read_text()))
    for name in EXCLUDED_CONFIG_FILES[1:]:
        if (root/name).exists(): raise ValueError(f'Unsupported configuration file {name}')
    interface=openai.get('interface')
    validate_interface(root,interface)
    if skill_interface(skill)!={'display_name':interface['displayName'],'short_description':interface['shortDescription']}:
        raise ValueError('Skill interface metadata diverges from plugin manifest')
    if (skill/'LICENSE').read_bytes()!=(root/'LICENSE').read_bytes(): raise ValueError('License mismatch')
    if (root/'.github/workflows').exists(): raise ValueError('GitHub Actions are out of scope')
    for path in skill.rglob('*'):
        if path.is_symlink(): raise ValueError('Symlink in standalone skill')
    return manifest

def validate_submission_archive(path):
    """Check our plugin ZIP (one top-level plugin directory) against OpenAI upload rules verifiable offline.

    The 512 MiB extracted and 5,000-entry limits are the portal's archive limits; images and
    descriptions are checked on the source tree by validate_project before packaging.
    """
    with zipfile.ZipFile(path) as archive:
        infos=archive.infolist()
        if not infos or len(infos)>5000: raise ValueError('Archive is empty or has too many entries')
        if sum(i.file_size for i in infos)>512*1024*1024: raise ValueError('Archive is too large when extracted')
        names=[i.filename for i in infos]
        if len(set(names))!=len(names): raise ValueError('Duplicate archive path')
        for info in infos:
            name=info.filename
            mode=(info.external_attr>>16)&0o170000
            if mode not in (0,0o100000,0o040000) or info.flag_bits&0x1: raise ValueError(f'Unsupported archive member {name}')
            parts=name.rstrip('/').split('/')
            if (not name or name!=name.strip() or '\\' in name or name.startswith('/') or ''.join(parts[:1]).endswith(':')
                    or any(part in ('','.','..') for part in parts) or len(parts)>20):
                raise ValueError(f'Unsafe archive path {name!r}')
            if (parts[-1] in EXCLUDED_CONFIG_FILES and parts[1:]!=['mcp.json']) or 'hooks' in parts[1:2]:
                raise ValueError(f'Archive contains excluded configuration {name}')
        roots={n.split('/',1)[0] for n in names}
        if len(roots)!=1 or any('/' not in n for n in names): raise ValueError('Archive needs exactly one top-level plugin directory')
        root=roots.pop()+'/'
        manifest=json.loads(archive.read(root+'plugin.json'))
        if set(manifest)-PORTABLE_MANIFEST_FIELDS: raise ValueError('Archive manifest has unsupported top-level fields')
        if root+'.claude-plugin/plugin.json' in names:
            adapter=json.loads(archive.read(root+'.claude-plugin/plugin.json'))
            if adapter!={k:v for k,v in manifest.items() if k!='$schema'}: raise ValueError('Archive adapter manifest diverges')
        openai=manifest.get('extensions',{}).get('com.openai',{})
        if not isinstance(openai.get('interface'),dict): raise ValueError('Archive manifest lacks interface metadata')
        if set(openai)-OPENAI_SETTINGS or 'screenshots' in openai.get('interface',{}): raise ValueError('Archive manifest declares excluded settings')
        validate_publication(openai)
        validate_review(openai)
        if root+'mcp.json' not in names: raise ValueError('Archive is missing mcp.json')
        validate_mcp_config(json.loads(archive.read(root+'mcp.json')))
        for field in INTERFACE_ASSETS:
            value=openai['interface'].get(field)
            if not isinstance(value,str) or root+value[2:] not in names: raise ValueError(f'Archive is missing {field}')
        skills={n[len(root):].split('/')[1] for n in names if n.startswith(root+'skills/') and n.count('/')>=3}
        if not skills or any(s.startswith('.') or root+f'skills/{s}/SKILL.md' not in names for s in skills):
            raise ValueError('Every packaged skill needs skills/<name>/SKILL.md')
        for skill in skills:
            text=archive.read(root+f'skills/{skill}/SKILL.md').decode('utf-8')
            head=re.match(r'---\n(.*?)\n---\n',text,re.S)
            fields=dict(re.findall(r'^(name|description):\s*(.+)$',head.group(1),re.M)) if head else {}
            if fields.get('name')!=skill or not 0<len(fields.get('description',''))<=1024 or len(f"{manifest['name']}:{skill}")>64:
                raise ValueError(f'Packaged skill {skill} has invalid frontmatter')
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
    if set(plugin) != {'name', 'source', 'policy', 'category'} or plugin['name'] != 'promptingcraft':
        raise ValueError('Invalid marketplace plugin entry')
    if plugin['policy'] != {'installation': 'AVAILABLE', 'authentication': 'ON_USE'}:
        raise ValueError('Invalid marketplace policy')
    if plugin['category'] != 'Developer Tools':
        raise ValueError('Invalid marketplace category')
    source = plugin['source']
    # A constrained generated destination prevents the materializer replacing source files.
    if source != {'source': 'local', 'path': './dist/promptingcraft-plugin'}:
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
