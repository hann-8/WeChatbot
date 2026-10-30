# QQ/SnowLuma → WeChatbot：一次批量迁移实施计划

返回[PROGRESS](../PROGRESS.md) / [TASKS](../TASKS.md) / [规划交接](../tracks/tasks/WX-MIGRATION-PLAN/HANDOFF.md) / [唯一medium指令](../tracks/tasks/WX-MIGRATION-PLAN/MEDIUM_START.md)。

2026-10-30（Asia/Shanghai）。本文件取代28日分三项实施的旧安排。本计划编写时只完成规划；现WX-MIG-ALL实现及必要检查已交付，见[报告](WX-MIG-ALL-REPORT.md)与[交接](../tracks/tasks/WX-MIG-ALL/HANDOFF.md)。以下保留规划依据与实施合同；用户提交统一指令后，medium只领取 **WX-MIG-ALL**，同轮实现全部可复用文字能力、必要检查、配置及启动入口，再交用户实测。旧MIG-01/02/03合并到本项，不要求三次领取；WXA-02/03保留历史，不再作为两道独立前置审批。

## 1. 目标与最小架构

用户的理解方向正确：保留聊天业务，替换平台接入。框架与客户端之间由框架负责，本项目主要适配业务的入站和出站接口，不自行改写QQ↔SnowLuma或微信↔wxauto4内部。

```text
QQ原链路：QQ ↔ SnowLuma/OneBot接入 ↔ QQ路由 ↔ 聊天业务
微信目标：微信 ↔ wxauto4 ↔ 微信薄适配/单群会话 ↔ 复用的聊天业务
```

直接复用模型runner、预算、自然表达/文本整理、整轮裁剪、回复计划、原生联网及记忆存储；补微信消息字段、触发、会话隔离和发送结果的小包装。QQ真实@、群角色、媒体地址和服务端ACK不能靠换字段名取得，不把整个QQ gate/AstrBot/gateway搬来。

**禁止过度防御性编程。** 只保留防错群发送、明确权限、数据隔离、额度/工具范围和unknown不重发等实际边界。没有服务端ACK、稳定微信ID或完整媒体能力，不阻断已明确的单群人工监督文字试用；不再按每个功能多轮规划/验收。

## 2. 当前依据与需要更新的旧判断

| 对象 | 本次只读核对 |
| --- | --- |
| 微信起点 | main=`33c18f01769b956d2dce1e0f83f773e64164e6f1`；起始干净。本规划差异随后产生，实施时保留并审阅 |
| 来源 | `E:/CodexWS/QQbot_Snowluma`，本地与fetch后origin/main均为`42911afc4c1f2bcfbbc3c26afc2647fd21992f08`；干净，不操作服务或local |
| 旧微信快照 | `vendor/qq-core-manifest.json`仍固定到`dd9373029412137023124751d75883824122c784`；63个登记文件，runner和工件锁有微信本地差异 |
| 微信现有接口 | `Wxauto4Client.current_chat/snapshot/send_once`只包装公开ChatInfo/GetAllMessage/SendMsg；真实收发未验 |
| 微信现有模型 | ModelFacade已调用QQ runner/预算/prepare_reply，但仅接离线替身，并有独立8000字符人设限制；config还会拒绝所有enabled feature和>131072政策 |
| Snow最新功能 | LAP-43原生WebSearch/WebFetch及参数封套/URL修复、thinking=false、owner控制；LAP-44 schema2全文记忆/同次增改删/保存回执、可扩大预算均已有源码和部署记录 |
| 工件 | 两根CLI锁均为2.168.0，headless SHA相同；微信已用项目内相对路径。不得用QQ的全局路径/账号配置覆盖它 |
| 真实前提 | 用户自报已登录微信4.2.0.11，接受换版，首试指定群；具体群名和测试发送者只放本机secrets |

源项目的部署/离线报告不等于微信已通过，也不是本轮重新验证QQ效果。旧计划“搜索代码尚不可用、长期记忆继续全部延期、owner未实现、48000是现行推荐”的判断不再用于本实施包。

[源码映射](WX-MIGRATION-SOURCE-MAP.json)固定本次来源、导入候选、需要更新/补齐的文件和插件资产哈希；不包含QQ本机数据。它用于少走重复核对步骤，不增加运行资格系统。动态导入遗漏由medium同轮补齐并写清来源，不为普通依赖细节另开规划。

