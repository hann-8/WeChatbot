"""Explicit continuous chat entry; default inspect never attaches UI or starts a model."""
import argparse
import asyncio
import hashlib
import json
from pathlib import Path
import queue
import sys
import threading

from .config import ROOT, load_config, local_path
from .chat_session import ChatBinding, ChatSession
from .chat_model import ChatCliModel
from .transports.wxauto4_adapter import Wxauto4Client, inspect_dependency, live_factory
from .wxauto4_trial import owner


def inspect(root=ROOT):
    cfg = load_config(root, directory='config/local')
    return dict(mode='inspect', **inspect_dependency(), backend=cfg.data['models']['llm']['backend'],
                channel_started=False, model_generations=0, sends=0,
                binding_present=local_path(root, 'secrets/wxauto4-chat.local.json').is_file())


async def live(root=ROOT):
    cfg = load_config(root, directory='config/local')
    binding_path = local_path(root, 'secrets/wxauto4-chat.local.json')
    binding = ChatBinding.read(binding_path)
    binding_digest = hashlib.sha256(binding_path.read_bytes()).digest()
    if not inspect_dependency()['dependency_present']:
        raise ValueError('install_wxauto4_41_1_7')
    # This branch is entered only through the explicit --live operator instruction.
    with owner(Path(root) / 'state/wxauto4-chat'):
        model = ChatCliModel(cfg, private_ids=[binding.chat_name, *binding.allowed_senders, *binding.blacklist])
        session = None
        try:
            session = ChatSession(cfg, binding, Wxauto4Client(live_factory), model)
            if not session.baseline():
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
    except Exception:
        # Framework exception text may include titles/messages; never echo it.
        raise SystemExit('Startup failed. Check local config, binding, CLI artifacts and client compatibility; no automatic retry.') from None


if __name__ == '__main__':
    main()
