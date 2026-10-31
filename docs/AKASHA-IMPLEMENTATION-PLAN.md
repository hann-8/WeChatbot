# Akasha 主线：一次完整落地计划

返回[PROGRESS](../PROGRESS.md) / [TASKS](../TASKS.md) / [规划交接](../tracks/tasks/WX-AKASHA-01/HANDOFF.md) / [唯一 sol/medium 指令](../tracks/tasks/WX-AKASHA-01/MEDIUM_START.md)。

2026-10-31，Asia/Shanghai。**当前只规划，不实施。** 用户已明确：Akasha 作为微信 main 路线；一次规划要覆盖基础和其他功能，用户自行提交给 gpt-6.1-sol/medium，一轮完成落地后实测，禁止过度防御性编码。本计划取代 wxauto 自研入口的后续投入，不删除旧成果或未决记录。

## 1. 一个实施任务和交付目标

后续仅领取 **WX-AKASHA-ALL**。安装/配置、微信接入、AstrBot 路由、模型、人设、记忆、图片、表情、群聊模式、控制、部署、检查和使用入口都在同一个任务里完成。下面的顺序是内部实施步骤，不能变成多轮规划、审批或“只做第一阶段后停止”。

采用现成 WeFlow 和 Akasha，不再写一套微信登录、读库、解密或 UI 收发内核。优先配置、现有 AstrBot 公开接口和现有 QQ 业务。对已核实的桥接协议缺口允许本计划明确的小补丁；不为了“原版不动”保留不能聊天的已知缺陷，也不维护全面私有 fork。

完成目标：操作者完成一次机器人账号选择/登录/取钥后，可以从此前指定微信群自然跟现有 bot 聊天，基础文字和下表增强能力已接好，QQ 原功能继续可用；一组启动/停止入口即可使用。能力质量由用户实测接受，不加长稳/生产资格或历史大矩阵作为交付前置。

## 2. 已核对的事实与实际缺口

| 项目 | 当前证据 |
| --- | --- |
| 微信项目 | E:/CodexWS/WeChatbot；main 起点 938187c，当前规划差异是本会话已知成果 |
| 原自研入口 | 微信初始化/入站成功，真实 CLI_START 后 PROTOCOL_ERROR；零生成元数据握手复现缺模块、stdout 无事件、user_messages_sent=0。没有修成，不再作为新主线依赖 |
| Akasha | alingalingling/Akasha-WeChat，固定 9dbe933a9f1bc46e33ca8121334bb1dd01173248；实际 app 在 wechat-weflow-bridge-ob11；已放 runtime/akasha-wechat/upstream，源码未改 |
| Akasha 架构 | WeFlow /api/v1/push/messages SSE → bridge → OneBot v11 反向 WS → AstrBot；出站是自带 UiaSender 的键盘/剪贴板操作 |
| WeFlow 可用副本 | 原作者 hicccc77/WeFlow 当前 Release 为空；采用公开维护分支 334456777/WeFlow v5.0.1，Windows x64 包 11376812 字节，发布摘要 8d88ca61c504c8d509fd7b6934e4d2261ba986f6a1e13df68c3732323e1b26fa 已核对；版本输出 5.0.1/6115746 |
| WeFlow 接口 | 普通 serve 提供向导/WebUI（默认18108）；serve --desktop --message-push 提供兼容桌面 API/SSE（默认5031）；不能把两种服务模式混用 |
| 环境 | 独立 runtime/akasha-wechat/venv 已准备，pip check 通过；实际 requests2.34.2、websockets15.0.1、uiautomation2.0.29、PyAutoGUI0.9.54、Pillow13.0.0。上游虽写 websockets>=12，但实际 additional_headers/asyncio 接口需新版本，不能降回12 |
| 现有 QQ/AstrBot | E:/CodexWS/QQbot_Snowluma，核对 main=42911afc4c1f2bcfbbc3c26afc2647fd21992f08，干净；AstrBot4.29.0、QQ aiocqhttp 端口6199；provider_source=qqbot_openai → 127.0.0.1:8765/v1 |
| QQ 业务归属 | QQRouter 在自有 plugins/qq_router；模型网关及全文 MemoryStore 在自有 qqbot_gateway。AstrBot 通用群 LTM 关闭。把桥接插进 AstrBot 不会自动继承这些逻辑 |
| 用户现场 | 已自报换到微信4.1.8.107；首试此前指定群，全体成员可触发，保留黑名单。已明确允许 WeFlow 本机读库/密钥；本人尚未安装 WeFlow |
| 本轮准备边界 | WeFlow 二进制核对执行了 --version/serve --help。另曾创建自己的首次配置服务，按最新“只规划”已凭 pid/创建时间/路径停止。没启动 Akasha，没读微信数据库/密钥，没修改现有 AstrBot/QQ 或实际收发 |