## 3. 同轮交付范围

| 能力 | 本轮实现与默认体验 |
| --- | --- |
| 收发和触发 | 一个绑定群、指定测试发送者、文本前缀唤醒；公开GetAllMessage轮询/SendMsg。可显式选择仅该绑定范围的all_allowed_text，不默认全群回复 |
| 人设和自然文字 | 微信能力说明＋角色正文＋natural_expression；复用回复计划/prepare_reply，出站单气泡纯文本，不把内部JSON发给群友 |
| 模型/预算 | 复用最新CodeBuddy runner和一次任务语义，带现有工具隔离、清理；不另写模型客户端 |
| 短期上下文 | 默认8个完整成功轮，按实际字节裁剪；会话/配置切换和重启清RAM，reset只清RAM |
| 本机控制 | status、pause、resume、reset、stop；仅本机终端，不从群消息执行运维。pause/stop使尚未提交结果失效 |
| 原生联网 | 默认提供WebSearch/WebFetch，由CLI判断是否需要；沿用最新修复/工具限制/来源封装，取消旧Python关键词/RSS前置 |
| 长期记忆 | 复用LAP-44 schema2全文快照、模型同次memory_updates增改删、原子保存和实际回执；只写微信自己的库/密钥 |
| 使用入口 | 一个本地启动脚本、一个忽略绑定文件、简明README；用户换好客户端并打开指定群后启动、实测 |

本批暂不实现识图、出站表情/文件/语音、成员名册/真实@、QQ式free注意力、无人值守/自动恢复。共用文件可能因依赖随包带入，但这些开关保持关闭；不因其缺口卡住上表交付。不开放第三方自动回复函数。

## 4. 最新共用代码如何取用

1. 以映射中的固定提交读取已跟踪源码，不复制整个源目录，不读QQ local/secrets/state/persona实际覆盖层。保留微信目录名`qqbot_gateway`以避免全库改导入。
2. 按backends、runner、budget、文本/回复、原生联网和schema2记忆的依赖候选更新所需文件；保留未用旧模块，未改变文件无需重抄。把微信runner的相对工件路径、可注入spawn接点合并回新版本，不照旧文件整份覆盖最新runner。
3. 原生联网还需要`adapters/codebuddy_vision_guard/`的三个已版本化插件文件；这是项目自己的CLI扩展资产，不是修改CLI/微信内部。补齐`hosted_cli_budget/vision_mod_guard/cli_web_policy`等导入及公共技术审阅字段。
4. `framework_upper()`还读取`reports/lap-42-vision-closure-sources.json`的bundle/types摘要、framework_parts、framework_upper_bytes，以及锁定包的`types/codebuddy-code.d.ts`。只带这些公开静态材料和匹配的types文件；不搬QQ active/probe/质量通过记录，不要求给无图微信文字路径重新做整套识图绑定。
5. 沿用微信自己的`config/versions.lock.json`和本机工件目录；仅准备/复制精确所需Node、CLI entry、headless bundle和types，哈希对齐。不得整份复制QQ的lock、npm用户目录、CLI配置或凭据。最新runner也必须支持微信原相对node/entry路径；不更新全局CLI。
6. 更新`vendor/qq-core-manifest.json`和`check_snapshot.py`：登记每个文件的真实来源提交/源hash/本地hash/必要微信差异。允许“旧文件保留＋新来源更新”的诚实混合快照，删除硬编码旧源提交断言；继续检查实际文件集与摘要。不加第二套版本/证明服务。

`create_runner`的最新native分支会读取QQ的bot.qq/access字段；微信包装不要伪造QQ配置。可先以原后端设置创建基础runner，再在微信接点设置native_web、web_config、web_private_ids和vision_settings；或给共用工厂增加一个明确、可选的平台中立私密标识参数并登记本地差异。优先改小接点，不新造事件总线/平台框架。

## 5. 单群会话与出站语义

### 5.1 绑定和入站

绑定文件`secrets/wxauto4-chat.local.json`仅保存本机account_alias、conversation_key、chat_type=group、chat_name、allowed_senders、blacklist和唤醒方式。conversation_key是本机生成的持久别名，不声称微信服务端ID；群名/昵称只是这次人工监督的精确匹配条件，不据此授予运维权限。

