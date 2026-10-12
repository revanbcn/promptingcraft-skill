import json
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts.prepare_marketplace import prepare
from scripts.validate import validate_marketplace

ROOT = Path(__file__).resolve().parents[1]


class MarketplaceTests(unittest.TestCase):
    def fixture(self, directory):
        root = Path(directory).resolve() / "repo"
        root.mkdir()
        for relative in ("skills", ".claude-plugin", "docs"):
            shutil.copytree(ROOT / relative, root / relative)
        for relative in ("plugin.json", "LICENSE", "README.md"):
            shutil.copy2(ROOT / relative, root / relative)
        catalog = root / ".agents/plugins/marketplace.json"
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps({
            "name": "dondego-local",
            "interface": {"displayName": "DondeGo Local"},
            "plugins": [{"name": "promptcraft",
                         "source": {"source": "local", "path": "./dist/promptcraft-plugin"},
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"},
                         "category": "Productivity"}]
        }))
        return root, catalog

    def test_source_resolves_from_marketplace_root_and_package_is_complete(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.fixture(directory)
            dest = prepare(root)
            self.assertEqual(dest, root / "dist/promptcraft-plugin")
            self.assertEqual(validate_marketplace(root), dest)
            self.assertFalse((root / ".agents/plugins/dist").exists())
            for source in (root / "skills/promptcraft").rglob("*"):
                if source.is_file() and "__pycache__" not in source.parts and source.suffix != ".pyc":
                    self.assertEqual(source.read_bytes(), (dest / "skills/promptcraft" / source.relative_to(root / "skills/promptcraft")).read_bytes())
            self.assertTrue((dest / "plugin.json").is_file())
            self.assertFalse(any(p.is_symlink() for p in dest.rglob("*")))
            self.assertFalse((root / "dist/SHA256SUMS").exists())

    def test_repeat_is_identical_and_refresh_removes_stale_generated_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.fixture(directory)
            dest = prepare(root)
            first = {p.relative_to(dest): p.read_bytes() for p in dest.rglob("*") if p.is_file()}
            prepare(root)
            self.assertEqual(first, {p.relative_to(dest): p.read_bytes() for p in dest.rglob("*") if p.is_file()})
            extra = root / "skills/promptcraft/references/transient.md"
            extra.write_text("Sanitized reference\n")
            prepare(root)
            self.assertEqual((dest / "skills/promptcraft/references/transient.md").read_text(), "Sanitized reference\n")
            extra.unlink()
            prepare(root)
            self.assertFalse((dest / "skills/promptcraft/references/transient.md").exists())

    def test_refuses_unmanaged_or_edited_target_without_changing_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.fixture(directory)
            dest = root / "dist/promptcraft-plugin"
            dest.mkdir(parents=True)
            (dest / "owner.txt").write_text("owner data")
            with self.assertRaises(ValueError):
                prepare(root)
            self.assertEqual((dest / "owner.txt").read_text(), "owner data")
            shutil.rmtree(dest)
            prepare(root)
            skill = dest / "skills/promptcraft/SKILL.md"
            skill.write_text("local edit")
            with self.assertRaises(ValueError):
                prepare(root)
            self.assertEqual(skill.read_text(), "local edit")

    def test_invalid_paths_and_metadata_are_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root, catalog = self.fixture(directory)
            baseline = json.loads(catalog.read_text())
            for path in ("../outside", "./../outside", "/tmp/outside", "./skills/promptcraft", "./dist/../../outside"):
                data = json.loads(json.dumps(baseline))
                data["plugins"][0]["source"]["path"] = path
                catalog.write_text(json.dumps(data))
                with self.assertRaises(ValueError, msg=path):
                    prepare(root)
            for key, value in (("installation", "UNKNOWN"), ("authentication", "UNKNOWN")):
                data = json.loads(json.dumps(baseline))
                data["plugins"][0]["policy"][key] = value
                catalog.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    prepare(root)
            self.assertFalse((root / "dist").exists())

    def test_refuses_symlink_source_and_parent(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root, _ = self.fixture(directory)
            (root / "dist").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                prepare(root)
            (root / "dist").unlink()
            (root / "dist").mkdir()
            (root / "dist/promptcraft-plugin").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                prepare(root)
            self.assertEqual(list(Path(outside).iterdir()), [])
