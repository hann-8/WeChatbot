# WX-AKASHA-ALL：一次完整落地的 sol/medium 指令

返回[规划交接](HANDOFF.md) / [PROGRESS](../../../PROGRESS.md) / [完整计划](../../../docs/AKASHA-IMPLEMENTATION-PLAN.md)。用户在 gpt-6.1-sol/medium 会话复制下方整段；当前规划会话不实施。

```text
请只领取WX-AKASHA-ALL，完整执行docs/AKASHA-IMPLEMENTATION-PLAN.md，在一次实施session里把Akasha/WeFlow作为微信main路线落地到现有AstrBot。基础和其他已列功能都在本次范围，最终交我实测。严禁过度防御性编码；不要拆多次规划/多阶段审批，不要只做环境或文字后停止，也不要再交一份实施计划。

先读微信根AGENTS/PROGRESS/TASKS、WX-AKASHA-01/HANDOFF和完整计划；涉及QQ根时读E:/CodexWS/QQbot_Snowluma的AGENTS/PROGRESS/主线HANDOFF/TASKS。两根同一个WX-AKASHA-ALL登记负责人、时间、精确归属并重读，创建实施HANDOFF及双向入口。保留本轮已知规划/准备成果和其他用户修改。原WeChat main起点938187c，QQ核对源42911af；开工重查实际HEAD，不重置用户或其他session变化。不要动旧NapCat根E:/CodexWS/QQbot。

用户明确选用现成alingalingling/Akasha-WeChat，并允许WeFlow本机读机器人微信账号数据库/密钥，不重复问意愿。原版上游已在runtime/akasha-wechat/upstream，固定9dbe933a9f1bc46e33ca8121334bb1dd01173248；独立venv/依赖已准备。WeFlow选用公开维护分支334456777/WeFlow v5.0.1 Windows x64，已下载并校验发布sha，--version/--help成功；这不是原作者官方安装包，不改解密/登录内核。先前向导进程已由规划方按身份停止，未读微信库/密钥、未真实收发。你同轮处理向导18108和桌面API/SSE5031、配置/取钥保存与启动入口，操作者正常配合账号选择/系统授权/登录；密钥/token只放忽略的本机目录，不输出或上传，不删除微信聊天数据。

主链必须是WeFlow公开消息/媒体API与SSE→Akasha薄桥接→现有AstrBot独立akasha-wechat平台/127.0.0.1:11229/ws→现有QQ自有业务/现有provider和模型网关→Akasha UIA回源。原QQ6199、Snow通道、账号/模型/权限和运行数据保留，不新写第二套LLM客户端，不再修/使用微信旧残缺CLI包，不复制QQ凭据/记忆库。

按计划第6节在固定运行副本做必要、可审阅的桥接层小补丁：确定性bot/user/group ID、完整message_id及原消息/成员/媒体关联、指定会话前置过滤、发送实际结果后才回OneBot结果、失败/unknown不重试、日志不漏token或原文。上游实际有Python hash不稳定、缺源关联、发送前回成功、忽略sender bool、最新图错绑、正文@伪装At等问题，不能只靠README认定可用。只修这类接点，不重写UIA/WeFlow/AstrBot内核，不建全面私有fork。

现有qq_router会stop非QQ事件，provider/装饰/出站钩子也有QQ栅栏，不能仅加端口。给自有插件做transport-aware分派，QQ原逻辑保持；微信按注册平台/真实绑定/来源走自己的入口，复用当前模型/人设、业务函数和队列。必要gateway profile或v2协议兼容小改同轮完成，不制造QQ可信身份/票据，不绕QQ权限。每次只回源平台，不做QQ微信群原文互转或群发。

本批全部接好：自然文字/同源角色；短期上下文；mention文本唤醒、all入站由bot/free/叫名/续聊判断、batch；schema2全文记忆/模型同次增改删/真实保存回执；原生WebSearch/WebFetch；精确当前消息识图；受控表情/adaptive；公开成员增强；实际可用时的原生@；本机/可信owner控制；Web管理/单配置入口/启动停止/普通断连恢复。私聊独立显式开关默认关。语音/视频/任意文件/B站退役分支按表准确关闭/提示，不新增ASR/TTS或付费API；无原生@/动图能力则明示实际替代，不因此卡住基础或留下另一轮规划。

共享模型和人物正文可以同源，共享记忆必须由本机pairings明确选定微信群↔QQ会话和actor_links，不凭同名合人/合群。facts_only和shared_context两种scope、未配对独立空间本批实现；操作者同轮选一次真实映射，不在公开文档写实际ID。共用现有MemoryStore服务，不复制key/库，reset只清短期。记忆全文、增改删、原子写和准确回执完整接线；网页材料不学进人类事实。

保留现有deepseek-v4.1-flash/low、thinking=false、524288可见UTF-8输入政策及当前reserves/历史配置；家庭Ollama手选不自动切换、不读家庭凭据。一次消息一个CLI任务，原生仅两工具/3调用/4步骤/90秒/单8000总12000字节，其余工具/MCP关。图文同轮，不再默认额外llava/caption模型。只裁完整历史，不截当前请求/记忆；不为旧小门槛删角色。源QQ现有识图/表情/free/记忆不能被静默关闭。

同轮完成完整计划第13节必要组合检查、实际可执行的模型零生成握手和配置/连接状态检查。普通依赖/格式/桥接错误自己修好，不回到规划；不补全库/72h/旧IQ矩阵。确实改QQ源影响native/vision技术绑定时，沿已有revalidate_lap43_native_web.py check/probe/activate，用当轮实际expected-binding/active和authorize-operator-trial同轮配对，不能抄旧摘要或停下来再索部署授权。

本指令授权本计划列明的依赖/配置/自有插件/必要薄补丁和受管部署；只启停有身份的项目进程，不退出/注销微信，不按进程名kill。操作者必须完成的登录/取钥/映射只让其做那个具体动作，之后在同一任务继续。不要主动反复真实生成/联网/发群样本；我在已选群自然实测即可。不能把inspect/初始化OK当模型已回复或用户已见消息。

最后交付可用主线、一套Start/Stop/Status和配置入口、README/能力表、必要检查/部署报告、HANDOFF/PROGRESS/TASKS。只提交审阅的本任务实现和已知规划文件；微信只main，QQ按其规则同轮合入main，普通push核远端SHA，不force，不夹带秘密/本机数据或他人差异。两根Git/部署分别报告。完成后交我实测，正常就接受；有具体故障继续本任务修，不追加新的规划轮。
```
