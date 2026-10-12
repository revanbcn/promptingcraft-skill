import copy
import json
import re
import shutil
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from scripts.validate import validate_interface, validate_project

ROOT = Path(__file__).resolve().parents[1]
ASSET_FIELDS = ('composerIcon', 'composerIconDark', 'logo', 'logoDark')
URL_FIELDS = ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL')


def png(width, height):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    header = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', header) + chunk(b'IEND', b'')


class InterfaceTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / 'plugin.json').read_text())
        self.interface = self.manifest['extensions']['com.openai']['interface']

    def sandbox(self, directory):
        root = Path(directory).resolve() / 'repo'
        root.mkdir()
        shutil.copytree(ROOT / 'assets', root / 'assets')
        return root

    def test_published_interface_metadata(self):
        validate_interface(ROOT, self.interface)
        # Stable technical id kept for installed v0.1.0 and local marketplace installs.
        self.assertEqual(self.manifest['name'], 'promptcraft')
        self.assertEqual(self.manifest['version'], '0.2.0')
        self.assertEqual(self.manifest['homepage'], 'https://promptingcraft.com')
        self.assertEqual(self.manifest['repository'], 'https://gitlab.com/revanalex/promptingcraft-skill')
        self.assertEqual(self.interface['displayName'], 'PromptingCraft.com')
        self.assertTrue(self.interface['longDescription'].startswith('PromptingCraft.com '))
        self.assertEqual(self.interface['developerName'], 'DondeGo team')
        self.assertEqual(self.interface['websiteURL'], 'https://promptingcraft.com')
        self.assertEqual(self.interface['supportURL'], 'https://promptingcraft.com/contact')
        self.assertEqual(self.interface['privacyPolicyURL'], 'https://promptingcraft.com/privacy')
        self.assertEqual(self.interface['termsOfServiceURL'], 'https://promptingcraft.com/terms')
        self.assertTrue(self.interface['longDescription'].endswith('Developed by the dondego.com team.'))
        self.assertNotIn('by DondeGo', json.dumps(self.manifest))

    def test_current_public_files_show_only_the_promptingcraft_com_brand(self):
        # Walk the working tree (CI images may lack git). Generated output and recorded
        # historical evidence keep their original wording and are excluded.
        skipped_dirs = {'.git', 'dist', '__pycache__', 'reports', 'node_modules'}
        historical = ('evals/results/', 'docs/superpowers/')
        # Frozen evaluation-harness wording; changing it would alter recorded eval semantics.
        frozen = {'tests/test_interface.py', 'scripts/evaluate.py', 'scripts/evaluate_fidelity.py'}
        files = []
        for path in sorted(ROOT.rglob('*')):
            rel = path.relative_to(ROOT).as_posix()
            if not path.is_file() or skipped_dirs.intersection(path.relative_to(ROOT).parts):
                continue
            if rel.startswith(historical) or re.fullmatch(r'docs/.*-ledger\.md', rel) or rel in frozen:
                continue
            files.append(path)
        stale = re.compile(r'PromptCraft|Promptcraft|by DondeGo')
        offenders = []
        for path in files:
            try:
                text = path.read_text()
            except (UnicodeDecodeError, FileNotFoundError):
                continue
            offenders += [f'{path.relative_to(ROOT)}:{n}' for n, line in enumerate(text.splitlines(), 1)
                          if stale.search(line)]
        self.assertEqual(offenders, [])
        for asset in (ROOT / 'assets').glob('*.svg'):
            self.assertIn('aria-label="PromptingCraft.com"', asset.read_text())
        self.assertIn('display_name: "PromptingCraft.com"',
                      (ROOT / 'skills/promptcraft/agents/openai.yaml').read_text())
        self.assertIn('\n# PromptingCraft.com\n', (ROOT / 'skills/promptcraft/SKILL.md').read_text())

    def test_text_limits(self):
        for field, limit in (('displayName', 30), ('shortDescription', 30), ('longDescription', 4000)):
            with self.subTest(field=field):
                interface = copy.deepcopy(self.interface)
                interface[field] = 'x' * (limit + 1)
                with self.assertRaises(ValueError):
                    validate_interface(ROOT, interface)

    def test_policy_urls_must_be_https(self):
        for field in URL_FIELDS:
            for value in ('http://promptingcraft.com', 'promptingcraft.com', '', None, 'https://'):
                with self.subTest(field=field, value=value):
                    interface = copy.deepcopy(self.interface)
                    interface[field] = value
                    with self.assertRaises(ValueError):
                        validate_interface(ROOT, interface)

    def test_asset_paths_are_package_relative_and_present(self):
        for field in ASSET_FIELDS:
            for value in ('assets/icon.svg', '/assets/icon.svg', './assets/missing.svg',
                          './../assets/icon.svg', 'https://promptingcraft.com/icon.svg'):
                with self.subTest(field=field, value=value):
                    interface = copy.deepcopy(self.interface)
                    interface[field] = value
                    with self.assertRaises(ValueError):
                        validate_interface(ROOT, interface)

    def test_assets_must_be_square_svg_or_png(self):
        cases = {
            'wide.svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 64"/>',
            'tiny.svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"/>',
            'noview.svg': '<svg xmlns="http://www.w3.org/2000/svg"/>',
            'script.svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><script>x</script></svg>',
            'broken.svg': '<svg',
            'icon.gif': 'GIF89a',
        }
        with tempfile.TemporaryDirectory() as directory:
            root = self.sandbox(directory)
            for name, content in cases.items():
                (root / 'assets' / name).write_text(content)
                with self.subTest(name=name):
                    interface = copy.deepcopy(self.interface)
                    interface['logo'] = './assets/' + name
                    with self.assertRaises(ValueError):
                        validate_interface(root, interface)
            (root / 'assets/wide.png').write_bytes(png(128, 64))
            interface = copy.deepcopy(self.interface)
            interface['logo'] = './assets/wide.png'
            with self.assertRaises(ValueError):
                validate_interface(root, interface)
            (root / 'assets/square.png').write_bytes(png(128, 128))
            interface['logo'] = './assets/square.png'
            validate_interface(root, interface)

    def test_symlinked_asset_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.sandbox(directory)
            (root / 'assets/linked.svg').symlink_to(root / 'assets/icon.svg')
            interface = copy.deepcopy(self.interface)
            interface['composerIcon'] = './assets/linked.svg'
            with self.assertRaises(ValueError):
                validate_interface(root, interface)

    def test_brand_colors_need_contrast(self):
        for field, value in (('brandColor', '#FFFFFF'), ('brandColor', '#EEEEEE'),
                             ('brandColorDark', '#212121'), ('brandColorDark', '#333333'),
                             ('brandColor', 'black'), ('brandColorDark', None)):
            with self.subTest(field=field, value=value):
                interface = copy.deepcopy(self.interface)
                interface[field] = value
                with self.assertRaises(ValueError):
                    validate_interface(ROOT, interface)

    def test_skill_interface_matches_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve() / 'repo'
            root.mkdir()
            for relative in ('skills', '.claude-plugin', 'assets'):
                shutil.copytree(ROOT / relative, root / relative)
            for relative in ('plugin.json', 'LICENSE', 'README.md'):
                shutil.copy2(ROOT / relative, root / relative)
            validate_project(root)
            yaml = root / 'skills/promptcraft/agents/openai.yaml'
            yaml.write_text(yaml.read_text().replace('PromptingCraft.com', 'Other Name'))
            with self.assertRaises(ValueError):
                validate_project(root)

    def test_project_requires_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve() / 'repo'
            root.mkdir()
            for relative in ('skills', '.claude-plugin'):
                shutil.copytree(ROOT / relative, root / relative)
            for relative in ('plugin.json', 'LICENSE', 'README.md'):
                shutil.copy2(ROOT / relative, root / relative)
            with self.assertRaises(ValueError):
                validate_project(root)
