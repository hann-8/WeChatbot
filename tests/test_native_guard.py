"""Shipped plugin + locked public dispatch function, hosted by a synthetic SDK."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from wechatbot.config import ROOT, load_config
from qqbot_gateway.cli_web_policy import native_contract
from qqbot_gateway.vision_mod_guard import Guard
from qqbot_gateway.token_budget import InputBudget
from qqbot_gateway.hosted_cli_budget import framework_upper, model_terms


class NativeGuardTests(unittest.TestCase):
    def test_envelopes_http_https_private_failure_and_limits(self):
        lock = json.loads((ROOT/'config/versions.lock.json').read_text())
        node = ROOT/lock['node']['path']
        bundle = (ROOT/lock['cli']['entry']).parent.parent/'dist/codebuddy-headless.js'
        data = bundle.read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), lock['cli']['headless_sha256'])
        source = data.decode('utf-8')
        module = source.split('26728(eA,el,ec){', 1)[1].split('},32483(eA,el,ec){', 1)[0]
        adapter = 'import * as ed from "node:util";\n' + module[module.index('let eu=["tool"'):] + '\nexport {dispatchModsToolCall};\n'
        web = load_config().data['features']['web']
        for variant in ('search_json', 'fetch_json', 'fetch_http', 'fetch_sdk_error', 'fetch_conflict', 'fetch_private_numeric_url'):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory(prefix='wx-native-synthetic-') as folder:
                work = Path(folder)
                policy = native_contract(web, ['987654321'], InputBudget(limit=524288))
                guard = Guard(work, 'synthetic policy', 'synthetic question', None,
                              dict(T=len('synthetic policysynthetic question'.encode()), F=framework_upper(), V=0, O=128000, C=1000000),
                              wire_message=dict(type='user', message=dict(role='user', content='synthetic question')),
                              native_web=policy)
                actual = work/'adapter.mjs'; actual.write_text(adapter, encoding='utf-8')
                result = subprocess.run([str(node),str(ROOT/'tests/fixtures/native_sdk_harness.mjs'),
                                         str(guard.root),variant,str(actual)],capture_output=True,
                                        text=True,encoding='utf-8',timeout=15)
                self.assertEqual(result.returncode,0,result.stderr)
                value = json.loads(result.stdout.strip().splitlines()[-1])
                proof = guard.read()
                if variant in ('fetch_conflict','fetch_private_numeric_url'):
                    self.assertEqual(value['calls'],0)
                    self.assertIn('refused',proof['stages'])
                else:
                    self.assertEqual(value['calls'],1)
                    self.assertEqual(value['steps'],2)
                    self.assertNotIn('refused',proof['stages'])
        # Same actual guard: clipped tool output, three calls/four steps, and budget refusal.
        for variant in ('normal','chain','budget'):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory(prefix='wx-native-synthetic-') as folder:
                work = Path(folder)
                policy = native_contract(web, [], InputBudget(limit=10 if variant=='budget' else 524288))
                guard = Guard(work,'synthetic policy','synthetic question',None,
                              dict(T=len('synthetic policysynthetic question'.encode()),F=framework_upper(),V=0,O=128000,C=1000000),
                              wire_message=dict(type='user',message=dict(role='user',content='synthetic question')),
                              native_web=policy)
                result = subprocess.run([str(node),str(ROOT/'tests/fixtures/native_harness.mjs'),str(guard.root),variant],
                                        capture_output=True,text=True,encoding='utf-8',timeout=15)
                self.assertEqual(result.returncode,0,result.stderr)
                value = json.loads(result.stdout.strip().splitlines()[-1]); proof = guard.read()
                if variant=='chain':
                    self.assertEqual((value['calls'],value['steps']),(3,4))
                elif variant=='budget':
                    self.assertEqual(value['calls'],0)
                    self.assertIn('refused',proof['stages'])
                else:
                    self.assertLessEqual(proof['native_web']['result_bytes'],8000)
                    self.assertNotIn('ref',value['output'])


if __name__ == '__main__':
    unittest.main()