启动时必须有一个明确群和非空测试发送者列表。用户手动打开该群；默认不ChatWith搜索/强制跳转。构造`WeChat(debug=False, resize=False)`后核对ChatInfo，先记当前可见消息基线，明确显示“基线就绪”，之后只处理新文字。忽略自己、系统、黑名单和非允许发送者；媒体暂不读取。UI ID只在本次窗口epoch内去重，重连/换群先暂停并重建基线，不回拉旧历史、不重放旧消息。

默认trigger_mode=text_prefix、prefix="bot "；它只是文本规则，绝不称为真实@。用户可在本机显式选择all_allowed_text，仍只覆盖该绑定群和allowed_senders；不扩大为全部群/全部成员。微信群里的pause/reset/“我是主人”不执行本机控制。

所有wxauto调用留在创建客户端的线程。模型沿用async runner单并发，等待队列默认5；不让多线程同时摸UI。生成前、保存记忆前及SendMsg前重新确认同一绑定/当前会话和pause状态；UI调用阻塞期间不承诺即时控制。

### 5.2 发送、unknown与上下文

每条入站最多一次模型任务、一次SendMsg。CLI任务内部允许固定上限的工具往返，不是第二次分类/润色模型；不自动切账号/模型/后端或重试。

新连续聊天入口不沿用旧挑战工具“所有发送都unknown、每条必须人工ACK”的规则：

| 实际结果 | 处理 |
| --- | --- |
| 框架返回明确成功 | 记local_reported，正常提交本轮RAM并处理下一条；不称服务端ACK，不逐条要求人工确认 |
| 明确提交前失败 | 记failed，不学习为成功对话；可处理后续新请求，不重发旧请求 |
| 超时、异常或无法解释返回 | 记unknown，暂停该会话后续生成/发送，不自动重试；本机confirm-sent或mark-not-sent只解决该记录，不触发重发 |
| 切窗、改绑定、reset/pause后旧结果返回 | 使旧结果失效，不发到新会话；保留已有未决记录 |

复用现有试用记录原子写函数，使用独立`state/wxauto4-chat/`记录新会话的提交等级；保留旧挑战台账，不清账。原严格mock Router/Gate/NormalizedEvent不改造成假的生产微信通道，新会话入口直接调用共用业务函数。只因UI提交等级较低，不额外搭一个资格/回执平台。

## 6. 文字、联网和长期记忆的接线

### 6.1 文字和模型

新增小型`chat_policy.py`组合微信能力说明、现有natural_expression和微信角色正文；保留已有微信persona，缺失或明确原始模板时才使用源仓库已版本化角色材料。不能覆盖用户后续编辑或复制QQ本机私密persona。

移除独立8000字符人设拒绝，改为角色文件有界读取＋最终system/当前请求/历史/记忆的InputBudget校验。先保留政策、当前请求和记忆全文，再按整轮裁剪短期历史；仍超限则本地明确失败，不硬截当前请求/记忆或换模型。不为读一个大角色另加第二次模型。

在现有ModelFacade旁提取共享文字调用助手，并提供明确的ChatCliModel/连续聊天入口；原离线替身调用不因import/inspect自动启动真实CLI。更新现有配置解析以支持已实现字段，去掉feature_unimplemented及131072上限等过时阻塞，不复制另一套配置系统；有限值和实际有效模型/工件容量仍核对。

### 6.2 原生联网

沿用最新cli_web_policy、CLIRunner及插件，固定WebSearch/WebFetch、MCP空、其余工具关闭。复用`WebRunner.run_native_v2`的来源/ReplyPlan处理或抽出其小型平台中立助手；不为了调用旧QQ HTTP协议伪造可信事件。最终只把当前实际成功工具证明里的最多2个公开URL附在单条文字上，工具过程不发群；失败准确说明本次未核实。

允许“不要联网”关闭当次工具。用过工具的正文不入长期记忆；沿用源代码的剔除逻辑。网页和群文本不提供本机权限，工具参数不带群名、账号/成员标识或整段历史。不回退到旧Python RSS/HTML检索，不新加检索服务/账号。

### 6.3 schema2记忆

