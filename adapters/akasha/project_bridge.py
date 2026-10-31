"""Reviewed protocol overlay for the pinned upstream. UIA is used unchanged."""
import asyncio
import base64
from collections import OrderedDict
import hashlib
import json
import os
from pathlib import Path
import threading
import time
from urllib.parse import urljoin, urlsplit,unquote
import uuid

import requests

def stable_id(account, kind, value):
    return int.from_bytes(hashlib.sha256(json.dumps([account,kind,str(value)],ensure_ascii=False).encode()).digest()[:6], 'big') or 1

def load_config():
    return json.loads(Path(os.environ['AKASHA_CONFIG']).read_text(encoding='utf-8'))

class Protocol:
    def __init__(self, cfg, sender, push, status_path):
        self.cfg=cfg; self.sender=sender; self.push=push; self.status_path=Path(status_path)
        self.account=cfg['bridge']['bot_wxid']; self.boot=uuid.uuid4().hex
        self.started=time.time(); self.seen=OrderedDict(); self.contacts={}; self.buffers={}
        self.lock=threading.Lock(); self.send_lock=asyncio.Lock()
        self.flags={}; self.generations={}; self.sse=False; self.ws=False; self.replies=0
        self.unknown={}
        if self.status_path.exists():
            old=json.loads(self.status_path.read_text(encoding='utf-8'))
            self.unknown=old.get('unknown',{});self.flags=old.get('paused',{});self.generations=old.get('generations',{})
            for sid in self.unknown:self.flags[sid]=True
        self.persist()

    def persist(self):
        self.status_path.parent.mkdir(parents=True,exist_ok=True)
        value=dict(boot=self.boot, sse=self.sse, astrbot_ws=self.ws, real_reply=False,
                   local_reported=self.replies, paused=self.flags, generations=self.generations,
                   unknown=self.unknown, pid=os.getpid(),user_acceptance='pending',uia_initialized=getattr(self.sender,'_ready',None))
        tmp=self.status_path.with_suffix('.tmp')
        with self.lock:
            tmp.write_text(json.dumps(value),encoding='utf-8');tmp.replace(self.status_path)

    def api(self, route, **params):
        r=requests.get(self.cfg['weflow']['url']+route,params=params,
                       headers={'Authorization':'Bearer '+self.cfg['weflow']['token']},timeout=10)
        r.raise_for_status();return r.json()

    def allowed(self, data):
        b=self.cfg['bridge'];sid=str(data.get('sessionId',''))
        group=data.get('sessionType')=='group' or sid.endswith('@chatroom')
        selected=b['sessions'] if group else (b['private_sessions'] if b['private_enabled'] else [])
        return (sid in {s['id'] for s in selected} and
                data.get('event','message.new')=='message.new' and
                not data.get('isSend') and data.get('senderUsername')!=self.account and
                data.get('senderUsername','') not in b['blacklist'] and data.get('sourceName','') not in b['blacklist'])

    def exact_message(self, data, media=False):
        # Match the full server ID; never choose the newest image in a room.
        result=self.api('/api/v1/messages',talker=data['sessionId'],start=data['timestamp'],end=data['timestamp'],
                        limit=100,media='1' if media else '0',image='1',voice='0',video='0',emoji='1')
        return next((m for m in result.get('messages',[]) if str(m.get('serverId',''))==str(data['rawid'])),None)

    def media(self, data, row):
        if not row or not row.get('mediaUrl'):return None
        url=urljoin(self.cfg['weflow']['url'],row['mediaUrl'])
        base=urlsplit(self.cfg['weflow']['url']);u=urlsplit(url)
        if (u.scheme,u.netloc)!=(base.scheme,base.netloc) or not u.path.startswith('/api/v1/media/'):return None
        r=requests.get(url,headers={'Authorization':'Bearer '+self.cfg['weflow']['token']},timeout=15,stream=True)
        r.raise_for_status();raw=bytearray()
        for chunk in r.iter_content(16384):
            raw.extend(chunk)
            if len(raw)>8*1024*1024:raise ValueError('image_size')
        folder=self.status_path.parent/'media';folder.mkdir(exist_ok=True)
        path=folder/(hashlib.sha256((data['sessionId']+str(data['rawid'])).encode()).hexdigest()+'.image')
        path.write_bytes(raw);return str(path)

    def receive(self, data):
        if not self.allowed(data):return
        if float(data.get('timestamp',0)) < self.started:return
        rawid=str(data.get('rawid',''))
        if not rawid:return
        key=(data['sessionId'],rawid)
        if key in self.seen:return
        self.seen[key]=True
        while len(self.seen)>4096:self.seen.popitem(last=False)
        row=None
        try:row=self.exact_message(data, data.get('content') in ('[图片]','[表情]','[动画表情]'))
        except requests.RequestException:pass
        if row and (row.get('isSend') or row.get('senderUsername')==self.account):return
        sender=(row or {}).get('senderUsername') or data.get('senderUsername') or data.get('senderWxid')
        if sender in self.cfg['bridge']['blacklist']:return
        # Trusted owner controls also work during a local pause; never generate.
        if sender and sender==self.cfg['bridge'].get('owner_wxid'):
            command=data.get('content','').strip()
            for nick in self.cfg['bridge']['nicknames']:command=command.replace('@'+nick,'').replace('＠'+nick,'').strip()
            actions={'暂停发言':'pause','恢复发言':'resume','重置本群上下文':'reset','重置会话':'reset','/重置':'reset'}
            if command in actions:self.control(actions[command],data['sessionId']);return
        if self.flags.get(data['sessionId']):return
        data=dict(data, sender_id=sender or 'local:'+data['sessionId']+':'+data.get('sourceName',''),
                  sender_trusted=bool(sender), reply_id=(row or {}).get('replyToMessageId'), media_path=None)
        if data.get('content') in ('[图片]','[表情]','[动画表情]'):
            try:data['media_path']=self.media(data,row)
            except (requests.RequestException,ValueError,OSError):pass
        sid=data['sessionId'];mode=self.cfg['bridge']['mode']
        if mode=='mention' and not any('@'+n in data.get('content','') or '＠'+n in data.get('content','') for n in self.cfg['bridge']['nicknames']):return
        if mode!='batch':self.emit([data]);return
        with self.lock:
            entry=self.buffers.setdefault(sid,[]);entry.append(data)
            if len(entry)==1:
                timer=threading.Timer(self.cfg['bridge']['buffer_seconds'],self.flush,args=(sid,));timer.daemon=True;timer.start()

    def flush(self,sid):
        with self.lock:rows=self.buffers.pop(sid,[])
        if rows:self.emit(rows)

    def emit(self, rows):
        d=rows[-1];sid=d['sessionId'];group=sid.endswith('@chatroom') or d.get('sessionType')=='group'
        selected=self.cfg['bridge']['sessions'] if group else self.cfg['bridge']['private_sessions']
        binding=next(s for s in selected if s['id']==sid)
        target=stable_id(self.account,'group' if group else 'user',sid)
        self.contacts[target]=(sid,binding['name'],group)
        uid=stable_id(self.account,'user',d['sender_id']);parts=[]
        for row in rows:
            parts.append(dict(type='text',data={'text':row.get('content','')}))
        source=dict(version=1,account=self.account,session=sid,boot=self.boot,
                    generation=self.generations.get(sid,0),sender=d['sender_id'],sender_trusted=d['sender_trusted'],
                    message_ids=[str(r['rawid']) for r in rows],timestamp=d['timestamp'],
                    rows=[{k:r.get(k) for k in ('rawid','sender_id','sender_trusted','sourceName','timestamp','content','reply_id','media_path')} for r in rows],
                    wake='text-derived' if any('@'+n in d.get('content','') or '＠'+n in d.get('content','') for n in self.cfg['bridge']['nicknames']) else 'none',
                    media_error=d.get('content') in ('[图片]','[表情]','[动画表情]') and not d.get('media_path'))
        source['members']=[]
        if group:
            try:
                roster=self.api('/api/v1/group-members',chatroomId=sid)
                source['members']=[dict(wxid=m.get('wxid'),name=m.get('groupNickname') or m.get('displayName') or m.get('nickname')) for m in roster.get('members',[])]
            except requests.RequestException:pass
        event=dict(time=int(d['timestamp']),self_id=stable_id(self.account,'bot',self.account),post_type='message',
                   message_type='group' if group else 'private',sub_type='normal' if group else 'friend',
                   message_id=stable_id(self.account,'message',sid+':'+':'.join(source['message_ids'])),
                   user_id=uid,message=parts,raw_message='\n'.join(r.get('content','') for r in rows),
                   sender=dict(user_id=uid,nickname=d.get('sourceName','')),akasha=source)
        if group:event.update(group_id=target,group_name=binding['name'])
        else:event['user_id']=target
        if self.push(event):self.persist()

    async def handle_api(self, data, ws):
        action=data.get('action');p=data.get('params',{});result={};code=0;message=''
        if action in ('send_msg','send_group_msg','send_private_msg'):
            target=int(p.get('group_id') or p.get('user_id') or 0)
            contact=self.contacts.get(target)
            if not contact:code=1404;message='UNBOUND_TARGET'
            else:
                sid,name,group=contact
                async with self.send_lock:
                    if self.flags.get(sid):code=1403;message='SESSION_PAUSED'
                    else:
                        sent=0
                        self.unknown[sid]=dict(at=time.time(),reason='sending');self.persist()
                        try:
                            for seg in p.get('message',[]):
                                typ=seg.get('type');value=seg.get('data',{})
                                if typ=='text':ok=await asyncio.to_thread(self.sender.send_text,name,value.get('text',''))
                                elif typ=='image':
                                    raw=value.get('file','')
                                    # Only the existing controlled meme delivery is allowed out.
                                    path=Path(unquote(raw.removeprefix('file:///')))
                                    allowed=Path(self.cfg['astrbot']['root'])/'state/meme-delivery'
                                    if not path.resolve().is_relative_to(allowed.resolve()):raise ValueError('unregistered_media')
                                    ok=await asyncio.to_thread(self.sender.send_image,name,str(path))
                                else:raise ValueError('unsupported_segment')
                                if ok is not True:raise RuntimeError('local_send_unknown')
                                sent+=1
                            if not sent:raise ValueError('empty_send')
                            self.replies+=1
                            self.unknown.pop(sid,None)
                            result=dict(message_id=stable_id(self.account,'local_reported',uuid.uuid4().hex),delivery_level='local_reported')
                        except Exception as error:
                            code=1500;message='LOCAL_SEND_UNKNOWN';self.flags[sid]=True
                            failure=getattr(self.sender,'failure',{}) or dict(error_type=type(error).__name__)
                            self.unknown[sid]=dict(at=time.time(),parts_completed=sent,**failure)
                        self.persist()
        elif action=='get_login_info':result=dict(user_id=stable_id(self.account,'bot',self.account),nickname=self.cfg['bridge']['nicknames'][0])
        elif action=='get_status':result=dict(online=self.sse,good=self.sse)
        elif action=='get_version_info':result=dict(app_name='Akasha project overlay',protocol_version='v11')
        elif action in ('get_group_list','get_friend_list'):
            result=[dict(group_id=k,group_name=v[1]) for k,v in self.contacts.items() if v[2]] if action=='get_group_list' else []
        else:code=1404;message='UNSUPPORTED_API'
        try:await ws.send(json.dumps(dict(status='failed' if code else 'ok',retcode=code,data=result,message=message,echo=data.get('echo'))))
        except Exception:
            if action in ('send_msg','send_group_msg','send_private_msg') and contact:
                self.flags[sid]=True;self.unknown[sid]=dict(at=time.time(),reason='result_connection_lost');self.persist()
            raise

    def control(self,action,sid):
        sessions=[sid] if sid else [s['id'] for s in self.cfg['bridge']['sessions']+self.cfg['bridge']['private_sessions']]
        for key in sessions:
            if action in ('pause','reset','resume'):
                self.generations[key]=self.generations.get(key,0)+1
                if action!='reset':self.flags[key]=action=='pause' or key in self.unknown
            elif action=='resolve-unknown':self.unknown.pop(key,None);self.flags[key]=False;self.generations[key]=self.generations.get(key,0)+1
        self.persist();return dict(ok=True)

def install(cfg, status_path):
    import state,config,bridge_core,ob_protocol,ob_client
    # Never allow upstream UIA or requests exceptions to log raw names/text/URLs.
    import logging
    logging.disable(logging.CRITICAL)
    protocol=Protocol(cfg,None,ob_protocol.push_event,status_path)
    original_init=bridge_core.WeFlowBridge.__init__
    def init(self,sender):original_init(self,sender);protocol.sender=sender
    bridge_core.WeFlowBridge.__init__=init
    bridge_core.WeFlowBridge.should_ignore=lambda self,d:not protocol.allowed(d) or not isinstance(d.get('content'),str)
    bridge_core.WeFlowBridge.add_to_buffer=lambda self,d:protocol.receive(d)
    # Keep upstream SSE connection/reconnect, remove sensitive logs by disabling logging.
    # Its timestamp and rawid dedup is retained; protocol adds account/session dedup.
    async def api(data):await protocol.handle_api(data,state._ob_ws)
    ob_client._handle_ob_api=api;ob_protocol._handle_ob_api=api
    state._wxid_to_int=lambda value:stable_id(protocol.account,'user',value)
    state._self_id_int=stable_id(protocol.account,'bot',protocol.account)
    return protocol
