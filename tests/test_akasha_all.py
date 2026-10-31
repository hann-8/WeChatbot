"""Real AstrBot adapter/router/provider with synthetic WeFlow/UIA/model only."""
import asyncio
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import site
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

WX=Path(__file__).resolve().parents[1]
QQ=Path('E:/CodexWS/QQbot_Snowluma')
sys.path[:0]=[str(WX/'adapters/akasha'),str(QQ),str(QQ/'src'),str(QQ/'tests')]
site.addsitedir(str(QQ/'runtime/astrbot-tool/astrbot/Lib/site-packages'))
from project_bridge import Protocol,stable_id

class BridgeTests(unittest.IsolatedAsyncioTestCase):
    def setup_protocol(self,folder,sender=None):
        cfg=json.loads((WX/'config/examples/akasha.json').read_text(encoding='utf-8'))
        cfg['bridge'].update(bot_wxid='wxid_synthetic_bot',sessions=[dict(id='synthetic@chatroom',name='Synthetic room')])
        cfg['astrbot']['root']=str(folder/'qq')
        self.events=[];p=Protocol(cfg,sender,self.events.append,folder/'state/akasha-wechat/bridge-status.json')
        p.push=lambda event:self.events.append(event) or True
        p.started=0
        p.exact_message=lambda d,media=False:dict(serverId=d['rawid'],senderUsername=d.get('sender','wxid_synthetic_user'),isSend=False)
        p.api=lambda *a,**k:dict(members=[])
        return p
    def data(self,rawid='1234567890123456789',**kw):
        return dict(event='message.new',sessionId='synthetic@chatroom',sessionType='group',rawid=rawid,
                    sourceName='Synthetic user',groupName='Synthetic room',content='@鱼鱼 合成问题',timestamp=int(time.time()),**kw)
    async def test_source_filter_ids_current_media_and_batch(self):
        with tempfile.TemporaryDirectory() as folder:
            p=self.setup_protocol(Path(folder));d=self.data();p.receive(d);p.receive(d)
            self.assertEqual(len(self.events),1);e=self.events[0]
            self.assertEqual(e['akasha']['message_ids'],[d['rawid']]);self.assertTrue(e['message_id'])
            self.assertFalse(any(s['type']=='at' for s in e['message']))
            q=self.setup_protocol(Path(folder));q.receive(d);self.assertEqual(self.events[-1]['user_id'],e['user_id'])
            p.receive(dict(d,sessionId='unselected@chatroom',rawid='2'));self.assertEqual(len(self.events),1)
            p.receive(dict(d,rawid='self',sender=p.account));self.assertEqual(len(self.events),1)
            p.cfg['bridge']['blacklist']=['blocked'];p.receive(dict(d,rawid='blocked',sender='blocked'));self.assertEqual(len(self.events),1)
            # Exact lookup returns the original full server ID, never a newer image.
            p.api=lambda *a,**k:dict(messages=[dict(serverId='newer',mediaUrl='wrong'),dict(serverId=d['rawid'],mediaUrl='correct')])
            self.assertEqual(Protocol.exact_message(p,d,True)['mediaUrl'],'correct')
            p.api=lambda *a,**k:dict(members=[])
            p.cfg['bridge']['mode']='batch';p.receive(dict(d,rawid='3'));p.receive(dict(d,rawid='4',sender='different'))
            p.flush(d['sessionId']);self.assertEqual(self.events[-1]['akasha']['message_ids'],['3','4'])
            self.assertNotEqual(self.events[-1]['akasha']['rows'][0]['sender_id'],self.events[-1]['akasha']['rows'][1]['sender_id'])
    async def test_result_after_sender_false_unknown_and_no_retry(self):
        for outcome in (True,False,None,RuntimeError('fixture')):
            with self.subTest(outcome=outcome),tempfile.TemporaryDirectory() as folder:
                order=[]
                class Sender:
                    def send_text(self,*a):
                        order.append('UIA')
                        if isinstance(outcome,Exception):raise outcome
                        return outcome
                class WS:
                    async def send(self,value):order.append(json.loads(value))
                p=self.setup_protocol(Path(folder),Sender());p.receive(self.data())
                target=self.events[-1]['group_id'];data=dict(action='send_group_msg',params=dict(group_id=target,message=[dict(type='text',data=dict(text='合成回复'))]),echo='fixture')
                await p.handle_api(data,WS());self.assertEqual(order[0],'UIA')
                self.assertEqual(order[1]['retcode'],0 if outcome is True else 1500)
                if outcome is True:
                    await p.handle_api(data,WS());self.assertEqual(sum(x=='UIA' for x in order),2)
                else:
                    await p.handle_api(data,WS());self.assertEqual(sum(x=='UIA' for x in order),1)
                    restarted=self.setup_protocol(Path(folder),Sender());self.assertTrue(restarted.unknown)
        with tempfile.TemporaryDirectory() as folder:
            calls=[];results=[]
            class Partial:
                def send_text(self,*a):calls.append(True);return len(calls)==1
            class WS:
                async def send(self,data):results.append(json.loads(data))
            p=self.setup_protocol(Path(folder),Partial());p.receive(self.data());target=self.events[-1]['group_id']
            await p.handle_api(dict(action='send_group_msg',params=dict(group_id=target,message=[dict(type='text',data=dict(text='fixture'))]*3)),WS())
            self.assertEqual(len(calls),2);self.assertEqual(results[0]['retcode'],1500)
            self.assertEqual(p.unknown['synthetic@chatroom']['parts_completed'],1)

