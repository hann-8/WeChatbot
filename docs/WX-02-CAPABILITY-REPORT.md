# WX-02 候选能力与离线报告

返回[PROGRESS](../PROGRESS.md) / [TASKS](../TASKS.md) / [交接](../tracks/tasks/WX-02/HANDOFF.md)。2026-10-23，Asia/Shanghai。状态：**本轮代码/离线范围完成；真实观察未执行，生产门槛未满足**。仅领取WX-02，不领取WX-03。

20:02起的文档复核 session `WX-02-gap-review-plan-20261023` 已完成[独立缺口复核与后续详细计划](WX-02-REVIEW-AND-PROVIDER-PLAN.md)。本报告的70项是 `402ffd2` 实施轮历史离线结果，本次未重跑测试，未实施provider或执行任何真实观察。复核建议停止以当前固定上游推进生产适配；只将一次有界UI元数据观察列为用户可选项，先另批代码/离线、再另批指定对象观察，任何一步均不自动满足WX-03。

## 来源、分发与依赖

实际核对[固定树](https://github.com/Hello-Mr-Crab/pywechat/tree/8589baa049bb91d3a500602c167f07b2f8397a13)及raw字节；上游源码commit是 `8589baa049bb91d3a500602c167f07b2f8397a13`，不是latest。11份源文件SHA-256/Git blob、带行号片段和原始许可见[vendor索引](../vendor/pyweixin/README.md)。GitHub树返回的blob与下载内容逐一匹配。

`src/setup.py`和`src/pyproject.toml`声明 **pywechat127 1.9.8**；64位setup.py包列表同时含旧pywechat和新pyweixin，32位只含旧模块。不能安装名为pyweixin的未知分发物，也不能把PyPI同版本号当成固定源码等价物。本轮不安装该分发物、不复制整个包，仅保存惰性审阅证据。源码只读接口直接封装必要window/list/runtime属性，当前不需额外运行依赖。

原实施轮审阅的Windows原语候选闭包锁为pywinauto0.6.9 → six1.17.0 / comtypes1.4.13 / pywin32311（CPython3.12-win_amd64）。实际wheel SHA-256、Requires-Dist及许可已核对并保留；仅下载到忽略cache，**未安装/导入/试运行**。可选[hash锁](../vendor/pyweixin/observation-requirements.lock)不改变默认uv.lock或安装行为。后续最小provider拟只使用标准库和已锁comtypes基础模块，避免pywinauto/代码生成初始化；仍待实施/验证，不能把四工件都当成必需安装项。没有引入上游音视频、PyAutoGUI、系统音量、MCP、Agent技能或浏览器依赖。

许可：根LICENSE是LGPL-2.1；pyproject classifier却为LGPLv3、setup只写LGPL。保留冲突，未自行重许可或断言分发合规。四份依赖实际license文本保留；pywin32的PSF元数据与多份组件许可分开记录。此处是工件事实，不是额外授权。

## 决定性源码证据

- `src/pyweixin/__init__.py`直接导入WeChatAuto/Tools/WinSettings/Config；`Uielements.py:44–45`在导入时访问GlobalConfig.language/Version。Config的懒属性会枚举进程命令行/读取注册表；因此连子模块导入也不安全，未采用“先import再关闭开关”。
- `WeChatAuto.py:4309–4334`按显示名/正则拆sender；`WeChatTools.py:294–305`自身wxid从本机账号目录推断且源码提示缓存风险，不证明选中账号，也不提供群成员稳定身份。本项目不调用这条目录路径。
- `WeChatAuto.py:4360–4403`以visible children runtime_id比较，读取消息文本并触及本机chatfiles路径；调用系统监听模式，图片只计数再按最后N条批量导出，并默认close_dialog_window=true。这不是本项目可以直接复用的安全监听器。
- AutoReply正文调用set_text/按键，没有本项目冻结目标、投递台账或关联ACK。函数存在只构成源码证据。

补充静态复核：`Tools.where_wxid_folder:166–193` 实际枚举进程并从 memory_maps 的 MMKV 路径推断账号目录，不是被允许的单窗口账号API；`Messages.send_messages_to_friend:3365–3418` 返回None，使用备注查找/剪贴板/按键，长文还可能转文件；`Messages.save_media:4100–4180` 打开历史预览并截图保存。`Tools.is_my_bubble:420–437` 也读取气泡截图作启发式判断。以上均不能引入最小只读provider；出站成员@选择辅助也不能证明入站真实@。固定链接、代码位置和观察可回答的范围见独立计划第4–5节。

## 逐项能力结论

以下“源码支持”全部不等于observed/passed；本机客户端版本/账号/实际窗口均未观察。

| 能力 | 固定源码可见事实 | 本轮实际证据/交付结论 |
| --- | --- | --- |
| stable account ID | Tools从本机目录猜自身wxid，可能缓存 | 未调用；操作者account_reference仅声明，不构成账号绑定；unverified |
| stable conversation ID | 窗口/会话标题及显示名 | 同名/改名不能作ID；unverified |
| stable sender ID | 显示名正则拆sender | 黑名单不能依赖昵称；identity_unverified |
| stable message ID | UI runtime_id | 进程/控件局部标识，非server_stable；unverified |
| display_name | UI文本/标题/正则 | source_supported；本轮不读取真实显示名，不能作主键 |
| UI runtime_id | element_info.runtime_id | source_supported；mock可读；重建/复用可能失效，非源消息ID |
| 可信真实@ | 未找到能满足本计划的结构化可信元数据 | mention_unverified；普通正文@不补true，不改reply_all |
| 自己消息 | UI几何/昵称启发式存在 | 未证明可信sender_is_self；不从气泡位置提升事实 |
| 图片事件 | refer-bubble标签/计数 | 图片/视频/引用可能共用类；实际image_event unverified |
| 当前图像素及来源 | 批量媒体导出函数存在 | 本项目pixels=unsupported/source=none，无材料句柄；0截图/落盘/取图 |
| 发送按键结果 | set_text/按键路径 | 只代表动作返回；本报告unknown/ack_level=none，delivery_unverified |
| API accepted / UI observed | 未证明与本任务关联的可靠ACK | 不标api_accepted/ui_observed，更不标服务端投递/已读 |

总出口固定 `identity_unverified / mention_unverified / delivery_unverified`，`production_eligible=false`。候选adapter.receive拒绝，send_text直接failed/none且不调用任何UI/check回调；keypress_result只报告unknown/none，不做投递。继承WX-01 gate，开关或伪造capability字段不能启用真实通道。

## 既有实现和入口（402ffd2）

`transports/pyweixin_adapter.py`封装明确注入的单窗口原语：核对pid/创建时间/hwnd/root runtime/list runtime/前台窗口，仅读绑定窗口内消息List的CheckBox runtime_id与class_name，读前/读后复核。没有查找相似群、全窗口扫描、窗口激活、输入、剪贴板、截图、取历史、数据库、关窗口或系统设置方法；不导入pyweixin/pywinauto。

`ProbeSession`仅接受精确MockPrimitives类型，不连接模型/历史/router。首次runtime元数据只作基线丢弃；每快照最多32项，单次session最多10项/120秒（可缩小，不可扩大）。同一runtime不重报；丢失旧runtime、列表重建、重复runtime、错窗、账号声明/连接代际变化、无UI、超量均停止；突发超过剩余预算整批拒绝。时钟在读前/后检查，超时返回数据丢弃。它不能识别原地runtime复用或证明没有漏报，所以不提供稳定去重保证。count统计runtime样本，不声称是真实微信消息条数。

本次复核明确其限制：account_reference只是caller声明，`BoundWindowPrimitives._check`核对的HWND/PID/root/list/前台相等不证明账号或聊天实体一致；同一主窗口若原地换会话且runtime不变可能无法察觉。`children()`已枚举后才检查32项，时钟检查也不能中断挂死COM。fake中换root/list测试不能提升为真实会话绑定或硬时限通过。可选后续计划因此仅接受指定独立聊天窗口、空基线与元数据白名单，另建自有可终止worker；不删除mock类型保护或修改业务gate。

默认命令：

```powershell
.venv/Scripts/python.exe -m wechatbot inspect
.venv/Scripts/python.exe -m wechatbot probe
.venv/Scripts/python.exe -m wechatbot probe --mode mock
.venv/Scripts/python.exe scripts/check_pyweixin_source.py
```

inspect/probe默认静态核对本地证据hash和固定版本，不联网、不导入上游、不读取微信；mock只运行内置自造runtime样本。证据缺失/漂移报告unavailable_or_invalid，生产资格仍false；检查器另提供非零失败。健康服务导入延后到显式构造，不为inspect启动服务。公开CLI没有observe模式。

**真实provider未接线，open_real_observation即使传observe/authorized=true也返回real_observation_closed。** 该函数先验证显式模式、后续授权声明、指定绑定、自造样本及≤120秒/≤10条限制，但这些参数不自动构成人类授权。尚未证明真实控件可绑定、同步COM能硬性超时，以及如何保证仅观察指定单窗口自造样本；本轮不以可调用函数冒充真实探针完成。若后续获真实观察指令，应先在WX-02范围补充隔离provider/硬时限控制并验证，再由用户指定账号、已打开单会话窗口和最多10条自造样本；仍必须0模型/0发送/0真实历史/0截图落盘。不能直接解除gate进入WX-03。

本轮0实际UI调用、0登录、0模型、0发送、0日常账号目录/数据库/密码读取，无客户端/QQ/WorkBuddy设置或进程操作。仅联网读取固定公开源码/PyPI元数据和锁定wheel，不执行其中代码。

## 离线验证与验收差额

新测试验证真实失败路径而非只查函数名：只读允许方法之外FakeWindow直接抛错；换焦点/复用pid在读items前拒绝；读中切窗丢弃；列表重建不作新消息；同名/改名/普通@/自己消息的process_local候选在身份门槛拒绝且不触及store；单张refer bubble不产生图像句柄；send无check/UI回调；虚拟列表/突发/累积上限/120秒前后检查；默认命令在禁止UI和runner导入、禁止socket与Popen的子进程里成功。原41项投递/预算/工具隔离等测试保留。

验证结果见本任务HANDOFF，新增29项、总70项离线测试。工件审阅通过11份上游文件、16份证据文件和4份wheel hash；WX-01快照仍63份/2处既有受控差异/3工件hash匹配。本机没有安装optional UI包。没有任何observed真实能力、真实接受或完整产品验收证据。测试不证明微信UI行为、跨进程稳定ID、锁屏/远程断开/24小时运行或真实图片/投递。

本次独立只读哈希复核：11份缓存固定源的SHA-256/Git blob、16份本地证据及4份缓存wheel hash均匹配；GitHub按完整ref复取初始化/Monitor/账号工具片段与锁定blob一致。发现一处证据质量缺陷：`excerpts.json`首条初始化片段为倒置区间64–60、内容仅换行；检查器没有校验有效区间，空切片可能通过。有效导入在54–57行，本次已从完整固定文件核实。故原hash/片段检查记录只保留为历史执行事实，不能声称十条有效代码片段全部通过；本轮未改检查器、证据JSON或hash，修复列入待授权P1。

需要回sol/max的产品/传输缺口：在固定上游中未找到可满足现有合同的账号/会话/成员/消息稳定身份、可信真实@、当前图绑定及关联发送接受结果。未找到接口不等于断言客户端内部绝无能力。选不同产品/传输或实验边界必须另行规划；不自动切iLink/Hook/付费协议/旧客户端/OCR，不改变黑名单/授权或全回复。一次只读元数据观察可核对本机有限UI可读性和自有worker退出，不能验收真实@、稳定ID、像素或项目ACK；这些仍unverified，当前pixels仍unsupported。

## 兼容、回滚与Git

默认配置/人设/真实模型/原WX-01业务保持原样，mock/mentions/single，生产关闭。仅inspect增加候选能力摘要和本地证据状态，新增probe inspect/mock只读命令。原QQ快照/manifest及WX-01测试未改。回滚本任务代码可移除probe/候选摘要，保留WX-01；不启动/结束日常微信，不改本机配置，不清pending/unknown。可选依赖未安装，无卸载/全局恢复操作。

仅本地Git交付，本项目无remote，不创建或借用QQ远端。源/轮子缓存为忽略cache；原实施提交402ffd2包含源码、测试、许可/锁/审阅证据与文档，本次复核提交仅含已登记五份文档。无凭据、原始私密消息或真实身份。
