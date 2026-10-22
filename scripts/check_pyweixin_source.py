"""Verify inert audit evidence, never import upstream or access UI/network.

Optional --source-dir points to an explicitly downloaded fixed source root.
Optional --wheel-dir verifies downloaded wheels; neither mode installs anything.
"""
import argparse
import hashlib
import json
from pathlib import Path

PIN = '8589baa049bb91d3a500602c167f07b2f8397a13'
ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT, source_dir=None, wheel_dir=None):
    base = root / 'vendor/pyweixin'
    lock = json.loads((base / 'source-lock.json').read_text('utf-8'))
    assert lock['commit'] == PIN and lock['distribution'] == 'pywechat127'
    assert lock['declared_version'] == '1.9.8' and lock['upstream_installed'] is False
    evidence = json.loads((base / 'evidence-hashes.json').read_text('utf-8'))
    for name, expected in evidence.items():
        assert hashlib.sha256((base / name).read_bytes()).hexdigest() == expected, name
    for entry in lock['files']:
        if entry['saved']:
            assert hashlib.sha256((base / entry['saved']).read_bytes()).hexdigest() == entry['sha256']
        if source_dir:
            data = (source_dir / entry['path']).read_bytes()
            assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
            assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == entry['git_blob']
    if source_dir:
        for entry in json.loads((base / 'excerpts.json').read_text('utf-8')):
            lines = (source_dir / entry['path']).read_text('utf-8').splitlines()
            assert '\n'.join(lines[entry['start'] - 1:entry['end']]) + '\n' == entry['text']
    deps = json.loads((base / 'dependencies.json').read_text('utf-8'))['artifacts']
    req = (base / 'observation-requirements.lock').read_text('utf-8')
    for row in deps:
        assert f"{row['name']}=={row['version']} --hash=sha256:{row['sha256']}" in req
        assert row['license_files'], row['name']
        if wheel_dir:
            assert hashlib.sha256((wheel_dir / row['filename']).read_bytes()).hexdigest() == row['sha256']
    return {'fixed_source_files': len(lock['files']), 'evidence_files': len(evidence),
            'dependency_artifacts': len(deps), 'ui_imported': False,
            'source_bytes_verified': source_dir is not None,
            'wheel_bytes_verified': wheel_dir is not None}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source-dir', type=Path)
    p.add_argument('--wheel-dir', type=Path)
    args = p.parse_args()
    print(json.dumps(check(source_dir=args.source_dir, wheel_dir=args.wheel_dir)))
