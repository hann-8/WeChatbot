# WeChatbot项目入口

Git主线已统一：2026-10-28以远端最新`c2bc5fa`（14:24，QQ功能迁移规划）为基线快进到本地；本地和GitHub均只保留`main`，GitHub默认分支与origin/HEAD均为main，旧分支提交完整保留。后续直接在main工作，见[主线交接](tracks/tasks/WX-GIT-MAIN/HANDOFF.md)。

当前规划：2026-10-28 **WX-MIGRATION-PLAN 已完成详细功能规划**，见[计划](docs/QQ-TO-WECHAT-MIGRATION-PLAN.md)、[交接](tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md)和[sol/medium指令](docs/IMPLEMENTATION_GUIDE.md)。按用户新意图把QQ成熟业务向wxauto4迁移，优先WX-MIG-01人设/纯文本/48000预算及角色字符门槛/模型代码接点，再02短期上下文与本机控制，再03指定网页读取。均仅规划、未实施；测试暂缓，WXA-02真实阻塞不挡独立代码准备。

后续实施统一 **gpt-6.1-sol/medium**，不再用Terra；27日临时选择保留为历史。输入政策可采用48000字节，不能据此宣称原生token窗口/实时能力已验。下午功能规划只改六份文档，已推送当时默认主线codex/bootstrap；此后用户改为main，见顶部主线交接。未改实际运行配置或调用模型/微信。

既有真实试用：WX-WXA-02 已领取但受阻，账号未准备、安装器版本证据不符；见[交接](tracks/tasks/WX-WXA-02/HANDOFF.md)和[报告](docs/WX-WXA-02-REPORT.md)。WX-WXA-01 已完成离线工具，真实微信与模型尚未验证。

此前规划：2026-10-27 `WX-WXAUTO4-PLAN-20261027` 已完成[详细计划](docs/WXAUTO4-IMPLEMENTATION-PLAN.md)与[medium指令](docs/IMPLEMENTATION_GUIDE.md)，11份文档复读、99个本地链接/围栏/双向入口与diff检查通过；只规划、不实施，未重跑业务测试。规划交接为[WX-WXAUTO4-PLAN](tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md)，文件归属和Git起点见[TASKS](TASKS.md)。

2026-10-27历史模型续作曾选择Terra；已被顶部28日sol/medium决定覆盖。WX-WXA-01已在独立实施会话完成离线范围，不重复领取。

2026-10-28（Asia/Shanghai）。唯一根进度入口，不另建根 HANDOFF。位置 `E:\CodexWS\WeChatbot`，独立于 QQbot。

目标：个人微信与朋友家人聊天，复用显式 CodeBuddy/家庭 Ollama 两路线，账号/配置/历史/清理独立。当前 **WX-01 核心及 WX-02 代码/离线范围完成，历史70项离线通过；真实能力全部未验，未部署**。WX-WXA-01 本轮全套80项离线通过。

当前路线：wxauto4免费版41.1.7＋微信4.1.8.107，公开API→薄封装→单会话人工监督试用→本项目固定runner→CodeBuddy。首期暂不加AstrBot，不连接QQ实例。用户自报4.1.15.13并已接受换版，不再询问换版意愿；实际更换尚未执行。依据为[26日选型](tracks/tasks/WX-FRAMEWORK-DECISION/HANDOFF.md)和[27日详细计划](docs/WXAUTO4-IMPLEMENTATION-PLAN.md)。WeChatFerry留作备选，不自行改写任何上游核心。

WX-WXA-01 已完成最小试用工具/可选包及离线验证并停止；WX-WXA-02另做配套客户端和一个指定会话的文字试验（0模型），WX-WXA-03另接一次CLI。WX-WXA-01 已完成离线范围，02受阻、03未领取。已有严格离线Gate不直接放开，试用明确记录UI昵称/临时ID与本地结果，不伪造生产身份、真实@或服务端ACK。

最新用户原则：个人娱乐先能用，现成公开接口和少量项目适配优先，不限定注入，允许功能延期或舍弃；不得为复刻QQ功能自行改写框架核心或维护私有fork。缺完整消息ID/@/服务端ACK先标限制，不一律否决人工监督的单会话试用，也不伪造能力。真实群触发/对象动作仍待具体规划，当前没有实施；详见[AGENTS](AGENTS.md)和[PLAN第2节](docs/PLAN.md)。

前次WX-02文档复核：`WX-02-gap-review-plan-20261023`（2026-10-23 20:02起，Asia/Shanghai）完成[缺口复核与后续详细计划](docs/WX-02-REVIEW-AND-PROVIDER-PLAN.md)，未实施、未重跑测试、未领取 WX-03。建议停止以当前固定上游推进生产；可选一次隔离UI元数据观察需另批代码/离线与指定对象真实观察，不是必须实施的步骤。归属与Git核对见 [TASKS](TASKS.md)。

阅读顺序：[AGENTS](AGENTS.md)→本入口→[当前交接](tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md)→[TASKS](TASKS.md)→[功能迁移详规](docs/QQ-TO-WECHAT-MIGRATION-PLAN.md)→[medium指令](docs/IMPLEMENTATION_GUIDE.md)。历史依据：[PLAN](docs/PLAN.md)、[RESEARCH](docs/RESEARCH.md)、[README](README.md)、[离线报告](docs/WX-01-OFFLINE-REPORT.md)。

