"""Single local entry for the pinned Akasha runtime (never manages WeChat)."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'runtime/akasha-wechat'
LOCAL = ROOT / 'config/local/akasha.json'
STATE = ROOT / 'state/akasha-wechat'
EXE = BASE / 'weflow/weflow-v5.0.1-windows-x64/weflow.exe'

def load():
    if not LOCAL.exists():
        LOCAL.parent.mkdir(parents=True, exist_ok=True)
        value = json.loads((ROOT/'config/examples/akasha.json').read_text(encoding='utf-8'))
        value['weflow']['token'] = secrets.token_hex(32)
        save(value)
    return json.loads(LOCAL.read_text(encoding='utf-8'))

def save(value):
    LOCAL.parent.mkdir(parents=True, exist_ok=True)
    tmp = LOCAL.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(LOCAL)

def environment(cfg):
    env = dict(os.environ, WEFLOW_HOME=str(BASE/'weflow-home'),
               WEFLOW_HTTP_TOKEN=cfg['weflow']['token'], PYTHONUTF8='1',
               AKASHA_CONFIG=str(LOCAL))
    return env

def alive(record):
    import psutil
    try:
        p = psutil.Process(record['pid'])
        return p if abs(p.create_time()-record['created']) < .02 and str(Path(p.exe()).resolve()).lower() == record['exe'].lower() else None
    except (psutil.Error, KeyError):
        return None

def stop(name):
    p = STATE/(name+'.json')
    if not p.exists(): return
    record = json.loads(p.read_text(encoding='utf-8'))
    process = alive(record)
    if process:
        if name in ('bridge','panel'):
            import requests
            try:
                status_path=STATE/'bridge-status.json'
                if status_path.exists() and json.loads(status_path.read_text(encoding='utf-8')).get('pid')==record['pid']:
                    requests.post('http://127.0.0.1:18766/control',json=dict(action='stop'),timeout=2)
                    process.wait(5)
            except Exception:pass
        if alive(record):process.terminate()
        try: process.wait(10)
        except Exception: raise RuntimeError('Managed process did not stop: '+name)
    p.unlink()

def launch(name, args, cfg, cwd=None):
    import psutil
    STATE.mkdir(parents=True, exist_ok=True)
    record = STATE/(name+'.json')
    if record.exists() and alive(json.loads(record.read_text(encoding='utf-8'))): return
    with (STATE/(name+'.log')).open('ab') as log:
        destination=subprocess.DEVNULL if name in ('setup','weflow') else log
        proc = subprocess.Popen(args, cwd=cwd or ROOT, env=environment(cfg),
                                stdout=destination, stderr=destination, creationflags=subprocess.CREATE_NO_WINDOW)
    p = psutil.Process(proc.pid)
    record.write_text(json.dumps(dict(pid=p.pid, created=p.create_time(), exe=str(Path(p.exe()).resolve()))), encoding='utf-8')

def prepare(cfg):
    upstream = BASE/'upstream/wechat-weflow-bridge-ob11'
    dest = BASE/'run'
    dest.mkdir(parents=True, exist_ok=True)
    for p in upstream.iterdir():
        if p.is_file() and p.name != 'config.json': shutil.copy2(p, dest/p.name)
    main=dest/'main.py'
    original=main.read_text(encoding='utf-8')
    old='/api/v1/messages?limit=1&access_token={config.ACCESS_TOKEN}'
    if old not in original:raise RuntimeError('Pinned upstream health接点已变化')
    main.write_text(original.replace(old,'/health'),encoding='utf-8',newline='\n')
    for p in (ROOT/'adapters/akasha').glob('*.py'): shutil.copy2(p, dest/p.name)
    generated=dict(weflow_base_url=cfg['weflow']['url'],access_token=cfg['weflow']['token'],
                   bot_wxid=cfg['bridge']['bot_wxid'],bot_nicknames=cfg['bridge']['nicknames'],
                   astrbot_ob_url=cfg['astrbot']['ws'],web_port=18766,group_reply_mode='all',
                   astrbot_attachments=str(STATE/'media'),buffer_seconds=cfg['bridge']['buffer_seconds'])
    (dest/'config.json').write_text(json.dumps(generated,ensure_ascii=False),encoding='utf-8')
    # Credentials stay in the single ignored config, never in the source copy.
    return dest

def status(cfg):
    import requests
    result = dict(environment_ready=EXE.exists(), selected=bool(cfg['bridge']['sessions']),
                  weflow_database=False, sse=False, astrbot_ws=False, model_metadata=False,
                  real_reply=False, processes={})
    for name in ('setup','weflow','bridge','panel'):
        p=STATE/(name+'.json')
        result['processes'][name]=bool(p.exists() and alive(json.loads(p.read_text(encoding='utf-8'))))
    try:
        r=requests.get(cfg['weflow']['url']+'/api/v1/sessions', headers={'Authorization':'Bearer '+cfg['weflow']['token']}, timeout=3)
        result['weflow_database']=r.status_code==200 and r.json().get('success',True) is not False
    except Exception: pass
    try:
        result.update(requests.get('http://127.0.0.1:18766/status', timeout=2).json())
    except Exception: pass
    try:
        gateway=requests.get('http://127.0.0.1:8765/health',timeout=2)
        result['gateway_ready']=gateway.status_code==200 and gateway.json().get('router_ready') is True
        proof=Path(cfg['astrbot']['root'])/'state/lap43-native-web-trial/cli-probe.json'
        if proof.exists():
            value=json.loads(proof.read_text(encoding='utf-8'))
            active=Path(cfg['astrbot']['root'])/'state/vision-evidence/active.json'
            bound=json.loads(active.read_text(encoding='utf-8')).get('binding') if active.exists() else None
            result['model_metadata']=value.get('passed') is True and value.get('binding')==bound and value.get('real_generations')==0 and value.get('positive_next_calls')==0
    except Exception: pass
    return result

def ensure_astrbot(cfg):
    def listening(port):
        try:
            with socket.create_connection(('127.0.0.1',port),timeout=1):return True
        except OSError:return False
    root=Path(cfg['astrbot']['root']);python=root/'.venv/Scripts/python.exe'
    ready=root/'state/router-ready.json'
    loaded=json.loads(ready.read_text(encoding='utf-8')) if ready.exists() else {}
    if listening(11229) and listening(8765) and loaded.get('wechat_config_sha256')==hashlib.sha256(LOCAL.read_bytes()).hexdigest():return
    env=dict(os.environ,PYTHONPATH=str(root/'src')+';'+str(root),QQBOT_ROOT=str(root),PYTHONUTF8='1')
    STATE.mkdir(parents=True,exist_ok=True)
    with (STATE/'astrbot-start.log').open('ab') as log:
        result=subprocess.run([str(python),str(root/'scripts/configure_akasha.py')],env=env,cwd=root,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode:raise RuntimeError('AstrBot incremental configuration failed')
        if listening(6199) or listening(8765):
            result=subprocess.run([str(python),str(root/'scripts/manage.py'),'stop'],env=env,cwd=root,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode:raise RuntimeError('Managed AstrBot stop failed')
        result=subprocess.run([str(python),str(root/'scripts/manage.py'),'start-desktop'],env=env,cwd=root,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode or not listening(11229):raise RuntimeError('AstrBot 11229 not ready; see local status')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('action', type=str.lower, choices=['prepare','inspect','setup','api','start','stop','status','pause','resume','reset','memory-status','resolve-unknown'])
    parser.add_argument('--session', default='')
    args=parser.parse_args(); cfg=load()
    if args.action=='prepare': prepare(cfg); print('Pinned runtime prepared; config: '+str(LOCAL))
    elif args.action=='setup':
        stop('bridge');stop('weflow')
        launch('setup',[str(EXE),'serve','--host','127.0.0.1','--port','18108'],cfg)
        dest=prepare(cfg)
        launch('panel',[str(BASE/'venv/Scripts/python.exe'),str(dest/'project_entry.py'),'--manage-only'],cfg,dest)
        print('WeFlow setup: http://127.0.0.1:18108/ui/ (local token available through management page)')
    elif args.action=='api':
        stop('setup')
        launch('weflow',[str(EXE),'serve','--desktop','--message-push','--host','127.0.0.1','--port','5031'],cfg)
        print('WeFlow desktop API requested on 5031.')
    elif args.action=='start':
        if not cfg['bridge']['sessions'] or not cfg['bridge']['bot_wxid']: raise SystemExit('Select the robot account and target session in local config first.')
        stop('setup');dest=prepare(cfg)
        launch('weflow',[str(EXE),'serve','--desktop','--message-push','--host','127.0.0.1','--port','5031'],cfg)
        import requests
        sessions=None
        for attempt in range(20):
            try:
                response=requests.get(cfg['weflow']['url']+'/api/v1/sessions',headers={'Authorization':'Bearer '+cfg['weflow']['token']},timeout=3)
                response.raise_for_status();value=response.json()
                if value.get('success') is True:sessions=value.get('sessions',[]);break
            except requests.RequestException:pass
            time.sleep(.5)
        if sessions is None:raise RuntimeError('WeFlow database/API not ready; open local setup.')
        chosen=cfg['bridge']['sessions']+(cfg['bridge']['private_sessions'] if cfg['bridge']['private_enabled'] else [])
        for binding in chosen:
            same=[s for s in sessions if s.get('displayName')==binding['name']]
            if len(same)!=1 or same[0].get('username')!=binding['id']:
                raise RuntimeError('Selected session name changed or is ambiguous; choose a unique local search name.')
        ensure_astrbot(cfg)
        stop('bridge')
        stop('panel')
        launch('bridge',[str(BASE/'venv/Scripts/python.exe'),str(dest/'project_entry.py')],cfg,dest)
        print(json.dumps(status(cfg), ensure_ascii=False))
    elif args.action=='stop':
        for name in ('bridge','weflow','setup','panel'): stop(name)
        print('Managed Akasha/WeFlow stopped; WeChat remains open.')
    elif args.action in ('status','inspect'): print(json.dumps(status(cfg), ensure_ascii=False, indent=2))
    else:
        import requests
        r=requests.post('http://127.0.0.1:18766/control',json=dict(action=args.action,session=args.session),timeout=5)
        r.raise_for_status();print(json.dumps(r.json(),ensure_ascii=False))

if __name__=='__main__': main()
