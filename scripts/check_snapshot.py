"""Local read-only audit: no QQ services, model executions or network requests."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(root=ROOT):
    from wechatbot.config import local_path
    manifest = json.loads((root / 'vendor/qq-core-manifest.json').read_text(encoding='utf-8'))
    assert len({r['path'] for r in manifest['files']}) == len(manifest['files']), 'duplicate_snapshot_path'
    assert all(len(row.get('source_commit', manifest['source_commit'])) == 40 for row in manifest['files'])
    expected = set()
    for row in manifest['files']:
        path = local_path(root, row['path'])
        assert path.is_file() and sha(path) == row['sha256'], 'snapshot_integrity'
        assert row['local_changes'] or row['source_sha256'] == row['sha256'], 'source_integrity'
        expected.add(row['path'])
    actual = {p.relative_to(root).as_posix() for p in (root / 'src/qqbot_gateway').rglob('*')
              if p.is_file() and '__pycache__' not in p.parts}
    assert actual == {p for p in expected if p.startswith('src/')}, 'snapshot_file_set'
    lock = json.loads((root / 'config/versions.lock.json').read_text(encoding='utf-8'))
    node = local_path(root, lock['node']['path'])
    entry = local_path(root, lock['cli']['entry'])
    bundle = entry.parent.parent / 'dist/codebuddy-headless.js'
    assert sha(node) == lock['node']['sha256'], 'node_integrity'
    assert sha(entry) == lock['cli']['entry_sha256'], 'entry_integrity'
    assert sha(bundle) == lock['cli']['headless_sha256'], 'bundle_integrity'
    assert sha(entry.parent.parent / lock['cli']['types_relative']) == lock['cli']['types_sha256'], 'types_integrity'
    assert json.loads((root / 'config/mcp-empty.json').read_text()) == {'mcpServers': {}}
    return dict(snapshot_files=len(expected), locally_changed=sum(bool(r['local_changes']) for r in manifest['files']),
                artifact_hashes='verified', executed_artifacts=False)


if __name__ == '__main__':
    try:
        print(json.dumps(check()))
    except (OSError, ValueError, KeyError, AssertionError):
        print('{"snapshot_audit":"failed"}')
        sys.exit(1)
