"""Reuse the pinned runner, budgets and cleanup. Only explicit offline seams exist."""
import asyncio
from qqbot_gateway.backends import create_runner, resolve_backend
from qqbot_gateway.chat_text import prepare_reply
from qqbot_gateway.token_budget import InputBudget, dialog_text, validate_model_settings
from .config import local_path


class ModelFacade:
    def __init__(self, config, *, offline_spawn=None, offline_transport_factory=None):
        settings = config.runner_settings()
        self.config = config
        profile = resolve_backend(settings)
        self.budget = InputBudget.from_settings(settings, validate_model_settings(settings))
        # No caller can accidentally create a real executable path in this phase.
        if profile['backend'] == 'codebuddy_cli' and offline_spawn is None:
            raise ValueError('real_model_closed')
        if profile['backend'] == 'ollama_ssh' and offline_transport_factory is None:
            raise ValueError('real_model_closed')
        for relative in ('runtime/requests', 'state/cli-cleanup/unresolved.json',
                         'state/configuration.lock', 'state/ollama-remote-result-unknown.json',
                         'config/versions.lock.json',
                         'config/cli-tools-denied.json', 'config/mcp-empty.json'):
            local_path(config.root, relative)
        self.runner = create_runner(config.root, settings, self.budget)
        if profile['backend'] == 'codebuddy_cli':
            self.runner.spawn = offline_spawn
        else:
            self.runner.factory = offline_transport_factory
        self.system = local_path(config.root, 'config/persona.md').read_text(encoding='utf-8')
        if len(self.system) > 8000:
            raise ValueError('persona_size')
        self.lock = asyncio.Lock()

    async def generate(self, event, history, trace):
        async with self.lock:
            selected = self.budget.select_history(self.system, event.text, history)
            prompt = dialog_text(selected + [dict(role='user', content=event.text)])
            self.budget.check(self.system, prompt)
            # A reused process must not inherit any QQ/current-image ContextVar.
            from qqbot_gateway.vision import CURRENT, AUDIT
            image_token, audit_token = CURRENT.set(None), AUDIT.set(None)
            try:
                result = await self.runner.run(self.system, prompt, trace)
            finally:
                CURRENT.reset(image_token)
                AUDIT.reset(audit_token)
            if result.finish_reason != 'stop' or not result.generation_performed:
                raise ValueError('incomplete_model_result')
            # Exactly one conversion to chat plain text, before any delivery intent.
            return prepare_reply(result.text, 8000)[0]

    def status(self):
        if hasattr(self.runner, 'cleanup_status'):
            return {'blocked': self.runner.cleanup_status()['blocked']}
        return {'blocked': self.runner.marker.exists()}

    async def close(self):
        if hasattr(self.runner, 'cleanup_close'):
            await self.runner.cleanup_close()
