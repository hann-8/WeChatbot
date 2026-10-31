# WeChatbot：Akasha主线

当前主线 **WeFlow → Akasha-WeChat → 现有 AstrBot**。WX-AKASHA-ALL 正在实施和受管部署；基础及增强接线、必要替身检查已完成，账号向导/真实绑定仍待操作者完成，尚未宣称真实微信聊天通过。[项目进度](PROGRESS.md) · [实施交接](tracks/tasks/WX-AKASHA-ALL/HANDOFF.md) · [实施报告](docs/WX-AKASHA-ALL-REPORT.md)。

现有 QQ 功能/凭据保持，模型与人设同源；记忆按本机显式会话/人物配对共享，未配对独立。原 wxauto/CLI 保留为历史，不参与 Akasha 主启动。

## Akasha 使用入口

```powershell
cd E:\CodexWS\WeChatbot
.\Start-Akasha.ps1 prepare
.\Start-Akasha.ps1 setup
.\Start-Akasha.ps1 start
.\Start-Akasha.ps1 status
.\Start-Akasha.ps1 stop
```

首次运行 `setup` 后打开 [本机管理页](http://127.0.0.1:18766)，点击带本机授权的 WeFlow 向导，选择机器人账号/目录，使用现成向导获取并保存数据库与图片密钥。必要退出/登录和系统授权由你正常操作，密钥不发到聊天。保存后点击“切到桌面 API”及“读取账号/会话选项”。

单一配置为忽略的 `config/local/akasha.json`，管理页可读取/保存，令牌不回显。`bridge.bot_wxid` 填已选机器人账号；`bridge.sessions` 填所选群的 `{"id":"所选sessionId","name":"微信中唯一可搜索的群名"}`。同名群需先在微信中改成可唯一搜索的名称。群内全体非黑名单成员可按规则触发，不设发送者白名单。`mode=all` 仅指入站，回复由同源 free/叫名/续聊策略决定；`mention` 只收文本唤醒，`batch` 保留合并前的每条消息/成员来源。私聊独立开关默认关闭，开启需单独填 `private_sessions`。

共享记忆只在 `pairings` 明确选择：`{"wechat_session":"所选微信群ID","qq_session":"已授权QQ会话ID","scope":"facts_only","actor_links":{"可信微信wxid":"对应真实QQ用户ID"}}`；两端 ID 只填本机。`facts_only` 共用 schema2 事实、短期独立；`shared_context` 同时共用所选会话 RAM。未配对、未链接人物均独立，不凭昵称自动合并。取消配对不会删除旧记忆。

保存配置后运行 `start`；会复用现有 AstrBot/gateway，必要时仅调用该项目受管启停入口加载微信平台，不运行旧的全量 AstrBot 配置重建。原 QQ 6199 保留，微信独立 11229，管理 18766，WeFlow 向导 18108/桌面 API 5031 共用专属 home。普通 SSE/WS 断连由原桥接重连，不回放启动前历史。

`pause` / `resume` / `reset` / `memory-status` / `resolve-unknown` 也可作为入口参数，`-Session` 可选定一个本机会话。reset 只清短期。发送明确完成记 `local_reported`，不是服务器 ACK 或用户已看见；false、异常、部分发送或返回连接丢失暂停该会话，不自动重发。核对微信实际情况后才用 `resolve-unknown` 继续，不补发旧结果。stop 只结束身份记录匹配的 Akasha/WeFlow/面板，不退出微信，不停止其他平台。

## 当前能力

| 能力 | 接线与边界 |
| --- | --- |
| 文字/角色/上下文/free/adaptive | 复用现有 QQ 自有业务、provider、队列、ReplyPlan，始终回源；真实效果待用户实测 |
| schema2 记忆 | 同次模型全文增改删、原子保存/准确回执；复用同一 MemoryStore/key/库，不复制 |
| 联网 | 同一 CLI 任务内仅 WebSearch/WebFetch，3调用/4步骤/90秒、单8000/总12000字节；无自动后端/账号切换 |
| 当前图片 | 完整 serverId 关联、一次性本机材料、现有原生归一化/同轮推理；失败不取旧图，不启动 caption 模型 |
| 表情/成员 | 只发送现有登记素材；公开群成员补充真实称呼，缺失不挡文字；GIF按首帧，不声明保留动画 |
| @ | 文本唤醒/称呼；原 UIA 发送接口不提供微信原生@，明确关闭 |
| 控制 | 本机管理；只有公开源可信 wxid 与显式 owner_wxid 相符才允许群内暂停/恢复/reset |
| 语音/视频/任意文件/B站退役功能 | 关闭/准确提示，不新增 ASR/TTS 或付费 API |

状态分别显示依赖、连库、SSE、AstrBot WS、零生成元数据检查及本地发送次数；任何一个绿灯都不代表用户已收到回复。详细证据与回滚见实施报告。

以下是旧 wxauto 文字版历史说明，保留供查阅，不作为主线启动步骤。原 Start-WeChatbot.ps1 仍是旧入口，后续 CLI 缺模块的 PROTOCOL_ERROR 未修复。

---

# 旧wxauto文字版（历史）

WX-MIG-ALL 已实现；2026-10-31用户反馈启动恢复、测试OK，单群文字版已接受。入口：[PROGRESS](PROGRESS.md)、[任务交接](tracks/tasks/WX-MIG-ALL/HANDOFF.md)、[检查报告](docs/WX-MIG-ALL-REPORT.md)。真实微信兼容、模型效果、原生联网服务与群发送均未由 agent 验收。

微信 → wxauto4 免费公开接口 → 单群会话 → 已有 CodeBuddy CLI/家庭 Ollama 业务。支持人设、单条自然纯文本、8轮RAM上下文、本机控制、CLI WebSearch/WebFetch、schema2会话独立全文记忆。媒体、成员、真实@和QQ式free关闭。

## 本机首次使用

本机 Python3.12、wxauto4 41.1.7及独立CLI工件已准备；config/local五份配置与secrets/wxauto4-chat.local.json空模板已建立。真实群名、昵称只填本机绑定，不提交Git。

1. 由你退出当前微信，正常安装兼容版本并登录。官方免费版支持说明目前到[微信4.1.8.107](https://docs.wxauto.org/docs/install.html)；你已反馈换成4.1.8.107并测试OK，无需再次换版。
2. 已有安装包：`C:/Users/yutha/AppData/Local/Temp/WeChatbot-WX-WXA-02/weixin_4.1.8.107.exe`。233506664字节，SHA-256 `b79aa3fdfd208d64f38fcc354684f9af213c05993c6f603521f2813930362b90`；Tencent签名Valid。安装器文件/产品元数据为4.1.8.1000/4.1.8.0，安装后看客户端版本和实际API表现，这个差异不作为永久阻断。agent未运行安装包；用户已自行完成换版。新安装时保留原数据；若旧版登录或安装遇到限制，记录具体提示，不自动绕过。
3. 编辑[本机绑定](secrets/wxauto4-chat.local.json)，填chat_name，必要时填blacklist；不需要发送者白名单，群内全部成员均可触发。account_alias和conversation_key是自定的本地持久别名，保持不变才能继续同一份记忆；不是微信服务端身份。昵称仅用于当前发送者标记，不要求逐人绑定。
4. 手动打开这个群，保持消息区域在最新位置。先运行只读检查，再显式启动live：

```powershell
cd E:\CodexWS\WeChatbot
.\Start-WeChatbot.ps1
.\Start-WeChatbot.ps1 -Live
```

默认命令仅inspect：0微信构造、0模型生成、0发送。-Live是本次会话的显式启动授权，无需再改旧mock总开关。看见baseline_ready后，让群内任意成员发新文字，如 `bot 你好`。启动可见文字不回放。前缀只是文本规则，不是真实@；可在绑定文件显式选all_allowed_text，适用于本群所有非黑名单成员；默认仍需要bot前缀，不自动回复每条闲聊。

同名昵称无法区分真实个人，记忆中的发送者标记也不是稳定微信身份。运行中不切群、滚到旧历史或改绑定；切群/窗口变化会暂停，返回目标群后在本机输入resume重建基线。绑定文件变更需停止后重启。

## 本机控制与实测

在启动脚本的本机控制台输入以下命令，群文字和模型输出均不能执行它们。

| 命令 | 行为 |
| --- | --- |
| status | 状态、队列、未决ID；0生成 |
| pause / resume | 暂停 / 复核目标并重建基线；旧生成结果失效 |
| reset | 清RAM和队列，长期记忆保留；不回放旧文字 |
| memory-status | 条数、字符、容量和最近保存结果，不显示正文 |
| stop | 停本项目及其创建的模型任务，不退出/注销微信 |
| confirm-sent [ID] / mark-not-sent [ID] | 你核实unknown后仅标记该记录；省略ID取首条，不补发，然后resume |

明确框架成功只记local_reported并继续，不逐条要人工ACK，不称服务端确认。发送异常/超时/不明返回记unknown，暂停该会话；记录保留，不重试、不清账。

按自己的节奏试普通文字和第二轮承接，再试pause/resume/reset、“记住一个自造称呼→reset→再问称呼”和一个联网问题/公开URL。实际原子写结果生成保存回执；已保存后发送失败不撤销记忆。正常就接受，不增加媒体或长稳验收轮次。

## 配置和隔离

唯一运行配置入口为config/local五份YAML，[字段说明](config/README.md)。微信自己的[persona.md](config/persona.md)保留，可直接编辑；不再有独立8000字符角色门槛，按最终输入预算校验，不擅自删人设。

默认CLI deepseek-v4.1-flash、effort=low、子进程alwaysThinkingEnabled=false；524288可见UTF-8字节政策，overhead/output各2048，context_window_tokens=null。它不是原生token窗口或免费额度保证。只裁完整旧历史，不截当前请求/全文记忆；最终wire/插件继续校验实际预算。

后端由操作者选择，本次保留实际后端/模型与账号。若选择家庭Ollama，沿原连接文件使用，不自动切CLI；原生工具仅CLI可用。inspect/健康检查0生成，每条文字一个模型任务，不自动修复/重试、切后端/账号或加付费API。

web准备true，最多3工具调用/4步骤/90秒，单结果8000/合计12000字节；仅WebSearch/WebFetch，MCP空，其余工具关闭。只附最多两个当次成功证明的公开URL，失败如实说明；工具材料不学进记忆。

memory/learning准备true，每会话50000 Unicode字符、单文件1048576/总8388608字节，均可配置扩大。使用源MemoryStore schema2全文与同次增改删，不用旧关键词/小候选方案。密钥只在微信secrets，库只在微信state/group-memory，按账号别名＋会话别名隔离。坏库/容量/保存失败保留原件，关闭该会话增强并提示一次，基本文字继续。日志/发送记录只有封闭元数据；原始聊天仅用于本轮模型/RAM，不写聊天日志。

## 新检出准备与必要检查

```powershell
uv sync --locked --extra wxauto4 --python <Python3.12路径>
New-Item -ItemType Directory -Force config/local, secrets
Copy-Item config/examples/*.yaml config/local/
Copy-Item config/examples/wxauto4-chat.example.json secrets/wxauto4-chat.local.json
.venv\Scripts\python.exe scripts/prepare_cli.py --node <匹配node.exe> --entry <匹配CLI包内bin/codebuddy>
.venv\Scripts\python.exe scripts/check_snapshot.py
.venv\Scripts\python.exe -m unittest tests.test_chat_migration tests.test_native_guard -q
```

复制模板仅用于新检出；已有local不用模板覆盖。prepare_cli仅复制并核对Node、entry、bundle、types，不执行CLI，不复制账号/凭据。[manifest](vendor/qq-core-manifest.json)为诚实混合快照：所需文件固定42911af，未用旧文件保留原提交；微信路径/spawn差异逐项登记。无源目录运行依赖，不启动QQ服务，不改第三方核心。

旧严格核心 `python -m wechatbot inspect/probe`、[wxauto4挑战工具](docs/WX-WXA-01-REPORT.md)和各自台账保留，不因新入口升级为真实微信能力。历史见[WX-01](docs/WX-01-OFFLINE-REPORT.md)、[WX-02](docs/WX-02-CAPABILITY-REPORT.md)。Git只用本项目main和origin，不借QQ远端。

## 启动错误诊断

若-Live失败，控制台输出startup_error JSON，并把相同封闭元数据写入忽略的state/startup-last-error.json：包含stage、error_type、代码文件/函数/行号及可用的数值错误码；不包含原始异常消息、群名、消息正文或局部变量。wxauto免费版广告本身不是报错。将这段JSON发回即可定位，不需要提供本机secrets。
