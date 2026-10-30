"""Explicitly copy hash-matching local CLI artifacts. Never run or install the CLI."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def main():
    from wechatbot.config import local_path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node', type=Path, required=True)
    parser.add_argument('--entry', type=Path, required=True)
    args = parser.parse_args()
    lock = json.loads((ROOT / 'config/versions.lock.json').read_text(encoding='utf-8'))
    bundle = args.entry.parent.parent / 'dist/codebuddy-headless.js'
    artifacts = [(args.node, lock['node']['path'], lock['node']['sha256']),
                 (args.entry, lock['cli']['entry'], lock['cli']['entry_sha256']),
                 (bundle, 'runtime/cli/codebuddy/dist/codebuddy-headless.js', lock['cli']['headless_sha256']),
                 (args.entry.parent.parent / lock['cli']['types_relative'],
                  'runtime/cli/codebuddy/' + lock['cli']['types_relative'], lock['cli']['types_sha256'])]
    # Validate all inputs before writing any artifact; no credentials/account reads.
    for source, _, expected in artifacts:
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise ValueError('artifact_mismatch')
    for source, relative, expected in artifacts:
        destination = local_path(ROOT, relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        if hashlib.sha256(destination.read_bytes()).hexdigest() != expected:
            raise ValueError('artifact_copy_mismatch')
    print('{"artifact_copy":"hash_verified","executed":false}')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError):
        raise SystemExit('artifact preparation failed; no execution attempted') from None