### 已核实不能只靠 README 判断的地方

1. Akasha `state._wxid_to_int` 用 Python hash()，默认进程之间会变；仅注释写“稳定”不能当稳定标识。
2. `make_message_event` 没有完整消息 ID/源消息关联；缓冲后又把原成员/消息信息变成文字，不能直接塞进现有 QQ 去重/记忆逻辑。
3. `ob_protocol._handle_ob_api` 在实际发送前先回成功，且忽略 sender 的 bool 结果；这不是微信送达证明，失败会被伪装成功。
4. mention 模式只从正文检测 @昵称，再合成 OneBot At；这是文本唤醒，不是微信原生可信 @。
5. 图片读取取“会话最新图片”容易错绑；图片还默认额外调用 llava/另一个模型，不能假设已等价复用当前识图。
6. 原桥接会打印 SSE token、联系人和原文；没有本项目要求的指定群前置过滤。
7. QQRouter.on_group 会 stop 掉其他 self/group，before_provider 等钩子也按 QQ 出站栅栏工作；不能只新增11229端口就说两端同一 bot。

这些是本批要一并补齐的有限接口工作，不是重新开发整套机器人。

## 3. 目标链路和“同一个 bot”的定义

```text
微信机器人账号
  ↕ WeFlow：本机读库、消息/媒体公开 API、SSE
Akasha：薄传输桥接、指定会话过滤、UIA 回发
  ↕ 独立 OneBot 连接 akasha-wechat / 127.0.0.1:11229/ws
现有 AstrBot 实例
  ↕ 自有 transport-aware 路由 / 共用业务
现有模型网关 / CodeBuddy 或手选家庭 Ollama
  ↕ 共用人设、受控联网、上下文、记忆、回复计划
```

- 复用现有 AstrBot 实例/安装、现有 provider 和模型后端，不复制另一个 CLI 残缺包，不新写第二个模型客户端，不开新付费 API。
- 人物正文、人设版本和模型配置同源；平台能力说明分别生成，微信不能声称具备 QQ 传输才有的能力。
- “共享记忆”必须有明确会话配对：指定微信群与哪个 QQ 会话共享事实空间、哪些人物确属同一个人。共用 AstrBot 或模型本身不完成此映射。
- 每轮只回发来消息的通道；本方案不是 QQ↔微信原始群消息互转/群发系统。
- 微信独立通道/过滤和管理配置仍放微信根；确需复用的 QQ 业务代码、provider、记忆由现有 AstrBot 的自有插件管理，不绕过现有 QQ 权限，也不从微信伪造 QQ 用户/管理员。

## 4. 本次全功能清单

