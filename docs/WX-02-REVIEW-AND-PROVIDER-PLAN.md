# WX-02 能力缺口复核与后续只读 provider 详细计划

返回 [PROGRESS](../PROGRESS.md) / [TASKS](../TASKS.md) / [WX-02 交接](../tracks/tasks/WX-02/HANDOFF.md) / [能力报告](WX-02-CAPABILITY-REPORT.md)。继承 [AGENTS](../AGENTS.md)、[原计划](PLAN.md)与[调研](RESEARCH.md)。

2026-10-23（Asia/Shanghai），session `WX-02-gap-review-plan-20261023`，20:02 开始。状态：**缺口复核与详细规划完成；下文 provider 全为待授权方案，未实施**。起始检查点 `402ffd201329f84278700dd3e89549fc3de23fa7`（`codex/bootstrap`），工作区干净、无 remote。文档归属仅本文件、能力报告、WX-02 交接、TASKS、PROGRESS；不得由本文触发真实观察或改变运行边界。

## 1. 结论与后续选择

固定上游 `8589baa049bb91d3a500602c167f07b2f8397a13` 的已审阅接口没有提供符合现有合同的 account/conversation/sender/message 稳定身份、入站可信真实 @、当前消息图像素绑定或关联发送接受结果。其账号路径还越过本项目允许的观察范围。现有资料不足以把任何一项提升为真实通过；这不等于断言微信客户端内部绝无这些能力。

**不建议继续以该上游推进生产适配；WX-03 条件未满足。** 下列选择交给用户，不自动执行：

| 选择 | 目的与出口 | 是否需要后续授权 |
| --- | --- | --- |
| A：停在当前缺口报告（建议） | 保留离线核心与 unverified，等待有明确身份/@/投递合同的新证据 | 本轮文档即可收口；无新增实施 |
| B：只做一次有界的 UI 元数据可行性观察 | 仅回答“指定独立窗口能否安全绑定、读到有限 UI 元数据、阻塞 worker 能否终止”；不能解决生产合同 | 先单独授权下文代码/离线包，再单独授权指定对象的真实观察 |
| C：重新选择产品/传输边界 | 例如用户选择其他产品入口、提供不同传输，或提出独立实验需求 | 回到规划并取得明确选择；本文不选择 iLink/Hook/付费协议/旧客户端/OCR，不放宽身份、黑名单或 @ 合同 |

B 的有限价值是排除本机 UI 树不可用、错误窗口附着和阻塞调用失控；没有必要为了这些结果继续开发自动聊天。即使 B 全部成功，仍不能领取 WX-03。若用户目标只剩“尽快实现亲友群自动回复”，B 不能提供足够收益，选择 A 即可。

## 2. 本轮核对范围、证据等级与 Git

已读 AGENTS、PROGRESS、TASKS、原 PLAN/RESEARCH/IMPLEMENTATION_GUIDE、bootstrap/WX-01/WX-02 交接及能力报告；本轮登记已写入并重读。历史规划中“目录仅文档”“WX-01 待实施”等是 2026-10-22 的阶段描述，当前状态以 PROGRESS 和实际源码为准。

- 起始 HEAD 为 WX-02 提交 `402ffd201329f84278700dd3e89549fc3de23fa7`，父检查点为 WX-01 `af04dcf`；该提交修改 30 个文件。`git status --short --branch` 显示工作区干净，`git remote -v` 无输出，工作根为本项目。后续只提交本轮五份文档，不创建远端、不推送。
- 只以 PowerShell/.NET 读取公开源码缓存并独立计算哈希，未执行项目检查器或测试：11 个固定上游文件 SHA-256 与 Git blob SHA-1 全匹配；16 份本地审阅证据、4 个已缓存 wheel 的 SHA-256 全匹配。这证明字节一致，不证明片段选取正确或真实能力成立。
- 通过 GitHub 只读连接器按完整 ref 复取 `__init__.py`、Monitor 相关段和 `get_current_wxid`；返回 blob 分别与 source-lock 对应。没有跟随 latest，也没有联网下载新的运行包。
- `70/70` 是 WX-02 交接记录的历史离线结果（原 41 + 新增 29），本轮未重跑、未生成新的通过计数。阅读测试只能证明其设计覆盖范围。真实 UI/登录/账号目录/数据库/截图/发送/模型/家庭 SSH 均未发生。
- 新发现审阅缺陷：`vendor/pyweixin/excerpts.json` 第一条 `__init__.py` 为 `start=64,end=60,text="\n"`，而该文件仅 60 行。`scripts/check_pyweixin_source.py:30–33` 未校验行区间，空切片仍可能匹配；因此原“片段原始行匹配”不能解释为十条有效代码证据全部通过。实际导入语句在第 54–57 行，本轮通过完整固定文件和远端 blob 重新核实，结论仍成立。本轮不改 evidence 文件/检查器/测试；修复列入可选后续离线包。

本文使用四种互不代替的证据：`source_review_only`（固定代码事实）、`offline_synthetic`（历史 fake/mock 通过）、`real_observed_metadata_only`（未来局部 UI 元数据观察）与产品接受。当前只有前两种；没有真实观察或完整接受。

## 3. 需求与非目标

保持个人微信亲友聊天的原产品目标，但在传输门槛未证时停止业务接入。可选 B 仅建设隔离观察器，能报告失败也是完成出口；不要求它产生 NormalizedEvent 或使能力通过。

需求：精确绑定操作者指定的一个已打开独立聊天 HWND；进程创建身份、root/list runtime 与前台窗口前后复核；阻塞 COM 调用留在自建可终止 worker；整个批次不超过 120 秒、最多 10 条人工自造样本；报告只有封闭元数据，默认 inspect/mock 完全无 UI 副作用。

