#!/usr/bin/env python3
"""Build byte-reproducible portable skill and plugin ZIPs, with SHA-256 checksums."""
import argparse
import hashlib
import zipfile
from pathlib import Path
try:
    from scripts.validate import validate_project
except ModuleNotFoundError:
    from validate import validate_project


def build(root,output):
    root=Path(root); output=Path(output); manifest=validate_project(root)
    output.mkdir(parents=True,exist_ok=True)
    version=manifest['version']; skill=root/'skills/promptcraft'
    skill_files=[p for p in sorted(skill.rglob('*')) if p.is_file()]
    plugin_files=skill_files+[root/p for p in ('plugin.json','.claude-plugin/plugin.json','LICENSE','README.md')]
    files=[]
    for kind,items in [('skill',skill_files),('plugin',plugin_files)]:
        dest=output/f'promptcraft-{kind}-{version}.zip'
        with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for p in sorted(items):
                if p.is_symlink(): raise ValueError('Archive cannot contain symlinks')
                relative=p.relative_to(skill if kind=='skill' else root)
                name=('promptcraft' if kind=='skill' else 'promptcraft-plugin')+'/'+relative.as_posix()
                info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0))
                info.create_system=3; info.external_attr=0o100644<<16; info.compress_type=zipfile.ZIP_DEFLATED
                payload=(root/'docs/plugin-archive.md').read_bytes() if kind=='plugin' and p==root/'README.md' else p.read_bytes()
                archive.writestr(info,payload,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
        files.append(dest)
    sums=''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in files)
    (output/'SHA256SUMS').write_text(sums)
    return files

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--output',type=Path,default=Path('dist'))
    args=parser.parse_args(); print('\n'.join(str(p) for p in build(Path(__file__).resolve().parents[1],args.output)))
