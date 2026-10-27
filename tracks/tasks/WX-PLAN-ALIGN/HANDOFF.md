# 微信架构说明与框架迁移原则

返回[PROGRESS](../../../PROGRESS.md) / [TASKS](../../../TASKS.md)。继承[AGENTS](../../../AGENTS.md)；架构依据见[PLAN](../../../docs/PLAN.md)。

状态：架构说明与框架迁移原则整理完成，仅文档，未实施。session `WX-PLAN-ALIGN-20261025`；负责人本会话 Codex，2026-10-25 12:03（Asia/Shanghai）开始。只领取本项说明/约束整理，未领取 WX-03。

## 目标、范围与检查点

用户先了解当前 WeChatbot 框架，并说明 QQ 从 NapCat 换 SnowLuma 时曾因 agent 追求功能复刻而长时间改写框架内部。用户要求避免重演：优先框架本身的稳定收发与公开接口，允许暂时舍弃不适配功能，再在项目侧逐步适配。

本项只澄清当前实际分层并记录该原则；不决定新的微信框架或是否改用 AstrBot，不重写已有离线代码。成功标准：能分清现有实现、用户期望的复用方向与尚未选择的接入路线；后续 agent 不会把旧功能或旧计划理解为改写第三方框架的授权。

起始 `codex/bootstrap` HEAD=`a66319d`，工作区干净，`git remote -v` 无输出。文件归属仅 AGENTS、PLAN、PROGRESS、TASKS 与本交接。保留其他 session/用户修改；本项不提交、不推送。

计划：核对现有文档/接口；记录框架迁移约束和架构差异；复读差异、检查本地链接及文档格式。真实 UI/登录/收发/模型/安装和 QQ 项目写入均不在本项范围。

## 已核对的现状

- 现有微信路线是候选 TransportAdapter → Gate → 自有轻量 Router → ModelFacade/固定 QQ runner 源码快照 → CodeBuddy CLI 或手选 Ollama；出站由投递层回到 adapter。PLAN 第2节明确没有接 AstrBot；README 与 router/model_facade 源码一致。
- WX-01 是离线核心，WX-02 是候选探针与缺口报告。真实通道/模型仍关闭；pyweixin 是验证候选，不能写成已选定、已接通或长期稳定。
- QQ 只读参考的 LAP-40 计划描述 SnowLuma → 项目 gate → AstrBot/qq_router → 模型，说明用户对 QQ 层次的理解大方向成立；该文档仍记“规划”，不能据此否认用户报告的迁移现状，也没有据此验证 QQ 当前运行状态。

## 完成与验证

AGENTS 与 PLAN 已同步公开接口优先、项目侧薄适配、允许功能延期/舍弃、不得自行改写框架核心的用户原则；PROGRESS/TASKS 已同步现状。保留既有离线代码和身份/授权/黑名单/unknown边界，不把现有代码变成未来选型前提。

五份归属文档写后重读；43个本地链接、配对代码围栏和PROGRESS/TASKS与本交接的双向链接检查通过，`git diff --check`通过。差异仅上述五份文档；没有新业务测试结果，70项仅为历史离线结果。未提交/推送，HEAD仍为起始检查点；QQ项目只读，未核验其当前运行状态。

后续第一步：用户明确发起接入任务后，先按最小原生收发能力和公开接口评估框架及AstrBot/既有模型层的复用，不预设pyweixin或自有Router。旧WX-02 provider计划不是必做项；不自动安装、观察、发送、调用模型或领取 WX-03。
