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

// The locked build's actual dispatchModsToolCall, extracted without booting CLI.
const {dispatchModsToolCall}=await import(pathToFileURL(process.argv[4]).href);
const fetch=variant.startsWith('fetch'),parallel=variant.includes('parallel');
const tool=fetch?'WebFetch':'WebSearch';
const inputs=Array.from({length:parallel?2:1},(_,i)=>fetch?
 {url:'https://example.com/news/'+i,prompt:'Read public facts'}:{query:'public news '+i});
if(variant==='fetch_http')inputs[0].url='http://example.com/news';
if(variant==='fetch_numeric_url')inputs[0].url='https://example.com/app/2358720';
if(variant==='fetch_private_numeric_url')inputs[0].url='https://example.com/profile/987654321';
if(variant==='fetch_numeric_prompt')inputs[0].prompt='Read profile 123456789';
if(variant==='search_url')inputs[0].query='public facts https://example.com/news';
if(variant==='search_drive')inputs[0].query='read C:/private.txt';
if(variant==='search_backslash')inputs[0].query='read C:\\private.txt';
if(variant==='search_unc')inputs[0].query='read \\\\server\\share';
if(variant==='search_private_id')inputs[0].query='look up 123456789';
const errors=[],outputs=[],events=[];
let calls=0,steps=0,early=[];
const invoke=async(input,i)=>{
 const id=(variant.includes('wrong_id')?'intruder-':'sdk-call-')+i;
 try {
  let wireInput=variant.includes('json')?JSON.stringify(input):input;
  if(variant==='fetch_invalid_json')wireInput='{';
  if(variant==='fetch_array_json')wireInput='[]';
  if(variant==='fetch_null_json')wireInput='null';
  const result=await dispatchModsToolCall({name:tool,callId:id,input:wireInput},async received=>{
   if(JSON.stringify(received)!==JSON.stringify(wireInput))throw Error('ARGUMENTS_CHANGED');
   calls++;
   if(variant==='fetch_sdk_error')throw Error('URL redirected to different host; use the redirect URL');
   return {content:'public fact https://example.com/news/'+i,title:'Public page'};
  },{dispatch:async(name,event,options)=>{
   events.push(event);
   if(variant.includes('conflict'))event.input={...input,prompt:'tampered'};
   return handlers[name](host,event,options.coreResult);
  }},variant.includes('flat'));
  outputs[i]={id,input,result};
 } catch(error){
  errors.push(String(error));
  if(variant==='fetch_sdk_error')outputs[i]={id,input,is_error:true,
    result:{content:'Error: '+String(error),error:String(error)}};
 }
};
const e=i=>({turnId:'one-task',index:i,model:q.model,messageCount:rows.length});
const first=await handlers['turn.step'](host,e(0),async event=>{
 steps++;
 if(variant.includes('race'))early=inputs.map(invoke);
 if(variant.includes('session_plan'))rows=rows.concat([{role:'assistant',content:[{type:'text',text:'model preamble'},
   ...inputs.map((input,i)=>({type:'tool_use',id:'sdk-call-'+i,name:tool,input}))]}]);
 return {...event,answer:'',toolUses:variant.includes('session_plan')?[]:inputs.map(input=>({name:variant.includes('badplan')?'Read':tool,input})),serverToolUses:[]};
});
await Promise.all(variant.includes('race')?early:inputs.map(invoke));
for(const out of outputs.filter(Boolean)){
 if(!variant.includes('session_plan'))rows.push({role:'assistant',content:[{type:'tool_use',id:out.id,name:tool,input:out.input}]});
 rows.push({role:'user',content:[{type:'tool_result',tool_use_id:out.id,content:JSON.stringify(out.result),is_error:!!out.is_error}]});
}
const second=await handlers['turn.step'](host,e(1),async event=>{
 steps++;return {...event,answer:'final',toolUses:[],serverToolUses:[]};
});
console.log(JSON.stringify({calls,steps,errors,second,outputs,events,first}));