| 功能 | 本批必须落地的行为 | 实际能力边界 |
| --- | --- | --- |
| 基础群聊收发 | WeFlow→Akasha→AstrBot→当前模型→UIA，一套完整链路 | 仅选定机器人账号和授权会话，不默认所有群/私聊 |
| 普通自然聊天 | 人设、称呼、认真完整回答、轻松简短回应；新群全成员可触发 | 不设发送者白名单，黑名单先过滤 |
| 触发/群聊模式 | mention文本唤醒、全量入站由 bot 判定、batch缓冲；接入现有 free/叫名/续聊判断 | 合成 At 明确标 text-derived；没原生元数据不冒充真@ |
| 叫名/空唤醒/引用续聊 | 复用现有 attention；空明确唤醒可短应声，实际引用可关联，无结构时只按文本 | 不从单纯“@名字”授予管理员或持久控制权 |
| 短期上下文 | 复用现有整轮/群RAM裁剪，按配置容量和输入政策运行；reset清短期 | 独立/配对共享两种 scope 在本批实现，不默认把无关群历史合并 |
| 人设和模型 | 同源角色正文、当前 deepseek-v4.1-flash/low、thinking=false；家庭路线保留手选 | 不改账号/额度来源；不自动换后端；不重新登录模型 |
| 共享长期记忆 | schema2全文、同次模型增改删、原子保存/真实回执；配置会话/人物配对后共用同一存储服务 | 不复制旧库/key；未配对则独立新空间，不凭同名自动合人 |
| WebSearch/WebFetch | 当前原生两工具、公开URL来源与“本次不联网”优先 | 3调用/4步骤/90秒，单8000/总12000字节，其余工具/MCP关闭 |
| 识图 | 当前消息精确取图→现有归一化/原生模型识图；图文同轮 | 无图片/取图失败准确提示；不取会话“最新图”冒充当前图，不另加caption模型 |
| 受控表情 | 复用当前已登记catalog/候选/自然表达/出站计划，通过Akasha图片发送 | 只用明确登记素材，不开放任意文件；GIF实际若只能首帧则明示，不伪称保留动图 |
| adaptive多气泡 | 使用既有ReplyPlan，不强凑条数；认真answer单条，闲聊按现有限额 | 部分发送/不明不自动补发；unknown不堵死其他无关会话 |
| 成员/称呼 | 优先用WeFlow公开成员/消息元数据，现有成员增强按实际数据接线 | 同名/改名不自动当同一人；能查成员不等于能发送原生@ |
| 受控原生@ | 仅现成发送接口确实产生微信原生@时启用，沿已有权限/限额 | 只有文本粘贴接口时用普通称呼并标不支持原生@，绝不伪装完成 |
| owner/暂停/恢复/reset | QQ现有owner控制不变；微信本机面板/控制台一定可用；可信wxid及显式owner映射成立时接远程owner指令 | 仅昵称/合成OneBot ID时不授管理员权；不增加远程shell |
| Web面板/配置 | 复用Akasha面板；显示WeFlow/AstrBot/接入状态、模式、暂停/恢复、配置保存 | 本机回环；配置/日志不回显密钥或原文 |
| 启动/停止/恢复 | 一份管理入口启动依赖/桥接；正常停止受管进程，不退出微信 | 普通WS/SSE断连可重连；不重放旧消息/unknown发送，不强求锁屏/无人值守长稳 |
| 私聊 | 本批提供单独显式白名单开关和独立会话scope，默认关闭 | 开启须操作者本机选对象；不因桥接默认支持就自动开放 |
| 语音/视频/任意文件/B站字幕 | 统一能力提示和关闭分支，避免假装读取或启动额外模型 | QQ未有成熟能力或已退役；不新增ASR/TTS/收费服务，不以其未支持卡住上表 |

“全放一份里”意味着所有这些接线、配置、降级和使用说明都由同一 medium 任务完成。表中有明确接口缺失的项，交付诚实的能力状态/可用替代，不另挂一个“待下一轮规划”才能聊天的前置。

## 5. WeFlow 账号/密钥与现成运行包

使用已下载的公开 WeFlow v5.0.1 Windows x64，不自行实现或修改 SQLCipher、取钥、登录、图片解密核心。维护分支与原作者项目不同，发布/版本已明示，不称原作者官方安装包。

- WEFLOW_HOME 只指向微信项目忽略的 runtime/akasha-wechat/weflow-home。机器人账号、数据路径、密钥、API token 只存本机私密配置；使用取钥保存模式，不打印密钥。
- 用户已同意读库，不再重复询问意愿。medium在同一轮提供一次现成首次设置向导：选择机器人账号/目录，按程序要求配合正常退出/登录；若需要管理员权限，让操作者从已准备入口正常授权。不能索取/猜测密码，不按进程名结束微信，不删除聊天数据。
- 普通 serve（本机18108/WebUI0.4.1）用于向导；配置好后用 serve --desktop --message-push（本机5031）给Akasha供兼容API/SSE。两模式token和同一home一致，避免看见网页却API端口根本没开。
- 不把“版本/帮助输出成功”当数据库已连接；用现成health/配置状态和一个已选会话的公开API核对。先确认账号/范围，再取消息/成员/媒体，不导出整份历史作测试。
- 只读微信数据库，不执行WeFlow的本地消息编辑、撤回拦截、朋友圈修改或防撤回动作。首次功能不需要的图片自动下载钩子、AI insight和全量导出关闭。
- token优先Header用于本项目接口请求；上游SSE query token如需保留，必须在日志脱敏，不输出整个URL。
- 环境/包缺失、普通依赖和HTTP/SSE兼容细节由medium同轮修好；真实客户端/账号权限确实要求人操作时只提出那个具体动作，不重新规划。