| 工作线 | 状态 | 下一步 | 交接 |
| --- | --- | --- | --- |
| WX-GIT-MAIN 同步与单main主线 | completed；本地/远端仅main，默认已核对 | 后续直接main；本任务四份协作文档随提交交付 | [HANDOFF](tracks/tasks/WX-GIT-MAIN/HANDOFF.md) |
| WX-MIGRATION-PLAN 功能迁移详规 | completed，仅文档；未实施/未跑业务测试 | sol/medium后续仅领WX-MIG-01，见详规 | [HANDOFF](tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md) |
| WX-WXA-02 客户端与单会话试用 | blocked；工件摘要/签名通过但版本证据不符，账号未准备 | 解决版本证据与账号准备后再收集绑定 | [HANDOFF](tracks/tasks/WX-WXA-02/HANDOFF.md) |
| WX-WXA-01 最小试用工具 | completed，离线验证；真实未验 | 停止；02 已领取 | [HANDOFF](tracks/tasks/WX-WXA-01/HANDOFF.md) |
| WX-WXAUTO4-PLAN 详细实施规划 | completed，仅文档；校验通过 | 规划完成；实施不自动串行 | [HANDOFF](tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md) |
| WX-FRAMEWORK-DECISION 框架选型 | 26日续作completed，仅文档；已补版本答复 | wxauto4免费＋微信4.1.8.107；用户已接受换版，后续进入明确实施任务 | [HANDOFF](tracks/tasks/WX-FRAMEWORK-DECISION/HANDOFF.md) |
| WX-PLAN-ALIGN 架构说明/框架迁移原则 | completed，仅文档；校验通过 | 原则已纳入本次选型决定 | [HANDOFF](tracks/tasks/WX-PLAN-ALIGN/HANDOFF.md) |
| WX-00 独立项目规划/引导 | completed，仅规划 | 保留历史依据 | [HANDOFF](tracks/bootstrap/HANDOFF.md) |
| WX-02 候选封装/能力探针 | 代码/离线完成；缺口复核/后续规划完成；真实未验 | [原复核计划](docs/WX-02-REVIEW-AND-PROVIDER-PLAN.md)保留历史；不继续新增provider投入 | [HANDOFF](tracks/tasks/WX-02/HANDOFF.md) |
| WX-01 离线核心/严格入口/模型快照/mock 闭环 | completed；已实现、离线通过 | 核心保留；回归70项中含原41项 | [HANDOFF](tracks/tasks/WX-01/HANDOFF.md) |

默认 transport=mock、enabled/sends=false、授权群空、私聊关闭且双名单空、mentions/single，视觉/网页/长期记忆/表情/成员等全部关闭。旧核心真实通道关闭，独立试用入口仅显式 live 可调用；能力资格恒 false；真实模型必须关闭，facade 仅接受离线底层替身。黑名单与授权前置，unknown 不重放/重试/清账。没有操作微信/UI/登录/数据库、家庭 SSH 或 QQ 运行实例。

WX-01 基线：独立 Python3.12/锁、五份中文严格模板、规范事件/能力分层、入口/有界串行队列/停言栅栏、冻结目标、SQLite 投递/有限隔离历史、只读 inspect/健康操作骨架；原 CLI/Ollama runner 底层替身业务闭环。固定源 commit `dd9373029412137023124751d75883824122c784`，63 文件 manifest、61 未改/2 处受控本地差异；工件复制/hash 通过，未执行真实 CLI。

未验证：微信客户端/安装/登录、稳定真实身份/@/消息 ID、图片绑定像素、真实发送接受结果、模型效果、锁屏/远程断开/24h。候选 pyweixin 的显示名/UI 临时 ID/按键返回不满足生产门槛；iLink 仍仅作未来明确选择，不自动替换。

WX-02 新增：固定pywechat源码/pywechat127 1.9.8分发与许可冲突审阅、4份可选原语wheel hash锁（未安装）、单窗口只读注入原语、inspect/mock与29项离线测试。真实provider未接线，open_real_observation拒绝；120秒/10样本仅离线时钟与计数验证，不冒充实际UI硬时限。

WX-02复核差额：11源/16证据/4wheel字节hash匹配，但初始化片段64–60倒置，检查器空切片可通过；有效导入54–57本次静态核实，修复仅列后续计划。注入窗口字段不能证明账号/会话身份，真实@/稳定ID/当前图/关联ACK未获合同；有界只读观察也不能补齐这些生产门槛。

既有任务序号与历史证据保留；后续先按最新首选和实际客户端版本规划一次最小文字收发，不要求全部自动群聊门槛先于任何试用。WX-03/04不自动领取；WX-WXA-02未安装/观察/收发/调用模型。真实身份/@/稳定性/确认等级继续如实记录，不能把旧冻结条件当作用户新指令后仍不可调整的绝对要求。

Git：独立仓库[hann-8/WeChatbot](https://github.com/hann-8/WeChatbot)，origin保持该地址。当前用户要求单main主线，后续直接在main工作；27日codex/bootstrap发布及保护路径检查保留为历史。所有secrets/local/state/runtime/logs/cache继续忽略。当前同步、默认分支、旧分支清理及远端SHA证据见[主线交接](tracks/tasks/WX-GIT-MAIN/HANDOFF.md)，不把分支整理视为功能实施或真实验收。