非目标：不自动登录/开窗/导航/改名/发送或操作键鼠剪贴板；不读取联系人、账号目录、进程内存映射、数据库、真实历史、消息正文、消息 Name/Value/TextPattern、图片或截图；不调用 Monitor/AutoReply/媒体保存/系统监听模式。不要以“观察”取得生产账号绑定或传输授权，不建设生产 receive/send，不改 gate/router/store/model_facade/QQ 快照或运行配置/人设，不启停业务服务/防睡眠/自启。不调用真实模型或家庭 SSH。

## 4. 决定性代码证据

以下位置均基于固定上游，不是本机观察。上游代码只读，不导入执行。

| 证据 | 已核实的行为 | 对合同的影响 |
| --- | --- | --- |
| [初始化第54–57行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/__init__.py#L54-L57)、[Uielements第44–45行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/Uielements.py#L44-L45)、[Config第181–228行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/Config.py#L181-L228) | 包导入链加载自动化/工具/设置；模块级配置读取可枚举命令行、读注册表 | 不能用导入整包后关开关的方式实现只读探针 |
| [Tools第166–193行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/WeChatTools.py#L166-L193)、[第294–305行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/WeChatTools.py#L294-L305) | 枚举 Weixin 进程并从 memory_maps 的 MMKV 路径推断账号目录，再取 wxid；源码提示多账号缓存 | 超出本项目允许范围，且不证明指定窗口属于当前所选账号；禁止调用 |
| [Tools第897–908行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/WeChatTools.py#L897-L908)、[Monitor第4309–4334行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/WeChatAuto.py#L4309-L4334) | session automation_id 带好友名称；发送者由显示名/正则拆文本 | 同名、改名与黑名单不能据此得到可信稳定身份 |
| [Monitor第4360–4402行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/WeChatAuto.py#L4360-L4402) | 对可见 CheckBox runtime 去差集；读正文/媒体路径，开启监听模式；图片计数后按数量导出，默认关窗口 | runtime 仅 UI 对象标识；不能直接调用该监听器，也不能把数量对应当当前图绑定 |
| [Messages第3365–3418行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/WeChatAuto.py#L3365-L3418) | 依备注找会话、剪贴板/按键发送，返回类型 None；长文还可能转 txt，末尾可关窗口 | 没有 trace 关联接受结果；也不满足纯文本/冻结目标/不关日常窗口边界 |
| [Messages.save_media第4100–4180行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/WeChatAuto.py#L4100-L4180) | 打开媒体历史与预览、捕获预览图片到文件、向前翻页 | 不是当前入站原件接口；本轮及最小 provider 均禁止复用 |
| [Tools.is_my_bubble第420–437行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/WeChatTools.py#L420-L437) | 捕获气泡图，再按像素/位置作启发式判断 | 不构成可信 sender_is_self；最小 provider 不调用 |
| [出站 @ 辅助第284–323行](https://github.com/Hello-Mr-Crab/pywechat/blob/8589baa049bb91d3a500602c167f07b2f8397a13/src/pyweixin/utils.py#L284-L323) | 输入成员昵称并操作 MentionPopover | 出站选择成员与入站真实 mention 元数据不同，不能据函数名声称真实 @ 已支持 |

`utils.py` 是本地公开缓存的补充静态阅读，不在原 11 文件 source-lock 中；其行为只作辅助线索，不提升原锁的覆盖计数。关键结论由已锁 Monitor/Tools/发送接口直接支持。最小 provider 如依赖新源文件/接口声明，须后续显式登记来源和 hash，不自动纳入当前已验集合。

[Microsoft GetRuntimeId 合同](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getruntimeid)明确 runtime 标识只用于 UI 比较，可随时间复用。因此多读几次、改名不变或人为重开窗口，均不能把它升级为源站消息 ID；AutomationId 也不能仅凭形似 ID 获得微信实体身份含义。

## 5. 缺口分类与观察能回答的范围

| 能力 | 当前证据与状态 | 最小只读观察的出口 | 缺口归属/继续条件 |
| --- | --- | --- | --- |
| account 稳定 ID + 所选账号绑定 | 目录推断不可调用；operator reference 只是声明；unverified | 只能确认所给 HWND/PID 仍一致，不确认登录账号 | 需要被允许的可信账号数据源与窗口对应合同 |
| conversation 稳定 ID | 标题/显示名/名称型 automation_id；unverified | 独立窗口局部对象能否固定，不能证明群/私聊实体身份或账号归属 | 上游/传输合同；主窗口聊天切换更不能用同 HWND 冒充同会话 |
| sender 稳定 ID / 黑名单 / sender_is_self | 昵称拆分、像素启发；identity_unverified / self unverified | 不读取正文或头像，不解析发送者；同名/改名仅离线反例 | 必须先获得可信稳定发送者；不能靠手工表、昵称 hash 或账号声明补齐 |
| source message ID / 新消息去重 | runtime_id；stable_message_id=unverified | 能观察可见 runtime 新增/消失/重建；不能确认源消息个数、无漏报或跨重启去重 | 需要稳定源消息 ID；原地 runtime 复用仍可能不可察觉 |
| 入站可信真实 @ | 审阅接口无结构化 mention 事实；mention_unverified | 元数据 profile 不读正文/@ 标记；无法对真实 @ 与字面 @ 作语义验收 | 上游能力/产品触发合同；不能改全回复/关键字或把 UI 可点击标签当 trusted mention |
| 当前图片事件 | refer bubble 类也可能含引用/视频；unverified | 可报告出现 refer 类 UI 对象，不能确认图片事件 | 需消息类型与来源的可信关联 |
| 当前图像素/材料句柄 | 上游为历史预览截图；当前本项目 pixels=unsupported、handle=null | 不取图，不创建句柄；样本图只作操作者自造的 UI 形态样本 | 图片入口独立接受：可信消息绑定、原件来源、RAM 有界规范化等须另规划；不自动扩成截图或最后 N 图 |
| 关联发送接受/ACK | None/按键返回；delivery_unverified、unknown/none | 0发送，无项目提交 trace；观察人工气泡不能验证本项目投递 | 需要可靠接受语义及与本次提交的无歧义关联；只读批次无权补做发送测试 |
| 绑定与硬时限 | fake wrapper 通过；真实 provider 未接线 | 可局部证实目标树可读/worker 退出时刻，或明确失败 | 工程可观测问题；成功也不替代上述传输合同 |

观察成功只能写 `real_observed_metadata_only` 并列出实际做过的操作；观察没有发现某字段，不能写“客户端一定没有”。当前资料未提供合同的能力全部保留 unverified；当前本项目未提供图像素则如实保持 unsupported。任何需要新增属性、个人资料页面、标识语义探查或发送动作的方案，先回规划/用户选择，不临时扩大本批次。

## 6. WX-02 实现边界与 70 项离线结果的实际含义

| 本地文件/范围 | 已实现或历史离线证明 | 尚未完成/不能推断 |
| --- | --- | --- |
| `transports/pyweixin_adapter.py:23–44` WindowBinding | 校验人工注入的声明、PID/创建时间/HWND/root/list runtime/epoch 的基本格式 | 没有真实采集这些字段；account_reference 不经账号核实 |
| 同文件 `80–118` BoundWindowPrimitives | 注入 wrapper 仅读 root/list/CheckBox runtime/class；读前后检查；fake 验证错窗/PID复用/列表变化拒绝 | 没有 real provider/Windows API 绑定；同步 COM 无隔离或强制超时；`children()` 在总量检查前已完成枚举；同 root/list 原地换聊天无法据此识别 |
| `pyweixin_probe.py:56–125` | mock 基线丢弃、有限差集、预算/重复/列表移除/时钟边界；ProbeSession 只接受精确 MockPrimitives 类型 | 120秒是调用前后查时钟，挂死调用不会返回；10是 new runtime 采样数，不是可信消息数；原地复用/瞬时切换仍不保证被发现 |
| adapter `121–131` / `140–168` | real API 固定拒绝；receive 拒绝；send_text 返回 failed/none、不调用任何 UI；keypress 示例 unknown/none；无图句柄 | 不能把当前 send_text 的 failed 当真实发送失败证据，因为从未尝试发送 |
| `__main__.py:7–24` / `status.py:5–13` | CLI 仅 inspect/mock；inspect 只检本地证据，production=false | 没有 observe CLI/真实账号发现/服务启动/真实模型 |
| `capabilities.py:23–26`、`gate.py:25–62` | production_eligible 恒 false；真实通道固定关闭，身份先于授权/材料/业务 store | 配置标 true 或伪造 capability 不提供真实资格；本文不修改这些保护 |
| `tests/test_pyweixin.py:68–298` | 新增29项 fake/mock失败路径、入口副作用隔离、候选拒绝、证据篡改检测；历史总70包含原41 | 同名/改名/@/自己消息测试验证“统一因身份不足拒绝”，没有验证微信侧正确解析它们；无真实 COM/客户端/图/投递证据 |

现有只读原语与 mock 已完成其离线工作，不应称“真实 provider 已实现”。后续若有 provider，必须新建独立观察路径，不能删除 ProbeSession 的 mock 类型检查后直接塞真实对象。

## 7. 可选 B 的行为合同与最小结构（待授权）

建议在 WX-02 内作为后续工作包登记，名称 `WX-02-P` 仅用于本文引用，**不是已领取任务，也不是 WX-03**。分两次授权：P1 代码/离线；P2 指定对象真实观察。P1 完成不自动获得 P2。

最小链路：`显式一次性请求 → 纯参数校验 → supervisor/自建 Job → worker 内 COM 初始化 → 指定 HWND 的 root/list 元数据 → 有界 IPC → 父进程封闭报告`。不接 router/gate/store，不构造 NormalizedEvent，不使用 sender_is_self 或 mention_self 的猜测值。

### 7.1 明确窗口绑定

1. P2 用户需另行指定：本人声明的账号别名（本批次自造标签，不是真实 ID）、一个已由操作者打开的独立测试聊天窗口、准确 HWND、目标 PID/进程创建标记、自造样本范围和本次≤120秒≤10条上限。没有数字窗口句柄就先停在缺参数；不能遍历桌面或按标题找群。PID/创建标记若由后续指定的单句柄准备动作读取，必须计入本次期限并仅访问该 HWND 对应 PID，不能枚举微信进程。
2. root 仅从明确 HWND 取得；`IsWindow`、`GetWindowThreadProcessId` 与目标进程 `GetProcessTimes` 复核，进程仅给查询权限，无读内存/账号路径权限。HWND/PID/创建时间任一不符就拒绝；不要用“进程名像微信”替代绑定。root runtime、消息 List runtime 由 worker 首次限定读取后冻结，不接受 caller 伪填为已验证。
3. 默认仅允许固定源码中出现的独立窗口类 `mmui::ChatSingleWindow`（Tools 第1453行为源线索），主窗口 `mmui::MainWindow` 拒绝。该类名仍不是会话 ID；目标账号和单聊天归属只按操作者声明记录。若当前客户端结构不同，报告 profile 不支持，不自动改主窗口方案。
4. List 定位仅使用 root 下明确结构路径、固定 control_type 与三种已审阅界面标签之一（消息/Messages/訊息）；固定标签可在限定控件上比较，不读取窗口/会话/消息名称。后续离线实现要给结构 profile 明确深度≤8、累计节点≤64；仅逐层原始子节点遍历，避免过滤walker在内部无界扫描，不得从桌面/兄弟窗遍历，不用模糊 best_match/全后代 FindAll。多 List、路径未知、预算耗尽或需联系人/会话列表辨认，全部拒绝。结构路径尚未经真实观察，不能在本轮编造一条已通过的路径。
5. 为不接触真实历史，P2 要求操作者指定新测试会话，首次基线消息项数必须为 0；非空直接停止，不作全文核对/滚动/旧记录读取。若客户端新会话也产生非空消息项而无法在该 profile 内区分，保持失败，不调用历史清空或自动删记录。
6. 每次读前后重查 HWND/PID/创建标记/root/list runtime/前台 HWND。窗口销毁、焦点离开、权限变化、列表重建/移除、声明 epoch 改变或进程重启都终止；不得自动重绑、激活、恢复窗口或重启批次。前后相等不能排除调用内部瞬时切换，应保留此限制，不宣称原子快照或可信账号/群绑定。

### 7.2 provider 的读取白名单与依赖

只允许目标原生句柄/指定 PID 创建时间、root/list/item 的 runtime ID、control_type、class_name，以及固定消息 List 标签的等值比较。新增样本仅保留 runtime/class 元数据；runtime 只在 worker 的本批次 RAM 内去重，日志/报告不输出 raw runtime、HWND/PID、创建时间或其 hash。

每快照最多处理32个消息项，用惰性逐项遍历；可额外读取一次“是否还有下一节点”来检测溢出，不取第33项属性，不预先建全量 children 列表。累计最多10个新增 runtime，任何突发超过剩余预算整批停止，不能切前10条当完整消息观察。未知/重复 runtime、类名不符合封闭集合、节点尺寸/层级/IPC 超限，停止并丢弃本帧。不能将这些计数命名为微信真实消息数。

依赖首选限于标准库 `ctypes` 的句柄/进程控制，加现有已锁 `comtypes==1.4.13` 基础模块与明确审阅的最小 UIAutomation COM 接口声明；不导入 pyweixin、pywechat 或 pywinauto 包初始化，不使用其 root 默认发现、自动化 wrapper/自动回复。仍属原 Windows UIA 路线，不宣称原上游有新接口。

最小 COM 接口声明须逐项对照微软 Windows SDK/官方接口的 IID、vtable 顺序、参数/SAFEARRAY/位数和释放所有权；记录实际用到的官方依据，做假指针/ABI/资源释放验证。仅包含 ElementFromHandle、限定 TreeWalker/属性读所需定义；如实现不能在该小范围正确成立，交付 provider_unverified 并停止，不现场扩用全套 UI 自动化。

已缓存 wheel 的静态阅读发现：pywinauto 的 `uia_defines.py:60` 会 GetModule；comtypes 的 `client/__init__.py:16` 会先选择生成目录，`_code_cache.py:50–83` 可能创建缓存目录，`_generate.py:195–208` 可写生成代码。因此禁止 `comtypes.client`/GetModule 自动生成，不能靠导入后才设置 gen_dir 防止首次写入。基础 comtypes 导入也初始化 COM，必须仅在 worker 设定 MTA 后发生。P1 不安装任何 UI 包/不执行该导入；P2 若获明确安装授权，只在项目专属可选环境中按已有 hash 安装实际所需工件，不装 pywechat127 整包、不改默认 uv.lock/全局 Python、不运行全局 postinstall。基础模块的导入闭包还须后续静态审阅；若发现客户端生成缓存等隐式路径则拒绝而非放过。

禁止读取消息及非目标控件的 Name，唯一例外是前述限定消息 List 的固定界面标签比较；禁止 `Value/TextPattern/GetProperties/dump_tree/print_control_identifiers`、消息 automation_id、未审阅批量 cache request、截图/像素、缩略图、URL或文件路径；异常文本和对象 repr 不输出。类名仅将明确允许的原生类映射为 `text_like/refer_like/system_like/other` 封闭枚举，未知原生类停止，不能把任意字符串带出 worker。

### 7.3 阻塞隔离和120秒硬时限

父进程绝不执行 COM/UI 调用；worker 为本项目本次创建的隐藏子进程，记录创建句柄/时间/批次 nonce。使用 `CREATE_SUSPENDED` 创建，先加入本项目新建的 Job，设置 `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`、禁 breakaway、限制子进程数量，再恢复执行；Job 不得加入已存在微信或任何附着进程。Job 创建/分配/限制设置失败时，结束尚未恢复的自建子进程并拒绝，不降级成无法取消的线程。

[Microsoft Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)说明 Job 只管理被加入的进程，关闭最后一个启用 kill-on-close 的 Job 句柄可终止其成员；[AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject)也可能因环境/嵌套限制失败。必须检查返回值，不能假定当前宿主可用。

从 supervisor 接受请求、创建进程之前记单调 `t0`，启动/导入/绑定/基线/轮询/IPC/退出都共用总预算。默认总期限120秒，最后5秒固定留给终止确认，故正常观察最多115秒；用户可缩到10–120秒，不能放大。单次 RPC 最多2秒且不超过当前剩余工作时间；poll 间隔250ms、仅一条在途请求，未返回不发下一次。

超出单调用预算、取消、父端关闭、预算满或任一失配立即停止接受新结果，并对自有 Job 执行终止；最多等到 `t0+seconds` 确认 worker 进程句柄已 signaled、Job 活动成员为0，封闭管道与句柄。父进程等待用有界异步/轮询，不能被同步 pipe recv、无限 join、COM 清理或 stdout 满管阻塞。worker 不继承 Job 最后句柄，父端退出时 kill-on-close 才能成立。

进程终止依据是[TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject)，而不是 Future.cancel/asyncio.wait_for/thread.join 超时或 worker 返回后看时钟；CPU 时间限制也不能替代 wall-clock。COM 对象/指针不跨进程传递，worker 按 MTA 初始化，参照[微软 UIA 线程说明](https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-threading)。

应报告 `hard_deadline_verified` 的具体证据：父端计时、终止调用结果、worker退出确认、最大实际耗时；P1 的自造阻塞进程结果与 P2 真 COM结果分开记录。仅能保证终止本项目观察客户端，不能保证取消微信/Windows服务端内部已开始的处理；不得结束它们。操作系统调度或终止确认超过期限、终止失败、宿主不能用 Job 时，写 `hard_deadline_unverified/cleanup_unknown`、关闭后续观察入口；不在失败后再跑一次，也不声称绝对实时保证。未有本机自有阻塞进程退出证据前不允许触碰真实 UI。

### 7.4 IPC 与封闭报告

父子使用一次性本地匿名管道，不开监听端口/HTTP/socket，不用 pickle/unpickle；限定 UTF-8 JSON frame≤16KiB、总IPC≤256KiB、单帧≤32项与严格未知字段/重复键/类型/长度拒绝。运行请求/绑定 raw 值仅 RAM，经匿名管道传入，不放进命令行、报告或异常；无消息文本输入字段。返回 nonce/顺序号/状态/本帧计数，迟到或其他 epoch 的结果丢弃。

默认只将聚合结果输出 stdout；若用户另外要求保存，仅写本项目忽略目录 `state/observations/<随机run_id>.json` 的封闭报告，不保存原始快照。独立 schema `wx-ui-observation/1` 包含：source pin、provider代码版本、profile枚举、请求/实际耗时与计数、基线是否为空、绑定各项 match/mismatch/unknown、退出确认与终止状态、UI类别计数、停止原因枚举、证据范围/未验证项；账号/会话归属另列 operator_declared_unverified，不能混在窗口match项中。禁止原始昵称/账号/群/发送者、它们的 hash、消息正文、raw runtime/句柄/PID/路径、URL、凭据、traceback、像素。报告≤16KiB。

即使所有工程项成功，报告仍须固定：`production_eligible=false`、`business_receive_enabled=false`、`send_attempts=0`、`model_calls=0`、stable IDs/mention/self/ACK 各 unverified、image pixels unsupported、material_handle=null。`real_observed_metadata_only` 只表明实际读到了本节准许的属性；不得把它写成传输 observed/passed 或复用作 capability digest。配置或报告中的 `authorized=true` 永远不是人类授权。

## 8. 配置、默认值与生效方式（仅规划）

本轮没有改配置。P1 也不改现有五份 YAML、defaults/config loader、人设或本地配置；现有 `runtime.ui_observation.enabled=false` 仍由 loader 强制约束。观察功能使用独立的一次性命令/请求，不是后台服务开关。

| 拟定入口/参数 | 默认/约束 | 生效规则 |
| --- | --- | --- |
| 现有 `inspect` / `probe --mode inspect` / `probe --mode mock` | 不变；无 UI/worker/模型/网络/服务 | 保持兼容，只本地证据检查或 synthetic |
| 新 `observe-ui`（P1后才可能存在） | 默认不执行；非显式命令不导入/构造 provider | P1 未满足 Job/IPC/离线安全验证前入口继续 real_observation_closed |
| 一次性 request | 用户后续指定窗口数字句柄、目标PID/创建标记、自造账号标签与测试范围；不读账号绑定 secrets | 从 stdin 解析一次到 RAM；未知/重复字段拒绝，没有自动发现/默认目标 |
| seconds / samples | 默认120/10，只可缩到10–120秒/1–10条 | 冻结本次快照，不热加载；seconds包含预留5秒清理 |
| per_call_seconds / poll_ms | 常量2秒/250ms，可按剩余预算缩短 | 不提供放大上限的配置项 |
| profile / node limits | 独立单窗口、明确语言枚举；深度8/结构64/消息项32固定 | 不自动检测语言/读注册表，未知profile拒绝 |
| send / model / text / pixels / screenshots | 全部固定关闭，不能出现在可启用参数中 | observe成功也不能启用 |
| 持久化 | 默认 stdout only；保存需用户要求，固定忽略路径 | 不落盘 raw UI，也不写业务历史/去重/投递台账 |

停止、取消、超时或变更目标后旧请求失效，下一批必须由用户新指令给定范围；没有缓存授权、账号/窗口重绑或自动重跑。手动改 bot.enabled/transport/sends 不能触发观察，也不能满足生产门槛。

## 9. 涉及文件与后续任务顺序

以下文件是将来 P1 可授权的候选清单，本轮均未创建/修改。实施者先对照实际状态登记归属；若需越出清单修改核心/配置，先写明原因并回到规划。

| 文件 | 拟做内容 |
| --- | --- |
| `src/wechatbot/ui_observation.py`（新） | 纯参数/请求/封闭结果合同、绑定比较、预算；默认无UI导入 |
| `src/wechatbot/observation_supervisor.py`（新） | 自有Job/隐藏worker创建、时限/取消/IPC/退出确认；Win32函数惰性使用 |
| `src/wechatbot/transports/uia_readonly_worker.py`（新） | worker唯一真实UI入口、允许属性/节点上限、无业务依赖 |
| `src/wechatbot/transports/uia_readonly_interfaces.py`（新） | 小范围COM声明，来源/ABI/资源所有权说明；仅worker加载 |
| `src/wechatbot/__main__.py`、`pyweixin_probe.py` | 显式命令调度/分层报告；旧ProbeSession仍mock only |
| `src/wechatbot/transports/pyweixin_adapter.py` | 仅必要的观察入口关联/共享纯数据合同；production/send/receive保护不改变 |
| `scripts/check_pyweixin_source.py`、`vendor/pyweixin/excerpts.json`、`evidence-hashes.json` | 修正初始化片段为54–57，先校验1≤start≤end≤行数及非空有效片段；同步hash；原固定源码字节不改 |
| `vendor/pyweixin/README.md`/依赖说明 | 区分原4工件审阅闭包与真实provider实际所需comtypes；记录接口来源/导入审阅；不默认装包 |
| `tests/test_pyweixin.py`、`tests/test_ui_observation.py`（新） | 证据区间回归、观察合同/失配/溢出/阻塞/退出与默认入口隔离测试 |
| `README.md`、本计划/能力报告、WX-02交接、TASKS/PROGRESS | 操作/接受差额与会话归属，不预写真实通过 |

任务顺序与完成出口：

1. **本轮复核/规划**：五份文档一致并本地提交，到此停止。
2. **P1-1（须后续实施指令）证据修正**：无 UI 地修正倒置片段/检查器，新增反例；保持锁定源码，不扩大来源。
3. **P1-2 纯合同/进程隔离**：先用完全自造 worker 验证 Job、时限、退出、管道边界/默认入口；未通过不做真实provider解封。
4. **P1-3 最小provider源码**：只静态编写/审阅接口、单句柄遍历和属性白名单，用fake COM/原生函数验证；不安装依赖、不导入真实COM、不附着微信。真实入口受前置证据与后续人类指令约束，不能因代码存在运行。
5. **P1-4 离线回归与本地交付**：执行下一节验证，明确目前仍无真实能力；提交归属文件，停止。若只完成可恢复部分，交接具体失败项，不假称P1全过。
6. **P2（另批）一次真实元数据观察**：用户明确选择B，提供具体对象/动作并授权所需可选包安装时才执行；若尚无绑定参数、空测试窗口或可终止worker证据，停止。120秒/10条任一先到即终止，不自动补样本。
7. **复核P2报告**：只接受工程元数据的观察结果；保持身份/@/图/ACK缺口。WX-03仍未可领取。若将来出现新可信传输证据，另行规划其身份语义/接受级别与真实验收，不能从本包自动推进。

## 10. 离线验证计划（后续实施者执行，本轮未运行）

| 验证组 | 有意义的失败路径/接受标准 |
| --- | --- |
| 原证据审阅 | 倒置/越界/空白片段均失败；正确54–57可匹配固定源，锁与证据hash可复核；不把hash正确当代码语义通过 |
| 默认副作用 | 原inspect/probe/mock阻断UI/COM/runner导入、socket、Popen仍成功；缺UI包也能运行；新模块普通import不创建进程、不读UI |
| 绑定 | 错HWND/PID/创建时间/root/list、账号声明/epoch变化、前台离开、同主窗切聊天、重复/未知List、非空基线、读中变化全部停止；只能读绑定范围，name/text/profile/消息属性越权直接抛错 |
| 节点与样本 | 结构深度/64节点、32项、额外节点检测、累计10、突发超额整批拒绝、重复/移除/原地复用歧义；不得声称稳定ID或无漏报 |
| 时限与进程所有权 | 自造worker卡在导入/绑定/RPC/写管道/退出各处；缩短总限与单限验证父端按时终止并确认；父端异常/取消/Job分配失败/创建后恢复前失败/worker子进程拒绝/迟到帧均覆盖。只能结束本次创建句柄，无按名字kill路径 |
| Windows Job本机核对 | 后续P1仅创建无UI、无COM的 synthetic子进程，记录实际退出耗时/Job零成员；不创建业务服务、不附着其他进程。不支持Job则real入口拒绝；mock Job测试不能独自写本机硬时限通过 |
| IPC/报告隐私 | 超大/畸形/重复键/未知字段/错nonce/序列、stdout满管、异常对象含自造敏感字段均拒绝；无路径/身份/正文/hash泄露；白名单JSON无pickle |
| 兼容回归 | 原70项中现有行为继续通过；核心默认/mock/投递unknown/预算/工具隔离保留，观察0模型0发送0store访问，生产能力恒false |

建议后续命令（确认归属后执行，不授权真实UI）：`.venv/Scripts/python.exe -m unittest discover -s tests -q`；`scripts/check_pyweixin_source.py`（可加明确公开缓存source/wheel路径）；`scripts/check_snapshot.py`；原inspect/probe/mock的副作用隔离验证；`git diff --check`及文档链接。UI可选环境未安装时真实provider测试应明确 not_run，而非用skip计数包装完整接受。无需为本文档改动重跑代码/模型测试。

## 11. 真实观察验收计划与最多10条样本（P2另批）

P2前置条件：明确人类授权及目标数字句柄/窗口；操作者自行打开的独立测试窗口、所声明账号和测试会话；基线无消息；P1已证明Job退出、默认隔离与报告隐私；依赖仅项目内明确授权的锁定工件；确认不会由本项目发送/改UI/读正文。缺一项就交付未执行原因，不为取得参数而扫描账号/会话。无法确保测试窗口只出现自造样本则不运行；运行后出现非预期结构/数量立即停止。因为缺可信sender ID，程序不能独立证明每次新增确由指定人发送，这一限制须随报告保留。

样本由操作者或后续明确授权的人手动产生，不由本项目控制微信；以下是**最多10条入站样本总额**，不是每类10条。120秒含启动和清理，不为凑满样本延时。profile无法识别一个消息对应多少UI项时，只记runtime计数差额并停止，不以消息数精确通过。

| 预留序号 | 人工自造内容类型 | 本观察器可记录的事实 | 不可声称 |
| --- | --- | --- | --- |
| 1–2 | 两条内容相同的短文本 | 是否出现两个不同的新UI对象及其类别 | 源消息ID/传输去重已通过 |
| 3 | 字面“@某名字”的短文本 | 新对象计数/类别 | mention_self=false已获可信证明 |
| 4 | 若本次明确允许，由操作者用微信界面选择真实@ | 新对象计数/类别，语义来自操作者声明 | mention_self=true已获可信证明 |
| 5 | 若窗口支持引用，操作者自造引用 | 是否出现refer类 | 当前图片/引用语义/原消息身份 |
| 6 | 一张操作者自造图片（本次需明确包含） | 是否出现refer或其他类，不读取像素 | image_event/pixels/current binding通过 |
| 7–8 | 两条短文本紧邻到达 | 本次可见runtime差集与预算是否停止 | 无漏报/可靠新消息边界 |
| 9–10 | 预留两条普通文本；可不使用 | 同上，达到预算必须停止 | 完成10条就可生产 |

真实@/图片/引用若未获该批次明确允许，可少用样本，留 not_tested；不自动换成发送测试。无需为同名/改名/账号重登/进程重启/锁屏/远程断开加真实操作，这些本批次不做；负例用离线覆盖。操作者主动取消、焦点离开/窗口关闭自然触发停止，观察器不自动操作以制造这些条件。

接受仅为：在授权窗口/时限内读到白名单元数据；全过程0模型/0发送/0正文或像素/0业务历史写入；退出确认可复核；没有扩大目标/属性/样本数；报告列明实际耗时、实际runtime样本、未读/未验能力和停止原因。未满10/空树/不支持profile也可形成有效失败报告。不得把一次成功外推至其他客户端/账号、跨重启、锁屏、远程断开或24小时。

## 12. 失败分支与未验证清单

| 触发 | 必须行为/最终证据 |
| --- | --- |
| 用户未选择B/只批准P1 | 不运行真实入口；P2 not_authorized，等待新指令，不领取03 |
| 无精确句柄/所选账号声明/合成范围 | parameter_missing，0 UI；不搜索联系人/群/账号目录 |
| Job或可终止worker无法建立 | isolation_unavailable；0真实UI，无线程降级 |
| 本机UI包缺失、COM声明/ABI未知 | provider_unavailable/unverified；不自动安装/换库/下载客户端 |
| 单窗口结构未知/无UI树/多List/主窗口 | profile_unverified；不猜路径、不OCR/Hook，不读其他会话 |
| 非空基线/意外新增/身份来源不可限定 | synthetic_scope_unverified；不读取或清理历史，不靠正文筛选 |
| 错窗/前台离开/PID复用/重建/移除 | binding_or_continuity_lost；丢弃当前结果、终止worker，不重绑 |
| 预算/IPC/异常/超时 | 停止并丢弃未确认结果；仅终止有创建身份的worker；不补发/补跑 |
| 超时后未确认退出 | cleanup_unknown/hard_deadline_unverified；关闭后续观察，保留元数据证据，不按名字扫杀、不动附着微信 |
| UI元数据顺利返回 | 只接受元数据观察，全部业务门槛仍unverified，图片pixels仍unsupported |
| 日后某新源宣称有ID/@/ACK | 重新固定来源并审阅语义/失效/归属，再另批真实验收；不从字段名直接给生产资格 |

真实验收差额完整保留：安装/客户端兼容、账号/会话/成员/源消息稳定ID、黑名单可可靠执行、可信真实@与self标记、新消息不漏报/重放、当前图原件与绑定、项目关联ACK、真实模型/投递、重启/断线/锁屏/远程会话/24h运行均未通过。最小provider只能缩小其中“本机有限UI可读与自有worker退出”的差额，不能替代其他项。

## 13. 兼容迁移与回滚

没有账号/群/私聊名单/真实历史或QQ数据迁移；NormalizedEvent v1、业务能力摘要、五份严格配置和默认命令不变。新观察报告schema `wx-ui-observation/1`只给独立工具使用，不导入业务capability或接受台账；未知版本拒绝，既有无该schema的mock/inspect报告不自动升级成真实观察证据。不要新增 accepted/passed 开关供操作者填入。

本轮回滚仅撤回本次归属文档的 Git 改动；不需要停止任何服务或恢复配置。P1以后回滚只移除新观察入口/provider模块、回到上个审阅提交，同时保留有效的证据区间修正或单独记录；按差异精确回退，不丢其他session修改。P2若曾创建worker，先只结束本批次有创建句柄的Job并确认，再禁用入口；不关闭/注销/结束附着微信，不动QQ/全局设置。观察报告可保留；业务pending/unknown与清理台账一律不删、不重放或自动清账。

可选环境安装即使日后获授权，也不影响默认环境；不自动全局卸载或递归清理。清理该项目环境须另核对精确绝对路径与授权范围；失败时保留已知工件/日志元数据，不用清理动作掩盖unknown。

## 14. 给后续 gpt-6.1-sol/medium 的完整实施指令

以下文本只在用户**另行选择B并发出实施指令**后使用；用户自行选择会话模型/档位，不由本文检测或切换。此指令仅P1，不包括P2，不领取WX-03。

```text
工作目录 E:\CodexWS\WeChatbot。仅在 WX-02 内实施已规划的 P1：只读 provider 的代码与离线验证；不领取 WX-03，不运行真实观察。用户已选择本阶段实施时才执行本段。

先读 AGENTS.md、PROGRESS.md、TASKS.md、WX-01/WX-02 HANDOFF、docs/WX-02-CAPABILITY-REPORT.md、docs/WX-02-REVIEW-AND-PROVIDER-PLAN.md，必要时查原PLAN/RESEARCH。核对git状态、402ffd2与本轮文档检查点；一个session只做本P1，登记负责人/开始时间/本计划第9节文件归属到WX-02交接/TASKS/PROGRESS，写后重读，保留其他修改。不建立WX-03交接。

先修正excerpts.json首条倒置区间为固定源__init__.py:54–57，检查器拒绝倒置/越界/空白片段，同步evidence hash，补反例。固定上游8589baa049bb91d3a500602c167f07b2f8397a13不变，不导入该包、不跟latest。既有70项是历史离线结果，不是微信能力。

按独立规划第7–10节实现纯请求/报告合同、supervisor与唯一worker路径。先做自造子进程/Job/IPC/时限验证，再编写最小UIA provider源码和fake COM验证。只用指定HWND，PID与创建身份、root/list runtime、前台前后检查；仅独立ChatSingleWindow profile，主窗口/空路径/多List/非空基线拒绝。限定结构深度8/节点64/消息项32，惰性读取；runtime仅进程本批次比较，不能变成实体ID。当前ProbeSession仍只接MockPrimitives，不删类型保护接真实UI。

标准库ctypes控制自有隐藏worker；comtypes基础模块与最小UIA接口声明仅在worker未来显式运行时惰性加载，声明来源/IID/ABI/资源释放须审阅。禁止pyweixin/pywechat/pywinauto初始化和comtypes.client/GetModule自动生成/目录fallback。P1不安装UI依赖、不导入COM、不访问微信。无法在白名单内实现就保持provider_unverified/real_observation_closed，交付具体原因，不放宽边界。

总预算从启动前开始，默认120秒（末5秒留清理），单RPC≤2秒，250ms单在途轮询，最多10新增runtime样本。CREATE_SUSPENDED→自有Job/kill-on-close/禁breakaway→恢复；分配失败不恢复。父端无COM，匿名管道严格JSON，不pickle/端口/无限join。卡在导入/绑定/调用/IPC/退出、取消或父端退出都只终止本次创建Job并确认句柄退出；默认命令绝不spawn。任何cleanup_unknown关闭后续观察，迟到数据丢弃，不重跑。可运行无UI无COM的自造worker来验证本机Job退出，不是业务服务，不能按进程名结束其他实例。

不读消息Name/Value/TextPattern、正文/真实历史/账号目录/数据库/内存映射/剪贴板/图片/截图；不登录/开窗/切焦点/改设置/发送/启停业务服务；不调用模型/家庭SSH或QQ端口。报告默认stdout封闭元数据，不回显身份/窗口数值/runtime/路径或其hash/异常正文。真实provider代码完成也不运行；状态始终production=false、业务receive/send关闭，所有稳定ID/@/self/关联ACK未验，pixels unsupported/handle null。

按计划第10节做有意义离线检查：证据区间、默认副作用、精确绑定失败、计数/结构/管道溢出、所有阻塞位置/Job失败/退出确认/隐私和原WX-01投递预算工具隔离回归。原70项行为保留，增加项按实际结果报告，不把未装UI包的not_run当真实通过。运行本项目unittest、固定源/hash与QQ快照检查、inspect/probe/mock副作用隔离和文档链接/diff检查；不通过就修可做部分或明确差额，不用真实观察诊断。

同步README/独立计划与能力报告、WX-02交接/TASKS/PROGRESS，区分代码已实现、离线通过、自有进程时限验证和真实UI未验。只本地提交本session归属文件，不创建remote/不推送。P1结束停下，给出真实观察仍缺的用户指定对象/范围与未验证合同；不自动安装依赖、执行P2、发送/调用模型、换iLink/Hook/付费协议/旧客户端/OCR、改变黑名单/@/全回复或领取WX-03。
```

P2不能复用上述实施文本作为授权。届时必须另有用户指令明确窗口/账号声明、自造测试范围、120秒/10条上限、0发送/0模型/0正文和像素，以及是否允许在项目专属可选环境安装锁定的必要UI原语。没有这些实际对象与动作，本任务只交付P1或缺口报告。

## 15. 本轮收口验证

本轮只做固定源码/本地代码静态复核、公开GitHub只读核对、哈希核对与文档编辑；未运行单元测试/项目CLI/服务/上游导入。五份归属文档写后重读，42个本地链接、115行表格列数和代码围栏检查通过；`git diff --check`通过，源代码/配置/人设/证据工件和原规划/旧交接均无差异。暂存集合须精确限定五份文档并再次检查，交付前核对提交与工作区。70项保留为历史结果，真实能力仍全部未验。本地文档提交号见交付消息/最新git log，无remote无推送；不自动实施下一阶段。
