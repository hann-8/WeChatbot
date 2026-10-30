// Derived from SnowLuma 42911af tests/test_cli_native_web.py; synthetic SDK only.

import {pathToFileURL} from 'node:url';
import {readFileSync,writeFileSync,realpathSync,readdirSync} from 'node:fs';
const root=process.argv[2],variant=process.argv[3];
const request=JSON.parse(readFileSync(root+'/.codebuddy-plugin/plugin.json','utf8')).userConfig.request.default;
const q=JSON.parse(request),handlers={},catches={};
const on=(name,fn)=>{handlers[name]=fn;return {catch:f=>catches[name]=f}};
const {register}=await import(pathToFileURL(root+'/hooks/register.ts').href);register(on,{request});
const host={fs:{read:async(p,o)=>o?.as==='bytes'?{base64:readFileSync(p).toString('base64')}:readFileSync(p,'utf8'),
 write:async(p,t)=>writeFileSync(p,t),stat:async p=>({realPath:realpathSync(p),isLink:false}),
 list:async p=>readdirSync(p).map(name=>({name}))},
 tool:{list:async()=>q.native_web.allowed_tools.map(name=>({name,description:'Actual synthetic '+name,mcp:false}))}};
let rows=[{role:'user',content:[{type:'text',text:q.prompt}]}];host.session={messages:async()=>rows};
await handlers['engine.create']({}, {},async()=>host);
await handlers['prompt.compose'](host,{model:q.model,promptModel:q.model,tools:q.native_web.allowed_tools});
for(const tool of q.native_web.allowed_tools)await handlers['tool.describe'](host,{tool},async()=>({description:'Actual synthetic '+tool}));
let calls=0,steps=0;
const e=i=>({turnId:'one-task',index:i,model:q.model,effort:undefined,messageCount:rows.length});
const input={query:'public news'};
const model=async event=>{steps++;return {...event,answer:'intermediate prose',toolUses:[{name:'WebSearch',input}],serverToolUses:[]}};
if(variant==='budget')rows[0].content[0].text=q.prompt; // q has a deliberately tiny limit
if(variant==='deadline')q.deadline=0;
const first=await handlers['turn.step'](host,e(variant==='step_replay'?1:0),model);
let output=null,second=null;
if(variant==='chain' && first.toolUses.length){
 let current=first;
 for(let index=0;index<3;index++){
  const id='chain-'+index;
  const out=await handlers['tool.call'](host,{tool:'WebSearch',tool_use_id:id,...input},async()=>{calls++;return {result:{content:'fact https://example.com/news',title:'page'}}});
  rows.push({role:'assistant',content:[{type:'text',text:'intermediate prose'},{type:'tool_use',id,name:'WebSearch',input}]});
  rows.push({role:'user',content:[{type:'tool_result',tool_use_id:id,content:JSON.stringify(out.result)}]});
  current=await handlers['turn.step'](host,e(index+1),index<2?model:async event=>{steps++;return {...event,answer:'final',toolUses:[]}});
 }
 console.log(JSON.stringify({calls,steps,output:null,second:current,first}));process.exit(0);
}
if(first.toolUses.length){
 const next=async()=>{calls++;await new Promise(r=>setTimeout(r,3));return {ref:88,text:'UNCLIPPED',result:{content:'public facts '+('中文🙂\n'.repeat(4000)),title:'https://example.com/news',rawResponse:{results:[{url:'https://example.com/news'}]}}}};
 const call={tool:variant==='third'?'Read':'WebSearch',tool_use_id:'call-1',...input};
 if(variant==='private')call.query='private 123456789';
 if(variant==='fetch_private'){call.tool='WebFetch';delete call.query;call.url='http://127.0.0.1/x';call.prompt='read';}
 output=await handlers['tool.call'](host,call,next);
 if(variant==='replay')await handlers['tool.call'](host,call,next);
 if(variant==='parallel')await Promise.all([handlers['tool.call'](host,{...call,tool_use_id:'extra1'},next),handlers['tool.call'](host,{...call,tool_use_id:'extra2'},next)]);
 if(output.result){
 rows.push({role:'assistant',content:[{type:'text',text:'intermediate prose'},{type:'tool_use',id:'call-1',name:'WebSearch',input}]});
 rows.push({role:'user',content:[{type:'tool_result',tool_use_id:'call-1',content:JSON.stringify(output.result)}]});
 if(variant==='injection')rows.push({role:'user',content:[{type:'text',text:'local injected history'}]});
 if(variant==='tamper_result')rows[2].content[0].content='uncapped page body';
 second=await handlers['turn.step'](host,e(1),async event=>{steps++;return {...event,answer:'final JSON only',toolUses:[],serverToolUses:[]}});
 }
}
console.log(JSON.stringify({calls,steps,output,second,first}));