## 6. Akasha 最小适配补丁

保留固定上游副本；实现补丁以项目内可审阅diff/overlay登记到来源清单，再部署到运行副本。只改下列桥接层接点，不改UIA/WeFlow/AstrBot第三方内核，不建另一个机器人框架。

### 6.1 IDs和源关联

- 用确定性的namespace/hash产生OneBot兼容整数ID，区分bot/user/group；输入含账号和原始会话标识。不能依赖随机Python hash。已有ID变更做明确迁移表或启用新adapter ID，不能重启后静默串/丢会话。
- OneBot事件必须带message_id；保留WeFlow rawid/sessionId、实际sender字段、原时间及缓冲内源消息列表，作为插件可识别的akasha来源扩展，不把显示名包装成服务端稳定身份。
- 在WeFlow公开API能取得真实sender wxid时使用并标来源；暂缺时保留session/name局部标记，基础聊天仍可用，但不据此owner鉴权或自动合并人物。
- 去重只覆盖本账号/会话和新事件；首次连接从当前基线继续，不把旧历史送模型。自动重连不自动重发已处理事件。

### 6.2 范围、触发与缓冲

- bridge_core.should_ignore在缓冲/取图/日志/模型之前过滤账号、允许sessionId、私聊开关/白名单、黑名单和自己消息。空授权列表不代表全开放。
- 首批绑定此前指定群；全体非黑名单成员可聊天，无allowed_senders门槛。后续增群只改一个本机配置并重载，不重新计算全库“资格”。
- 要复用free判定时Akasha all只表示“允许群新消息完整入站”，最终是否回复交现有bot。不要在桥接层仅@预过滤后又期待模型能旁观续聊。
- 缓冲默认不叠加两套长等待；batch模式保留原消息成员/ID列表，不能只剩一句合并文字。叫名/明显请求可及时处理，ambient合并不自动多次生成。
- At由正文推断必须标明text-derived；只有公共元数据真正提供原生@时才算native。群友不能用正文制造QQ管理员/可信票据。

### 6.3 发送结果和日志

- 修掉发送前统一回成功的行为：执行一次对应本地sender，按实际bool/异常返回OneBot结果；映射不存在不能拿数字ID去搜第一个联系人。
- 同一会话串行发送，复用原有UIA搜索/发送；只发送当前已授权会话，不自动跨群补发。多个文字/图部件按ReplyPlan计数；失败/部分/返回不明记本地unknown，停止该轮后续部件，不自动重试。
- UIA明确完成只记local_reported/bridge_local，不叫服务端ACK。正常成功不逐条索人工确认；未决只有需要人工核实时才显示。
- 不修改第三方登录/心跳/缓存机制，也不为每次按键建一套证明链。一次必要的目标匹配和失败处理即可。
- 删除/脱敏SSE token、原文、联系人及异常URL的原样日志；面板仅显示连接、枚举错误、计数、耗时和能力状态。

### 6.4 图片与媒体接点

- 入站按扩展中的rawid/session定位同一条消息及媒体，禁止“会话最新图”替代；只有当前实际解密出的图片才进入图像分支。
- 不默认启动独立llava/额外caption API。先把图片以标准OneBot附件/私有媒体句柄交现有原生识图路径，沿当前模型与预算，文字＋图片同一次模型任务。
- 附件目录必须是实际AstrBot配置路径/明确共享目录；处理base64和实际本地附件，不把任意用户文本当文件路径或任意URL下载器。
- 图片/成员/原生@缺失只关闭该增强并准确提示，文字分支继续；语音/视频/文件不额外触发新模型。

## 7. 现有 AstrBot/QQ 自有业务的接入方式

### 7.1 独立平台、共用业务

新增aiocqhttp平台 `id=akasha-wechat`，127.0.0.1:11229/ws；原QQ6199及Snow链不改。新平台回到现有AstrBot，继承同一个可用provider/后端；连接的是新平台入口，不能把微信直接插入QQ OneBot gate端口。

