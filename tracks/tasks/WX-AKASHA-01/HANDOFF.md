# WX-AKASHA-01：Akasha一次完整规划

返回[PROGRESS](../../../PROGRESS.md) / [TASKS](../../../TASKS.md)，继承[AGENTS](../../../AGENTS.md)。

状态：completed，完整计划、唯一指令及最终文档QA完成；实现尚未领取。详细合同见[完整计划](../../../docs/AKASHA-IMPLEMENTATION-PLAN.md)，用户只提交[唯一sol/medium指令](MEDIUM_START.md)。用户最新明确把Akasha作为main，本轮准备好后写全基础和其他功能的一份详细方案＋一份sol/medium指令，由用户自行提交实施，不拆多轮、不再过度防御。用户已睡，继续独立规划；不再启动/改接线/微信/模型。起点main=938187c；本会话已知故障登记和新路线差异保留。

额度条件：用户指定5h剩余低于5%时保存并于北京时间2026-10-31 06:30续做。00:51账户实时primary=300分钟、usedPercent=87，即剩余13%，当时不满足暂停条件；不得擅用账户reset credit。后续长段工作前核对，触发时用当前chat的一次heartbeat续做，不能仅口头承诺定时醒来。

目标：通过现成WeFlow/Akasha接现有AstrBot，交付全部功能、依赖、薄补丁、部署/回滚的一份完整合同；上游原始副本保留，未来实施仅允许计划列明的有限桥接协议补丁，不修改第三方内核。共用AstrBot不自动保证共用QQ业务或记忆，需以当前provider/plugin/session实际配置为准，不伪造已经互通。

上游固定9dbe933a9f1bc46e33ca8121334bb1dd01173248。源码为WeFlow SSE→OneBot反向WS→AstrBot，出站用UIA键盘/剪贴板；默认Web管理只绑定127.0.0.1。上游main.py会自动启动桥接，不在缺少真实绑定/依赖时直接运行。

用户已明确答复“确认改用，目前没装WeFlow”，同意这条路线的本机数据库/密钥准备；AGENTS已相应更新。首期仍以机器人账号和已有指定群为目标，不自动合并QQ记忆或扩大群范围。上游自己的UIA发送会使用键盘/剪贴板，这是所选现成项目的实现，不再作为原“不另写脚本”的冲突。

已完成本地准备：上游源码9dbe933保持未修改；独立runtime/akasha-wechat/venv装好requirements及websockets15.0.1（实际additional_headers用法需要新asyncio接口，原>=12声明不足），pip check通过。真实配置只在忽略的上游config.json，管理页预选18766、AstrBot新WS11229，未运行桥接。

WeFlow原作者hicccc77/WeFlow当前releases为空；公开维护分支334456777/WeFlow提供5.0.1 Windows x64现成包，API文档保留5031 /api/v1/push/messages兼容形状。已下载11376812字节并与作者.sha256核对：8d88ca61c504c8d509fd7b6934e4d2261ba986f6a1e13df68c3732323e1b26fa；解压在runtime/akasha-wechat/weflow/weflow-v5.0.1-windows-x64。版本/帮助核对执行--version/serve --help，版本5.0.1/6115746；另曾启动下述首次配置服务，没有打开数据库或调用模型。

先前首次配置服务使用该副本普通serve/127.0.0.1:18108/WebUI0.4.1，WEFLOW_HOME限定runtime/akasha-wechat/weflow-home；令牌仅本机config/子进程环境，不输出。创建身份在state/akasha-wechat/weflow-setup-process.json。按最新“只规划”已核对pid/创建时间/路径并结束本会话自己的服务；不退出微信/QQ。未启动Akasha/连接AstrBot/模型请求，未读取微信数据库/密钥。实施时仍须用户一次完成机器人账号的WeFlow向导。

现有AstrBot只读事实：QQ平台aiocqhttp使用6199，provider_source是qqbot_openai→本机8765网关，通用AstrBot群LTM关闭；qq_router.on_group直接拒绝其他self/group。因此不能仅加WebSocket就宣称同一QQ机器人/记忆已复用。需给新平台单独路由，保留原QQ行为；实际修改现有AstrBot/QQ插件前补精确归属和必要定向验证。

