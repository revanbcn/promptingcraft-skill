import copy
import json
import re
import shutil
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from scripts.validate import validate_interface, validate_project, validate_publication

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
        self.assertEqual(self.manifest['name'], 'promptingcraft')
        self.assertEqual(self.manifest['version'], '0.3.0')
        self.assertEqual(self.manifest['homepage'], 'https://promptingcraft.com')
        self.assertEqual(self.manifest['repository'], 'https://gitlab.com/revanalex/promptingcraft-skill')
        self.assertEqual(self.interface['displayName'], 'PromptingCraft.com')
        self.assertTrue(self.interface['longDescription'].startswith('PromptingCraft.com '))
        # Publisher is the verified individual who operates the project; DondeGo is credited
        # only as the developer in descriptive text.
        self.assertEqual(self.manifest['author'], {'name': 'Aleksandr Prokofyev', 'url': 'https://promptingcraft.com'})
        self.assertEqual(self.interface['developerName'], 'Aleksandr Prokofyev')
        self.assertNotIn('DondeGo team', json.dumps(self.manifest))
        self.assertEqual(self.interface['websiteURL'], 'https://promptingcraft.com')
        self.assertEqual(self.interface['supportURL'], 'https://promptingcraft.com/contact')
        self.assertEqual(self.interface['privacyPolicyURL'], 'https://promptingcraft.com/privacy')
        self.assertEqual(self.interface['termsOfServiceURL'], 'https://promptingcraft.com/terms')
        self.assertTrue(self.interface['longDescription'].endswith('Developed by the dondego.com team.'))
        self.assertNotIn('by DondeGo', json.dumps(self.manifest))

    def test_release_notes_are_the_only_publication_setting(self):
        # publication.countries is omitted on purpose: no country restriction is intended.
        publication = self.manifest['extensions']['com.openai']['publication']
        self.assertEqual(set(publication), {'release_notes'})
        notes = publication['release_notes']
        self.assertIn('https://mcp.promptingcraft.com/mcp', notes)
        self.assertIn('otherwise it says so and falls back to other official sources or its bundled dated references', notes)
        self.assertTrue(notes.endswith('Developed by the dondego.com team.'))
        self.assertNotRegex(notes.lower(), r'guarantee[sd]? (better|improve)|official (openai|anthropic) (plugin|partner)')

    def test_review_information_for_mcp_submission(self):
        from scripts.validate import validate_review, MCP_TOOLS
        openai = self.manifest['extensions']['com.openai']
        validate_review(openai)
        review = openai['review']
        self.assertEqual(len(review['test_cases']['positive']), 5)
        self.assertEqual(len(review['test_cases']['negative']), 3)
        used = {t.strip() for c in review['test_cases']['positive'] for t in c['tools_triggered'].split(',')}
        self.assertEqual(used, MCP_TOOLS, 'every tool is exercised by a positive case')
        server = (ROOT / 'mcp/src/server.js').read_text()
        self.assertEqual(set(re.findall(r"registerTool\('([a-z_]+)'", server)), MCP_TOOLS)
        self.assertNotRegex(json.dumps(review), r'(?i)password|api[_ -]?key|token|/Users/')
        bad_cases = [
            {**review, 'test_cases': {**review['test_cases'], 'positive': review['test_cases']['positive'][:4]}},
            {**review, 'test_cases': {**review['test_cases'], 'negative': review['test_cases']['negative'] * 2}},
            {**review, 'demo_recording_url': 'http://example.com/demo'},
            {**review, 'reviewer_instructions': 'x'},
            {**review, 'test_cases': {**review['test_cases'], 'positive': [{**review['test_cases']['positive'][0], 'tools_triggered': 'run_shell'}] + review['test_cases']['positive'][1:]}},
        ]
        for bad in bad_cases:
            with self.assertRaises(ValueError):
                validate_review({**openai, 'review': bad})

    def test_mcp_fallback_is_disclosed_and_never_credited_to_the_server(self):
        # Regression: with the server unreachable, Codex answered from other official pages
        # without saying that PromptingCraft.com guidance retrieval was unavailable.
        skill = ' '.join((ROOT / 'skills/promptingcraft/SKILL.md').read_text().split())
        self.assertIn('If they are absent or fail, say in the source note that PromptingCraft.com '
                      'guidance retrieval was unavailable', skill)
        self.assertIn('labeled by how that evidence was actually obtained', skill)
        self.assertIn('Never attribute live verification to PromptingCraft.com unless one of its tools returned it', skill)
        cases = {c['id']: c for c in json.loads((ROOT / 'evals/mcp/cases.json').read_text())['cases']}
        self.assertEqual(cases['mcp-unavailable-fallback']['server'], 'unreachable')
        self.assertTrue(any('retrieval was unavailable' in o for o in cases['mcp-unavailable-fallback']['expected_observations']))
        self.assertEqual(cases['mcp-available-control']['server'], 'reachable')

    def test_retired_identifier_is_not_shipped(self):
        # 0.3.0 renamed promptcraft to promptingcraft; only migration notes and history keep it.
        shipped = [ROOT / 'plugin.json', ROOT / '.claude-plugin/plugin.json', ROOT / '.cursor-plugin/marketplace.json',
                   ROOT / '.agents/plugins/marketplace.json', ROOT / 'mcp.json', ROOT / 'mcp/src/server.js',
                   ROOT / 'mcp/src/catalog.js', ROOT / 'mcp/src/catalog-index.json',
                   *sorted((ROOT / 'skills/promptingcraft').rglob('*.*'))]
        for path in shipped:
            if path.suffix in {'.md', '.json', '.js', '.py', '.yaml', '.txt'}:
                self.assertNotRegex(path.read_text(), r'(?i)prompt_?craft(?!ing)', path)
        self.assertEqual(self.manifest['name'], 'promptingcraft')

    def test_mcp_configuration_is_the_production_guidance_server(self):
        from scripts.validate import validate_mcp_config
        config = json.loads((ROOT / 'mcp.json').read_text())
        validate_mcp_config(config)
        server = config['mcpServers']['promptingcraft-guidance']
        for bad in ({**server, 'url': 'https://example.com/mcp'}, {**server, 'type': 'sse'},
                    {**server, 'headers': {'Authorization': 'Bearer x'}}):
            with self.assertRaises(ValueError):
                validate_mcp_config({**config, 'mcpServers': {'promptingcraft-guidance': bad}})
        with self.assertRaises(ValueError):
            validate_mcp_config({**config, 'mcpServers': {'promptingcraft-guidance': server, 'other': server}})

    def test_publication_settings_are_validated(self):
        base = json.loads((ROOT / 'plugin.json').read_text())['extensions']['com.openai']
        for bad in ({}, {'release_notes': ''}, {'release_notes': 1}, {'countries': ['ES']}, ['release_notes']):
            with self.assertRaises(ValueError, msg=bad):
                validate_publication({**base, 'publication': bad})

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
                      (ROOT / 'skills/promptingcraft/agents/openai.yaml').read_text())
        self.assertIn('\n# PromptingCraft.com\n', (ROOT / 'skills/promptingcraft/SKILL.md').read_text())

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
            for relative in ('plugin.json', 'mcp.json', 'LICENSE', 'README.md'):
                shutil.copy2(ROOT / relative, root / relative)
            validate_project(root)
            yaml = root / 'skills/promptingcraft/agents/openai.yaml'
            yaml.write_text(yaml.read_text().replace('PromptingCraft.com', 'Other Name'))
            with self.assertRaises(ValueError):
                validate_project(root)

    def test_project_requires_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve() / 'repo'
            root.mkdir()
            for relative in ('skills', '.claude-plugin'):
                shutil.copytree(ROOT / relative, root / relative)
            for relative in ('plugin.json', 'mcp.json', 'LICENSE', 'README.md'):
                shutil.copy2(ROOT / relative, root / relative)
            with self.assertRaises(ValueError):
                validate_project(root)

    def test_directory_listing_values(self):
        self.assertEqual(self.interface['category'], 'Developer Tools')
        self.assertEqual(self.interface['shortDescription'], 'Source-backed agent prompts')
        self.assertEqual(len(self.interface['defaultPrompt']), 3)
        text = self.interface['longDescription']
        self.assertIn('not affiliated with or endorsed by OpenAI, Anthropic or Cursor', text)
        self.assertIn('no PromptingCraft.com service receives your prompts', text)
        self.assertIn('take only fixed categories and identifiers as input and do not ask for task text', text)
        self.assertTrue(1 <= len(self.interface['capabilities']) <= 20)
        self.assertEqual(self.manifest['keywords'][0], 'agent-skills')
        self.assertIn('does not guarantee better downstream results', text)
        self.assertNotRegex(text, r'(?i)\bofficial (openai|anthropic) (plugin|partner)|(?<!not )guarantees? (better|improved)')

    def test_directory_rules_reject_invalid_listing(self):
        cases = {
            'too many prompts': {'defaultPrompt': ['a', 'b', 'c', 'd']},
            'duplicate prompts': {'defaultPrompt': ['Prepare a prompt.', 'prepare  a prompt.']},
            'long prompt': {'defaultPrompt': ['x' * 129]},
            'mention': {'defaultPrompt': ['Ask @promptingcraft for a prompt.']},
            'multi-line prompt': {'defaultPrompt': ['one\ntwo']},
            'unknown category': {'category': 'Coding'},
            'screenshots': {'screenshots': ['./assets/shot.png']},
            'too many capabilities': {'capabilities': [f'Capability {n}' for n in range(21)]},
            'long capability': {'capabilities': ['x' * 121]},
            'duplicate capabilities': {'capabilities': ['Review prompts', 'review  prompts']},
            'multi-line capability': {'capabilities': ['one\ntwo']},
        }
        for label, change in cases.items():
            with self.subTest(label):
                interface = copy.deepcopy(self.interface)
                interface.update(change)
                with self.assertRaises(ValueError):
                    validate_interface(ROOT, interface)
