"""Project lifecycle and local panel around the upstream Akasha bridge."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
import time
import subprocess
import sys
import requests
from project_bridge import load_config,install

cfg=load_config()
home=Path(os.environ['AKASHA_CONFIG']).parents[2]
status_path=home/'state/akasha-wechat/bridge-status.json'
protocol=install(cfg,status_path)
from uia_dispatch import install_sender
install_sender(cfg)
import main,state

class Panel(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        if self.path=='/setup':
            self.send_response(302);self.send_header('Location','http://127.0.0.1:18108/ui/?token='+cfg['weflow']['token']);self.end_headers();return
        if self.path=='/config':
            value=load_config();value['weflow']['token']='';body=json.dumps(value,ensure_ascii=False).encode();kind='application/json'
        elif self.path=='/choices':
            value=dict(sessions=[],qq_sessions=[],account='',members=[])
            try:
                result=protocol.api('/api/v1/sessions',limit=1000)
                value['sessions']=[dict(id=s.get('username') or s.get('sessionId'),name=s.get('displayName') or s.get('name') or s.get('nickname')) for s in result.get('sessions',[])]
                exe=home/'runtime/akasha-wechat/weflow/weflow-v5.0.1-windows-x64/weflow.exe'
                result=subprocess.run([str(exe),'config','get','wxid','--json'],env=dict(os.environ,WEFLOW_HOME=str(home/'runtime/akasha-wechat/weflow-home')),capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode==0:
                    d=json.loads(result.stdout);d=d.get('data',d);value['account']=d.get('value',d.get('wxid','')) if isinstance(d,dict) else d
                qroot=Path(cfg['astrbot']['root'])
                code="import sys,json;sys.path.insert(0,'src');from qqbot_gateway.config_files import load_consumer;from pathlib import Path;s=load_consumer(Path('.').resolve());print(json.dumps(s['access']['allowed_groups']))"
                result=subprocess.run([str(qroot/'.venv/Scripts/python.exe'),'-X','utf8','-c',code],cwd=qroot,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode==0:value['qq_sessions']=json.loads(result.stdout)
                for room in load_config()['bridge']['sessions']:
                    roster=protocol.api('/api/v1/group-members',chatroomId=room['id'])
                    value['members'] += [dict(session=room['id'],wxid=m.get('wxid'),name=m.get('groupNickname') or m.get('displayName') or m.get('nickname')) for m in roster.get('members',[])]
            except Exception:value['error']='API_NOT_READY_OR_ACCOUNT_NOT_SAVED'
            body=json.dumps(value,ensure_ascii=False).encode();kind='application/json'
        elif self.path=='/status':
            value=json.loads(status_path.read_text(encoding='utf-8'));body=json.dumps(value).encode();kind='application/json'
        else:
            body=('''<!doctype html><meta charset="utf-8"><title>Akasha 本机管理</title><h1>Akasha 微信</h1>
<p>单一配置：config/local/akasha.json。密钥不回显。原生@不支持；图片/GIF按当前帧。</p>
<a href="/setup" target="_blank">打开带本机授权的 WeFlow 向导</a>
<button onclick="control('api')">向导保存后：切到桌面API</button><button onclick="choices()">读取账号/会话选项</button>
<pre id="choices"></pre><textarea id="config" style="width:95%;height:400px"></textarea><button onclick="save()">保存本机配置</button>
<h2>一次选择实际记忆配对</h2><button onclick="loadPairing()">载入本机会话选项</button><br>
<label>微信群 <select id="wxRoom"></select></label><label>QQ会话 <select id="qqRoom"><option value="">请选择</option></select></label>
<label>共享范围 <select id="scope"><option value="facts_only">仅长期事实，短期独立</option><option value="shared_context">长期事实和短期上下文</option></select></label><br>
<label>可选同一人映射 <select id="wxActor"><option value="">不合并人物</option></select></label><input id="qqActor" placeholder="明确对应的QQ用户ID（可留空）"><button onclick="savePairing()">保存本次配对选择</button>
<p>群名/成员同名不会自动合并；只有你在本机明确选择的会话和人物才共用记忆。</p>
<script>function opt(select,value,label){let o=document.createElement('option');o.value=value;o.textContent=label;select.append(o);}async function loadPairing(){let c=await(await fetch('/config')).json(),x=await(await fetch('/choices')).json();wxRoom.replaceChildren();for(let s of c.bridge.sessions)opt(wxRoom,s.id,s.name);qqRoom.replaceChildren();opt(qqRoom,'','请选择一个QQ会话');for(let [i,id]of x.qq_sessions.entries())opt(qqRoom,id,`${i+1} · ${id}`);opt(qqRoom,'__independent__','保持独立空间，不配对');wxActor.replaceChildren();opt(wxActor,'','不合并人物');for(let m of x.members)opt(wxActor,m.wxid,`${m.name} · ${m.wxid}`);}async function savePairing(){if(!wxRoom.value||!qqRoom.value){alert('先选择会话');return;}let c=await(await fetch('/config')).json();c.pairings=c.pairings.filter(p=>p.wechat_session!==wxRoom.value);if(qqRoom.value!=='__independent__'){let links={};if(wxActor.value&&qqActor.value.trim())links[wxActor.value]=qqActor.value.trim();c.pairings.push({wechat_session:wxRoom.value,qq_session:qqRoom.value,scope:scope.value,actor_links:links});}c.operator_pairing_reviewed=true;let r=await fetch('/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(c)});let x=await r.json();alert(x.saved?'已保存，本任务继续加载。':JSON.stringify(x));config.value=JSON.stringify(c,null,2);}</script>
<button onclick="location.reload()">刷新</button><pre id="s"></pre>
<button onclick="control('pause')">暂停</button><button onclick="control('resume')">恢复</button><button onclick="control('reset')">重置短期</button>
<h2>本机记忆</h2><input id="room" placeholder="所选会话sessionId；检查可留空"><button onclick="memory('memory-status')">查看计数/容量</button><button onclick="memory('memory-export')">导出到本机</button><input id="record" placeholder="要删除的记忆record_id"><button onclick="memory('memory-delete')">删除该条</button><button onclick="memory('memory-clear')">清除此所选空间</button><pre id="memoryResult"></pre>
<p>增删前先查看当前摘要。配对空间的删除会影响配对双方；取消配对请在上方配置移除pairings条目后保存/重启，旧记忆保留。</p>
<script>let memoryDigest;async function memory(action){if(action!=='memory-status'&&!room.value){alert('先填写一个明确会话并查看摘要');return;}let r=await fetch('/control',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action,session:room.value,expected:memoryDigest,record_id:record.value})});let x=await r.json();memoryResult.textContent=JSON.stringify(x,null,2);if(action==='memory-status'&&x.results?.length===1)memoryDigest=x.results[0].digest;}</script>
<script>fetch('/status').then(r=>r.json()).then(x=>s.textContent=JSON.stringify(x,null,2));fetch('/config').then(r=>r.json()).then(x=>config.value=JSON.stringify(x,null,2));function control(action){fetch('/control',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action})}).then(()=>location.reload())}function choices(){fetch('/choices').then(r=>r.json()).then(x=>document.getElementById('choices').textContent=JSON.stringify(x,null,2))}function save(){fetch('/config',{method:'POST',headers:{'Content-Type':'application/json'},body:config.value}).then(r=>r.json()).then(x=>alert(JSON.stringify(x)))}</script>''').encode();kind='text/html; charset=utf-8'
        self.send_response(200);self.send_header('Content-Type',kind);self.end_headers();self.wfile.write(body)
    def do_POST(self):
        # Browser origin must be the loopback panel, never a remote web page.
        if self.headers.get('Origin') not in (None,'http://127.0.0.1:18766'):
            self.send_error(403);return
        try:value=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))))
        except (ValueError,TypeError):self.send_error(400,'Invalid JSON');return
        if self.path=='/config':
            old=load_config();value['weflow']['token']=old['weflow']['token']
            if value['bridge']['mode'] not in ('all','mention','batch'):self.send_error(400);return
            p=Path(os.environ['AKASHA_CONFIG']);tmp=p.with_suffix('.tmp')
            tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(p)
            result=dict(saved=True,restart_required=True)
        elif value.get('action')=='api':
            subprocess.Popen([sys.executable,str(home/'scripts/akasha.py'),'api'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
            result=dict(requested=True)
        elif value.get('action') in ('memory-status','memory-export','memory-delete','memory-clear'):
            actions={'memory-status':'inspect','memory-export':'export','memory-delete':'delete','memory-clear':'clear'}
            body=dict(value,action=actions[value['action']])
            response=requests.post('http://127.0.0.1:18767/memory',json=body,timeout=5)
            result=response.json() if response.status_code==200 else dict(error='MEMORY_CHANGED_OR_UNAVAILABLE')
        elif value.get('action')=='stop':
            result=dict(stopping=True)
            threading.Thread(target=self.server.shutdown,daemon=True).start()
        else:result=protocol.control(value.get('action'),value.get('session',''))
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(json.dumps(result).encode())

def monitor():
    while state.running:
        protocol.ws=bool(state._ob_ws)
        protocol.sse=bool(state.bridge_instance and state.bridge_instance._sse_session and state.bridge_instance._sse_session.status_code==200)
        protocol.persist();time.sleep(1)

if __name__=='__main__':
    if '--manage-only' not in sys.argv:
        main._start_bridge()
        threading.Thread(target=monitor,daemon=True).start()
    try:ThreadingHTTPServer(('127.0.0.1',18766),Panel).serve_forever()
    finally:
        main._stop_bridge()
        if state.sender_instance and hasattr(state.sender_instance,'close'):state.sender_instance.close()
