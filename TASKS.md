# WeChatbot任务台账

当前唯一实施：**WX-AKASHA-ALL ready_for_user_test**，负责人本会话Codex，2026-10-31T10:25:51+08:00起。全部代码接线/40项当前组合检查/零生成握手与两侧受管部署完成；用户已保存账号/密钥和facts_only＋1 actor_link，原指定群实际SSE/WS已连，交用户自然实测；具体故障继续同任务。精确归属/验证/Git见[实施交接](tracks/tasks/WX-AKASHA-ALL/HANDOFF.md)。以下规划/旧路线登记为历史，保留原事实。

本轮规划：2026-10-31 `WX-AKASHA-01`，负责人本会话Codex，用户明确改用现成Akasha接现有AstrBot、以此作为main，并在00:51前后追加“本轮只做一次详细规划，基础与其他可迁功能全放同一方案/sol-medium指令，用户自行提交实施，严禁过度防御”；用户已睡，继续规划。先前源码/独立环境/WeFlow二进制准备保留，停止本会话创建的首次配置服务，不再实施。用户已明确允许WeFlow读库，未安装；当前未读数据库/密钥、未真实收发。起点main=938187c；保留本会话已知的故障登记/新路线差异。归属：AGENTS.md、PROGRESS.md、TASKS.md、docs/AKASHA-IMPLEMENTATION-PLAN.md、tracks/tasks/WX-AKASHA-01/HANDOFF.md、tracks/tasks/WX-AKASHA-01/MEDIUM_START.md、README.md、docs/IMPLEMENTATION_GUIDE.md、原ALL交接及必要路线说明。QQ/Snow现有代码/配置/运行实例本轮只读；完整规划须覆盖同轮所需的跨项目精确归属，不留后续再规划的必需接线。5h剩余低于5%时保存检查点，按北京时间2026-10-31 06:30继续；00:51实时读数剩余13%，未触发。

续作登记：2026-10-31T06:31:26+08:00，同一session按一次heartbeat恢复WX-AKASHA-01最终文档QA，仅原9份文档归属；不实施、不commit/push，QQ源只读。

本轮交付：WX-AKASHA-01 completed，完整计划、唯一sol/medium指令及最终文档QA已完成；已按额度条件于06:30恢复并收尾；WX-AKASHA-ALL为后续用户提交的唯一实施任务，未预领取。9份文档/90个本地链接/12份HANDOFF索引及diff检查通过，QQ源干净无改；一次续做自动化已实际删除，未commit/push。范围/实际证据见[规划交接](tracks/tasks/WX-AKASHA-01/HANDOFF.md)。

历史登记（随Akasha选择停止，未修复）：2026-10-31 00:22（Asia/Shanghai）WX-MIG-ALL故障续修：session `WX-MIG-ALL-chat-protocol-debug-20261031`，负责人本会话Codex。用户当前实报无法聊天，提供live日志：baseline_ready、MEMORY_LOAD、CLI_START后连续PROTOCOL_ERROR，尚未生成/发送回复。起点main=938187c，工作区干净；原“测试OK”记录不能替代当前真实聊天结果。仅续修ALL，优先定位/最小修复CLI接线，不新规划或扩大功能。初始归属为src/qqbot_gateway/workbuddy_cli_runner.py、src/wechatbot/chat_model.py、必要cli_control/原生guard接点、相关定向测试、vendor/qq-core-manifest.json、PROGRESS/TASKS/README/ALL交接及报告；实际改动收敛后记录。源Snow及运行微信不操作，不主动真实模型/发送，不自动重试或改账号；本轮未新增Git发布指令。登记写后重读。

此前文字版收尾（历史）：2026-10-31（Asia/Shanghai），用户先反馈“现在可以了”，随后反馈“测试ok，继续”。据此记录指定单群文字版启动恢复、整体试用OK并由用户接受；用户未逐项列出记忆/联网/本机控制结果，不扩写为这些专项全部实测通过，不称服务端ACK或长期稳定性证明。 本轮仅文档及框架本机工件忽略规则，无业务改动/新测试或真实操作。

WX-MIG-ALL 2026-10-30交付：实现/必要检查completed，60项相关离线检查和74项快照/工件摘要通过；源42911af只读不变，未操作真实微信/模型/联网服务/发送。新启动入口与本机空绑定已准备，交用户实测后停止。文件与证据见[本任务交接](tracks/tasks/WX-MIG-ALL/HANDOFF.md)和[报告](docs/WX-MIG-ALL-REPORT.md)。本轮按授权仅main提交检查文件及上轮规划，普通push核SHA。

