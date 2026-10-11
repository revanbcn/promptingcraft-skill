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
                    root=Path(a)/x.stem/('promptcraft' if 'skill-' in x.name else 'promptcraft-plugin')
                    skill=root if 'skill-' in x.name else root/'skills/promptcraft'
                    self.assertTrue((skill/'references/rubric.md').is_file())
                    self.assertEqual((skill/'LICENSE').read_bytes(),(ROOT/'LICENSE').read_bytes())
                    for page in root.rglob('*.md'):
                        for link in re.findall(r'\]\(([^)]+)\)',page.read_text()):
                            if not link.startswith('https://'):
                                self.assertTrue((page.parent/link).is_file(),(page,link))
            sums=(Path(a)/'SHA256SUMS').read_text()
            for x in first: self.assertIn(hashlib.sha256(x.read_bytes()).hexdigest(),sums)
    def test_install_isolated_hosts_and_refuse_overwrite(self):
        for host,folder in [('codex','.agents'),('claude','.claude')]:
            with tempfile.TemporaryDirectory() as d:
                dest=install(ROOT/'skills/promptcraft',Path(d),host)
                self.assertEqual(dest,Path(d)/folder/'skills/promptcraft')
                self.assertTrue((dest/'references/sources.json').exists())
                with self.assertRaises(FileExistsError): install(ROOT/'skills/promptcraft',Path(d),host)
    def test_install_refuses_symlink_destination(self):
        with tempfile.TemporaryDirectory() as d,tempfile.TemporaryDirectory() as out:
            (Path(d)/'.agents').symlink_to(out,target_is_directory=True)
            with self.assertRaises(ValueError): install(ROOT/'skills/promptcraft',Path(d),'codex')