当前qq_router所有事件钩子按QQ self/group拒绝，必须在本批做平台分派：

- 原QQ路径仍执行原Snow连接/票据、owner、群名单/黑名单和出站栅栏，行为不变。
- 新微信路径按注册平台ID、机器人账号/允许微信会话和Akasha来源字段校验；不要为了复用把微信self_id/group_id塞入QQ allowed_groups/admin_users。
- 把共享的构造当前轮、队列/上下文、调用provider、回复计划、记忆/工具等逻辑提取为小接点或传入TransportContext；不要复制一份完整qq_router，也不为两平台重写共用业务。
- TransportContext至少包含platform/account/conversation/sender标识及来源、当前消息ID列表、触发置信级、回发通道和能力。缺陷只在对应平台分支处理，不新增通用插件平台。
- before_provider、on_response、decorating/after-send等钩子必须同样分派，不能只改on_group而仍被QQ输出栅栏拦掉。外部Akasha的API结果按本地等级记录，不拿QQ的合成ACK冒充微信确认。
- 出站固定回源adapter；不因共享内存把答复发到QQ对应群，不允许跨平台回环。

### 7.2 现有 provider/gateway

复用当前qqbot_openai及CodeBuddy/Ollama网关，而非微信旧残缺CLI副本。现有网关有标准OpenAI入口和v2群轮协议；必要时把其平台固化策略改为受管的transport profile，默认缺省仍为QQ，新增wechat_akasha profile。仅自有插件/网关改动，AstrBot核心不fork。

- 内部qqbot_request等字段名可保留为现成wire协议名称，不等于声称来源是QQ。传输身份/权限在入口已区分，schema字段如需平台标记用向后兼容可选字段，旧QQ请求不改义。
- QQ与微信可共享同一模型、人设正文、模型参数和调用队列。微信平台能力政策只描述已接通功能，不把QQ真实@、群号或成员凭据写成微信事实。
- 维持一次群消息一个CLI任务、单并发和实际队列；CLI内部仍可做原有有限工具往返，不增加分类/润色/图像描述的第二模型任务。
- 实际模型仍deepseek-v4.1-flash，low、alwaysThinkingEnabled=false、524288可见UTF-8输入政策及当前reserves；它不是原生token窗口或免费保证。现有家庭后端选择保留，不读/复制家庭凭据，不自动切换。
- 不重新迁一份CLI全包，不安装全局新CLI、不改变登录账号。若既有provider本身有具体缺依赖/接线故障，本批同轮修复并做真实可执行的零生成握手；不能再把import/摘要通过等同模型已可运行。

## 8. 人设、上下文与共享记忆

### 8.1 人设/短期上下文

以现有QQ bot角色正文为同源内容，通过平台能力政策组合；不复制实际QQ账户/访问配置进微信群。正文改动仍由用户控制，实施不擅自删角色段落。配置窗口按当前加载值，不把旧微信8轮或8000角色字符门槛重新带回来。

短期scope含平台/账号/会话；默认独立。配置会话配对时可选择facts_only（共享长期事实，短期独立）或shared_context（指定配对双方共用短期对话），两种方式同批实现。没有映射的群绝不自动串入。

保留当前请求/政策/当前图与记忆全文，只按完整历史轮裁剪，仍超实际预算则本地说明，不截当前问题、不临时换模型。reset只清对应短期scope，pause/resume不复活旧队列。

### 8.2 schema2全文长期记忆

复用现有MemoryStore、增改删/版本事务、实际保存回执，不建第二个长期记忆引擎，不复制旧memory.json/key。

- 在现有AstrBot自有业务中用一个记忆服务提供canonical_room。显式QQ↔微信会话配对共用同一canonical_room；未配对微信为独立新空间。
- 不凭群名相同自动配对。首次本机配置向导让操作者选实际微信群及是否配对已有QQ会话；只在本机显示/保存名字和ID，不写公开报告。
- 人物显式actor_links才映射为同一人；可靠wxid缺失时用有来源标记的本地别名，不以昵称冒充跨平台稳定身份。未映射仍可记该群内事实，不阻断普通聊天。
- 使用全文快照＋同次回复memory_updates，保存前确认当前会话/版本，原子写失败保原件；真实保存结果再构造回复回执。reset后能读回同一库，更新/删除不重复执行。
- 沿当前50000 Unicode字符/单文件1048576字节/总8388608字节，容量与输入政策可配置扩大；不恢复旧候选/关键词/240字节/小条数限制。
- 网页工具结果不写成人类长期事实；绑定换群、改配对、退群只停止该scope增强，不删除/覆盖旧数据。
- 管理页支持计数/容量/最近结果，本机显式导出/删除/取消配对。原始记忆正文与密钥不进日志或Git。

