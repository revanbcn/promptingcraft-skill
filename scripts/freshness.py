#!/usr/bin/env python3
"""Bounded, read-only public documentation monitoring. Python 3.11+, stdlib."""
import argparse
import copy
import hashlib
import http.client
import ipaddress
import json
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_SOURCES = 32
TIMEOUT = 15


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')


def validate_url(url, policy, resolve=False):
    parsed=urllib.parse.urlsplit(url)
    if (parsed.scheme != 'https' or parsed.username or parsed.password or parsed.port not in (None,443)
            or parsed.hostname not in policy['hosts'] or parsed.query or parsed.fragment
            or len(url)>2048 or '%' in parsed.path or '\\' in url or any(x in parsed.path.split('/') for x in ('.','..'))
            or any(ord(x)<33 for x in url)):
        raise ValueError('URL outside explicit public HTTPS policy')
    if not any(parsed.path.startswith(p) for p in policy['path_prefixes']):
        raise ValueError('Path outside policy')
    if resolve:
        addresses=socket.getaddrinfo(parsed.hostname,443,type=socket.SOCK_STREAM)
        if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
            raise ValueError('Non-public DNS destination')
    return url


def validate_registry(registry):
    if registry.get('schema_version') != 1 or not isinstance(registry.get('sources'),list):
        raise ValueError('Invalid registry schema')
    if len(registry['sources'])>MAX_SOURCES: raise ValueError('Registry exceeds fetch bound')
    policies=registry.get('policies',{})
    for policy in policies.values():
        if not policy.get('hosts') or not policy.get('path_prefixes'): raise ValueError('Missing policy')
        for host in policy['hosts']:
            if not re.fullmatch(r'[a-z0-9.-]+',host) or '.' not in host: raise ValueError('Invalid host')
            try: ipaddress.ip_address(host)
            except ValueError: pass
            else: raise ValueError('IP literal prohibited')
        if any(not p.startswith('/') or '..' in p or '%' in p for p in policy['path_prefixes']):
            raise ValueError('Invalid path prefix')
    seen=set()
    for source in registry['sources']:
        sid=source.get('id','')
        if not re.fullmatch(r'[a-z0-9-]+',sid) or sid in seen: raise ValueError('Invalid/duplicate id')
        seen.add(sid)
        if source.get('provider') not in policies or source.get('role') not in ('guidance','index','packaging','evaluation'):
            raise ValueError('Invalid source provider/role')
        if not source.get('applicability'): raise ValueError('Missing applicability')
        days=source.get('refresh_policy',{}).get('max_age_days')
        if not isinstance(days,int) or isinstance(days,bool) or not 1<=days<=365: raise ValueError('Invalid refresh interval')
        validate_url(source['canonical_url'],policies[source['provider']])
        if source['role']=='index':
            pattern=source.get('candidate_pattern','')
            if not pattern or len(pattern)>160: raise ValueError('Missing/bounded candidate pattern')
            re.compile(pattern)
    return registry


class ContentParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts=[]; self.main_parts=[]; self.skip=0; self.main=0; self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','nav','header','footer','aside','noscript'): self.skip+=1
        if tag in ('main','article'): self.main+=1
        if tag=='a':
            href=dict(attrs).get('href')
            if href: self.links.append(href)
    def handle_endtag(self,tag):
        if tag in ('script','style','nav','header','footer','aside','noscript'): self.skip=max(0,self.skip-1)
        if tag in ('main','article'): self.main=max(0,self.main-1)
    def handle_data(self,data):
        if not self.skip:
            self.parts.append(data)
            if self.main: self.main_parts.append(data)


