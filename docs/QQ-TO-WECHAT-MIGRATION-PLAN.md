# QQbot → WeChatbot：先迁移易复用功能的详细计划

返回[PROGRESS](../PROGRESS.md) / [TASKS](../TASKS.md) / [本轮交接](../tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md) / [实施指令](IMPLEMENTATION_GUIDE.md)。

2026-10-28（Asia/Shanghai）。状态：仅规划，功能未实施。后续统一由 **gpt-6.1-sol / medium** 落地；不再使用 Terra 实施本项目。用户已授权本规划 commit/push 并直接进入当前默认主线 `codex/bootstrap`。本轮不跑业务测试，不处理微信账号/安装器，不执行真实微信、模型、公共网页或家庭 SSH。

## 1. 迁移含义、目标与本轮出口

这里的迁移，是把 **QQbot 当前 SnowLuma 主线的成熟聊天业务复用到 WeChatbot 的 wxauto4 路线**。来源是功能实现与行为合同；账号、群、凭据、聊天记录、旧历史、记忆库、图库和运行环境不随功能复制。

目标是先让微信具备好用的文字聊天基础：人设和自然回复、受控模型调用、短期上下文、本机重置/暂停；随后增加用户指定网页的正文读取。先准备这些平台依赖较少的代码，真实收发和模型试验以后集中做。WX-WXA-02 当前阻塞不妨碍文档规划及独立代码准备。

本轮交付详细行为、配置默认值、文件范围、任务次序、后续验证与回滚合同。仅完成本计划不代表代码已迁移、开关已启用或微信可自动聊天。

## 2. 固定基线与真正要补的接点

- 来源 QQ main：`52866fe10cc654d2e12c5520f7afc5aa8bbe0179`。
- 微信功能基线：`codex/wxauto4-trial-kit` / `29240978a298e3fd5a47a21af7eb10a670d48994`。
- 微信原默认主线：`codex/bootstrap` / `8ad1334a66ee9d3ff7cedc70b51ce4fa3dc085ac`。试用分支仅多两次已有提交，适合连同本轮文档普通快进；保留其作者/历史，不 squash 混入文档。
- 微信已有 63 文件 QQ 核心快照，manifest 源提交为 `dd9373029412137023124751d75883824122c784`。18 个共享模块按 Git blob 抽查：12 个与 QQ 当前 main 相同；token_budget、workbuddy_cli_runner、persona、web_policy、web_retrieval、web_extractor 不同。
- chat_text、reply_plan、session_queue、backends、public_http/public_network、group_memory、attention、meme_catalog、reply_delivery、group_silence、turn_v2 已有相同源码。**这些模块通常不需要再复制，主要工作是微信调用面和语义适配。**
- 微信 `ModelFacade` 只接受离线替身，`Router`/`Gate`/`NormalizedEvent` 仍为严格离线核心。wxauto4 当前独立试用只用 ChatInfo/GetAllMessage/SendMsg，昵称和 UI ID 只在人工监督范围内有效；不强制塞回生产事件，不改 capability 为 true 冒充接通。
- WX-WXA-01 的 10 专项/80 全套通过是已交付历史报告，本轮未重跑。WX-WXA-02 尚未真实收发，WX-WXA-03 尚未真实生成，这些记录继续保留。

