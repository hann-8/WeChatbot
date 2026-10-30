"""Constructor failure reaches a useful, redacted startup report; no real UI."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, patch

from wechatbot.wxauto4_chat import StartupFailure, live, report_failure


class StartupDiagnosticTests(unittest.IsolatedAsyncioTestCase):
    async def test_framework_constructor_failure_has_stage_without_private_text(self):
        with tempfile.TemporaryDirectory(prefix='wx-startup-synthetic-') as folder:
            root = Path(folder)
            (root/'secrets').mkdir()
            (root/'secrets/wxauto4-chat.local.json').write_text(json.dumps(dict(
                account_alias='synthetic', conversation_key='synthetic', chat_name='private-group-sentinel',
                blacklist=[], chat_type='group', trigger_mode='text_prefix', prefix='bot ')), encoding='utf-8')
            model = AsyncMock()
            with patch('wechatbot.wxauto4_chat.load_config', return_value=object()), \
                 patch('wechatbot.wxauto4_chat.inspect_dependency', return_value={'dependency_present': True}), \
                 patch('wechatbot.wxauto4_chat.ChatCliModel', return_value=model), \
                 patch('wechatbot.wxauto4_chat.live_factory', side_effect=RuntimeError('private-group-sentinel private-message-sentinel')):
                with self.assertRaises(StartupFailure) as caught:
                    await live(root)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                value = report_failure(caught.exception, root)
            self.assertEqual(value['stage'], 'wxauto_init')
            self.assertEqual(value['error_type'], 'RuntimeError')
            self.assertTrue(value['frames'])
            saved = (root/'state/startup-last-error.json').read_text(encoding='utf-8')
            self.assertEqual(json.loads(saved), value)
            self.assertNotIn('private-group-sentinel', saved + output.getvalue())
            self.assertNotIn('private-message-sentinel', saved + output.getvalue())
            model.close.assert_awaited_once()


if __name__ == '__main__':
    unittest.main()