2026-10-30 22:37（Asia/Shanghai）：本会话 Codex 领取唯一任务 **WX-MIG-ALL**，session WX-MIG-ALL-20261030。main 起点33c18f0；保留上轮十份规划差异。归属：统一计划第9节的微信业务/配置/启动/定向测试、映射共用源码与资产、manifest/CLI准备脚本、README/本任务报告及交接、PROGRESS/TASKS和已知规划文档。源固定42911af只读；不运行真实UI/模型/发送。授权审阅后commit及普通push main。见[本任务交接](tracks/tasks/WX-MIG-ALL/HANDOFF.md)。

2026-10-30 21:53（Asia/Shanghai）规划续作：session `WX-MIGRATION-CLARIFY-20261030`，负责人本会话Codex，仅续作 **WX-MIGRATION-PLAN**。用户确认禁止过度防御性编程、先能用，要求精简AGENTS并说明两端接口适配与业务复用；自报账号已准备并在本机登录，随后追加检查SnowLuma更新、详细规划一次medium批量迁移后由用户实测。起点main=`33c18f0`，工作区干净；源只读核对E:/CodexWS/QQbot_Snowluma本地/实时origin/main均为42911afc4c1f2bcfbbc3c26afc2647fd21992f08，干净。归属：AGENTS.md、PROGRESS.md、TASKS.md、docs/QQ-TO-WECHAT-MIGRATION-PLAN.md、docs/IMPLEMENTATION_GUIDE.md、tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md、tracks/tasks/WX-MIGRATION-PLAN/MEDIUM_START.md、docs/WX-MIGRATION-SOURCE-MAP.json、tracks/tasks/WX-WXA-02/HANDOFF.md、docs/WX-WXA-02-REPORT.md。仅查源码/修订规划，不领取实施或真实试用，不改源项目或操作微信/模型；本轮未另获commit/push指令，保留为本地可审阅差异。写后重读登记及交接。

30日续作结果：completed，仅规划。统一计划/medium指令和固定源码映射已交付，十份归属文件（九Markdown/一JSON）、75个本地链接、围栏/UTF-8 LF/所有工作线双向入口/归属与diff检查通过，52个固定Git blob摘要匹配。AGENTS为4001字节/30行，原9581字节/52行；已写禁止过度防御和一次批量交付原则。用户补充已登录4.2.0.11、先测指定群且接受换版，旧账号阻塞解除；免费配套公开文档仍到4.1.8.107。未实施、未运行业务测试或微信/CLI生成/工具服务/发送/SSH；源42911af保持干净，本地/远端微信HEAD仍33c18f0，本轮规划保留未暂存/未提交差异。下一步仅WX-MIG-ALL，用户提交统一指令后由medium同轮实现，用户实测。

历史登记：`WX-GIT-MAIN-20261028`，2026-10-28 23:01（Asia/Shanghai）起，负责人本会话Codex；仅领取 **WX-GIT-MAIN 远端同步与单main主线**，已完成分支整理。用户要求拉取今天下午最新提交并只保留main。起点本地`codex/wxauto4-trial-kit=2924097`，工作区干净；fetch确认远端最新`codex/bootstrap=c2bc5fadcafcda2d5c6ebb08edbb4fc2767ef9ff`，三个远端分支均为其祖先，只有本项目一个worktree。已普通快进、改名main并推送，GitHub默认与origin/HEAD均为main；三个远端旧分支和本地旧codex/bootstrap已安全删除，历史提交保留。归属：AGENTS.md、PROGRESS.md、TASKS.md、tracks/tasks/WX-GIT-MAIN/HANDOFF.md；登记写后重读，四文档72个本地链接/围栏/UTF-8 LF及双向入口检查通过。本任务文档随main提交推送并在会话核最终SHA，不领取功能实施或运行真实微信/模型。见[交接](tracks/tasks/WX-GIT-MAIN/HANDOFF.md)。

2026-10-28 14:06（Asia/Shanghai）：session `WX-FEATURE-MIGRATION-PLAN-20261028`，负责人本会话 Codex，领取新任务 **WX-MIGRATION-PLAN**。用户要求把 QQbot（SnowLuma 主线）易迁移功能优先规划到 WeChatbot，测试暂缓，并明确要求规划完成后 commit/push。仅文档规划，不实施代码、不运行业务测试或真实微信/模型。来源 QQ main=`52866fe10cc654d2e12c5520f7afc5aa8bbe0179`；基线微信试用分支=`29240978a298e3fd5a47a21af7eb10a670d48994`，曾据此建立 `codex/wechat-feature-migration-plan` 作为准备指针；用户随后明确允许直接推主线，最终交付改为 `codex/bootstrap` 的普通快进。本机无另一台电脑项目目录，使用 GitHub 精确提交和本地文档覆层审阅，最终提交只含本任务六文件。归属：`AGENTS.md`、`PROGRESS.md`、`TASKS.md`、`docs/IMPLEMENTATION_GUIDE.md`、`docs/QQ-TO-WECHAT-MIGRATION-PLAN.md`、`tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md`。登记写后重读；保留试用分支两个既有提交的历史后快进主线，本轮新增提交仍只含六份文档；不处理 WX-WXA-02 真实阻塞。

