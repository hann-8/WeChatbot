"""One selected existing runner task, with a small WeChat output wrapper."""
from dataclasses import dataclass
import asyncio
import json

from qqbot_gateway.backends import create_runner, resolve_backend
from qqbot_gateway.token_budget import InputBudget, dialog_text, validate_model_settings
from qqbot_gateway.group_memory import auxiliary
from qqbot_gateway.reply_plan import _pairs, make_reply_plan
from qqbot_gateway.cli_web_policy import SCOPE, public_url, source_urls
from .chat_policy import compose
from .config import local_path


@dataclass
class ChatAnswer:
    plan: object
    aux: dict
    used_web: bool = False


class ChatCliModel:
    def __init__(self, config, *, runner=None, private_ids=()):
        self.config = config
        settings = config.runner_settings()
        self.profile = resolve_backend(settings)
        self.budget = InputBudget.from_settings(settings, validate_model_settings(settings))
        features = config.data['features']
        self.web = dict(features['web'])
        self.web['enabled'] &= self.profile['backend'] == 'codebuddy_cli'
        # Base factory gets no QQ-shaped settings; attach platform-neutral policy here.
        self.runner = runner or create_runner(config.root, settings, self.budget)
        self.runner.native_web = self.web['enabled']
        self.runner.web_config = self.web
        self.runner.web_private_ids = list(private_ids)
        self.runner.vision_settings = settings
        path = local_path(config.root, 'config/persona.md')
        # Read bound follows configured visible policy, not an arbitrary role character gate.
        if path.stat().st_size > self.budget.limit:
            raise ValueError('persona_exceeds_input_policy')
        character = path.read_text(encoding='utf-8')
        self.system = compose(character, self.web, features['memory'])
        self.lock = asyncio.Lock()
        self.output = dict(max_reply_chars=8000, delivery_mode='single')

    async def generate(self, question, sender_ref, source, history, request_id):
        async with self.lock:
            current = json.dumps(dict(platform='wechat', question=question, sender_ref=sender_ref,
                                      memory=source.get('memory')), ensure_ascii=False)
            # Memory and the current question are indivisible; only whole old pairs trim.
            selected = self.budget.select_history(self.system, current, history)
            prompt = dialog_text(selected + [dict(role='user', content=current)])
            self.budget.check(self.system, prompt)
            from qqbot_gateway.vision import CURRENT, AUDIT
            image, audit = CURRENT.set(None), AUDIT.set(None)
            scope = SCOPE.set((True, question))
            try:
                result = await self.runner.run(self.system, prompt, request_id)
            finally:
                SCOPE.reset(scope); CURRENT.reset(image); AUDIT.reset(audit)
            if result.finish_reason != 'stop' or not result.generation_performed:
                raise ValueError('incomplete_model_result')
            raw = json.loads(result.text, object_pairs_hook=_pairs)
            if (not isinstance(raw, dict) or set(raw) != {'wechat_reply','text','memory_updates','memory_receipt'}
                    or type(raw['wechat_reply']) is not int or raw['wechat_reply'] != 1
                    or not isinstance(raw['text'], str) or not raw['text'].strip()):
                raise ValueError('chat_output_format')
            aux = auxiliary(raw, source)
            body = raw['text']
            proof = result.parameters.get('native_web', {})
            used_web = bool(proof.get('calls'))
            if used_web:
                urls = proof.get('urls', [])
                allowed = [u for u in urls if public_url(u)]
                if not allowed or any(u not in allowed for u in source_urls(body)):
                    body = '本次联网未取得可核实的公开来源，没有采用这次答复。'
                else:
                    body += '\n' + '\n'.join(dict.fromkeys(allowed[:2]))
                # Neither tool prose nor model-derived tool facts may enter memory.
                aux.update(updates={}, reason='no_action')
            plan = make_reply_plan(json.dumps(dict(qqbot_reply=1, kind='answer', bubbles=[body]),
                                             ensure_ascii=False), self.output | {'delivery_mode': 'adaptive'}, question)
            return ChatAnswer(plan, aux, used_web)

    async def close(self):
        if hasattr(self.runner, 'cleanup_close'):
            await self.runner.cleanup_close()
