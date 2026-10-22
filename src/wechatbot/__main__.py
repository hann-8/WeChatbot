import argparse
import json
from .config import load_config
from .status import inspect


def main():
    parser = argparse.ArgumentParser(description='Offline inspection/probe; 0 UI/model/send')
    parser.add_argument('command', choices=['inspect', 'probe'])
    parser.add_argument('--mode', choices=['inspect', 'mock'], default='inspect')
    parser.add_argument('--config-dir', default='config/examples')
    args = parser.parse_args()
    try:
        config = load_config(directory=args.config_dir)
        if args.command == 'probe':
            from .pyweixin_probe import inspect_candidate, mock_probe
            result = mock_probe() if args.mode == 'mock' else inspect_candidate()
        else:
            result = inspect(config)
    except (ValueError, OSError, KeyError, TypeError):
        print(json.dumps({'configuration': 'invalid', 'production_eligible': False}))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
