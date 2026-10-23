# WX-02 候选封装与能力探针交接

返回[PROGRESS](../../../PROGRESS.md) / [TASKS](../../../TASKS.md)。继承[AGENTS](../../../AGENTS.md)。

当前状态：**WX-02 缺口复核与后续详细规划完成；未实施provider，真实观察仍未执行，WX-03门槛未满足。** 本次session `WX-02-gap-review-plan-20261023`，2026-10-23 20:02（Asia/Shanghai）开始，负责人本会话 Codex；登记已写后重读。归属仅本交接、PROGRESS/TASKS、[能力报告](../../../docs/WX-02-CAPABILITY-REPORT.md)和[独立复核计划/完整medium指令](../../../docs/WX-02-REVIEW-AND-PROVIDER-PLAN.md)。起始 `codex/bootstrap` HEAD=`402ffd201329f84278700dd3e89549fc3de23fa7`、工作区干净、无 remote；本轮不改代码/证据JSON/运行配置/人设，不领取 WX-03。

本次结论：固定上游没有提供能满足现有身份/@/当前图/关联ACK合同的已证接口，账号目录推断路径不可调用。建议停在缺口报告；可选一次隔离单窗口元数据观察仅用于工程可行性，必须先另批代码/离线P1、再另批具体对象P2。独立计划列明需求/非目标、代码证据、默认/生效方式、涉及文件/顺序、Job隔离/120秒硬时限、最多10条自造样本、离线和真实接受、兼容/回滚与失败分支。P1/P2仅规划，未领取/未授权，不改变原业务门槛。

本次验证：只读重算11个缓存固定源SHA-256/Git blob、16份本地证据与4个缓存wheel SHA-256，均匹配；GitHub固定ref复核初始化/Monitor/账号工具blob。发现`excerpts.json`首条64–60倒置且仅换行，检查器空切片仍可能通过；实际导入54–57已从完整固定源码确认。原“片段匹配通过”不能当十条有效代码片段全通过。本轮不修代码/证据，后续P1先修。未运行项目CLI/测试/服务/真实UI或模型，70项仅保留为历史离线结果。

本次文档收口：五份归属文档写后重读；42个本地链接、115行表格列数与代码围栏检查通过，`git diff --check`通过。相对402ffd2的src/config/scripts/tests/vendor/锁/AGENTS/README/原PLAN/RESEARCH/IMPLEMENTATION_GUIDE/bootstrap与WX-01交接均无差异；未发现其他session修改。仅本地提交这五份文档，提交号见交付消息/最新git log；无remote/无推送。没有创建或操作本项目运行进程，已有忽略目录保持原样。

后续第一步：用户选择保留报告、可选P1或另行规划产品/传输后，下一session再核对Git/归属。读取本交接与独立计划即可继续；不自动执行P1/P2或领取03。真实稳定身份/真实@/图片来源与像素/项目关联ACK全部未验，pixels仍unsupported；只读观察成功也不能消除此差额。

以下保留实施轮检查点（`402ffd2`）：**代码/离线授权范围完成；真实观察未执行，生产门槛缺口保留**。session `WX-02-pyweixin-offline-20261023`，2026-10-23 00:23（Asia/Shanghai）开始。仅领取WX-02，未领取03；无UI/模型/发送授权。

已完成：固定上游 `8589baa049bb91d3a500602c167f07b2f8397a13` 的11份源码/分发/许可审阅；实际分发pywechat1271.9.8含pyweixin，不安装整包；4份Windows CPython3.12 x64可选原语wheel闭包/hash/许可（未安装）；单绑定窗口最小只读原语；metadata-only mock探针；默认inspect本地hash审阅；候选adapter拒绝生产收发；能力逐项报告unverified。详细结论和源码证据见[独立报告](../../../docs/WX-02-CAPABILITY-REPORT.md)、[vendor](../../../vendor/pyweixin/README.md)。

边界：没有导入上游初始化/UI包，没有调用真实窗口/键鼠/剪贴板/监听模式/截图/本机账号目录/数据库，没有登录/发送/模型/家庭SSH或QQ操作。源/轮子只通过公开网络读取到忽略cache；没有执行下载代码或安装/运行postinstall。未知身份不进业务store，普通@不补可信标记，当前图无句柄、pixels unsupported，按键结果unknown/none，production=false。

真实provider未接线，CLI仅inspect/mock；open_real_observation验证显式模式/后续授权声明/指定账号参考和窗口/自造样本/≤120秒≤10项后仍拒绝real_observation_closed。注入原语只经过fake UI验证；同步COM硬时限/真实账号与窗口绑定未证，不把源码存在写成observed。以后实际观察仍需用户另行指定对象并先补齐隔离provider，不因已有函数绕过；不得直接领取03。runtime原地复用/虚拟列表/突发漏报不能保证，列表移除/重建直接停止。

文件归属：src/wechatbot/transports/pyweixin_adapter.py、src/wechatbot/pyweixin_probe.py、src/wechatbot/__main__.py、src/wechatbot/status.py、tests/test_pyweixin.py、scripts/check_pyweixin_source.py、vendor/pyweixin/（含局部.gitattributes保存原始证据字节）、docs/WX-02-CAPABILITY-REPORT.md、README.md、PROGRESS.md、TASKS.md、本交接。WX-01源码快照/测试/默认锁与配置、原PLAN/RESEARCH/实施指引/旧交接未改。开始工作区干净，无其他session不明差异。

验证：

- `.venv/Scripts/python.exe -m unittest discover -s tests -q`：70/70通过，10.825s（原41+新增29）。同名/改名/普通@/自己消息在identity门槛拒绝，错窗/读中切换/pid复用/代际/列表重建/突发/上限/时钟/单图/副作用隔离有离线负例；保留投递/预算/工具隔离回归。
- `.venv/Scripts/python.exe scripts/check_pyweixin_source.py --source-dir cache/wx02/upstream --wheel-dir cache/wx02/wheels`：历史命令返回通过，11上游文件Git blob+SHA-256、16本地证据、4wheel字节hash匹配；片段区间质量缺陷见本次复核，不能按十条有效片段全过解释。未安装/导入/执行上游。
- `.venv/Scripts/python.exe scripts/check_snapshot.py`：原63文件、既有2处受控差异、3工件hash通过，未执行工件。
- `git diff --cached --check`通过；37个本任务Markdown本地链接有效；16份证据的暂存Git blob hash与工作区一致。局部attributes仅对下载原件保留字节/原始空白，本地manifest归一为LF，避免检出后hash漂移。
- inspect/probe/mock在禁止UI/runner导入、socket/Popen的独立进程通过；observe CLI拒绝，real API关闭；篡改证据检测通过。没有真实客户端/模型/接受测试。

交付：仅本地 `codex/bootstrap` 检查点；提交号见git log与交付消息，无remote/不推送。只提交本任务文件，忽略cache保留公开上游/4wheel；既有.venv/runtime/state保持原样，无config/local/secrets。根PROGRESS/TASKS双向索引已同步。

剩余：原实施范围已交付；本次追加证据区间待修项已规划但未实施。真实账号/会话/发送者/消息稳定ID、真实@、当前图绑定像素、关联发送接受和UI硬超时都未证，WX-02真实阶段未完成。现有合同下不能启用生产或认定WX-03条件通过。涉及产品/传输边界的缺口仍由用户另行选择；不自动换iLink/Hook/付费协议/旧客户端/OCR、放宽黑名单或全回复。等待用户新指令，不自动登录/启动/领取新任务。
