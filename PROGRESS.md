当前实施：**WX-AKASHA-ALL active**，见[本次交接](tracks/tasks/WX-AKASHA-ALL/HANDOFF.md)；用户已提交完整实施指令，下方只规划描述为历史。

# WeChatbot项目入口

2026-10-31（Asia/Shanghai）。唯一根进度入口；Windows根E:/CodexWS/WeChatbot，独立于QQ，不另建根HANDOFF。

**当前主线：WeFlow → Akasha-WeChat → 现有AstrBot。WX-AKASHA-ALL已实施接线并部署QQ侧，微信账号向导/真实绑定待操作者完成，同任务继续。** 当前看[实施交接](tracks/tasks/WX-AKASHA-ALL/HANDOFF.md) / [报告](docs/WX-AKASHA-ALL-REPORT.md) / [使用入口](README.md)。[完整合同](docs/AKASHA-IMPLEMENTATION-PLAN.md)及[原规划交接](tracks/tasks/WX-AKASHA-01/HANDOFF.md)保留；不再提交一轮规划。禁止过度防御性编程。

计划包含账号/WeFlow准备、必要桥接协议修复、现有AstrBot跨平台路由、共用模型/人设、上下文、显式配对共享记忆、原生联网、当前图识别、受控表情/free/adaptive、成员与控制、管理界面、启动/恢复/回滚。缺原生@等能力用表内明确替代，不另留必需规划轮。

当前：固定Akasha运行副本及协议overlay、独立venv、WeFlow维护分支v5.0.1、单配置/管理/启停入口已交付；当前定向34＋微信组合6通过，CLI真实零生成配对完成。现有AstrBot已增量监听11229，原QQ恢复connected/ready；微信向导18108/面板18766已启动，尚未保存机器人账号/密钥及实际映射，未真实收发。不能把接线/检查写成微信已能聊天。

旧wxauto文字版保留。此前用户反馈启动恢复/测试OK是历史记录；随后真实日志出现CLI_START后PROTOCOL_ERROR，零生成握手确认CLI运行包缺模块，未修复。原离线检查不证明当前真实链路可用；现在按用户选择转Akasha，不再扩大旧路线投入。旧实现、检查报告、配置和未决记录均从对应交接读取。

微信Git只用main，origin为[hann-8/WeChatbot](https://github.com/hann-8/WeChatbot)。本轮起点938187c，已知规划与本次实现一同检查提交；QQ从42911af隔离实施后快进main并受管部署。两处Git/部署分别记录，秘密/数据/运行工件不发布。

| 工作线 | 状态 | 下一步/入口 |
| --- | --- | --- |
| WX-AKASHA-ALL 一次实施 | active；代码/检查与QQ侧受管部署完成，账号向导/映射待操作者，同任务继续 | [实施交接](tracks/tasks/WX-AKASHA-ALL/HANDOFF.md) / [报告](docs/WX-AKASHA-ALL-REPORT.md) |
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