## 9. 其余增强一次接好

### 原生联网

完整复用当前WebSearch/WebFetch和已修复参数封套/HTTP(S)处理；不要重启旧Python关键词/RSS/HTML前置。来源只取本次实际成功工具的公开URL，最多2个，失败准确说未核实。共享队列的每个请求带本轮平台私密标识，不能把微信群名/wxid/QQ号码、密钥、整段历史或记忆上传为检索参数；不加新的检索账号/付费API。

### 识图/表情/自然输出

复用现有归一化、当前原生图封套和模型能力，不重做旧IQ六例。新WeFlow图源只增加一种具体的受管媒体来源，源消息匹配、字节/像素/最终预算沿现有检查；当前CodeBuddy能处理的图直接同轮推理。图片材料失败给准确提示，不导致所有文本停机。

受控表情复用当前已登记catalog和候选策略，素材只是本机已登记集合。跨平台发送只转换最终PreparedPart；不拷贝未授权图库或开放任意文件/语音。自然表达/adaptive沿源策略：一条能说清就一条，最多条数不是目标，认真回答不被闲聊短句上限截断。GIF、原生@的实际发送形态在报告中说明，不能默默降级后说全部原生能力已过。

### 成员、权限、控制和模式

用WeFlow公开消息/成员接口补充实际成员资料；cache采用框架现成机制，不重做收发/心跳/恢复层。真实@数据确实可取得时再走原生规则，缺失则文本叫名/唤醒同样能聊。成员增强不足只影响增强。

QQ原owner暂停/恢复/重置保持。微信一定提供本机Web/控制台；若该会话已经取得真实sender wxid且本机显式设置owner则支持同类远程控制，否则回复不具管理员身份，不能拿昵称/OneBot hash控制服务。普通成员仍可提出当前聊天偏好，不等同运维权限。

实现status、pause/resume、reset、stop、memory-status、未决确认；暂停只阻止未提交的新生成/发送，真正已进入UIA的动作不能保证撤回。正常本地成功继续；未知结果留记录、只暂停相应会话，人工处理不触发自动补发。

## 10. 配置、端口和操作入口

公开模板不含真实账号/群/密钥。本机一个akasha接入配置入口管理以下字段，必要时生成上游config.json，不要求操作者手工维护多份互相绑定的技术JSON：

| 配置组 | 字段/约定 |
| --- | --- |
| source/runtime | 固定Akasha commit、WeFlow版本/发布hash、独立venv路径；只读记录，不每次重建资格 |
| weflow | home、5031 API地址、18108向导地址、token secret引用、所选profile/account；本机私密 |
| astrbot | 现有root、adapter_id=akasha-wechat、127.0.0.1:11229/ws、实际attachments目录；不覆盖原QQ6199 |
| bridge | 本机管理18766、bot wxid/昵称、会话allowlist、私聊独立开关、blacklist、buffer、输入模式；无发送者白名单 |
| behavior | 共享模型/人设引用、free/mention/batch、single/adaptive、已支持vision/meme/member开关；能力状态真实 |
| pairing | 微信会话→canonical_room/QQ会话、facts_only/shared_context、显式actor_links；默认未配对独立 |
| controls | 本机管理；可选真实owner wxid；不接受正文自报身份 |
| lifecycle | 仅本项目创建身份、状态、端口、未决记录；无全局自启、防睡眠、批量kill |

管理入口至少提供：Prepare/Inspect（零生成）、SetupWeFlow、Start、Status、Pause/Resume/Reset、Stop。正常一次Start依次检查/启动自己拥有的WeFlow桌面API和Akasha；既有AstrBot正常就复用，不再启动第二份。向导和运行模式切换处理好18108/5031，不让用户靠猜。

启动只开放配置会话；如果API未配置、目标为空或11229没就绪，显示具体缺项。运行状态区分“环境就绪、WeFlow已连库、SSE已连、AstrBot WS已连、模型元数据已取、已真实回复”，不把某一个绿灯当全部已通。

