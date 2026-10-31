# 当前实施入口：WX-AKASHA-ALL

2026-10-31 已领取 WX-AKASHA-ALL，正在按[完整合同](AKASHA-IMPLEMENTATION-PLAN.md)实施/部署。当前使用方法见 [README](../README.md)，检查及真实状态见[实施报告](WX-AKASHA-ALL-REPORT.md)和[实施交接](../tracks/tasks/WX-AKASHA-ALL/HANDOFF.md)。不再提交另一份实施计划或重复领取任务；账号向导/真实会话由操作者配合，之后在同一任务继续接通并交用户实测。

下方所有wxauto分段/ALL指令均为历史，不能再领取或覆盖当前合同；旧CLI缺模块故障保留，路线暂停。

---

历史更新：WX-MIG-ALL曾实现并交付，按[README](../README.md)由用户实测；[当前交接](../tracks/tasks/WX-MIG-ALL/HANDOFF.md)。下方旧分段指令留作历史，不再逐项领取。

# 历史wxauto medium实施指令（当时：gpt-6.1-sol）

## 2026-10-30：一次WX-MIG-ALL批量迁移

使用[唯一可复制medium指令](../tracks/tasks/WX-MIGRATION-PLAN/MEDIUM_START.md)，详细合同见[统一计划](QQ-TO-WECHAT-MIGRATION-PLAN.md)。旧MIG-01/02/03已合并，不再逐项停下来；文字/人设/模型/短期上下文/本机控制/原生联网/schema2记忆同轮准备，最后交用户实测。

用户确认禁止过度防御性编程、先能用。账号已准备且自报登录微信4.2.0.11；先测一个指定群，接受换版，不重复问意愿。免费配套按统一计划准备；旧安装器文件元数据差异不作为永久阻断，用户完成正常换版/登录。真实群名和发送者只入本机secrets。

后续统一sol/medium，直接main，不建任务分支。当前为规划，未领取WX-MIG-ALL、未操作微信或模型；用户提交上述指令后才实施。

## 历史复制指令（保留依据，不能覆盖上方现行合同）

下方26—28日阶段说明/版本/分支及单次挑战次数属于当时合同，不再要求先重复执行WXA-02再领取WXA-03，或拆三次迁移。实际新入口与用户实测范围从30日统一计划读取；旧真实结果和未决记录保留。

返回[PROGRESS](../PROGRESS.md) / [PLAN](PLAN.md) / [调研](RESEARCH.md)。用户自行选择medium，每次只领一项。无需为已授权离线实施中的普通实现细节重复确认。

2026-10-26更新：WX-01及WX-02离线部分已交付，下文保留历史复制指令，不重复领取。最新[选型](../tracks/tasks/WX-FRAMEWORK-DECISION/HANDOFF.md)推荐wxauto4免费版，先核客户端兼容、再规划单会话文本收发、最后接模型，不要求完整源消息ID/服务端回执先于任何人工监督试用。25日唯一Hook/一律冻结的决定已修订。本轮仅调研与规划，没有授权安装/真实窗口动作/发送/模型或领取WX-03；旧指令不能直接用于新路线，后续具体实施仍由用户指定。

已收到版本答复：当前微信4.1.15.13，用户接受换版；按wxauto4免费版41.1.7＋微信4.1.8.107规划准备，不再把换版意愿列作待确认项。客户端更换尚未执行，进入明确实施任务后再按该任务范围操作。

## 2026-10-27既有试用合同：01已交付，02/03真实范围后置

2026-10-27详细规划已写入[wxauto4实施计划](WXAUTO4-IMPLEMENTATION-PLAN.md)，由[当前任务交接](../tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md)管理。按顺序每次只执行下面一个文本块。第一项不需要真实会话名；后两项的占位内容由用户填齐，不能由agent猜。用户自行选择medium，不自动切换或声称检测到设置。

