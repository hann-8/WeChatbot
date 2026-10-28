# WeChatbot任务台账

本次登记：`WX-GIT-MAIN-20261028`，2026-10-28 23:01（Asia/Shanghai）起，负责人本会话Codex；仅领取 **WX-GIT-MAIN 远端同步与单main主线**，已完成分支整理。用户要求拉取今天下午最新提交并只保留main。起点本地`codex/wxauto4-trial-kit=2924097`，工作区干净；fetch确认远端最新`codex/bootstrap=c2bc5fadcafcda2d5c6ebb08edbb4fc2767ef9ff`，三个远端分支均为其祖先，只有本项目一个worktree。已普通快进、改名main并推送，GitHub默认与origin/HEAD均为main；三个远端旧分支和本地旧codex/bootstrap已安全删除，历史提交保留。归属：AGENTS.md、PROGRESS.md、TASKS.md、tracks/tasks/WX-GIT-MAIN/HANDOFF.md；登记写后重读，四文档72个本地链接/围栏/UTF-8 LF及双向入口检查通过。本任务文档随main提交推送并在会话核最终SHA，不领取功能实施或运行真实微信/模型。见[交接](tracks/tasks/WX-GIT-MAIN/HANDOFF.md)。

2026-10-28 14:06（Asia/Shanghai）：session `WX-FEATURE-MIGRATION-PLAN-20261028`，负责人本会话 Codex，领取新任务 **WX-MIGRATION-PLAN**。用户要求把 QQbot（SnowLuma 主线）易迁移功能优先规划到 WeChatbot，测试暂缓，并明确要求规划完成后 commit/push。仅文档规划，不实施代码、不运行业务测试或真实微信/模型。来源 QQ main=`52866fe10cc654d2e12c5520f7afc5aa8bbe0179`；基线微信试用分支=`29240978a298e3fd5a47a21af7eb10a670d48994`，曾据此建立 `codex/wechat-feature-migration-plan` 作为准备指针；用户随后明确允许直接推主线，最终交付改为 `codex/bootstrap` 的普通快进。本机无另一台电脑项目目录，使用 GitHub 精确提交和本地文档覆层审阅，最终提交只含本任务六文件。归属：`AGENTS.md`、`PROGRESS.md`、`TASKS.md`、`docs/IMPLEMENTATION_GUIDE.md`、`docs/QQ-TO-WECHAT-MIGRATION-PLAN.md`、`tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md`。登记写后重读；保留试用分支两个既有提交的历史后快进主线，本轮新增提交仍只含六份文档；不处理 WX-WXA-02 真实阻塞。

本轮规划结果：详细计划已完成；后续实施统一 **gpt-6.1-sol/medium**，不再用 Terra。先 WX-MIG-01 人设/纯文本/48000预算与8000字符门槛/模型接点，再 WX-MIG-02 短期上下文/本机控制，后 WX-MIG-03 指定URL读取。三项实施均未领取，真实测试暂缓；下方27日模型/首项领取描述保留为历史，现行入口以本轮计划为准。文档检查与Git交付见[本轮交接](tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md)。

历史登记：`WX-WXA-02-20261027`，2026-10-27 20:07（Asia/Shanghai）起，负责人本会话 Codex；起点 `e750878`，工作区干净，分支 `codex/wxauto4-trial-kit`。归属：PROGRESS.md、TASKS.md、docs/WX-WXA-02-REPORT.md、tracks/tasks/WX-WXA-02/HANDOFF.md；真实绑定仅项目忽略的 secrets 文件，客户端工件不提交。仅配套客户端与一次明确单会话文字试验，0模型；目标尚缺。

