# WeChatbot项目入口

当前任务：2026-10-27 `WX-WXAUTO4-PLAN-20261027` 已完成[详细计划](docs/WXAUTO4-IMPLEMENTATION-PLAN.md)与[medium指令](docs/IMPLEMENTATION_GUIDE.md)，11份文档复读、99个本地链接/围栏/双向入口与diff检查通过；只规划、不实施，未重跑业务测试。当前交接为[WX-WXAUTO4-PLAN](tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md)，文件归属和Git起点见[TASKS](TASKS.md)。

2026-10-27（Asia/Shanghai）。唯一根进度入口，不另建根 HANDOFF。位置 `E:\CodexWS\WeChatbot`，独立于 QQbot。

目标：个人微信与朋友家人聊天，复用显式 CodeBuddy/家庭 Ollama 两路线，账号/配置/历史/清理独立。当前 **WX-01 核心及 WX-02 代码/离线范围完成，历史70项离线通过；真实能力全部未验，未部署**。本次文档整理未重跑测试。

当前路线：wxauto4免费版41.1.7＋微信4.1.8.107，公开API→薄封装→单会话人工监督试用→本项目固定runner→CodeBuddy。首期暂不加AstrBot，不连接QQ实例。用户自报4.1.15.13并已接受换版，不再询问换版意愿；实际更换尚未执行。依据为[26日选型](tracks/tasks/WX-FRAMEWORK-DECISION/HANDOFF.md)和[27日详细计划](docs/WXAUTO4-IMPLEMENTATION-PLAN.md)。WeChatFerry留作备选，不自行改写任何上游核心。

下一推荐只领取 **WX-WXA-01**，完成最小试用工具/可选包及离线验证后停止；WX-WXA-02另做配套客户端和一个指定会话的文字试验（0模型），WX-WXA-03另接一次CLI。三项均未领取。已有严格离线Gate不直接放开，试用明确记录UI昵称/临时ID与本地结果，不伪造生产身份、真实@或服务端ACK。

最新用户原则：个人娱乐先能用，现成公开接口和少量项目适配优先，不限定注入，允许功能延期或舍弃；不得为复刻QQ功能自行改写框架核心或维护私有fork。缺完整消息ID/@/服务端ACK先标限制，不一律否决人工监督的单会话试用，也不伪造能力。真实群触发/对象动作仍待具体规划，当前没有实施；详见[AGENTS](AGENTS.md)和[PLAN第2节](docs/PLAN.md)。

前次WX-02文档复核：`WX-02-gap-review-plan-20261023`（2026-10-23 20:02起，Asia/Shanghai）完成[缺口复核与后续详细计划](docs/WX-02-REVIEW-AND-PROVIDER-PLAN.md)，未实施、未重跑测试、未领取 WX-03。建议停止以当前固定上游推进生产；可选一次隔离UI元数据观察需另批代码/离线与指定对象真实观察，不是必须实施的步骤。归属与Git核对见 [TASKS](TASKS.md)。

阅读顺序：[AGENTS](AGENTS.md)→本入口→[当前交接](tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md)→[TASKS](TASKS.md)→[详细计划](docs/WXAUTO4-IMPLEMENTATION-PLAN.md)→[medium指令](docs/IMPLEMENTATION_GUIDE.md)。历史依据：[PLAN](docs/PLAN.md)、[RESEARCH](docs/RESEARCH.md)、[README](README.md)、[离线报告](docs/WX-01-OFFLINE-REPORT.md)。