依据：[目标模型调用面](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/src/wechatbot/model_facade.py#L9-L51)、[配置限制](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/src/wechatbot/config.py#L94-L109)、[试用实现](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/src/wechatbot/wxauto4_trial.py#L82-L153)、[固定快照](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/vendor/qq-core-manifest.json)。

## 3. 按迁移难度排序

| 功能 | 复用/适配工作 | 顺序及决定 |
| --- | --- | --- |
| 人设、自然语气、纯文本和长度处理 | 复用角色材料、natural_expression、prepare_reply；补微信能力说明 | 第一批 WX-MIG-01 |
| CodeBuddy 调用、预算、串行与清理 | 已有固定 runner；准备显式监督调用面，保留旧离线入口 | 第一批 WX-MIG-01；承接 WXA-03 的代码准备 |
| 短期上下文 | 复用整轮裁剪/预算；给当前监督会话增加内存上下文 | 第二批 WX-MIG-02 |
| 本机重置/暂停/继续 | 会话级小状态；不依赖微信昵称鉴权 | 第二批 WX-MIG-02 |
| 指定 URL 的网页正文读取 | 复用公共 HTTP、正文提取、证据预算；只增加明确单页入口 | 第三批 WX-MIG-03 |
| adaptive 多气泡发送 | 生成计划容易复用，但分次提交、部分发送与未决处理仍需适配 | 后续候选；前三批保持单气泡 |
| 长期记忆自动学习 | 源模块已有；需要会话/人物稳定关联和成功回复确认 | 延后；先短记忆，不搬旧库 |
| free、叫名/引用/续聊、真实群 @ | 缺微信原生身份/@/引用与触发实测；QQ 43 新规则本身也仅规划 | 延后；不把文本名字当平台真实 @ |
| 图片理解、表情发送、成员名册/受控 @ | 依赖 wxauto4 对应原生接口与媒体/成员真实效果 | 延后；不为追平功能改框架核心 |
| 搜索“最新消息” | QQ 当前 SEARCH_QUALITY_PASSED=false，来源功能尚未可用 | 不作为现成能力迁移；保留网页读取 |
| B站字幕、ASR、自动登录/长稳 | 前者已在 QQ 退役，其他不属于当前易迁移聊天能力 | 不纳入前三批 |

不设抽象插件平台、OneBot 转换、AstrBot 桥接、通用事件总线或第二套模型客户端；已有纯函数直接调用，必要接点放在 `src/wechatbot/`。

## 4. WX-MIG-01：先迁移人设、回复和模型代码准备

### 4.1 人设与能力合同

使用微信自己的 `config/persona.md` 保存可编辑角色材料。可采用 QQ 已版本化角色正文作为候选，保留称呼和表达；不复制 QQ 授权群/QQ 身份/私聊关闭等平台政策，不自动导入任何本机私密角色文件。

微信新增一个小型 `chat_policy.py`：组合微信当前真实能力说明、已有 `natural_expression(1)` 和角色正文。首批只描述“当前明确选择的一条文字请求、单条自然纯文本、一次尝试、无群管理/媒体/搜索”；网页阶段再按实际材料扩展。不照搬 QQ `compose_persona` 中写死的群 @ 和 QQ 群协议。

复用 `prepare_reply` 做一次纯文本处理，保留代码/JSON 的字面含义；首个监督模型试用仍按原合同不超过 500 字符、一次 SendMsg，不发送内部 JSON/状态报告。认真问题不靠第二次润色模型补长答案。多气泡协议不在本项启用。

### 4.2 输入预算允许 48000，并修正独立的人设长度限制

用户已明确预算可调整，48000 可以采用。微信当前 16384 是配置值，配置解析上限为 131072；固定能力记录中的 DeepSeek maxInputTokens=1000000，未发现阻止 48000 的更低静态硬上限。该记录与 CLI 2.168.0 工件摘要绑定，仍不是本轮真实握手或原生有效窗口证明。

因此，后续实施的 CodeBuddy **推荐输入政策为 48000**，overhead/output reserve 各保持 2048，context_window_tokens 仍为 null；模型 deepseek-v4.1-flash、reasoning_effort=auto 保留微信当前选择，不照抄 QQ 的 low 或家庭后端设置。数字仍沿现有字段名，但这里统计项目可见 UTF-8 wire 字节，不能称 48000 个模型 token，也不保证免费、credits 或延迟不变。

只提高预算还不够：QQ 角色正文为 19,256 UTF-8 字节、9,585 Unicode 字符；微信 `ModelFacade` 当前另有 `len(system)>8000` 拒绝，直接搬入会触发 persona_size。应移除这个独立的固定字符门槛，改为按输入预算进行文件字节预检，并对“微信政策+角色+当前完整请求”执行既有 InputBudget 校验。人物内容能在 48000 内容纳时，不为旧 8000 限制擅自删角色段落；不能仅删校验后无限读取。

先保留固定政策与当前问题，再按完整 user/assistant 轮裁剪旧历史；仍超限则本地拒绝，不截断当前请求、不临时改模型或继续放宽。若实施时有效元数据/真实控制握手显示更低上限，采用较低边界并记录具体差额，不能只凭旧记录强行通过。本轮不运行握手或模型。

此项修改模板中所选 CodeBuddy 的一个输入标量 16384→48000；其他模型参数、Ollama 预算不变。已有 local 不用模板覆盖：只在后续代码实施明确归属内更新对应标量，或保留原值并报告尚未迁移。只改模板不会改变已有 local 的运行值。

依据：[预算与长度代码](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/src/wechatbot/model_facade.py#L30-L51)、[配置校验](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/src/wechatbot/config.py#L122-L135)、[能力记录](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/config/cli-capabilities.json)、[实际字节算法](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/src/qqbot_gateway/token_budget.py#L27-L65)。

### 4.3 显式模型入口与文件范围

复用固定 create_runner/InputBudget、工具/MCP 隔离、视觉 ContextVar 清空、一次尝试及既有清理台账。对 `ModelFacade` 提取小型共享文字调用助手，让旧 `generate(event,...)` 继续走离线替身；新增明确命名的 `TrialCliModel` 监督入口，输入为文字/历史/trace，不造虚假 NormalizedEvent。

先完成代码准备，CLI 构造与实际调用仍只在后续明确选中的监督入口执行；导入模块、inspect/mock 不应拉起真实 CLI。不得捕获 real_model_closed 后静默改用真实执行，不动冻结 `src/qqbot_gateway/` 快照。真实 WXA-03 的一次生成/一次发送上限及前提继续保留，代码准备不自动消耗或增加真实次数。

预期范围：`src/wechatbot/chat_policy.py`、`model_facade.py`、必要的 `config.py` / `config/examples/models.yaml` / `wxauto4_trial.py` 接点，以及定向离线验证与任务文档。不加入新后端、图像协议、全局 CLI 配置或账号切换。

完成出口：人设/能力说明和纯文本路径可独立调用；48000 与 persona_size 替代规则落地；监督调用面可注入替身，旧 mock 路径仍明确关闭真实模型。未跑验证就标“代码准备、未验证”，不能借历史 80 项晋升通过。

## 5. WX-MIG-02：短期上下文与本机控制

只管理当前人工监督绑定和本次会话周期的 RAM。scope 至少含本机账号别名、会话类型/准确名称、指定测试者、本次运行 epoch，以及人设/所选模型配置版本；这些是本机隔离键，不声称是真实微信稳定身份。切窗、换绑定、重建、重启或版本变化即清空，不跨人/会话合并。

沿用 `chat.history_turns=8` 的存储上限及 InputBudget/trim_history 的完整轮裁剪语义；送模型前还会按字节进一步裁剪，不承诺每次带满 8 轮。先用内存容器，不另造持久记忆库，不将 wxauto4 昵称硬写到原严格 Store 的可信身份字段。

仅在对应回复被人工确认看到后提交一整轮；框架 status=成功只能记 local_reported。未决期间停止后续自动生成/发送，不能把“已生成”当“已聊天成功”。这与原一次试用台账一致；人工确认不伪装服务端 ACK。连续会话的确认提示只用于确实存在未决结果，不逐条增加与动作无关的确认。

本机动作：reset 清 RAM 并使待发送旧结果失效；pause 阻止新的生成/提交，resume 只恢复之后新请求。暂停保留 RAM，重置不清发送/模型未决台账。检查点在本项目可控制的提交前；已经进入框架 SendMsg 的动作无法撤回，框架阻塞期间也不保证即时响应。

先提供会话对象的方法和现有终端入口的小接点，不新建 Web 管理台、远程命令或文件监视器。群成员消息、“我是主人”、昵称、模型输出不执行控制命令；QQ 43 owner-only 本身尚未实现，不能当作已成熟代码直接迁来。

预期范围：新增小型 `src/wechatbot/session_context.py`，复用模型调用助手和 `wxauto4_trial.py` 的显式监督接点；旧 `Store` / `Gate` 的严格身份合同保留。本项先备好内存业务，真实多轮运行范围以后由用户选择，不自动将单次挑战试用扩成常驻群机器人。

## 6. WX-MIG-03：只迁移用户指定网页的读取

只处理当前明确请求中给出的一个公共 HTTP(S) URL；没有 URL 时普通文字继续，不搜索，不从历史/记忆补链接。不读微信转发消息、聊天数据库、登录页、内网地址、文件或视频，也不接新检索账号/付费提供方。

用目标已有 PublicHTTP/PublicResolver/PublicNetwork 和 WebExtractor、sources_for_budget 组合一个小型 `url_reader.py`。不直接启用目标旧 Retriever：它还连接 B站字幕服务；也不为这一步全量同步 Snow 的新 web/vision/runner 代码。正文提取依赖在实施前按现有锁核对，只加实际必需项，不升级无关包。

首期固定上限：每轮 1 页、15 秒、响应 1MiB、最多 2 次受原公共边界约束的重定向、正文最多 4000 UTF-8 字节。正文/来源/当前请求/人设共同进入 48000 政策，先裁历史，再缩正文；不能读到正文就不假装已阅读。网页内容仅作材料，不能改变调用、身份、模型或发送目标。

取得材料后仍只做原本的一次模型生成；失败不追加搜索、备用站或修复模型。代码追加实际 URL 来源，给来源完整字符串预留输出空间，再裁回答正文；500 字符首试限制仍适用，不截断 URL。如果来源本身占满限额，本地说明无法在本次回复限额内输出，0生成。日期未知只说明日期未知，不冒充“最新”。

默认 `features.web.enabled=false`；本项真正接通后才允许显式监督入口选择 true，其他 feature 仍 false。配置解析复用现有严格读取/形状校验：必要时抽取共用读取助手并增加一个专供监督路径的加载入口，仅放行已实现 web；原 load_config/严格离线 Gate 仍不支持真实生产 transport。开关不依赖捕获 feature_unimplemented 再绕过验证。

预期范围：`src/wechatbot/url_reader.py`、模型输入组合和监督配置加载的最小接点；使用现有 feature 字段，不加搜索/媒体字段。普通网页质量尚需后续真实检查；不将 QQ 旧搜索问题带到微信重做。

依据：[QQ 搜索关闭](https://github.com/hann-8/qq-persona-bot/blob/52866fe10cc654d2e12c5520f7afc5aa8bbe0179/src/qqbot_gateway/web_policy.py#L6-L11)、[目标旧 Retriever](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/src/qqbot_gateway/web_retrieval.py#L106-L144)、[源文字与来源约束](https://github.com/hann-8/qq-persona-bot/blob/52866fe10cc654d2e12c5520f7afc5aa8bbe0179/src/qqbot_gateway/persona.py#L41-L43)。

## 7. 配置、默认值和生效方式

| 配置/状态 | 计划默认与生效 |
| --- | --- |
| 后续实施 agent | 全部 gpt-6.1-sol/medium；历史 Terra 记录仅作已发生事实 |
| config/persona.md | 微信独立角色材料；可迁已版本化 QQ 角色正文，不自动复制秘密/旧历史 |
| CodeBuddy input_budget.context_input_limit_tokens | 推荐 48000；只影响选中 CodeBuddy profile 的可见 UTF-8 字节政策 |
| overhead/output reserve | 各 2048；不宣称为远端原生输出 token 设置 |
| context_window_tokens / reasoning_effort / model | null / auto / deepseek-v4.1-flash，保持当前目标选择 |
| chat.history_turns | 沿用 8，范围 1..32；上下文提交还受预算与确认状态约束 |
| 首次监督输出 | 沿原 WXA-03 ≤500 字符、一次提交；adaptive 延后 |
| web.enabled | 默认 false，MIG-03 实现后只在明确监督入口启用 |
| vision/memes/memory/members/bilibili | 保持 false；短期 RAM 不等于 memory 功能开关 |
| 真实入口/真实模型 | 默认关闭；代码准备不触发安装、登录或调用 |

配置在一次明确启动/新会话时读取快照，不加热更新。模型/人设/预算变化重新构造会话，清本轮 RAM，不改未决记录。示例配置、已有 local 与运行加载值分开报告；不迁 QQ local/secrets，不从全局环境猜账号/群或从 persona 推权限。

## 8. 实施顺序与现有任务关系

| 任务 | 独立交付与依赖 | 本轮状态 |
| --- | --- | --- |
| WX-MIG-01 | 人设/纯文本/48000与字符门槛修复/监督模型代码准备；不依赖 WXA-02 真实通过 | planned，优先下一项 |
| WX-MIG-02 | 短期 RAM 与本机控制；复用 MIG-01 文字接口，先做独立内存业务 | planned，不自动领取 |
| WX-MIG-03 | 单 URL 读取；依赖 MIG-01 输入组合，MIG-02 非硬前置 | planned，不自动领取 |
| WX-WXA-02 | 配套客户端/账号/一个指定会话的一收一发；既有真实阻塞保留 | blocked，另定时段 |
| WX-WXA-03 | 在 WXA-02 目标收发已实测后，进行一次真实 CLI/一次发送 | 真实范围仍 planned |

每次只领一个任务。MIG-01 可完成原 WXA-03 的共用代码准备，但不能把 WXA-03 的真实验收改成 completed；不得建立第二套 TrialCliModel 或独立 runner。后续真实试验复用已迁功能，并明确本轮所选人设、预算和上下文范围；若从原空历史单次试验改成多轮，先由用户选定具体范围，不沿用旧次数当新授权。

## 9. 验证、验收与测试暂缓

本轮只查源码/固定版本/文档链接、状态和 Git 差异；没有项目测试、inspect/mock、真实网络采样或控制握手。用户说测试不急，不要求先补一整套矩阵才能继续规划/独立代码准备。

未来按功能做必要定向验证：MIG-01 检查角色 9585 字符可在48000政策内处理、最终wire超限拒绝、纯文本与一次调用；MIG-02 检查整轮裁剪、scope/版本切换、未确认不学习、reset/pause不解未决；MIG-03 检查显式单URL、HTTP限制、失败0生成、来源不编造及一次调用。优先复用原替身和有意义反例，不为每个字段写镜像测试、不默认跑全库。

代码准备、离线验证、微信真实收发、真实模型回复、真实多轮/网页效果分别记录。以后做真实测试时只检查选中的功能，不以图片/成员/长稳/全功能资格阻挡文字功能试用。实际身份、显示名、临时ID和ACK等级继续如实标明。

## 10. 分支、兼容和回滚

本轮只提交六份文档：AGENTS、PROGRESS、TASKS、IMPLEMENTATION_GUIDE、本计划、本交接。用户已授权直接推主线；默认分支名仍为 codex/bootstrap，不自行改名或改变默认分支。保持两个试用提交的原历史，新增文档提交以试用 HEAD 为父，普通快进默认主线，提交前重查两条远端；如出现新独立提交，先保留并重新核对，不能 force 覆盖。

未来实施从届时主线重新确认起点，可用 codex/ 前缀隔离代码。云端任务使用实际 checkout，只做代码/文档和适合该平台的离线工作；微信/QQ客户端真实运行仍在Windows，不能把Linux容器检查写成真实收发。本笔记本不留存项目，交付后删除本轮本地覆层。固定快照、原 mock/严格核心和旧试用命令保留；不做全库同步/清理，不修改 QQ、上游 wxauto4 或日常微信。

回滚按任务代码提交撤销；未决/attempt/清理记录始终保留。撤销代码不退出附着微信、不删 state、记忆或登录资料。预算回滚仅恢复自己改过的 CodeBuddy 标量，角色文件恢复仅限本任务已保存的版本，不覆盖后续用户修改。已经明确不用的 Terra 不能作为回滚后的实施默认。

## 11. sol/medium 首项接续指令

下面只用于后续用户选择实施；本规划提交不自动启动。

```text
你是 gpt-6.1-sol/medium。请在实际 WeChatbot 项目只领取 WX-MIG-01，按 docs/QQ-TO-WECHAT-MIGRATION-PLAN.md 第1—4、7—10节完成最容易迁移的文字功能代码准备，交付后停止。
先读 AGENTS、PROGRESS、TASKS 和 WX-MIGRATION-PLAN/HANDOFF，核对主线最新 HEAD/工作区；登记本任务负责人、时间、文件并写后重读，保留用户/其他session修改。
复用固定QQ核心与现有微信调用面：增加微信能力/人设组合、一次纯文本处理，以及显式 TrialCliModel 共用接点。旧 ModelFacade 默认仍仅离线替身，不造生产身份/资格，不改框架核心，不新建后端。
输入政策可按本计划改为48000，overhead/output各2048，保留模型/auto/null。同步处理8000字符人设门槛，以最终UTF-8 wire预算校验；QQ角色正文9585字符不是必须先删到8000。已有local只改归属内精确标量或报告保留，不能模板覆盖。
本项不安装/切换/登录/观察微信，不运行真实CLI/模型、公共网页、SSH或发送，不领取WXA-02/03真实试用。测试按用户当前“暂缓”安排，不自行展开完整矩阵；必要静态与定向离线检查据实记录，没跑就标未验。
仅提交本任务检查文件，按届时适用的Git授权核远端SHA，不force；更新任务报告、HANDOFF/PROGRESS/TASKS后停止，不自动做MIG-02/03。
```

## 12. 来源与适用性

本计划对源码与 Git 状态的判断固定到第2节提交；现行 wxauto4/客户端兼容、CLI登录/额度/模型效果和真实运行状态未重新验证。已有报告仅说明各自记录时点。

- [QQ 固定业务与自然表达](https://github.com/hann-8/qq-persona-bot/blob/52866fe10cc654d2e12c5520f7afc5aa8bbe0179/src/qqbot_gateway/persona.py#L15-L43)、[纯文本处理](https://github.com/hann-8/qq-persona-bot/blob/52866fe10cc654d2e12c5520f7afc5aa8bbe0179/src/qqbot_gateway/chat_text.py#L46-L102)、[回复计划](https://github.com/hann-8/qq-persona-bot/blob/52866fe10cc654d2e12c5520f7afc5aa8bbe0179/src/qqbot_gateway/reply_plan.py#L89-L135)。
- [微信预算/角色接点](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/src/wechatbot/model_facade.py)、[短历史已有严格实现](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/src/wechatbot/store.py#L82-L92)、[监督发送与未决](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/src/wechatbot/wxauto4_trial.py#L133-L153)。
- [WX-WXA-01 已交付报告](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/docs/WX-WXA-01-REPORT.md)、[WX-WXA-02 阻塞](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/docs/WX-WXA-02-REPORT.md)、[旧最小试用合同](https://github.com/hann-8/WeChatbot/blob/29240978a298e3fd5a47a21af7eb10a670d48994/docs/WXAUTO4-IMPLEMENTATION-PLAN.md#L144-L175)。
