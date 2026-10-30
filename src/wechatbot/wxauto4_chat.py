"""Explicit continuous chat entry; default inspect never attaches UI or starts a model."""
import argparse
import asyncio
import hashlib
import json
from pathlib import Path
import queue
import sys
import threading
import traceback

from .config import ROOT, load_config, local_path
from .chat_session import ChatBinding, ChatSession
from .chat_model import ChatCliModel
from .transports.wxauto4_adapter import Wxauto4Client, inspect_dependency, live_factory
from .wxauto4_trial import owner, write_record


class StartupFailure(Exception):
    def __init__(self, stage, error):
        # Never include exception text, source lines, locals, or UI titles.
        self.diagnostic = dict(stage=stage, error_type=type(error).__name__, frames=[
            dict(file=Path(frame.filename).name, function=frame.name, line=frame.lineno)
            for frame in traceback.extract_tb(error.__traceback__)[-8:]])
        for field in ('winerror', 'errno', 'hresult'):
            value = getattr(error, field, None)
            if type(value) is int:
                self.diagnostic[field] = value
        if isinstance(error, KeyError) and error.args and error.args[0] in ('chat_name', 'chat_type'):
            self.diagnostic['missing_field'] = error.args[0]
        super().__init__('startup_failed')


def startup_step(stage, function, *args, **kwargs):
    try:
        return function(*args, **kwargs)
    except Exception as error:
        raise StartupFailure(stage, error) from None


def report_failure(error, root=ROOT):
    diagnostic = error.diagnostic if isinstance(error, StartupFailure) else StartupFailure('entry', error).diagnostic
    result = dict(event='startup_error', **diagnostic)
    path = Path(root) / 'state/startup-last-error.json'
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        write_record(path, result)
    except OSError:
        pass
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return result


def inspect(root=ROOT):
    cfg = startup_step('config', load_config, root, directory='config/local')
    return dict(mode='inspect', **inspect_dependency(), backend=cfg.data['models']['llm']['backend'],
                channel_started=False, model_generations=0, sends=0,
                binding_present=local_path(root, 'secrets/wxauto4-chat.local.json').is_file())


async def live(root=ROOT):
    cfg = startup_step('config', load_config, root, directory='config/local')
    binding_path = local_path(root, 'secrets/wxauto4-chat.local.json')
    binding = startup_step('binding', ChatBinding.read, binding_path)
    binding_digest = hashlib.sha256(binding_path.read_bytes()).digest()
    if not inspect_dependency()['dependency_present']:
        raise ValueError('install_wxauto4_41_1_7')
    # This branch is entered only through the explicit --live operator instruction.
    with owner(Path(root) / 'state/wxauto4-chat'):
        model = startup_step('model_init', ChatCliModel, cfg, private_ids=[binding.chat_name, *binding.blacklist])
        session = None
        try:
            client = startup_step('wxauto_init', Wxauto4Client, live_factory)
            session = startup_step('session_init', ChatSession, cfg, binding, client, model)
            if not startup_step('baseline', session.baseline):
                print(json.dumps(session.status())); return
            commands = queue.Queue()
            def read_console():
                for line in sys.stdin:
                    commands.put(line)
                commands.put('stop')
            threading.Thread(target=read_console, daemon=True).start()
            print('Local commands: status / pause / resume / reset / memory-status / stop')
            if cfg.data['models']['llm']['backend'] != 'codebuddy_cli':
                print('Selected backend retained. Native WebSearch/WebFetch require CodeBuddy CLI.')
            while not session.stopped:
                while not commands.empty():
                    print(json.dumps(session.command(commands.get_nowait()), ensure_ascii=False))
                try:
                    if hashlib.sha256(binding_path.read_bytes()).digest() != binding_digest:
                        session.invalidate('binding_changed')
                    session.poll()
                    await session.advance()
                except (OSError, ValueError, KeyError, TypeError):
                    session.invalidate('framework_or_binding_error')
                    print(json.dumps(session.status()))
                await asyncio.sleep(0.5)
        finally:
            if session:
                await session.close()
            else:
                await model.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    try:
        if args.live:
            asyncio.run(live())
        else:
            print(json.dumps(inspect(), ensure_ascii=False))
    except KeyboardInterrupt:
        print('stopped')
    except Exception as error:
        report_failure(error)
        raise SystemExit(1) from None


if __name__ == '__main__':
    main()