2026-10-28已按用户新决定将全部后续实施指令统一为gpt-6.1-sol/medium；Terra不再是本项目实施选择。该选择指开发agent，机器人后端仍按计划使用CodeBuddy。下方01保留作已交付合同，不能再次执行；真实02/03须用户另选。

```text
你是gpt-6.1-sol/medium。请在E:\CodexWS\WeChatbot只领取WX-WXA-01：实现wxauto4最小试用工具及离线验证，完成后停止。

先读AGENTS.md、PROGRESS.md、tracks/tasks/WX-WXAUTO4-PLAN/HANDOFF.md、TASKS.md、docs/WXAUTO4-IMPLEMENTATION-PLAN.md第1—5节和本指令。读取当前Git HEAD/diff；基线是包含该详细计划的文档提交，不能回退到旧a66319d丢掉选型更新。按需要建codex/wxauto4-trial-kit分支。修改前登记session、Asia/Shanghai时间和实际文件归属，首次建立tracks/tasks/WX-WXA-01/HANDOFF.md并同步PROGRESS/TASKS、写后重读。保留其他session/用户修改。

配套已定为wxauto4免费版41.1.7＋微信4.1.8.107；用户现用4.1.15.13并已接受换版，不再询问换版意愿。本项只允许在本项目Python3.12 x64环境准备可选依赖及离线运行，不下载/安装/切换微信客户端，不import或构造真实WeChat，不观察窗口、操作键鼠剪贴板、登录、发送、SSH或调用模型。

按计划只新增薄封装src/wechatbot/transports/wxauto4_adapter.py和试用入口src/wechatbot/wxauto4_trial.py，加test_wxauto4_trial.py、合成绑定示例及vendor/wxauto4/manifest.json；只记录wheel元数据/hash/公开合同/许可位置，不提交wheel、不反汇编、不改上游核心或选择器。pyproject/uv.lock加入Windows可选extra并仅锁必要依赖；基础mock安装不强制wxauto4，不全局重装或升级无关固定依赖。README/报告/任务交接与入口同步。

inspect与mock不能import wxauto4，实际流程通过工厂/时钟替身测试。live命令单独显式开启，留到WX-WXA-02再运行。用ChatInfo/GetAllMessage/SendMsg三个免费公开业务方法；首试只操作用户已打开的一个会话，不用ChatWith/GetSession/Plus监听/自动回复/联系人/历史数据库接口。微信初始化参数按固定包公开合同处理，未知返回归unknown，不能靠对象bool假装微信已接受。

实现TrialBinding/TrialMessage和单owner的最小试用台账：昵称仅显示名、UI ID仅本次周期、production_eligible=false；不伪造NormalizedEvent或放开旧Gate。初始快照只建基线不触发，既有正文不打印/落盘/送模型。默认每2秒检查，最多120秒/10条候选，只消费指定测试者的一条新自造挑战文本；self/system/非文字/其他人/试用黑名单先拒绝。切窗、ID重建、超时或歧义则停。SendMsg前复核当前会话，恰好调用一次且不传who，不补发、不拆泡。先落盘与消耗次数再副作用；异常/取消/未知返回和重启不重放，未决记录不因换trial编号自动解除。过程状态和ACK等级分开，框架本地成功不解除未决；操作者确实看到后可标completed_observed，不伪造服务端ACK。日志只封闭元数据，合成输入验证无隐私泄漏。

验证实际调用计数和状态转移，覆盖旧基线/新消息/重复/黑名单/错窗/超时/上限/取消/unknown/重启未决；不要写只照实现字段断言的测试。跑新增针对性测试及现有全套unittest一次、scripts/check_snapshot.py、inspect/mock和git diff --check；测试数按实际结果，不沿用历史70项作本轮通过数。固定runner/旧默认配置/QQ仓库不改，不接模型、不做OneBot/AstrBot桥或功能复刻。

更新docs/WX-WXA-01-REPORT.md和HANDOFF/PROGRESS/TASKS，写明已实现、离线通过、真实全部未验及实际live命令。沿用户Git授权，只stage/commit本任务检查文件；origin应为用户已授权建立的https://github.com/hann-8/WeChatbot.git，核对后普通push并核HEAD=实际远端分支SHA，不force或借QQ地址。提交后停止，不领取WX-WXA-02、不实际操作微信。
```

