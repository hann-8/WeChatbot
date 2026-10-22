# WeChatbot任务台账

返回[PROGRESS](PROGRESS.md)。先读[AGENTS](AGENTS.md)，一个session领取一项，实施前记录session/开始时间/文件并重读；首次实施再建该项HANDOFF及双向链接。未领取行不预建空交接。

| ID | 范围 | 状态/证据 | 负责人/时间 | 下一步 |
| --- | --- | --- | --- | --- |
| WX-00 | 需求、上游调研、独立架构与medium指引 | completed，仅规划；0代码/运行操作；[HANDOFF](tracks/bootstrap/HANDOFF.md) | LAP-38-vision-web-wechat-plan，2026-10-22 23:19（Asia/Shanghai）起；仅本引导包文档 | 用户后续选medium领取WX-01 |
| WX-01 | 离线核心/严格入口/投递/固定模型源码复用/mock | completed；已实现/41项离线通过；[HANDOFF](tracks/tasks/WX-01/HANDOFF.md) | WX-01-offline-core-20261023，2026-10-23 00:01（Asia/Shanghai）；src/config/tests/vendor/pyproject/锁/README/报告/台账 | [报告](docs/WX-01-OFFLINE-REPORT.md)；核心保留，WX-02进度见下行 |
| WX-02 | pyweixin封装与能力探针 | 本轮代码/离线完成；真实缺口保留；[HANDOFF](tracks/tasks/WX-02/HANDOFF.md) | WX-02-pyweixin-offline-20261023，2026-10-23 00:23（Asia/Shanghai） | [能力报告](docs/WX-02-CAPABILITY-REPORT.md)；门槛缺口回sol/max，未授权真实观察，不领取03 |
| WX-03 | 已证明能力的真实适配与回归 | 条件待领取，依赖02门槛 | 未登记 | 身份/@/投递未证不能启用；不得换协议/降低合同 |
| WX-04 | 小批次真实文本/当前图及部署接受 | 条件待领取 | 未登记 | 明确实际对象/模型总数/发送动作后执行；不做自启 |

WX-00 文件归属：原七份引导文档，保留历史正文。WX-01 文件归属：src/、config/、tests/、scripts/、vendor/、pyproject.toml、uv.lock、.gitignore/.gitattributes、README.md、docs/WX-01-OFFLINE-REPORT.md、PROGRESS/TASKS/本任务交接；AGENTS 仅同步初始阶段描述。没有真实运行实例；未安装/导入实际 UI 适配。

WX-02 本轮归属：src/wechatbot/transports/pyweixin_adapter.py、src/wechatbot/pyweixin_probe.py、src/wechatbot/__main__.py、src/wechatbot/status.py、tests/test_pyweixin.py、scripts/check_pyweixin_source.py、vendor/pyweixin/、docs/WX-02-CAPABILITY-REPORT.md、README.md、PROGRESS.md、TASKS.md、tracks/tasks/WX-02/HANDOFF.md；必要时新增固定第三方锁文件。不改WX-01核心/快照或运行配置。开始工作区干净，无其他领取/未提交文件。

WX-02 结果：70/70离线通过（原41+新增29），11份固定源/16份证据/4份wheel hash通过；默认inspect/mock，生产关闭。真实provider未接线，身份/@/发送/图片均未验；新任务或产品/传输变更回sol/max。只本地提交，无remote，不改WX-01测试/模型快照/默认依赖或运行配置。
