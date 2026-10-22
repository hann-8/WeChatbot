# WeChatbot 离线核心

独立 Python 3.12 项目，当前仅完成 **WX-01 实现及离线验证**。入口见 [PROGRESS](PROGRESS.md)、[任务交接](tracks/tasks/WX-01/HANDOFF.md)、[离线报告](docs/WX-01-OFFLINE-REPORT.md)。微信身份、真实 @、发送确认、图片、登录及长期运行全部未验。

默认 `transport=mock`、`enabled=false`、`sends_enabled=false`、授权群空、私聊关闭、`mentions`、`single`，媒体/联网/长期记忆等均关闭。当前没有真实传输实现；修改开关不能产生生产资格。命令行只提供只读 `inspect`，没有启动真实通道、登录、发消息或真实生成命令。不自动进入 WX-02。

## 本地准备与检查

在本项目目录用已有 Python 3.12 和 uv 创建独立环境：

```powershell
uv sync --locked --python <本机Python3.12路径>
.venv\Scripts\python.exe -m wechatbot inspect
```

`uv.lock` 仅锁本项目依赖，editable 的 `.` 是本项目自身；没有 QQ editable、软链或 QQ 服务端口依赖。没有安装 pyweixin/pywechat、OpenClaw 或 AstrBot。aiohttp/Pillow 是固定 runner 的模块导入依赖，当前图片/联网路径均关闭。

原 CLI 构造器先核验工件，离线测试也保留这项检查。本机已将 SHA-256 匹配的 Node、CLI 入口和 headless bundle 独立复制到被忽略的 `runtime/cli`，没有执行这些工件，也没有全局重装。新检出需从操作者已有、与锁匹配的本机安装显式准备：

```powershell
.venv\Scripts\python.exe scripts/prepare_cli.py --node <node.exe路径> --entry <CodeBuddy包内bin/codebuddy路径>
.venv\Scripts\python.exe scripts/check_snapshot.py
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

版本/hash 不匹配会拒绝，不能用改 hash 或自动下载其他版本绕过。准备脚本只读显式输入工件并复制到新 root，不读 CLI 账号/设置/凭据，不运行 Node/CLI。这仅证明离线工件可加载，不证明复制出的 CLI 能真实生成；真实执行及其运行依赖仍须后续明确授权。

## 配置与接口

五份中文逐参数模板见 [config/README](config/README.md)。loader 按代码拥有的封闭 schema 验证，拒绝未知/重复字段、YAML alias、错误类型和值、越界路径。一次加载产生固定快照和摘要，保存后下次手动构造实例生效；不热更、不读 QQ 配置。`inspect --config-dir config/local` 要求五份完整本地文件，不做隐式混合回退。状态输出只有封闭元数据，不显示私密身份/正文/路径。

核心顺序为 `NormalizedEvent → Gate → 有界队列/当前目标复核 → InputBudget → 固定 runner 一次调用 → 投递状态机 → mock ACK → 有限历史`。传输/可信身份、黑名单、授权会话检查均在窗口/模型/材料/历史之前。正文 @ 和显示名不提供可信 @ 或身份。私聊需独立开关且发送者、会话两个名单都满足；历史按账号/类型/会话/发送者隔离。

`ModelFacade` 在本阶段强制要求显式离线进程/传输替身；不会默认调用真实模型。CodeBuddy 复用原 runner 的 tools 空、空 MCP、工具拒绝、无 session persistence、一次尝试和 `CleanupOwner`。Ollama 复用原生 payload/单次调用/unknown marker，但只测试了假传输；没有家庭连接文件，也没有 SSH。

`reasoning_effort=auto` 不传 effort；显式 effort 仍由原 runner 在唯一用户输入前检查当前控制握手，不凭旧快照宣称实际生效。CLI 原生窗口必须 null；输入预算是保守 UTF-8 wire 计量，不是实测 tokenizer 或免费额度保证。Ollama 的 `num_ctx/think/num_predict` 是原生请求字段；没有真实效果证据。

## 台账、恢复与限制

项目独占 `state/core-owner.lock`，第二 owner 拒绝。SQLite 在模型前持久化 prepared，在发送前持久化 submitted；接受结果和 assistant 历史在同一事务提交。启动时 prepared/submitted 转 unknown，只恢复状态，不重放事件/请求。unknown 阻断对应目标；模型清理 unknown 阻断后续模型。不提供自动清账/补发。默认单气泡、最多 8000 字符、一次提交，不拆分、不自动 @ 或引用。

`api_accepted`、`ui_observed`、`none` 分开记录；当前测试中的 api_accepted 只是 mock 的合成关联确认。真实 UI 按键返回不会被此实现证明为 accepted。目标/账号/代际或停言栅栏变化会作废输出；提交后无法确认则 unknown、不入 assistant 历史。群明确停言无确认回复；同条停言优先，后续可信新 @ 恢复，重连保留停言、owner 重启复位。

每发送者历史默认 8 个完整轮次；每 RAM 窗口最多 32 条、最多 256 个 scope。持久 seen 上限 100000、attempts 上限 10000，历史 scope 上限 256；容量满拒绝继续，不挤掉 unknown 或靠清账恢复。历史/台账是必要本机状态，全部 Git 忽略；当前没有自动保留期清理。

健康服务只有显式构造的 `make_health_server` 操作骨架，固定 `127.0.0.1:8875`，`GET /health` 返回只读元数据。无开机自启或默认监听；端口冲突拒启，不自动改端口。测试只做本机临时端口冲突，不访问微信或 QQ。

回滚保持真实通道关闭，退出本项目 owner 即可；保留 pending/unknown 状态，恢复旧代码必须配对配置和 manifest。不退出/注销/结束日常微信，不按进程名清理，不操作 QQ。源码快照中未接入的 QQ 入口和功能只供溯源，禁止作为本项目启动入口。

Git 当前仅本地 `codex/bootstrap` 检查点，没有 remote。后续需用户提供新项目远端和发布授权。
