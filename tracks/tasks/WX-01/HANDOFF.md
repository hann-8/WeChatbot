# WX-01 离线核心交接

返回[PROGRESS](../../../PROGRESS.md) / [TASKS](../../../TASKS.md)。继承[AGENTS](../../../AGENTS.md)。

状态：**completed；已实现、41 项离线测试通过；全部真实能力未验**。session `WX-01-offline-core-20261023`，2026-10-23 00:01（Asia/Shanghai）开始。仅领取 WX-01，未领取 WX-02。

已完成：独立 Python3.12.14 项目/uv.lock、五份中文严格配置/独立人设、规范事件/adapter 能力摘要、严格 gate、冻结目标/停言代际、有界单并发队列、单 owner SQLite 去重/投递/有限隔离历史、mock、只读 inspect 和健康操作骨架。实际固定 CLI runner 的底层 synthetic spawn 完成预算→一次用户输入→隔离/解析/清理→mock ACK→历史；Ollama 原 runner 经假 transport 完成原生请求，0 SSH。

复用固定源 `dd9373029412137023124751d75883824122c784` 的已跟踪公开文件；63 个 manifest 条目，61 未改/2 处差异（CLI root 相对路径与 spawn 接缝、只保留文本 CLI 公开锁）。未读 QQ config/local/secrets/状态或家庭资料，未修改 QQ。Node/CLI 工件独立复制到忽略 runtime，hash 通过，未执行；重建见 [README](../../../README.md)。没有 QQ editable/软链/服务依赖。

本任务修改：src/、config/、tests/、scripts/、vendor/、pyproject.toml、uv.lock、.gitignore/.gitattributes、README、[独立报告](../../../docs/WX-01-OFFLINE-REPORT.md)、PROGRESS/TASKS/本交接；AGENTS 仅同步当前阶段/Git事实。原 PLAN/RESEARCH/IMPLEMENTATION_GUIDE/bootstrap 交接保留。开始时只有七份文档，无独立 Git、无其他未提交内容；本地初始提交纳入审阅的引导文档及本任务文件。

验证：`.venv/Scripts/python.exe -m unittest discover -s tests -v` 最终 41/41 通过（4.374s）；`python scripts/check_snapshot.py` 63 文件/3 工件 hash 通过；`python -m wechatbot inspect` valid/mock/false/false/production=false；`uv lock --check` 23 包一致。详细覆盖/修复见报告。只读状态 0 模型/0 UI/0发送；没有实际健康服务启动。

关键合同：准入在窗口/材料/模型/历史前；真实 @ 未知不触发；私聊发送者/会话双绑定；同文不同 ID 分别处理、稳定 ID 重启去重；pending 重启转 unknown 不重放、模型/投递 unknown 不自动重试或清账；原任务关联 ACK 才入 assistant 历史；停言/账号/会话/连接代际变化使旧输出失效。没有 free/媒体/联网/长期记忆实现。容量满拒绝，不丢 unknown。真实通道即使开关改 true 仍无生产资格。

本地 Git：`codex/bootstrap`；检查点提交号见 `git log -1` 与交付消息。无 remote，未推送。工作区没有待交接的源文件差异；忽略的 `.venv/runtime/state/__pycache__` 保留，其中 state 仅离线 synthetic 清理记录，无凭据/真实消息。没有创建 config/local 或 secrets。

剩余：WX-01 无未完成实施项；微信可信身份/@/ID/发送 ACK/图像/登录/真实模型/长稳全部未验，也不是本任务接受项。等用户另行指令再领取 WX-02；其默认 mock/inspect，真实观察需指定账号/单窗口/自造样本批次授权。不自动登录/发消息/切后端/调用家庭主机/模型。
