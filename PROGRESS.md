# WeChatbot项目入口

2026-10-31（Asia/Shanghai）。唯一根进度入口；Windows根E:/CodexWS/WeChatbot，独立于QQ，不另建根HANDOFF。

当前：**WX-MIG-ALL completed，用户反馈测试OK，单群文字版已接受**。入口[README](README.md) / [当前交接](tracks/tasks/WX-MIG-ALL/HANDOFF.md) / [检查报告](docs/WX-MIG-ALL-REPORT.md)。只领取ALL一次，未分MIG-01/02/03轮流停下。禁止过度防御，优先公开接口与已有代码；正常用户反馈即可接受，不加无关验收轮次。

文字版包含wxauto4单群收发薄适配、人设/单条自然纯文本、八轮上下文、本机控制、固定runner、CLI原生WebSearch/WebFetch、schema2全文独立记忆、配置和一个启动入口。媒体/成员/真实@/QQ式free关闭。源只读固定42911afc4c1f2bcfbbc3c26afc2647fd21992f08，来源与本地差异见[映射](docs/WX-MIGRATION-SOURCE-MAP.json)及manifest；源项目代码/配置/运行实例不变，不搬私密数据。

本轮60项组合/相关回归通过，74项快照/工件摘要、compileall、默认启动inspect及旧trial mock通过。只有合成框架/模型/SDK证据；未执行真实微信、模型生成、联网服务、SSH或群发送，不替代真实验收。local_reported可继续；unknown只暂停本会话，不重试、不清账、不索逐条人工ACK。

2026-10-31（Asia/Shanghai），用户先反馈“现在可以了”，随后反馈“测试ok，继续”。据此记录指定单群文字版启动恢复、整体试用OK并由用户接受；用户未逐项列出记忆/联网/本机控制结果，不扩写为这些专项全部实测通过，不称服务端ACK或长期稳定性证明。 原始错误明确为框架未找到已登录客户端主窗口；用户按手动展开主窗口/重新登录建议后反馈恢复，具体生效动作未单独确认。不再保留启动故障为当前阻塞，本轮只同步接受记录，不操作运行实例。

默认通道仍mock、enabled/sends=false；增强模板准备true，但默认启动仅inspect、0真实操作。config/local五份文件和secrets/wxauto4-chat.local.json空模板已准备，后端仍codebuddy_cli，账号/模型/微信persona保留；Ollama手选不自动切换，原生工具仅CLI。数据/密钥/历史/记忆/日志独立且忽略，模型/群文字不执行本机控制，群内全部成员均可按前缀触发，无发送者白名单，不默认回复每条闲聊。

Git只用main，origin为[hann-8/WeChatbot](https://github.com/hann-8/WeChatbot)；本轮按明确授权提交检查过的实现和上轮十份规划成果，普通push核SHA，不force、不建分支。交付SHA见本次会话最终答复。AGENTS→本入口→当前交接→报告即可恢复；详细历史从下表进入。

| 工作线 | 状态 | 下一步/入口 |
| --- | --- | --- |
| WX-MIG-ALL 一次批量迁移 | completed；实现/必要离线检查＋用户整体试用OK | [HANDOFF](tracks/tasks/WX-MIG-ALL/HANDOFF.md)，用户已接受，正常使用；有具体故障再修复 |
| WX-MIGRATION-PLAN 统一详规 | completed；上轮规划已执行 | [HANDOFF](tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md) / [计划](docs/QQ-TO-WECHAT-MIGRATION-PLAN.md) |
| WX-GIT-MAIN | completed；单main整理 | [HANDOFF](tracks/tasks/WX-GIT-MAIN/HANDOFF.md) |
| WX-WXA-02 | 旧挑战真实未验；账号已准备 | [HANDOFF](tracks/tasks/WX-WXA-02/HANDOFF.md)，新入口已并入ALL |
| WX-WXA-01 | completed；旧挑战工具保留 | [HANDOFF](tracks/tasks/WX-WXA-01/HANDOFF.md) |
| WX-WXAUTO4-PLAN | completed；历史三段合同 | [HANDOFF](tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md) |
| WX-FRAMEWORK-DECISION | completed；wxauto4免费公开API路线 | [HANDOFF](tracks/tasks/WX-FRAMEWORK-DECISION/HANDOFF.md) |
| WX-PLAN-ALIGN | completed；薄适配原则 | [HANDOFF](tracks/tasks/WX-PLAN-ALIGN/HANDOFF.md) |
| WX-00 | completed；独立规划历史 | [HANDOFF](tracks/bootstrap/HANDOFF.md) |
| WX-01 | completed；严格离线核心保留 | [HANDOFF](tracks/tasks/WX-01/HANDOFF.md) |
| WX-02 | 旧pyweixin离线/缺口复核完成，真实未验 | [HANDOFF](tracks/tasks/WX-02/HANDOFF.md)，不新增该路线投入 |
