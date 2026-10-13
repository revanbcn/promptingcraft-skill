import hashlib
import json
import re
import tempfile
import unittest
import zipfile
from pathlib import Path
from scripts.package import build
from scripts.install_skill import install
from scripts.validate import validate_project

ROOT=Path(__file__).resolve().parents[1]
class PackagingTests(unittest.TestCase):
    def test_project_metadata_resources_and_registry(self):
        validate_project(ROOT)
    def test_archives_reproducible_self_contained_and_checksums(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            first=build(ROOT,Path(a)); second=build(ROOT,Path(b))
            self.assertEqual([p.name for p in first],[p.name for p in second])
            for x,y in zip(first,second):
                self.assertEqual(x.read_bytes(),y.read_bytes())
                with zipfile.ZipFile(x) as z:
                    names=z.namelist(); self.assertTrue(any(n.endswith('/SKILL.md') for n in names))
                    self.assertTrue(any(n.endswith('/references/sources.json') for n in names))
                    self.assertFalse(any('.git/' in n or '__pycache__' in n for n in names))
                    z.extractall(Path(a)/x.stem)
                    root=Path(a)/x.stem/('promptingcraft' if 'skill-' in x.name else 'promptingcraft-plugin')
                    skill=root if 'skill-' in x.name else root/'skills/promptingcraft'
                    self.assertTrue((skill/'references/rubric.md').is_file())
                    self.assertEqual((skill/'LICENSE').read_bytes(),(ROOT/'LICENSE').read_bytes())
                    for page in root.rglob('*.md'):
                        for link in re.findall(r'\]\(([^)]+)\)',page.read_text()):
                            if not link.startswith('https://'):
                                self.assertTrue((page.parent/link).is_file(),(page,link))
            self.assertEqual([p.name for p in first],['promptingcraft-skill-0.3.0.zip','promptingcraft-plugin-0.3.0.zip'])
            with zipfile.ZipFile(first[1]) as z:
                names=set(z.namelist())
                for asset in ('icon.svg','icon-dark.svg','logo.svg','logo-dark.svg'):
                    self.assertIn('promptingcraft-plugin/assets/'+asset,names)
                    self.assertEqual(z.read('promptingcraft-plugin/assets/'+asset),(ROOT/'assets'/asset).read_bytes())
                self.assertIn('promptingcraft-plugin/skills/promptingcraft/SKILL.md',names)
                self.assertEqual(z.read('promptingcraft-plugin/mcp.json'),(ROOT/'mcp.json').read_bytes())
            with zipfile.ZipFile(first[0]) as z:
                self.assertFalse(any('/assets/' in n for n in z.namelist()))
            sums=(Path(a)/'SHA256SUMS').read_text()
            for x in first: self.assertIn(hashlib.sha256(x.read_bytes()).hexdigest(),sums)
    def test_install_isolated_hosts_and_refuse_overwrite(self):
        for host,folder in [('codex','.agents'),('claude','.claude'),('cursor','.cursor')]:
            with tempfile.TemporaryDirectory() as d:
                dest=install(ROOT/'skills/promptingcraft',Path(d),host)
                self.assertEqual(dest,Path(d)/folder/'skills/promptingcraft')
                self.assertTrue((dest/'references/sources.json').exists())
                self.assertFalse(any('__pycache__' in p.parts or p.suffix == '.pyc' for p in dest.rglob('*')))
                with self.assertRaises(FileExistsError): install(ROOT/'skills/promptingcraft',Path(d),host)
    def test_install_refuses_symlink_destination(self):
        with tempfile.TemporaryDirectory() as d,tempfile.TemporaryDirectory() as out:
            (Path(d)/'.agents').symlink_to(out,target_is_directory=True)
            with self.assertRaises(ValueError): install(ROOT/'skills/promptingcraft',Path(d),'codex')


class SubmissionArchiveTests(unittest.TestCase):
    def built(self, directory):
        return build(ROOT, Path(directory))[1]

    def rewrite(self, source, target, extra=None, drop=None, rename=None, patch_manifest=None, patch_adapter=None):
        patches = {'promptingcraft-plugin/plugin.json': patch_manifest,
                   'promptingcraft-plugin/.claude-plugin/plugin.json': patch_adapter}
        with zipfile.ZipFile(source) as old, zipfile.ZipFile(target, 'w') as new:
            for info in old.infolist():
                if drop and info.filename == drop: continue
                name = rename(info.filename) if rename else info.filename
                data = old.read(info.filename)
                if patches.get(info.filename):
                    data = json.dumps({**json.loads(data), **patches[info.filename]}).encode()
                new.writestr(name, data)
            for name, data in (extra or {}).items(): new.writestr(name, data)
        return target

    def test_built_plugin_archive_passes_offline_submission_rules(self):
        from scripts.validate import validate_submission_archive
        with tempfile.TemporaryDirectory() as d:
            manifest = validate_submission_archive(self.built(d))
            self.assertEqual(manifest['extensions']['com.openai']['interface']['category'], 'Developer Tools')

    def test_submission_archive_rejects_excluded_or_unsafe_content(self):
        from scripts.validate import validate_submission_archive
        with tempfile.TemporaryDirectory() as d:
            source = self.built(d)
            variants = {
                'mcp': dict(extra={'promptingcraft-plugin/.mcp.json': '{}'}),
                'nested mcp': dict(extra={'promptingcraft-plugin/skills/promptingcraft/mcp.json': '{}'}),
                'app': dict(extra={'promptingcraft-plugin/.app.json': '{}'}),
                'hooks': dict(extra={'promptingcraft-plugin/hooks/hooks.json': '{}'}),
                'sibling': dict(extra={'README.md': 'x'}),
                'parent': dict(extra={'promptingcraft-plugin/../x': 'x'}),
                'missing skill': dict(drop='promptingcraft-plugin/skills/promptingcraft/SKILL.md'),
                'missing logo': dict(drop='promptingcraft-plugin/assets/logo.svg'),
                'missing mcp.json': dict(drop='promptingcraft-plugin/mcp.json'),
                'top-level mcpServers': dict(rename=None, extra=None, drop=None, patch_manifest={'mcpServers': './.mcp.json'}),
                'divergent adapter': dict(patch_adapter={'version': '9.9.9'}),
            }
            for label, change in variants.items():
                with self.subTest(label):
                    target = self.rewrite(source, Path(d) / f'{label}.zip', **change)
                    with self.assertRaises((ValueError, KeyError)):
                        validate_submission_archive(target)
