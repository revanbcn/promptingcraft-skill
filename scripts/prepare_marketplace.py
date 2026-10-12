#!/usr/bin/env python3
"""Materialize the local marketplace plugin from the canonical reproducible ZIP.

No user configuration is changed. Refuse unmanaged destinations or local edits.
"""
import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path
try:
    from scripts.package import build
    from scripts.validate import validate_marketplace, validate_project
except ModuleNotFoundError:
    from package import build
    from validate import validate_marketplace, validate_project

MARKER = '.promptcraft-generated.json'


def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlink in generated plugin')
        if path.is_file() and path.relative_to(root).as_posix() != MARKER:
            result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def prepare(root):
    root = Path(root).resolve()
    dest = validate_marketplace(root, require_source=False)
    if dest.exists():
        marker = dest / MARKER
        if not marker.is_file() or marker.is_symlink():
            raise ValueError('Refusing unmanaged plugin destination')
        previous = json.loads(marker.read_text())
        if previous != {'schema_version': 1, 'files': inventory(dest)}:
            raise ValueError('Refusing locally edited generated plugin')
    # Build uses the same canonical source and file selection as release packaging.
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.promptcraft-build-', dir=dest.parent) as temporary:
        temporary = Path(temporary)
        archives = build(root, temporary / 'archives')
        archive = next(p for p in archives if '-plugin-' in p.name)
        with zipfile.ZipFile(archive) as zipped:
            zipped.extractall(temporary / 'stage')
        stage = temporary / 'stage/promptcraft-plugin'
        validate_project(stage)
        (stage / MARKER).write_text(json.dumps({'schema_version': 1, 'files': inventory(stage)}, indent=2, sort_keys=True) + '\n')
        if dest.exists():
            # Recheck before replacing only our own, unmodified generated tree.
            if json.loads((dest / MARKER).read_text()) != {'schema_version': 1, 'files': inventory(dest)}:
                raise ValueError('Generated plugin changed during build')
            dest.rename(temporary / 'previous')
        try:
            stage.rename(dest)
        except OSError:
            if (temporary / 'previous').exists():
                (temporary / 'previous').rename(dest)
            raise
    validate_marketplace(root)
    return dest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(prepare(args.root))