## 后续单独复制：WX-WXA-02，客户端与一次文字试用

此块只在用户发出实际实施指令并补齐对象后使用；填写行为不是再询问“是否同意换版”。

```text
你是gpt-6.1-sol/medium。在E:\CodexWS\WeChatbot只领取WX-WXA-02，完成后停止。先读AGENTS/PROGRESS/TASKS、WX-WXA-01交接和实际报告、docs/WXAUTO4-IMPLEMENTATION-PLAN.md第3—6节；核对HEAD/diff，登记session/时间/文件并首次建立本项HANDOFF及入口链接，写后重读，保留他人修改。

本项授权准备配套微信4.1.8.107，并在一个指定会话做基本文字试验：本地账号别名=<填写>；类型group或friend=<填写>；准确会话显示名=<填写>；测试发送者=<填写>；试用黑名单=<填写，空时写空>；新自造输入/输出=<填写>。仅0模型、最多120秒/10候选和一次SendMsg；这里不授权其他会话/自动群回复。真实绑定写本项目secrets忽略文件，报告只用代号。缺目标时先完成可独立准备部分，再一次收集缺失项，不猜联系人。

用户现用4.1.15.13且已接受换版。本任务可下载/校验计划内客户端工件，检查摘要、Authenticode发布者/状态与文件版本后按正常安装流程准备；关闭当前客户端、系统交互及扫码登录由操作者完成。不自动卸载/删除聊天数据、不读微信数据库/账号目录/密码/密钥、不绕登录限制、不改全局设置/启动项、不按进程名kill微信。安装若实际要求删数据或其他未涵盖动作，停那个动作并说明，不再次泛问换版意愿。

先按WX-WXA-01报告核可选包及实际命令。由操作者手动打开指定会话，试用期间不切其他聊天。读取当前已加载消息只为RAM内UI ID基线，不打印/存旧正文、不拉更早历史；基线建立后由约定亲友发新自造文本，仅消费这一条。self/system/非文字/其他发送者/试用黑名单不触发。框架在该指定会话所需焦点/界面/剪贴板动作包含在本次试用范围，项目不另写键鼠发送器。目标变化/ID重建/账号疑变/窗口歧义立即停，不自动恢复。

发送自造测试文字前复核ChatInfo，一次SendMsg且不传who；没有可靠返回即unknown，不补发、不撤回、不换trial编号再试。框架本地报告与操作者在正确会话/对端看到分别记录，不冒充服务端ACK。文件传输助手可作另行明确的出站自检，不能将自己消息当亲友新入站验收。已有未决先处理其观察记录，不能删台账重试。

报告具体版本/兼容及接收、调用发送、本地返回、人工观察各状态，失败也正常收口；不反复换版本或改框架/买Plus。同步本任务报告/HANDOFF/PROGRESS/TASKS并只提交已检查文件，有明确remote才push核SHA。结束不接模型、不领取WX-WXA-03、不做常驻/多群/图片。
```

## 后续单独复制：WX-WXA-03，一次CLI模型回复

