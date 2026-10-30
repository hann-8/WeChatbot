# WX-MIG-ALL：一次批量迁移medium指令

返回[规划交接](HANDOFF.md) / [PROGRESS](../../../PROGRESS.md) / [统一计划](../../../docs/QQ-TO-WECHAT-MIGRATION-PLAN.md)。本文件供用户在medium会话提交；当前规划会话不实施。

```text
请只领取WX-MIG-ALL，按docs/QQ-TO-WECHAT-MIGRATION-PLAN.md一次完成微信可用文字版的批量迁移、配置和启动入口，完成后交我实测。不要分MIG-01/02/03轮流停下等指令。禁止过度防御性编程，优先公开接口、现有代码和必要的小适配。

先读AGENTS、PROGRESS、TASKS、WX-MIGRATION-PLAN/HANDOFF、统一计划和WX-MIGRATION-SOURCE-MAP.json。当前微信main规划起点33c18f0；工作区规划文档是上轮已知成果，保留并审阅，不覆盖其他修改。登记本任务负责人/时间/文件，建立WX-MIG-ALL/HANDOFF及双向入口，写后重读。

来源只读E:/CodexWS/QQbot_Snowluma的42911afc4c1f2bcfbbc3c26afc2647fd21992f08（规划时本地/远端一致）。按固定提交更新所需QQ共用模块与导入，不全量复制/启动源项目；带最新原生联网参数封套/HTTP(S)修复、thinking=false及LAP-44 schema2记忆。保留微信自己的相对Node/CLI路径和注入替身接点；补三份codebuddy_vision_guard资产、公开framework审阅字段、锁定types/codebuddy-code.d.ts。不要复制QQ配置、账号、实际persona覆盖层、历史/记忆/图库/家庭凭据/active或probe。

一次接通：wxauto4公开ChatInfo/GetAllMessage/SendMsg薄适配；一个指定群/全体群成员可触发（黑名单除外）/文本唤醒；人设与单条自然纯文本；8轮短期上下文；本机status/pause/resume/reset/stop；固定CodeBuddy任务；WebSearch/WebFetch；schema2会话独立记忆和真实保存回执。旧挑战工具和严格mock入口保留，不造生产NormalizedEvent或真实@资格，不新建AstrBot/OneBot桥接或另一套模型客户端。

按计划准备CLI deepseek-v4.1-flash/low、alwaysThinkingEnabled=false、524288可见UTF-8字节政策、overhead/output各2048、context_window_tokens=null。修掉8000字符角色门槛及131072旧政策封顶，最终wire预算校验；不擅自删人设。web限3工具/4步骤/90秒/单8000合计12000字节，其余工具和MCP关闭。memory/learning准备true、每会话50000 Unicode字符/文件1048576/总8388608，可配置扩大；用源MemoryStore全文/同次增改删，不回到旧关键词/小候选方案。保留实际后端/账号；若本机已选Ollama则不自动切换，说明原生工具仅CLI可用。

明确的wxauto成功只记local_reported并继续，不要求逐条人工ACK；真实发送不明才暂停该会话，不重试/清账。模型/群文本不执行本机控制；不默认全群回复。只裁完整短期历史，不裁当前请求/全文记忆。源QQ协议只复用业务纯函数，微信所需语义用小包装，不伪造QQ号或可信ID。

我已登录微信4.2.0.11，首试一个指定群，也接受更换能配套的客户端，不要重复问换版意愿。免费wxauto4当前公开支持配套为41.1.7＋微信4.1.8.107；同轮准备依赖、已有安装包/必要工件和简明换版说明。退出/正常安装/登录由我完成，不自动卸载数据、操作微信/安装UI或kill进程；不要把安装器4.1.8.1000/4.1.8.0的元数据差异当永久拒绝条件。真实群名/黑名单只填本机secrets，不写报告/提交。

交付一个启动入口和一个本地绑定文件模板，默认不开真实通道/发送；我显式启动live后才实际操作。你同轮做计划第10节必要静态/定向替身检查，普通缺依赖/接线问题自己修好；不展开全库/长稳/生产级证明矩阵，不做真实微信/模型/联网服务/群发验收。媒体、成员、真实@、free未接通先关闭，不影响文字版交付。

完成后更新README、任务报告、HANDOFF/PROGRESS/TASKS，明确已实现/必要检查结果/待我实测/仍需我完成的具体客户端动作。仅提交检查过的本任务实现及上轮规划文档，普通push main并核远端SHA，不force、不建分支；源项目不变。交付后停止，由我实测，正常就接受，不另加无关验收轮次。
```