复用MemoryStore.prepare/stage、auxiliary、receipt_plan；内部回复可继续使用源v2字段，但出站只提取纯文本。若输入封装需要微信字段，仅写一个本地DTO/转换助手；不修改或伪造NormalizedEvent、QQ消息ID和真实@能力。

记忆按account_alias＋conversation_key隔离，密钥在微信自己的secrets，数据在微信自己的state/group-memory。成员关联为本地允许发送者别名，明示不是跨改名稳定身份；不从QQ导入任何库或key、不跨群串库。人工指定这个会话即可试用，不先要求拿到服务端用户ID。

每轮提供该会话记忆全文，由同次模型提出memory_updates新增/覆盖/删除；不恢复旧关键词/候选、小条数/240字节门槛。保存前确认当前绑定仍有效，使用源版本/事务/原子写。保存结果先生成真实回执再创建发送记录，不能把模型“已记住”直接当保存成功。已经保存但发送失败时保留记忆和结果，不谎报回滚；unknown按5.2处理，不重复执行已保存更新。

reset只清RAM，长期记忆保留；本机memory-status可显示条数/字符/最近结果。全库导出/删除不是群命令，日常停机不清记忆。坏库/容量失败只关闭该会话记忆增强并提示一次，基础文字仍可用，不覆盖原件；明确要求记住时回执如实说明失败。模型/格式整体失败不另发第二次修复请求。

## 7. 配置与生效

在现有五份配置/defaults中增加必要字段，只有一个config/local入口；真实对象/昵称放secrets绑定，不再派生第二套手工版本文件。模板可准备好下列功能，但bot.enabled/sends默认false；只有用户明确运行live入口才构造wxauto、启动模型和发消息。

| 字段/行为 | 推荐值/处理 |
| --- | --- |
| 后端/模型 | codebuddy_cli / deepseek-v4.1-flash；家庭Ollama保留，用户手动选择，不读取家庭凭据 |
| CLI推理/思考 | 迁移源所用low；子进程alwaysThinkingEnabled=false，不能把low说成启用了思考 |
| CodeBuddy可见输入政策 | 524288 UTF-8字节，overhead/output各2048，context_window_tokens仍null；取代旧48000建议以容纳全文记忆，不称原生token窗口或免费保证 |
| 可配置容量 | 去除微信131072字段封顶；沿实际C/F/V/O/当前模型工件范围校验，可降低/扩大，不加一个新的随意常数上限 |
| 短期历史/队列 | 8完整轮，单并发、队列5；按实际字节进一步裁剪 |
| 回复 | single、自然纯文本；max_reply_chars沿已有8000，不沿旧挑战工具500字限制裁掉正常答案 |
| 联网 | enabled=true、engine=codebuddy_cli、search_enabled=true；最多3工具调用/4主步骤/90秒，单结果8000、合计12000字节 |
| 记忆 | enabled/learning_enabled=true；max_chars_per_group=50000、单文件1048576字节、总8388608字节；均可配置扩大，不被默认值封顶 |
| 不支持的能力 | vision/memes/members/bilibili关闭，无真实@、QQ式free和出站媒体 |
| 发送结果 | local_reported可继续；unknown仅暂停本会话，不自动重发 |

已有local先备份，仅改本任务明确涉及的CLI输入政策/effort及新增功能配置，保留账号、所选后端/模型、Ollama参数和用户无关设置；已有自定义值逐项审阅，不模板覆盖。若用户原来显式选择家庭路线则保持选择，并说明本轮原生联网只适用CLI；不得自动切后端。

## 8. 客户端配套：同轮准备，用户换版/登录