28日规划结果（已被30日统一范围取代）：原三项实施均未领取，未调用真实微信/模型；现合并为WX-MIG-ALL，旧48000预算/指定URL限定/长期记忆延期不再限制新方案。下方27日模型/首项描述保留为历史，当前入口见[统一计划](docs/QQ-TO-WECHAT-MIGRATION-PLAN.md)和[交接](tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md)。

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
| WX-MIGRATION-PLAN | 最新Snow源码/统一批量迁移详规、精简规范 | completed；75链接/52源blob/归属检查通过；[计划](docs/QQ-TO-WECHAT-MIGRATION-PLAN.md) / [HANDOFF](tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md) | WX-MIGRATION-CLARIFY-20261030，21:53起 | 用户提交统一medium指令；当前不实施 |
| WX-MIG-ALL | 单群收发/文字/模型/上下文/本机控制/原生联网/schema2记忆和启动入口 | completed；用户测试OK接受，既有离线/摘要证据保留；[HANDOFF](tracks/tasks/WX-MIG-ALL/HANDOFF.md) | 本会话Codex，2026-10-30 22:37 | 用户已接受，正常使用 |
| WX-MIG-01 | 原人设/纯文本/预算/模型接点 | merged_into WX-MIG-ALL，未单独实施 | 历史任务号保留 | 不再单独领取/停下 |
| WX-MIG-02 | 原短期上下文/本机控制 | merged_into WX-MIG-ALL，未单独实施 | 历史任务号保留 | 不再单独领取/停下 |
| WX-MIG-03 | 原指定URL读取 | merged_into WX-MIG-ALL；采用最新原生两工具 | 历史任务号保留 | 不恢复旧Python检索前置 |
| WX-WXAUTO4-PLAN | wxauto4详细规划/medium指令 | completed，仅文档；11份文档/99链接/围栏/入口/diff校验通过；[HANDOFF](tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md) | WX-WXAUTO4-PLAN-20261027，19:05起；上方登记文件 | 规划时停止；01后续已完成离线实施 |
| WX-WXA-01 | 最小试用工具/可选依赖/离线验证 | completed；10项专项、80项全套离线通过；[HANDOFF](tracks/tasks/WX-WXA-01/HANDOFF.md) | WX-WXA-01-20261027，本会话，19:56起 | 停止；真实试用另行授权 |
| WX-WXA-02 | 配套客户端/指定群文字试用历史 | 30日用户自报已登录4.2.0.11、接受换版；实际兼容/收发未验；[HANDOFF](tracks/tasks/WX-WXA-02/HANDOFF.md)、[报告](docs/WX-WXA-02-REPORT.md) | 原领取记录保留；本次仅同步用户状态 | 新准备/入口并入ALL，旧挑战台账保留，不作为单独前置 |
| WX-WXA-03 | 原固定CLI模型一次试用 | 未真实生成；代码/实测接点并入ALL | 未单独领取，历史合同保留 | 不要求先做02再开一轮03；用户在新入口实测 |
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

2026-10-30 23:16 Asia/Shanghai，本会话Codex按用户反馈续修WX-MIG-ALL：取消连续聊天的发送者白名单，指定群全部成员可按前缀触发，保留黑名单和本机控制边界。归属src/wechatbot/chat_session.py、chat_model.py、chat_policy.py、wxauto4_chat.py、绑定模板及忽略的本机绑定、tests/test_chat_migration.py、README/AGENTS/计划/报告/PROGRESS/TASKS/当前HANDOFF。无真实通道操作。

续修完成：取消连续入口的发送者白名单，绑定群全部非黑名单成员可按bot前缀触发；旧allowed_senders读取时忽略，模板及本机文件移除。9项迁移定向检查通过，默认inspect仍0真实通道/模型/发送，未运行live。本机绑定格式已验证，用户填写的其他值保留。

2026-10-30 23:21 Asia/Shanghai，本会话Codex续修WX-MIG-ALL启动故障：用户实报-Live在wxauto初始化附近失败，原入口吞掉异常。范围为启动诊断、必要公开API适配、替身检查及README/报告/当前交接/PROGRESS/TASKS；不自行执行live或操作微信。先补封闭元数据诊断再据具体证据修复，不把广告输出当兼容结论。

