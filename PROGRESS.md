# WeChatbot项目入口

2026-10-23（Asia/Shanghai）。唯一根进度入口，不另建根 HANDOFF。位置 `E:\CodexWS\WeChatbot`，独立于 QQbot。

目标：个人微信与朋友家人聊天，复用显式 CodeBuddy/家庭 Ollama 两路线，账号/配置/历史/清理独立。当前 **WX-01 核心及 WX-02 代码/离线范围完成，70 项离线测试通过；真实能力全部未验，未部署**。

阅读顺序：[AGENTS](AGENTS.md)→本入口→[WX-02 当前交接](tracks/tasks/WX-02/HANDOFF.md)→[TASKS](TASKS.md)→[README](README.md)/[离线报告](docs/WX-01-OFFLINE-REPORT.md)。规划依据：[PLAN](docs/PLAN.md)、[RESEARCH](docs/RESEARCH.md)、[实施指引](docs/IMPLEMENTATION_GUIDE.md)。

| 工作线 | 状态 | 下一步 | 交接 |
| --- | --- | --- | --- |
| WX-00 独立项目规划/引导 | completed，仅规划 | 保留历史依据 | [HANDOFF](tracks/bootstrap/HANDOFF.md) |
| WX-02 候选封装/能力探针 | 本轮代码/离线完成；真实缺口保留 | [能力报告](docs/WX-02-CAPABILITY-REPORT.md)；门槛缺口回sol/max，真实观察另批 | [HANDOFF](tracks/tasks/WX-02/HANDOFF.md) |
| WX-01 离线核心/严格入口/模型快照/mock 闭环 | completed；已实现、离线通过 | 核心保留；回归70项中含原41项 | [HANDOFF](tracks/tasks/WX-01/HANDOFF.md) |

默认 transport=mock、enabled/sends=false、授权群空、私聊关闭且双名单空、mentions/single，视觉/网页/长期记忆/表情/成员等全部关闭。真实通道没有可执行实现，能力资格恒 false；真实模型必须关闭，facade 仅接受离线底层替身。黑名单与授权前置，unknown 不重放/重试/清账。没有操作微信/UI/登录/数据库、家庭 SSH 或 QQ 运行实例。

WX-01 基线：独立 Python3.12/锁、五份中文严格模板、规范事件/能力分层、入口/有界串行队列/停言栅栏、冻结目标、SQLite 投递/有限隔离历史、只读 inspect/健康操作骨架；原 CLI/Ollama runner 底层替身业务闭环。固定源 commit `dd9373029412137023124751d75883824122c784`，63 文件 manifest、61 未改/2 处受控本地差异；工件复制/hash 通过，未执行真实 CLI。

未验证：微信客户端/安装/登录、稳定真实身份/@/消息 ID、图片绑定像素、真实发送接受结果、模型效果、锁屏/远程断开/24h。候选 pyweixin 的显示名/UI 临时 ID/按键返回不满足生产门槛；iLink 仍仅作未来明确选择，不自动替换。

WX-02 新增：固定pywechat源码/pywechat127 1.9.8分发与许可冲突审阅、4份可选原语wheel hash锁（未安装）、单窗口只读注入原语、inspect/mock与29项离线测试。真实provider未接线，open_real_observation拒绝；120秒/10样本仅离线时钟与计数验证，不冒充实际UI硬时限。

任务顺序保留 WX-01→WX-02→有真实证据才 WX-03→WX-04 明确小批次；本轮仅WX-02代码/离线完成，真实身份/@/图像/ACK缺口回sol/max。没有授权真实观察或整串推进。

Git：本地独立仓库/`codex/bootstrap` 检查点；无 remote、无推送。所有 secrets/local/state/runtime/logs/cache 忽略；没有复制 QQ 私密配置或家庭资料。初始规划来自 QQ LAP-38 的已版本化引导副本，后续只维护本项目；QQ 地址不是微信远端。