当前登记：`WX-WXA-01-20261027`，2026-10-27 19:56（Asia/Shanghai）起，负责人本会话 Codex；起点 `8ad1334`，干净工作区，分支 `codex/wxauto4-trial-kit`。归属：src/wechatbot/transports/wxauto4_adapter.py、src/wechatbot/wxauto4_trial.py、tests/test_wxauto4_trial.py、config/examples/wxauto4-trial.example.json、vendor/wxauto4/manifest.json、pyproject.toml、uv.lock、README.md、docs/WX-WXA-01-REPORT.md、PROGRESS.md、TASKS.md、tracks/tasks/WX-WXA-01/HANDOFF.md。只实施离线试用工具和依赖准备；不操作真实微信或模型。完成验证后按授权提交并推送。

27日模型选择续作登记：`WX-WXAUTO4-PLAN-terra-20261027`，2026-10-27 19:51（Asia/Shanghai）起，负责人本会话Codex，沿用WX-WXAUTO4-PLAN的文档续作。用户提出用terra medium试本项目落地能力；本次只调整实施人选与复制指令，首项仍为WX-WXA-01，不领取/实施该项。归属为AGENTS.md、PROGRESS.md、TASKS.md、docs/IMPLEMENTATION_GUIDE.md、docs/WXAUTO4-IMPLEMENTATION-PLAN.md、tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md六份文档。起点codex/bootstrap=`fa12125b1424bfa73ca92fe717e71ecd92d4be53`，工作区干净，origin为已授权公开WeChatbot；沿Git授权只提交检查文档并push核SHA，写后重读。

模型续作结果：completed，仅文档；六份文档写后复读、66个本地链接/围栏/UTF-8 LF与diff检查通过，三段当前指令均为Terra medium，业务代码/配置/依赖不变，未运行业务测试或实施。后续只从当前首段指令领取WX-WXA-01。

当前任务登记：`WX-WXAUTO4-PLAN-20261027`，2026-10-27 19:05（Asia/Shanghai）起，负责人本会话 Codex；仅领取 **WX-WXAUTO4-PLAN 详细规划**，不实施。文件归属：AGENTS.md、PROGRESS.md、TASKS.md、docs/PLAN.md、docs/RESEARCH.md、docs/IMPLEMENTATION_GUIDE.md、docs/WXAUTO4-IMPLEMENTATION-PLAN.md、tracks/bootstrap/HANDOFF.md、tracks/tasks/WX-FRAMEWORK-DECISION/HANDOFF.md、tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md；审阅并保留前轮 tracks/tasks/WX-PLAN-ALIGN/HANDOFF.md。起点 `codex/bootstrap` / `a66319d`，六份已跟踪文档修改与两份未跟踪交接是本会话前轮已知成果，不重置；无已暂存文件、无 remote。用户授权本任务审阅文件的 commit/push；缺少微信远端地址已询问，先完成本地工作，不借用QQ远端。写后重读登记，再核实公开API与本地接口，完成计划、可复制medium指令和文档校验后停止。

当前规划交接：[WX-WXAUTO4-PLAN](tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md)。下方26日记录为前轮历史；本轮没有领取真实实施或WX-03/04。

