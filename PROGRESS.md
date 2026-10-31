当前实施：**WX-AKASHA-ALL ready_for_user_test**，见[本次交接](tracks/tasks/WX-AKASHA-ALL/HANDOFF.md)；用户已提交完整实施指令，下方只规划描述为历史。

2026-10-31实测续修：用户实报无回复，并指出双账号时自动化实际落在大号、大号随后退出。已停桥接，修正UIA对象跨线程接点，新增操作者显式窗口/进程身份绑定及联系人切换结果检查；当前机器人窗口已绑定，SSE/WS恢复。依据用户“未收到”反馈归档旧unknown，仅恢复新消息，不补发旧结果；再次群测待反馈。今后换号/重开机器人微信：只保留机器人窗口，执行bind-window后start。

# WeChatbot项目入口

2026-10-31（Asia/Shanghai）。唯一根进度入口；Windows根E:/CodexWS/WeChatbot，独立于QQ，不另建根HANDOFF。

**当前主线：WeFlow → Akasha-WeChat → 现有AstrBot。WX-AKASHA-ALL实施/部署完成，WeFlow/Akasha/现有AstrBot实际连接正常，交用户在原指定群自然实测；具体故障继续同任务。** 当前看[实施交接](tracks/tasks/WX-AKASHA-ALL/HANDOFF.md) / [报告](docs/WX-AKASHA-ALL-REPORT.md) / [使用入口](README.md)。[完整合同](docs/AKASHA-IMPLEMENTATION-PLAN.md)及[原规划交接](tracks/tasks/WX-AKASHA-01/HANDOFF.md)保留；不再提交一轮规划。禁止过度防御性编程。

计划包含账号/WeFlow准备、必要桥接协议修复、现有AstrBot跨平台路由、共用模型/人设、上下文、显式配对共享记忆、原生联网、当前图识别、受控表情/free/adaptive、成员与控制、管理界面、启动/恢复/回滚。缺原生@等能力用表内明确替代，不另留必需规划轮。

当前：代码/单配置/管理/启停入口已交付，34＋6项当前组合与CLI真实零生成配对通过。用户已在WeFlow保存机器人账号/密钥，原指定群已唯一匹配；用户保存facts_only及1条明确actor_link。WeFlow连库/SSE、Akasha→11229 WS、UIA初始化、gateway/router_ready和当前配置摘要核对正常；原QQconnected/online/ready，local/persona/provider不变。未代用户主动真实生成/发群样本，启动核对时local_reported=0；群聊效果待用户实测，不把连接状态冒充用户已看见回复。

旧wxauto文字版保留。此前用户反馈启动恢复/测试OK是历史记录；随后真实日志出现CLI_START后PROTOCOL_ERROR，零生成握手确认CLI运行包缺模块，未修复。原离线检查不证明当前真实链路可用；现在按用户选择转Akasha，不再扩大旧路线投入。旧实现、检查报告、配置和未决记录均从对应交接读取。

微信Git只用main，origin为[hann-8/WeChatbot](https://github.com/hann-8/WeChatbot)。本轮起点938187c，已知规划与本次实现一同检查提交；QQ从42911af隔离实施后快进main并受管部署。两处Git/部署分别记录，秘密/数据/运行工件不发布。

| 工作线 | 状态 | 下一步/入口 |
| --- | --- | --- |
| WX-AKASHA-ALL 一次实施 | ready_for_user_test；全部接线/必要检查/两侧部署完成，真实连接正常，群聊效果待用户反馈 | [实施交接](tracks/tasks/WX-AKASHA-ALL/HANDOFF.md) / [报告](docs/WX-AKASHA-ALL-REPORT.md) |
| WX-AKASHA-01 一次完整规划 | completed；完整方案/唯一medium指令已交付，尚未实施 | [HANDOFF](tracks/tasks/WX-AKASHA-01/HANDOFF.md)，用户提交WX-AKASHA-ALL后一次落地 |
| WX-MIG-ALL 旧wxauto文字版 | 历史实现/离线通过；后续真实CLI缺模块未修，路线已替代 | [HANDOFF](tracks/tasks/WX-MIG-ALL/HANDOFF.md)，保留代码/配置/历史，不继续扩修 |
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