def normalize(body,content_type,role):
    if len(body)>MAX_BYTES: raise ValueError('Response exceeds size limit')
    text=body.decode('utf-8-sig',errors='strict')
    ctype=content_type.split(';')[0].strip().lower()
    if ctype not in ('text/html','text/plain','text/markdown','text/x-markdown','application/xhtml+xml'):
        raise ValueError('Unsupported documentation MIME type')
    if '\x00' in text: raise ValueError('Binary response')
    if ctype in ('text/html','application/xhtml+xml'):
        p=ContentParser(); p.feed(text)
        text=' '.join(p.main_parts or p.parts)
    text=re.sub(r'\s+',' ',text).strip()
    if len(text)<100 or len(text.split())<12: raise ValueError('No usable source content')
    prefix=text[:500].lower()
    if any(x in prefix for x in ('verify you are human','just a moment','access denied','checking your browser','captcha challenge')):
        raise ValueError('Access challenge, not documentation')
    return text


def discover(body,base,policy,pattern):
    text=body.decode('utf-8-sig',errors='strict')
    parser=ContentParser(); parser.feed(text)
    refs=parser.links+re.findall(r'\]\(([^\s)]+)\)',text)
    refs+=re.findall(r'^https://[^\s]+',text,re.M)
    candidates=set()
    for ref in refs:
        url=urllib.parse.urljoin(base,ref).split('#')[0]
        # Markdown variants identify the same documentation page.
        if url.endswith('.md'): url=url[:-3]
        try: validate_url(url,policy)
        except ValueError: continue
        if re.search(pattern,url,re.I): candidates.add(url)
    if len(candidates)>5000: raise ValueError('Index candidate bound exceeded')
    return sorted(candidates)


class PolicyRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self,policy):
        self.policy=policy; self.count=0
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        self.count+=1
        if self.count>4: raise ValueError('Redirect limit exceeded')
        validate_url(newurl,self.policy,resolve=True)
        redirected=super().redirect_request(req,fp,code,msg,headers,newurl)
        if redirected:
            for header in ('If-none-match','If-modified-since'): redirected.remove_header(header)
        return redirected


def fetch_public(url,policy,validators):
    validate_url(url,policy,resolve=True)
    headers={'User-Agent':'PromptingCraft.com-docs-check/0.2 (public read-only)',
             'Accept':'text/markdown,text/plain,text/html', 'Accept-Encoding':'identity'}
    if validators.get('etag'): headers['If-None-Match']=validators['etag']
    if validators.get('last_modified'): headers['If-Modified-Since']=validators['last_modified']
    # No ambient proxy credentials, cookies, netrc, or authenticated session.
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),PolicyRedirect(policy))
    try: result=opener.open(urllib.request.Request(url,headers=headers),timeout=TIMEOUT)
    except urllib.error.HTTPError as error: result=error
    with result:
        data=result.read(MAX_BYTES+1)
        return {'status':result.code,'body':data,'url':result.geturl(),
                'headers':{k.lower():v for k,v in result.headers.items()}}