27日Git授权补充：用户明确要求在其GitHub创建public的WeChatbot，已创建[hann-8/WeChatbot](https://github.com/hann-8/WeChatbot)，本地origin已指向该仓库；“缺地址”已解决。当前133个文件及三次提交的145个历史blob完成受保护路径/常见秘密模式检查，未发现命中；仍只stage审阅的11份文档，不上传忽略工件/凭据。提交和远端SHA以实际Git交付为准。

返回[PROGRESS](PROGRESS.md)。先读[AGENTS](AGENTS.md)，一个session领取一项，实施前记录session/开始时间/文件并重读；首次实施再建该项HANDOFF及双向链接。未领取行不预建空交接。

26日历史续作：`WX-FRAMEWORK-DECISION-practical-20261026`，2026-10-26 18:44（Asia/Shanghai）登记，负责人本会话 Codex；**按用户“以能用为优先、不限定注入”完成选型/试用规划修订**。沿用WX-FRAMEWORK-DECISION一项，未领取WX-03或实施任务。归属为AGENTS、PLAN、RESEARCH、IMPLEMENTATION_GUIDE、PROGRESS、TASKS、选型交接七份文档。当时本地`codex/bootstrap` HEAD=`a66319d`、无remote，未提交/推送；七份文档57个本地链接、围栏、双向入口和`git diff --check`通过，未运行业务测试。该轮未提交文档由27日本任务完整检查后归入文档检查点，不代表真实实施。

用户补充：当前微信版本为`4.1.15.13`，接受更换版本。选型配套确定为wxauto4免费版＋微信`4.1.8.107`；不重复询问换版意愿，不把该答复记成安装/登录/真实收发已完成。仅补齐上述归属文档，未启动实施。

| ID | 范围 | 状态/证据 | 负责人/时间 | 下一步 |
| --- | --- | --- | --- | --- |
| WX-GIT-MAIN | 拉取最新远端，统一单main及后续Git规则 | completed；本地/远端仅main，默认已核对；[HANDOFF](tracks/tasks/WX-GIT-MAIN/HANDOFF.md) | WX-GIT-MAIN-20261028，23:01登记 | 后续直接main；四份协作文档随提交交付，停止本Git任务 |
| WX-MIGRATION-PLAN | QQ业务向wxauto4的分阶段详细规划 | completed，仅文档；[计划](docs/QQ-TO-WECHAT-MIGRATION-PLAN.md) / [HANDOFF](tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md) | WX-FEATURE-MIGRATION-PLAN-20261028，14:06登记 | 本轮主线Git交付后停止；后续统一sol/medium |
| WX-MIG-01 | 人设/纯文本/48000输入与角色门槛/监督模型代码准备 | planned，未领取；不依赖WXA-02真实通过 | 未登记，不预建空交接 | sol/medium首推，仅独立代码准备；不自动启用真实模型 |
| WX-MIG-02 | 短期RAM上下文与本机reset/pause/resume | planned，未领取；依赖MIG-01文字接点 | 未登记 | 不搬旧历史/记忆库，不把昵称当稳定身份 |
| WX-MIG-03 | 显式指定单URL正文读取 | planned，未领取；复用公共HTTP/提取/预算 | 未登记 | 默认关闭，无搜索/媒体；实际网络与模型另定时段 |
| WX-WXAUTO4-PLAN | wxauto4详细规划/medium指令 | completed，仅文档；11份文档/99链接/围栏/入口/diff校验通过；[HANDOFF](tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md) | WX-WXAUTO4-PLAN-20261027，19:05起；上方登记文件 | 规划时停止；01后续已完成离线实施 |
| WX-WXA-01 | 最小试用工具/可选依赖/离线验证 | completed；10项专项、80项全套离线通过；[HANDOFF](tracks/tasks/WX-WXA-01/HANDOFF.md) | WX-WXA-01-20261027，本会话，19:56起 | 停止；真实试用另行授权 |
| WX-WXA-02 | 配套客户端/一个指定会话文字收发 | blocked；[HANDOFF](tracks/tasks/WX-WXA-02/HANDOFF.md)、[报告](docs/WX-WXA-02-REPORT.md) | WX-WXA-02-20261027，本会话，20:07起 | 解决账号准备与工件版本证据，≤1发送、0模型 |
| WX-WXA-03 | 固定CLI模型一次文字回复 | planned、未领取 | 未登记 | 02实测后另领，≤1生成/1发送，人工监督 |
| WX-FRAMEWORK-DECISION | 委托选型；26日按能用优先修订 | completed，仅文档；已补版本答复；[HANDOFF](tracks/tasks/WX-FRAMEWORK-DECISION/HANDOFF.md) | WX-FRAMEWORK-DECISION-practical-20261026，18:44登记；上述七份文档 | wxauto4免费＋微信4.1.8.107；换版意愿已明确，后续按具体实施任务推进 |
| WX-PLAN-ALIGN | 说明现有分层，记录框架原生接口优先与允许功能延期 | completed，仅文档；校验通过；[HANDOFF](tracks/tasks/WX-PLAN-ALIGN/HANDOFF.md) | WX-PLAN-ALIGN-20261025，2026-10-25 12:03（Asia/Shanghai）；前轮五份文档 | 架构原则已纳入本次选型决定，不领取03 |
| WX-00 | 需求、上游调研、独立架构与medium指引 | completed，历史规划；[HANDOFF](tracks/bootstrap/HANDOFF.md) | LAP-38-vision-web-wechat-plan，2026-10-22 23:19（Asia/Shanghai）起；仅本引导包文档 | 01/02离线已交付，当前下一项见WX-WXA-01 |
| WX-01 | 离线核心/严格入口/投递/固定模型源码复用/mock | completed；已实现/41项离线通过；[HANDOFF](tracks/tasks/WX-01/HANDOFF.md) | WX-01-offline-core-20261023，2026-10-23 00:01（Asia/Shanghai）；src/config/tests/vendor/pyproject/锁/README/报告/台账 | [报告](docs/WX-01-OFFLINE-REPORT.md)；核心保留，WX-02进度见下行 |
| WX-02 | pyweixin封装与能力探针 | 实施轮代码/离线完成；缺口复核/规划完成；真实缺口保留；[HANDOFF](tracks/tasks/WX-02/HANDOFF.md) | 实施：WX-02-pyweixin-offline-20261023，00:23；复核：WX-02-gap-review-plan-20261023，20:02起（2026-10-23，Asia/Shanghai） | [原复核计划](docs/WX-02-REVIEW-AND-PROVIDER-PLAN.md)保留历史；不再新增provider投入，不领取03 |
| WX-03（旧生产路线） | 已证明能力的真实适配与回归 | 未领取，历史门槛保留 | 未登记 | 不作为WX-WXA人工监督试用的前置，不伪称已通过 |
| WX-04（旧生产路线） | 真实文本/当前图及部署接受 | 未领取，历史范围保留 | 未登记 | 当前只推进另行明确的WX-WXA任务，不自动领取本项 |

WX-00 文件归属：原七份引导文档，保留历史正文。WX-01 文件归属：src/、config/、tests/、scripts/、vendor/、pyproject.toml、uv.lock、.gitignore/.gitattributes、README.md、docs/WX-01-OFFLINE-REPORT.md、PROGRESS/TASKS/本任务交接；AGENTS 仅同步初始阶段描述。没有真实运行实例；未安装/导入实际 UI 适配。

WX-02 原实施轮归属（402ffd2）：src/wechatbot/transports/pyweixin_adapter.py、src/wechatbot/pyweixin_probe.py、src/wechatbot/__main__.py、src/wechatbot/status.py、tests/test_pyweixin.py、scripts/check_pyweixin_source.py、vendor/pyweixin/、docs/WX-02-CAPABILITY-REPORT.md、README.md、PROGRESS.md、TASKS.md、tracks/tasks/WX-02/HANDOFF.md；包含固定第三方锁文件。不改WX-01核心/快照或运行配置。原实施开始工作区干净，无其他领取/未提交文件；这不是本次复核的代码写入授权。

WX-02 结果：70/70离线通过（原41+新增29），11份固定源/16份证据/4份wheel hash通过；默认inspect/mock，生产关闭。真实provider未接线，身份/@/发送/图片均未验；新任务或产品/传输变更回sol/max。只本地提交，无remote，不改WX-01测试/模型快照/默认依赖或运行配置。

WX-02复核轮（2026-10-23）：session `WX-02-gap-review-plan-20261023`，20:02起；归属能力报告、独立复核计划、WX-02交接及PROGRESS/TASKS。上述70项保留为历史结果，未重跑。独立只读核对11源/16证据/4wheel hash匹配；发现初始化证据区间64–60倒置、检查器缺区间校验，有效导入54–57已静态核实。证据JSON/检查器/代码未修，后续修正列入可选P1。建议停止当前UI上游的生产推进；可选一次元数据provider须分开授权代码/离线和真实对象观察，不能补齐稳定身份/@/像素/关联ACK或领取WX-03。该轮最终仅本地文档提交，真实验收差额见报告/计划/交接。