旧wxauto入口保留但从主启动中移除，不并行监听/回复同一个群；由操作者正常stop旧实例，不由新脚本按Python名字结束进程。日志/临时媒体/配置/数据库/密钥仍忽略。

## 11. 文件和跨项目归属

| 根 | 预计改动 |
| --- | --- |
| WeChatbot | AGENTS/PROGRESS/TASKS/README，接入说明/报告/实施HANDOFF；新增adapters/akasha的来源锁、薄补丁/配置生成/必要启动控制；单一Start-Akasha入口与本机模板；相关组合测试 |
| Akasha运行副本 | 固定源旁边部署运行副本，仅本计划第6节桥接层补丁；配置/日志/附件在忽略目录。保持原始upstream副本可复核 |
| WeFlow | 只用现成二进制/公开API和自己的home，不改源码、解密/登录内核或微信数据库 |
| QQbot_Snowluma | 必要自有plugins/qq_router的transport-aware分派/共享业务接点、微信平台helper；确有需要的gateway/profile/群记忆配置兼容小改；configure_astrbot只做增量新平台，不重跑覆盖整个QQ配置的旧脚本 |
| AstrBot运行配置 | 备份后增量新增akasha-wechat平台及其配置/会话路由，原QQ平台/模型/账号/数据保留；必要自有插件同步，不改AstrBot第三方核心 |
| 实施台账 | 同一个WX-AKASHA-ALL在两根登记精确文件/同一session，避免另一会话同时启停；微信PROGRESS仍为本项总入口，不再开第二个规划任务 |

不得改旧NapCat根E:/CodexWS/QQbot或登录/相册/私密历史。未来medium按实际diff收敛归属；普通函数拆分/依赖/SDK差异和本计划已列失败分支自行完成，不因原始文件清单少列一个必要小文件就停下来索新规划。

## 12. 一轮落地顺序与部署

1. 读取当前两根AGENTS/PROGRESS/TASKS和本计划，确认HEAD/未提交归属；保留本轮已知规划和所有用户修改。登记唯一实施任务WX-AKASHA-ALL，写后重读。
2. 固定/核对现成包、venv与来源，准备WeFlow向导；操作者同轮完成一次机器人账号/必要登录取钥。普通依赖/缺模块问题现场修好，不重新选型或自写解密。
3. 应用必要Akasha桥接补丁、目标会话/身份/媒体元数据和日志处理；将现有AstrBot自有业务分派/模型/共享记忆/全部增强接线一次完成，写好配置和管理入口。
4. 做第13节少量有意义检查；发现格式/参数/接口/打包问题同轮修复。旧QQ行为必须保留，不用“正在迁移”静默关掉原识图/记忆/free。
5. 备份精确配置，按受管进程身份正常停/更新/启动必要服务。只加新通道/所选配置，不重装AstrBot、不覆写QQ local。若自有QQ源码改变影响现行native/vision技术绑定，沿原revalidate helper同轮完成check、必要零生成probe和operator-trial配对，不重跑旧IQ质量批次或再等一次授权。
6. 现有helper接口为scripts/revalidate_lap43_native_web.py check/probe/activate，probe/activate使用当轮实际expected-binding/expected-active与authorize-operator-trial，不能复制旧摘要冒充当前。只为确实受影响的源做原有必要配对，不另造微信“资格证”平台。
7. 实际核对WeFlow API/SSE、AstrBot WS、加载的provider/profile/能力/配置和0生成模型元数据握手。把新状态和具体用户动作一次交付；用户在授权群自然实测，正常就接受，有具体故障在同任务修，不新增规划轮。

本计划未来实施指令同时授权这些已列的受管部署/配置变更；当前规划会话不实施。模型真实生成、工具服务和微信发送不由agent反复造样本。操作者在该轮指定群自然发测试消息后可据同轮元数据排障，不把“0生成握手通过”写成实际聊天通过。

## 13. 必要检查与用户接受

避免字段镜像测试、全库/72h/极端竞态矩阵。至少用真实AstrBot适配类＋当前bridge代码＋替身模型/UIA/WeFlow做以下组合，优先复用已有测试：