class FrameworkTests(unittest.IsolatedAsyncioTestCase):
    setup_protocol=BridgeTests.setup_protocol
    data=BridgeTests.data
    async def test_actual_adapter_shared_business_gateway_provider_and_two_rounds(self):
        import logging
        logging.disable(logging.CRITICAL)
        import test_transport_router as fixture
        from qqbot_gateway.attention import Attention
        from qqbot_gateway.participation import validate_participation
        from qqbot_gateway.group_memory import MemoryStore
        from qqbot_gateway.reply_plan import DEFAULTS,digest
        from qqbot_gateway.task_store import TaskStore
        from qqbot_gateway.token_budget import InputBudget
        from qqbot_gateway.model_gateway import application,ModelQueue
        from qqbot_gateway.backends import BackendResult
        from aiohttp.test_utils import TestClient,TestServer
        fixture.RouterTests.setUpClass()
        f=fixture.RouterTests('test_actual_js_gate_astrbot_parser_time_sender_image_and_no_reply_fetch')
        await f.asyncSetUp();tasks=None
        try:
            p=self.setup_protocol(f.root);cfg=p.cfg;cfg['pairings']=[dict(wechat_session='synthetic@chatroom',qq_session='111',scope='facts_only',actor_links={'wxid_synthetic_user':'333'})]
            r=f.router;r.output=dict(DEFAULTS,bubble_delay_min_ms=0,bubble_delay_max_ms=0);r.web=dict(engine='codebuddy_cli',enabled=True,search_enabled=True)
            r.vision=dict(enabled=True);r.members=dict(enabled=False);r.bilibili=dict(enabled=False)
            r.participation=validate_participation(dict(mode='free',attention=dict(enabled=True,aliases=['鱼鱼'])))
            r.group_turns=Attention(r.participation,'qepoch');r.group_turns.bot=r.bot
            r.memory=MemoryStore(f.root,r.bot,r.groups,cfg=dict(enabled=True,learning_enabled=True));r.persona='合成人设'
            r.memes=SimpleNamespace(cfg=dict(enabled=False));r.budget=InputBudget(limit=524288)
            tasks=r.tasks=TaskStore(f.root/'tasks.sqlite3')
            from plugins.qq_router import wechat
            config=f.root/'config/local/akasha.json';config.parent.mkdir(parents=True);config.write_text(json.dumps(cfg),encoding='utf-8')
            with patch.object(wechat,'CONFIG',config):r.wechat=wechat.create_route(r)
            route=r.wechat;route.status_path=p.status_path;route.connection=lambda:p.boot;route.connection_id=p.boot
            p.ws=True;p.persist()
            class Sender:
                def send_text(self,name,text):return True
            p.sender=Sender()
            class Bot:
                async def send_group_msg(self,**kw):
                    class WS:
                        async def send(self,data):self.value=json.loads(data)
                    ws=WS();await p.handle_api(dict(action='send_group_msg',params=kw),ws)
                    if ws.value['retcode']:raise RuntimeError('fixture_send_unknown')
                    return ws.value['data']
            bot=Bot();adapter=f.Adapter.__new__(f.Adapter);adapter.bot=bot
            class Runner:
                count=0
                async def run(self,system,prompt,trace):
                    self.count+=1;self.last=json.loads(json.loads(prompt)[-1]['content'])
                    return BackendResult(json.dumps(dict(qqbot_turn_reply=2,decision='speak',kind='answer',bubbles=['合成答复'],meme_id=None,response_to_seq=self.last['target_seq'],mention=None,memory_updates={'new_1':'合成记忆'} if self.count==1 else {},memory_receipt=self.count==1)))
            runner=Runner();app=application(ModelQueue(runner),'t'*32,budget=r.budget,output=r.output,
                v2=dict(mode='free',config_version=digest(r.persona_id),aliases=['鱼鱼'],memory_enabled=True,learning_enabled=True,memory_config=r.memory.cfg))
            from plugins.qq_router.provider import QQBotProvider,ProviderOpenAIOfficial
            provider=QQBotProvider.__new__(QQBotProvider)
            async with TestClient(TestServer(app)) as client:
                async def model(self,prompt=None,session_id=None,**kwargs):
                    response=await client.post('/v1/chat/completions',json=dict(model='workbuddy-local',messages=[dict(role='system',content=kwargs['system_prompt']),dict(role='user',content=prompt)],qqbot_request=self._group_request.get()),headers={'Authorization':'Bearer '+'t'*32,'X-QQBot-Trace':self._group_trace.get(),'X-QQBot-Transport':self._transport.get()})
                    value=await response.json();self_test.assertEqual(response.status,200,value)
                    return SimpleNamespace(**value, choices_obj=None)
                self_test=self
                for round in (1,2):
                    p.receive(self.data(rawid=str(round)));row=self.events[-1]
                    msg=await adapter.convert_message(f.Event(row));e=f.MessageEvent(msg.message_str,msg,f.PlatformMetadata(name='aiocqhttp',description='fixture',id='akasha-wechat'),str(row['group_id']),bot)
                    gen=r.on_group(e);req=await anext(gen)
                    await r.before_provider(e,req)
                    with patch.object(ProviderOpenAIOfficial,'text_chat',model):value=await provider.text_chat(prompt=req.prompt,session_id=req.session_id,system_prompt=req.system_prompt)
                    value.choices=[SimpleNamespace(message=SimpleNamespace(content=x['message']['content'])) for x in value.choices]
                    response=SimpleNamespace(raw_completion=value);run=SimpleNamespace(messages=[])
                    await r.preserve_gateway_text(e,run,response)
                    self.assertFalse(e.get_extra('qq_group_invalid'))
                    await r.deliver_reply(e)
                    with self.assertRaises(StopAsyncIteration):await anext(gen)
                    self.assertEqual(tasks.delivery(e.get_extra('qq_delivery_key'))['state'],'sent')
                self.assertEqual(runner.count,2);self.assertEqual(p.replies,2)
                self.assertEqual(len(r.memory._load('111')['records']),1)
                self.assertEqual(r.memory.namespace('111'),r.memory.namespace(str(row['group_id'])))
                self.assertEqual(r.memory.actor('111','333'),r.memory.actor(str(row['group_id']),str(row['user_id'])))
                # Reset clears RAM only; the paired schema2 facts remain.
                gid=str(row['group_id']);old=route.group_turns.group_epoch(gid)
                p.control('reset','synthetic@chatroom');p.receive(self.data(rawid='3'))
                msg=await adapter.convert_message(f.Event(self.events[-1]));e=f.MessageEvent(msg.message_str,msg,f.PlatformMetadata(name='aiocqhttp',description='fixture',id='akasha-wechat'),gid,bot)
                gen=r.on_group(e);req=await anext(gen)
                self.assertNotEqual(route.group_turns.group_epoch(gid),old)
                self.assertEqual(len(json.loads(req.prompt)['memory']['records']),1)
                await gen.aclose()
                # A pause invalidates already accepted event generations.
                p.control('pause','synthetic@chatroom');self.assertFalse(route.silence_allowed(e))
                p.control('resume','synthetic@chatroom');self.assertFalse(route.silence_allowed(e))
        finally:
            if tasks:tasks.close()
            await f.asyncTearDown();fixture.RouterTests.tearDownClass()

if __name__=='__main__':unittest.main()
