import argparse
import json
from .config import load_config
from .status import inspect


def main():
    parser = argparse.ArgumentParser(description='WX-01 offline configuration inspection; 0 UI/model/send')
    parser.add_argument('command', choices=['inspect'])
    parser.add_argument('--config-dir', default='config/examples')
    args = parser.parse_args()
    try:
        result = inspect(load_config(directory=args.config_dir))
    except (ValueError, OSError, KeyError, TypeError):
        print(json.dumps({'configuration': 'invalid', 'production_eligible': False}))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