def check(registry,baseline,fetch=fetch_public,checked_at=None,budget_seconds=180):
    validate_registry(registry)
    checked_at=checked_at or timestamp(); previous=baseline.get('sources',{})
    rows=[]; start=time.monotonic()
    for source in registry['sources']:
        sid=source['id']; url=source['canonical_url']; old=previous.get(sid,{})
        # A new canonical target cannot inherit validators/content from the old URL.
        if old.get('canonical_url')!=url: old={}
        row={'id':sid,'provider':source['provider'],'canonical_url':url,'checked_at':checked_at,
             'source_published_at':None,'source_updated_at':None,'withdrawal_confirmed':False}
        try:
            if time.monotonic()-start>=budget_seconds: raise TimeoutError('Run budget exhausted')
            policy=registry['policies'][source['provider']]
            res=fetch(url,policy,{k:old[k] for k in ('etag','last_modified') if old.get(k)})
            validate_url(res['url'],policy)
            headers={k.lower():v for k,v in res['headers'].items()}
            row.update(http_status=res['status'],resolved_url=res['url'],
                       retry_after=headers.get('retry-after'))
            if res['status']==304:
                if not old.get('hash'): raise ValueError('304 without usable baseline')
                row.update({k:copy.deepcopy(old[k]) for k in ('hash','etag','last_modified','candidates','last_content_checked_at') if k in old})
                row.update(state='unchanged',verification='conditional-not-modified')
            elif res['status']==200:
                content=normalize(res['body'],headers.get('content-type',''),source['role'])
                digest=hashlib.sha256(content.encode()).hexdigest()
                row.update(hash=digest,etag=headers.get('etag'),last_modified=headers.get('last-modified'),
                           last_content_checked_at=checked_at,verification='usable-content-fetched',
                           state='new' if not old.get('hash') else ('unchanged' if old['hash']==digest else 'changed'))
                if source['role']=='index':
                    links=discover(res['body'],res['url'],policy,source['candidate_pattern'])
                    row.update(candidates=links,new_candidates=sorted(set(links)-set(old.get('candidates',[]))),
                               removed_candidates=sorted(set(old.get('candidates',[]))-set(links)))
            else:
                row.update(state='unavailable',reason='HTTP response did not supply documentation')
        except (ValueError,UnicodeError,OSError,urllib.error.URLError,http.client.HTTPException,KeyError,TypeError) as error:
            row.update(state='error',reason=type(error).__name__)
        rows.append(row)
    failed=sum(x['state'] in ('error','unavailable') for x in rows)
    return {'schema_version':1,'checked_at':checked_at,
            'overall':'error' if rows and all(x['state']=='error' for x in rows) else ('partial' if failed else 'complete'),
            'sources':rows,'removed_from_registry':sorted(set(previous)-{x['id'] for x in rows}),
            'note':'Unavailable pages and absent index links do not prove guidance withdrawal. No instructions are rewritten.'}


def baseline_from(report,previous):
    result=copy.deepcopy(previous or {'schema_version':1,'sources':{}})
    result.setdefault('sources',{})
    for row in report['sources']:
        if row['state'] in ('new','changed','unchanged') and row.get('hash'):
            result['sources'][row['id']]={k:copy.deepcopy(v) for k,v in row.items()
                                        if k not in ('state','reason','new_candidates','removed_candidates')}
    return result


def readable(report):
    lines=[f"# PromptingCraft.com freshness — {report['overall']}",f"Checked at: {report['checked_at']}",'']
    for row in report['sources']:
        lines.append(f"- {row['id']}: **{row['state']}** — {row['canonical_url']}")
        if row.get('new_candidates'): lines.append('  New candidates: '+', '.join(row['new_candidates']))
        if row.get('removed_candidates'): lines.append('  Missing index links (not withdrawal): '+', '.join(row['removed_candidates']))
        if row.get('reason'): lines.append('  Reason: '+row['reason'])
    if report['removed_from_registry']: lines.append('Removed from registry: '+', '.join(report['removed_from_registry']))
    lines.extend(['',report['note'],'Fetch times and HTTP Last-Modified are not publication dates.'])
    return '\n'.join(lines)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registry',type=Path,default=Path('skills/promptcraft/references/sources.json'))
    parser.add_argument('--baseline',type=Path,default=Path('sources-baseline.json'))
    parser.add_argument('--output',type=Path,required=True,help='Untracked/private output directory')
    parser.add_argument('--write-baseline',action='store_true',help='Write proposed baseline only to the output directory; review before committing')
    args=parser.parse_args()
    registry=json.loads(args.registry.read_text())
    baseline=json.loads(args.baseline.read_text()) if args.baseline.exists() else {}
    report=check(registry,baseline)
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'freshness.json').write_text(json.dumps(report,indent=2)+'\n')
    (args.output/'freshness.md').write_text(readable(report))
    if args.write_baseline: (args.output/'baseline-proposed.json').write_text(json.dumps(baseline_from(report,baseline),indent=2)+'\n')
    print(readable(report))
    return 0 if report['overall']=='complete' else 2

if __name__=='__main__': raise SystemExit(main())