| 工作线 | 状态 | 下一步 | 交接 |
| --- | --- | --- | --- |
| WX-WXAUTO4-PLAN 详细实施规划 | completed，仅文档；校验通过 | 首推WX-WXA-01；三项不自动串行实施 | [HANDOFF](tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md) |
| WX-FRAMEWORK-DECISION 框架选型 | 26日续作completed，仅文档；已补版本答复 | wxauto4免费＋微信4.1.8.107；用户已接受换版，后续进入明确实施任务 | [HANDOFF](tracks/tasks/WX-FRAMEWORK-DECISION/HANDOFF.md) |
| WX-PLAN-ALIGN 架构说明/框架迁移原则 | completed，仅文档；校验通过 | 原则已纳入本次选型决定 | [HANDOFF](tracks/tasks/WX-PLAN-ALIGN/HANDOFF.md) |
| WX-00 独立项目规划/引导 | completed，仅规划 | 保留历史依据 | [HANDOFF](tracks/bootstrap/HANDOFF.md) |
| WX-02 候选封装/能力探针 | 代码/离线完成；缺口复核/后续规划完成；真实未验 | [原复核计划](docs/WX-02-REVIEW-AND-PROVIDER-PLAN.md)保留历史；不继续新增provider投入 | [HANDOFF](tracks/tasks/WX-02/HANDOFF.md) |
| WX-01 离线核心/严格入口/模型快照/mock 闭环 | completed；已实现、离线通过 | 核心保留；回归70项中含原41项 | [HANDOFF](tracks/tasks/WX-01/HANDOFF.md) |

默认 transport=mock、enabled/sends=false、授权群空、私聊关闭且双名单空、mentions/single，视觉/网页/长期记忆/表情/成员等全部关闭。真实通道没有可执行实现，能力资格恒 false；真实模型必须关闭，facade 仅接受离线底层替身。黑名单与授权前置，unknown 不重放/重试/清账。没有操作微信/UI/登录/数据库、家庭 SSH 或 QQ 运行实例。

WX-01 基线：独立 Python3.12/锁、五份中文严格模板、规范事件/能力分层、入口/有界串行队列/停言栅栏、冻结目标、SQLite 投递/有限隔离历史、只读 inspect/健康操作骨架；原 CLI/Ollama runner 底层替身业务闭环。固定源 commit `dd9373029412137023124751d75883824122c784`，63 文件 manifest、61 未改/2 处受控本地差异；工件复制/hash 通过，未执行真实 CLI。

未验证：微信客户端/安装/登录、稳定真实身份/@/消息 ID、图片绑定像素、真实发送接受结果、模型效果、锁屏/远程断开/24h。候选 pyweixin 的显示名/UI 临时 ID/按键返回不满足生产门槛；iLink 仍仅作未来明确选择，不自动替换。

WX-02 新增：固定pywechat源码/pywechat127 1.9.8分发与许可冲突审阅、4份可选原语wheel hash锁（未安装）、单窗口只读注入原语、inspect/mock与29项离线测试。真实provider未接线，open_real_observation拒绝；120秒/10样本仅离线时钟与计数验证，不冒充实际UI硬时限。

WX-02复核差额：11源/16证据/4wheel字节hash匹配，但初始化片段64–60倒置，检查器空切片可通过；有效导入54–57本次静态核实，修复仅列后续计划。注入窗口字段不能证明账号/会话身份，真实@/稳定ID/当前图/关联ACK未获合同；有界只读观察也不能补齐这些生产门槛。

既有任务序号与历史证据保留；后续先按最新首选和实际客户端版本规划一次最小文字收发，不要求全部自动群聊门槛先于任何试用。WX-03/04不自动领取，本轮未安装/观察/收发/调用模型。真实身份/@/稳定性/确认等级继续如实记录，不能把旧冻结条件当作用户新指令后仍不可调整的绝对要求。

Git：独立本地仓库/`codex/bootstrap`，起点`a66319d`。27日用户明确授权本任务审阅文档commit/push，并补充要求创建public的WeChatbot；已建[hann-8/WeChatbot](https://github.com/hann-8/WeChatbot)并配置origin，发布分支codex/bootstrap。所有secrets/local/state/runtime/logs/cache忽略；当前文件及三次提交的保护路径/常见秘密模式检查未发现问题。按实际Git结果核对本地HEAD与远端分支SHA，不把建仓完成写成推送已完成。