- 目标群新文字→完整OneBot事件/稳定ID→正确平台分派→现有provider→回源一条自然文字；自己/黑名单/未授权群不进模型，非QQ不会再被QQRouter无差别stop。
- 重启ID稳定、首连/重连不回放旧历史，缓冲保留成员/源消息；不会QQ/微信回环或发往另一平台。
- UIA明确false/抛错/部分发送不会预先回成功、不会重试；正常成功可连续第二轮，不逐条要人工ACK。
- 人设/上下文/预算按当前配置，空唤醒/叫名/续聊和free沉默判断接通；pause/reset后的旧结果不再发出。
- schema2新增/更新/删除、reset短期后读回、同一配对空间跨平台读回；未配对/同名成员不串，失败保原件、回执准确。
- 当前消息图精确绑定，图片失败不看旧图，受控表情和adaptive次序正确；不额外启动caption模型或任意出站文件。
- 原生两工具/来源/次数和私密标识限制保留；成员/@不冒充，owner/本机控制不能由昵称或模型输出取得。
- QQ原文字/free/owner/识图/表情/记忆不回归；必要技术配对与真实可执行CLI零生成握手通过，不只检查hash/import。

用户实测只需同一个群正常聊、问一次需要联网的问题、发一张图、按需要表情、记住一个自造称呼并reset后再问；需要跨平台记忆时选好一对会话后在另一端问相同称呼。按实际反馈记录接受，未逐项测试的项写“已接线、待实用反馈”，不强制做完表格每项才交付。

不能再次把“环境inspect成功/初始化成功”记成“真实聊天OK”；要区分CLI_START、模型确实返回、UIA确实提交和用户看见回复。若用户报错，优先修具体代码/依赖，不转成新功能规划。

## 14. 主线、兼容和回滚

微信项目只在main，Akasha取代旧自研入口成为当前主线。旧源码/配置/历史和未决保留，不删除。QQ根按其现行必要隔离/部署规则同轮完成，最终合到main，不能拆成又一轮用户审批或长期悬空分支。

本次规划由用户审阅后交medium；实施只提交检查过的本任务文件和已知规划成果，普通push对应远端并核SHA，不force、不夹带秘密/用户差异。两仓库提交与部署结果分别报告，不把Git推送当服务已运行。

回滚停止本任务受管桥接/WeFlow进程，恢复精确平台/插件/配置备份，保留WeFlow home、密钥、配对/共享记忆新增数据、未决和用户后续修改。不退出微信，不批量kill，不用旧空库覆盖新记忆，不回退QQ其他会话新成果。关闭一个增强功能不应关掉已能用的基本文字。

## 15. 交付形式与不再追加规划的约定

同一轮交付：可运行主线＋一套入口/本机配置＋更新README/真实能力表＋必要检查/部署报告＋HANDOFF。上文所有功能、缺口、降级、基础设施和相互依赖都在本实施范围内。medium不得只交source clone/环境就绪/一份新计划，也不得完成文字后把已列的图片/记忆/控制留作另一个规划任务。

对于确实拿不到的第三方原生能力，用本计划列明的关闭/替代行为完成并报告具体缺口；不为追平旧功能自行修改第三方登录/解密内核，不编造已实现。普通对接问题同轮处理，操作者必须亲自完成的登录/系统授权只需其做那个动作，不重新讨论已授权方案。

### 主要源码依据

- [Akasha固定源码](https://github.com/alingalingling/Akasha-WeChat/tree/9dbe933a9f1bc46e33ca8121334bb1dd01173248/wechat-weflow-bridge-ob11)：bridge_core.py、state.py、ob_protocol.py、uia_sender.py、main.py、ob_client.py。
- [WeFlow维护分支v5.0.1](https://github.com/334456777/WeFlow/releases/tag/v5.0.1)、[native-cli](https://github.com/334456777/WeFlow/blob/v5.0.1/docs/zh-CN/native-cli.md)、[HTTP/SSE API](https://github.com/334456777/WeFlow/blob/v5.0.1/docs/zh-CN/HTTP-API.md)。
- 本机QQ源42911af的plugins/qq_router/main.py、provider.py、scripts/configure_astrbot.py、model_gateway.py、group_memory.py、LAP-43/44交接；AstrBot4.29配置管理/平台实现已只读核对。实际源码版本变更由medium开工时核对，不自动认为旧摘要仍匹配。