```text
你是gpt-6.1-sol/medium。在E:\CodexWS\WeChatbot只领取WX-WXA-03。先读AGENTS/PROGRESS/TASKS、WX-WXA-02交接/报告、docs/WXAUTO4-IMPLEMENTATION-PLAN.md第4—6节及本指令，登记session/时间/文件并首次建立本项HANDOFF/双向链接，写后重读，保留现有差异。

前提是该目标最小收发已经实测且无未决记录；不要求先有服务端ACK、稳定wxid或真实@。本次明确目标/测试者=<填写或明确沿用WX-WXA-02本机忽略绑定>；本次新的自造输入=<填写>。本项授权离线接线后在这个人工监督会话做最多一次真实CodeBuddy生成和一次纯文本发送；失败/unknown消耗次数，不补跑、不自动推进常驻运行。

按计划复用本项目固定InputBudget/create_runner/纯文本过滤/工具MCP隔离/清理，在model_facade.py增显式CLI试用工厂或TrialCliModel，复用共用函数而非复制runner；保留原ModelFacade默认要求离线替身的行为。试用输入只为选中的新测试纯文本，history为空，视觉ContextVar清空，不伪造生产NormalizedEvent、不放开旧Gate/真实@、不改qqbot_gateway快照或QQ环境。CodeBuddy固定deepseek-v4.1-flash，一次尝试、串行、既有预算/超时/清理，不换账号/后端/模型，不买额度或接Ollama真实连接。

先验证本项目runtime/cli的锁定工件、工具隔离、清理状态；健康检查0生成，缺工件/认证/额度/握手能力则报告，不静默走别的路线或从QQ复制凭据。必要准备只使用现有prepare_cli及明确给定的本机匹配工件，不全局重装。模型意图和次数在生成前落盘，崩溃不重生成；模型/清理unknown不清账。新测试者/黑名单/会话检查均在生成前完成，旧可见消息不交模型。

先用真实runner底层替身做从试用入口到生成/过滤/同目标发送的离线闭环，运行受影响回归及snapshot/diff检查。真实尝试只针对上述新自造输入，最多一次生成，输出一条自然纯文本且≤500字符；超出/目标变化/unknown本次不发，不截成多泡、不改who找新目标。发送前复核当前会话，一次SendMsg。分别记录生成、发送调用、框架报告和人工观察，不把UI返回当服务端确认，不写持久对话历史。

更新本项报告/HANDOFF/PROGRESS/TASKS，列已实现/离线/真实证据及限制；只commit已检查文件，明确remote才push核远端SHA，不force。结束即停，不做图片、free、多群、长期记忆或24h运行，不自动领取下一项。
```

## 历史指令：WX-01离线核心（已交付，不重复领取）

```text
你是gpt-6.1-sol/medium。请在E:\CodexWS\WeChatbot开发，只领取WX-01。
先读本目录AGENTS.md、PROGRESS.md、tracks/bootstrap/HANDOFF.md、TASKS.md、docs/PLAN.md和docs/RESEARCH.md。核对本目录已有文件和git状态；登记WX-01的session/开始时间/涉及文件，建立该任务HANDOFF并连回PROGRESS/TASKS，写后重读，保留所有用户/其他session修改。

按PLAN做独立Python3.12项目离线骨架、五份中文逐参数配置模板/loader、NormalizedEvent/能力分层/严格入口/当前目标/队列/有限历史/投递状态机/mock适配及只读状态。默认transport=mock、enabled/sends=false、授权群空、私聊关闭/白名单空、mentions、single，所有新增媒体/联网/记忆能力关闭。可信身份→黑名单→授权→窗口/材料/模型/历史的顺序不得改变；昵称/临时UI ID/正文hash不算稳定身份，真实@未知不触发群生产。

按PLAN从QQ固定已提交基线dd9373029412137023124751d75883824122c784导出已跟踪qqbot_gateway源码及必要公开能力/锁文件，在新root独立保存并记录逐文件manifest；禁止复制QQ config/local、secrets、state、runtime、logs、历史或图库，禁止editable/软链/连接QQ gate或模型端口。不要修改QQ仓库。公开锁若含QQ绝对路径必须按新root正确重定位并验证工件，不能执行QQ runtime或全局重装CLI。只在新的model_facade复用runner/预算/工具隔离/清理语义，不运行要求QQ身份的旧入口，不在QQ做共享核心重构。

本轮不安装/导入/操作pyweixin、微信或OpenClaw，不读微信数据库/本地账号目录，不登录、不触碰UI/键鼠/剪贴板/防睡眠、不SSH/发消息/调用真实模型。只用自造身份/文本和实际runner底层替身，完成从gate到mock投递确认及历史的真实业务离线闭环。微信默认CodeBuddy深度/原生窗口按现有能力处理，家庭模型只保留空连接模板，不读取/复制QQ家庭秘密或自动换模型。

验证未授权/黑名单/私聊关闭均在模型/材料/新增历史前拒绝，普通@与真实@区分、同名/改名/错账号/旧代际、稳定ID去重、同文不同消息、回环、取消/部分输出/unknown不重放、纯文本/工具隔离、配置root和端口/状态独立。ACK等级要如实，不把UI按键返回当确认。受影响检查通过后不要无故扩大测试。

更新README、独立报告、WX-01交接/TASKS/PROGRESS，区分已实现/离线通过与所有真实能力未验。可初始化本地Git，默认codex/bootstrap分支，只commit本任务审阅文件；本项目尚无remote，不创建或臆造远端、不把QQ地址拿来push。报告本地提交号和保留差异，结束不自动开始WX-02/真实验证。
```

