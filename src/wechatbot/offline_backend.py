"""Synthetic protocol subprocess replacement: never launches a process or network."""
import asyncio
import json


class _Input:
    def __init__(self, process):
        self.process = process
        self.data = bytearray()

    def write(self, value):
        self.data.extend(value)

    async def drain(self):
        await asyncio.sleep(0)

    def close(self):
        self.process.stdout.feed_data(self.process.payload)
        self.process.stdout.feed_eof()
        self.process.stderr.feed_eof()
        self.process.returncode = 0
        self.process.done.set()


class SyntheticProcess:
    pid = 2147483647  # Nonexistent; no owned OS process was created by this fixture.

    def __init__(self, payload):
        self.payload = payload
        self.stdout, self.stderr = asyncio.StreamReader(), asyncio.StreamReader()
        self.stdin = _Input(self)
        self.returncode = None
        self.done = asyncio.Event()

    async def wait(self):
        await self.done.wait()
        return self.returncode


class OfflineSpawn:
    def __init__(self, text='这是一条离线合成回复。'):
        self.text = text
        self.calls = []
        self.processes = []
        self.tools = []
        self.partial = False

    async def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        model = args[args.index('--model') + 1]
        rows = [dict(type='system', subtype='init', tools=self.tools, mcp_servers=[], model=model)]
        if not self.partial:
            rows.append(dict(type='result', subtype='success', is_error=False, result=self.text))
        process = SyntheticProcess(('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n').encode())
        self.processes.append(process)
        return process