启动续修检查点：用户自报已换4.1.8.107；已修复入口吞掉全部异常的问题，startup_error会显示阶段/异常类型/安全代码帧与数值错误码，并写state/startup-last-error.json，不含异常原文/群名/消息。新增构造器失败与隐私反例，连同9项迁移检查共10项通过；默认inspect仍0真实操作。未重跑live，真实启动原因待用户提供新诊断，尚不声称已修复实际框架故障。

2026-10-31 00:15 Asia/Shanghai，本会话Codex继续WX-MIG-ALL收尾：用户反馈启动已恢复，随后明确“测试ok，继续”，记录本次单群文字版用户接受。归属AGENTS.md、PROGRESS.md、TASKS.md、README.md、docs/WX-MIG-ALL-REPORT.md、tracks/tasks/WX-MIG-ALL/HANDOFF.md及.gitignore。保留新出现的_temp/与wxauto_logs/本机工件，不读内容、不删除、不提交；仅补忽略。无代码/配置/运行实例改动，无新增验收。

2026-10-31T10:25:51.763167+08:00：唯一任务 **WX-AKASHA-ALL**，负责人本会话Codex，session WX-AKASHA-ALL-20261031。起点WeChatbot main=938187c。归属：adapters/akasha/**、scripts/*Akasha*及akasha管理脚本、config/examples/akasha*、tests/test_akasha*、README/docs/报告与当前9份规划、PROGRESS/TASKS/实施HANDOFF。完整执行微信计划；已有微信9份规划差异保留，QQ开工干净。不操作旧NapCat根。只管理有创建身份的项目进程；授权受管部署/检查/提交普通push，真实聊天交用户。

2026-10-31T11:05:04.308079+08:00：WX-AKASHA-ALL交用户实测。WeFlow桌面API/bridge受管运行，18766面板、11229独立WS正常；QQ connected/ready且保护检查不变。用户明确回复配对已保存；实际ID/密钥仅本机忽略配置。未主动真实生成/群发样本。

2026-10-31T11:16:39.271914+08:00 WX-AKASHA-ALL具体故障续修，负责人本会话Codex：用户实报Start-Akasha.ps1 status向Python传空--session导致argparse失败。起点main=0cec96d，工作区干净。精确归属仅Start-Akasha.ps1、TASKS.md、本任务HANDOFF；改为仅非空Session才传该可选参数，验证真实status命令。无需重启服务、修改QQ/配置、模型生成或发送；沿原授权审阅提交并普通push。

续修结果：Start-Akasha.ps1仅在Session非空时追加--session和值；当前PowerShell直接运行.\Start-Akasha.ps1 status及Windows PowerShell5.1 -File调用均exit=0、返回状态JSON，SSE/WS仍true。未重启/生成/发送。验证同时看到当前会话有1项unknown且已暂停，保持原记录，不重发、不清账；这与本次参数错误分开。

2026-10-31T11:22:51.902371+08:00 WX-AKASHA-ALL发送故障续修，负责人本会话Codex。用户先不确定是哪条，随后确认“没有回复”。起点main=918de1d、工作区干净。范围：只读当前指定群投递元数据/本机UIA环境，必要adapters/akasha桥接发送接点与定向测试、PROGRESS/TASKS/HANDOFF/报告及受管bridge部署；不改UIA内核、QQ源/配置，不主动模型或发样本，不补发旧结果。未知旧记录留存，按本次人工反馈处理后仅恢复新消息。

本轮精确补充归属adapters/akasha/uia_dispatch.py、source.json、project_entry.py、tests/test_akasha_uia.py：只修现成UIA工厂/调用的线程归属，联系人切换结果检查及错误类型元数据。只读工作线程探针已复现OSError/CoInitialize缺失；uiautomation本机源码明确要求当前线程初始化且Control不能跨线程。两进程同为非提升权限，最后失败部件是text，不臆断图片/权限原因。

用户新增现场事实：之前同时登录两个微信，自动化实际落在大号；随后大号退出。已立即按创建身份停止bridge，WeFlow/QQ/客户端保持，不再发消息。将补发送窗口的显式本机绑定（账号引用＋窗口/进程创建身份），窗口丢失不跟随另一个账号；原UIA按标题全局FindWindow缺少账号绑定是另一确定缺口，不能将该现场全归因COM。补充归属scripts/akasha.py、Start-Akasha.ps1、config/examples/akasha.json及README。

发送续修收尾：UIA同线程/显式窗口与进程绑定/联系人返回检查已实现和部署，6项组合通过。当前新消息恢复；旧unknown和投递证据留存，无补发/主动模型/发送。用户关于多账号的实际反馈已写报告，日常bind-window/start步骤已入README；继续WX-AKASHA-ALL待新消息实测。