## 历史指令：WX-02候选接入/探针（已交付，不重复领取）

```text
你是gpt-6.1-sol/medium。工作目录E:\CodexWS\WeChatbot，只领取WX-02。
先读AGENTS/PROGRESS/活动HANDOFF/TASKS及docs/PLAN.md、RESEARCH.md、已完成WX-01交接。先登记并重读文件归属，其他任务修改保持原样。

按固定上游8589baa049bb91d3a500602c167f07b2f8397a13核对pywechat中的pyweixin，锁定真正需要的分发物/依赖与许可，封装必要UI原语，不使用AutoReply/全会话扫描/历史导出/系统监听模式/自动关闭微信。先完成mock和默认inspect工具，不导入有副作用的上游初始化，不执行实际UI调用。源码更新不自动跟随latest；所选版本需明确记录。

能力报告逐项区分稳定account/conversation/sender/message ID、显示名、UI runtime_id、可信真实@、当前图可得像素与来源、发送接受结果等级。不能由“函数存在”写observed/passed。真实UI入口默认关闭，必须显式观察模式及后续用户指定账号/已打开单会话窗口/120秒最多10条自造样本，0模型/0发送，不读真实历史/数据库、截图落盘或遍历其他会话。当前这段指令仅授权代码/离线，不自动运行真实观察。

如果只能获得昵称/临时元素/按键结果，交付identity_unverified/mention_unverified/delivery_unverified的明确报告，生产保持关闭。不要自动切iLink/Hook/付费协议/旧微信/OCR，不因门槛未过而放宽黑名单或改全回复。先完成独立可做部分；需要改变产品/传输边界的缺口回sol/max。

按PLAN的同名/改名/重连/虚拟列表/突发/普通@/自己消息/错窗/单图绑定和副作用隔离做有意义离线测试，保留WX-01投递/预算/工具隔离回归。同步任务交接/索引和独立报告，只提交本任务文件；没有用户给出的远端继续只做本地Git提交。结束不自动领取WX-03/登录/发消息/模型。
```

## 历史WX-03/04进入条件（不作为当前最小试用前置）

下文是原pyweixin生产路线的门槛，仅保留历史。当前wxauto4人工监督试用走WX-WXA-01/02/03及独立合同，不因缺稳定ID/真实@/服务端ACK一律禁止试用，也不据试用成功宣称原生产路线通过。

WX-03仅在WX-02已用实际证据证明所选会话的可信身份、真实@、新消息去重和可关联发送结果后领取；按PLAN第3节实现实际适配，默认仍不启用。若未达到，不能复制一条“继续完整实现”的泛化指令绕过结论，应将具体缺口交回max。

WX-04须后续明确：一个目标会话/哪些发送者、是否私聊开关、所选模型、总调用/发送次数与进程操作归属；文本首批最多2次生成、各一次发送，失败/取消/unknown占次、不补跑。图片按独立入口与所选原生质量/预算后再验，未验部分关闭。只在具体审阅结果后启用本机配置，不注册开机自启，不改变QQ实例。