本轮最终归属：AGENTS、PROGRESS、TASKS、README、docs/IMPLEMENTATION_GUIDE、docs/AKASHA-IMPLEMENTATION-PLAN、本交接、MEDIUM_START、WX-MIG-ALL/HANDOFF共9份文档；现有QQ运行链和AstrBot配置只读，应用代码没有修改。完整计划第11节列出未来同轮跨项目归属。

规划成果已涵盖全功能清单、Akasha确定性ID/源关联/真实本地发送结果/指定群过滤/精确图片补丁、AstrBot所有钩子的平台分派、provider复用、显式共享记忆、增强、单配置入口、必要组合检查与受管部署。用户下一步只需提交MEDIUM_START给sol/medium，实施创建WX-AKASHA-ALL交接，不新开规划轮。

最终QA见下方06:30续作结果；当前尚未真实连库/微信/模型收发，不声明可用。规划暂留main工作区，未commit/push；后续实施指令已明确收纳经检查的规划差异。


## 额度检查点 2026-10-31T01:11:26+08:00

账户实时primary usedPercent=96 / 300分钟，即5h剩余4%，触发用户“低于5%则2026-10-31 06:30am继续”的明确指令。现在停止实质工作，不使用账户reset credit。待同一chat一次heartbeat恢复，当前chat=01a18305-e5c3-71e0-9143-747d998a399c。

已写完整计划（约33KB）和唯一MEDIUM_START（约6KB），项目9份入口/交接文档已统一新路线；应用代码/QQ配置未改。尚未做最终QA，因此PROGRESS/TASKS内completed暂改为待QA。

06:30只做以下收尾，不另规划或实施：读取本交接和两份新工件；检查AGENTS与有限桥接补丁许可一致、原wxauto故障历史没有误当当前可用；检查9份文档UTF-8/LF、围栏、本地链接/双向入口、git diff --check和秘密/归属；修必要的文档问题；确认QQ源无改动；回写QA结果与completed。无需业务测试，不启动WeFlow/Akasha/模型/微信。Git不新增发布授权，本轮规划留main工作区，后续medium指令已授权同实现收纳。最后向用户交付计划与唯一指令的绝对路径链接，讲清未实施。

已通过Codex automation_update实际创建并view核对：id=akasha，kind=heartbeat，ACTIVE，目标为本chat；每日06:30、COUNT=1（本机Asia/Shanghai，下一次即2026-10-31 06:30）。本机automation.toml已读回确认，无重复既有任务；API未提供nextRun字段。恢复收尾后核对一次调度已耗尽，不另建周期任务。


## 06:30续作登记

2026-10-31T06:31:26+08:00，负责人仍为本会话Codex，只续WX-AKASHA-01文档收尾，原9份归属不变。已重读项目入口和两份工件；当前main保持，QQ源42911af且工作区干净。额度自然刷新后剩余94%，未使用reset credit；最终QA进行中。


## 最终交付 2026-10-31T06:32:17+08:00

WX-AKASHA-01 completed。9份归属文档检查通过：UTF-8无BOM/LF、Markdown围栏/表格、90个本地链接、PROGRESS对12份HANDOFF的索引、当前交接双向入口、计划与唯一指令的任务/平台/记忆/工具约定一致；git diff --check通过，常见秘密模式未命中。差异严格为登记的9份Markdown，无应用代码改动，未运行业务测试。

已再次核对QQ源main=42911afc4c1f2bcfbbc3c26afc2647fd21992f08，工作区干净；没有改QQ配置/运行实例。微信仍main，规划未commit/push，忽略的本地准备保留；未运行WeFlow/Akasha/模型/微信，未读库/密钥或发送。

本次06:30一次续做已完成，automation_update(mode=delete,id=akasha)实际返回deleteStatus=deleted；自动化已删除，不再调度。下一步由用户复制MEDIUM_START整段给gpt-6.1-sol/medium，一次领取WX-AKASHA-ALL并按计划落地全部已列功能，然后用户自然实测；本规划会话到此结束。