2026-10-30官方[安装页](https://docs.wxauto.org/docs/install.html)仍说明免费版支持到微信4.1.8.107；[PyPI](https://pypi.org/project/wxauto4/41.1.7/)免费包为41.1.7。用户当前4.2.0.11不在该支持说明范围，不能写成“已经兼容”或“必然不能运行”。本批推荐配套为项目Python3.12 x64＋wxauto4 41.1.7＋微信4.1.8.107，不切付费Plus或其他框架。

medium同轮核对本项目已准备依赖和已有安装包；可复用此前临时工件及已记摘要，必要时仅下载计划归档工件到临时目录。准备换版入口/简明说明后，由用户退出当前客户端、正常安装及登录；不卸载数据、不退出账号、不自动操作安装UI。已获得接受换版的答复，不再问一轮意愿。

旧`4.1.8.1000/4.1.8.0`是安装器文件/产品元数据，不能仅凭它们与发布标签不同就永久封死试用。摘要/发布者用于核对工件；真正配套版本看用户安装后客户端显示及公开API实际表现。用户数据删除、登录限制或旧版无法登录如发生，报告具体问题，不自行绕过；代码和其余可用成果照常完成，不把它们卡在安装器前。

## 9. medium文件归属和同轮顺序

| 范围 | 预期文件 |
| --- | --- |
| 薄适配与连续入口 | transports/wxauto4_adapter.py；新增wxauto4_chat.py、chat_session.py，保留原wxauto4_trial命令 |
| 微信业务小接点 | 新增chat_policy.py，model_facade.py；必要小型memory/native输出助手可并入session，不为每层另造框架 |
| 配置 | config.py、defaults.py、config/examples五份YAML、wxauto4-chat.example.json；本机config/local精确字段和secrets绑定忽略 |
| 共用代码/CLI资产 | 源码映射所列src/qqbot_gateway文件、三份插件资产、公共审阅字段、必要运行types；更新原manifest/check_snapshot/prepare_cli |
| 启动和使用 | 一个Windows启动脚本，README中配置/启动/本机命令/换版/实测说明，不新建Web管理台 |
| 定向验证与交接 | 复用原mock/模型替身，新增必要会话/记忆/native测试；任务报告、WX-MIG-ALL/HANDOFF、PROGRESS/TASKS |

同一session一次领取WX-MIG-ALL，顺序为：固定源/保留差异→更新共用依赖和配置→薄适配/模型/上下文/联网/记忆→启动入口与客户端准备→必要检查→交付用户实测。它们是内部步骤，不是新的审批/任务关卡；不要做完MIG-01停下来等第二次指令。

当前规划文件是上轮已知成果，实施时保留并可随本任务检查后提交；不把它们当未知用户改动丢弃。源QQ/SnowLuma及运行实例保持只读，不复制其local、人设覆盖层或运行证据。

## 10. 必要检查和完成标准

不先补全库/长稳/极端竞态矩阵。medium同轮完成少量有意义的组合反例：

- 源码/资产可导入、manifest一致、相对工件路径与types齐全；inspect/mock均0真实UI/模型/发送。
- 一次新文字→同一模型替身任务→一条SendMsg；启动基线不回放、自己/黑名单不触发，错群/暂停后的旧结果不发送。
- 明确框架成功可继续第二轮；unknown不重试、不清账，既有unknown记录保持。
- 大角色不再被8000字符误拒；预算超限只裁历史，不截当前请求/全文记忆；不意外开启工具/第二次模型。
- native包包含最新参数封套/HTTP(S)修复和工具/结果上限；非法来源不当作证据，工具失败不偷偷改后端。
- schema2新增→清RAM/新Store读回→更新/删除、保存失败原件保留和准确回执；联网材料不学进库，跨会话不串。

检查通过即交付可启动版本和真实未验说明，不要求先由agent调用真实模型、联网服务或群发。用户负责后续实际效果；有具体问题就在本任务范围修复，不新增一轮完整规划。客户端版本未配套时写成明确的用户动作，不把代码准备称全部受阻。

## 11. 用户实测与回滚

用户换好配套客户端、登录、打开指定群；首次只填一个忽略绑定文件中的群名/测试发送者，再用启动脚本运行。无需重复配置QQ群号、多个服务端口、技术绑定和每条ACK。

按自己的节奏试：普通文字和第二轮承接；pause/resume/reset；“记住一个自造称呼→reset短期上下文→再次询问”；一条需要联网或给定URL的问题。看到这些行为正常即可按用户接受记录，不要求媒体或长稳全通过；原历史80项与QQ的33项都不冒充微信真实结果。原native质量/5万字符成本和稳定性仍按实际体验，不作永远不掉线承诺。

回滚仅撤销本任务代码/精确local字段；保留原始消息之外的发送未决、微信记忆/密钥和用户后续修改，不退出微信、不删聊天数据、不改QQ。关闭web/memory只停增强，不关闭已能用的基本文字。Git只在main进行，按用户届时提交的实施指令提交/普通push归属文件并核SHA，不force、不建分支。
