"""Five strict YAML documents, one immutable snapshot, no legacy QQ loader."""
from copy import deepcopy
import hashlib
import json
import re
from pathlib import Path
import yaml
from .contracts import opaque
from .defaults import DEFAULTS

ROOT = Path(__file__).resolve().parents[2]
NAMES = ('bot', 'chat', 'models', 'features', 'runtime')


class StrictLoader(yaml.SafeLoader):
    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent):
            raise ValueError('yaml_alias')
        return super().compose_node(parent, index)


def mapping(loader, node):
    result = {}
    for k, v in node.value:
        key = loader.construct_object(k)
        if not isinstance(key, str) or key in result:
            raise ValueError('yaml_key')
        result[key] = loader.construct_object(v)
    return result


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def local_path(root, relative):
    root = Path(root).resolve()
    relative = Path(relative)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('project_path')
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink() or current.is_junction():
            raise ValueError('project_path')
    if not current.resolve().is_relative_to(root):
        raise ValueError('project_path')
    return current


def _shape(value, example):
    if example is None and isinstance(value, str):
        return  # Nullable model digest; field-specific validation below.
    if type(value) is not type(example):
        raise ValueError('config_type')
    if isinstance(example, dict):
        if set(value) != set(example):
            raise ValueError('config_fields')
        for key in example:
            _shape(value[key], example[key])
    if isinstance(example, list):
        if len(value) > 256 or len(set(map(str, value))) != len(value):
            raise ValueError('config_list')
        for item in value:
            opaque(item)


class Config:
    def __init__(self, root, data):
        self.root = Path(root).resolve()
        self._json = json.dumps(data, sort_keys=True, ensure_ascii=False, allow_nan=False)
        self.digest = hashlib.sha256(self._json.encode()).hexdigest()

    @property
    def data(self):
        return json.loads(self._json)

    def runner_settings(self):
        d = self.data
        return dict(llm=d['models']['llm'], chat={'history_turns': d['chat']['history_turns']},
                    output={'max_reply_chars': 8000}, vision={'enabled': False})


def load_config(root=ROOT, *, directory='config/examples'):
    root = Path(root).resolve()
    defaults, data = {}, {}
    for name in NAMES:
        defaults[name] = deepcopy(DEFAULTS[name])
        file = local_path(root, f'{directory}/{name}.yaml')
        if file.stat().st_size > 65536:
            raise ValueError('config_size')
        try:
            data[name] = yaml.load(file.read_text(encoding='utf-8'), Loader=StrictLoader)
        except (yaml.YAMLError, RecursionError, UnicodeError):
            raise ValueError('config_syntax') from None
        _shape(data[name], defaults[name])
    b, c, m, f, r = (data[n] for n in NAMES)
    if b['platform'] != 'wechat' or b['transport'] not in ('mock', 'pyweixin'):
        raise ValueError('transport')
    if b['account_binding_file'] != 'secrets/wechat-account.local.json':
        raise ValueError('binding_path')
    if c['participation']['mode'] != 'mentions' or c['output']['delivery_mode'] != 'single':
        raise ValueError('phase_unsupported')
    if not 1 <= c['history_turns'] <= 32:
        raise ValueError('history_turns')
    if c['direct']['allowed_conversations'] and not c['direct']['allowed_users']:
        raise ValueError('direct_binding')
    if any(f[name]['enabled'] for name in ('vision', 'memes', 'members', 'bilibili')):
        raise ValueError('feature_unimplemented')
    from qqbot_gateway.group_memory import validate_config as validate_memory
    validate_memory(f['memory'])
    web = f['web']
    if (web['engine'] != 'codebuddy_cli' or not 1 <= web['cli_max_tool_calls'] <= 3 or
            not 1 <= web['cli_max_turns'] <= 4 or not 1 <= web['cli_tool_result_bytes'] <= 8000):
        raise ValueError('web_limits')
    if (r['host'] != '127.0.0.1' or not 1024 <= r['health_port'] <= 65535 or
            r['health_port'] in (8765, 8766) or r['raw_message_logging'] or r['auto_start'] or
            r['ui_observation']['enabled']):
        raise ValueError('runtime_boundary')
    llm = m['llm']
    if llm['backend'] not in ('codebuddy_cli', 'ollama_ssh') or llm['max_concurrency'] != 1 or not 1 <= llm['queue_limit'] <= 32:
        raise ValueError('model_queue')
    cli, ollama = (llm['profiles'][n] for n in ('codebuddy_cli', 'ollama_ssh'))
    if (ollama['access_file'] != 'secrets/home-5070-runtime.local.json' or
            (ollama['expected_digest'] is not None and
             not re.fullmatch(r'(sha256:)?[a-f0-9]{64}', ollama['expected_digest']))):
        raise ValueError('unconfigured_home_profile')
    if not 1024 <= ollama['num_ctx'] <= 32768 or not 1 <= ollama['num_predict'] <= 4096 or ollama['think']:
        raise ValueError('native_profile')
    if (not 0 <= ollama['keep_alive_seconds'] <= 3600 or not 0 <= ollama['temperature'] <= 2 or
            not 0 < ollama['top_p'] <= 1 or not 1 <= ollama['top_k'] <= 100 or
            not 1 <= len(ollama['model']) <= 128):
        raise ValueError('native_sampling')
    for profile in (cli, ollama):
        if not 1 <= profile['run_timeout_seconds'] <= 300 or not 1 <= profile['cleanup_seconds'] <= 30:
            raise ValueError('model_timeout')
        budget = profile['input_budget']
        if any(type(v) is not int or v < 1 for v in budget.values()):
            raise ValueError('budget')
        if budget['context_input_limit_tokens'] <= budget['context_overhead_reserve_tokens']:
            raise ValueError('budget')
    from qqbot_gateway.token_budget import validate_model_settings, InputBudget, known_models
    if cli['model'] not in known_models():
        raise ValueError('unknown_cli_model')
    settings = Config(root, data).runner_settings()
    validate_model_settings(settings, backend='codebuddy_cli')
    InputBudget.from_settings(settings).validate_capacity()
    return Config(root, data)
