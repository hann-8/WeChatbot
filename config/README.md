# 配置索引

返回[README](../README.md)。公开默认值逐参数中文说明位于：

| 模板 | 作用 |
| --- | --- |
| [bot.yaml](examples/bot.yaml) | 平台、真实通道总开关、候选 transport、未来账号绑定、授权群和黑名单 |
| [chat.yaml](examples/chat.yaml) | 微信独立私聊双名单、mentions、停言、有限历史、single |
| [models.yaml](examples/models.yaml) | 显式选定 CLI/Ollama、单并发队列、预算/超时/原生参数 |
| [features.yaml](examples/features.yaml) | 首期全部关闭的媒体/联网/记忆/成员功能 |
| [runtime.yaml](examples/runtime.yaml) | 独立回环健康端口、UI/发送/日志/自启边界 |

[persona.md](persona.md) 是独立中性正文，不复制 QQ 人设，不授予工具和真实收发能力。

`config/local/`、`secrets/`、`state/`、`runtime/`、`logs/`、`cache/` 全部忽略。本机配置若需要，操作者自行建立五份完整文件；WX-01 没有生成真实账号/群/家庭连接资料。`allowed_users` 和 `allowed_conversations` 分别绑定可信发送者与会话；这项补充名单是严格私聊绑定所需，不用显示名填充。

`versions.lock.json` 只保留固定 CLI 文本路线的公开版本与 hash；Node/入口/bundle 路径均是本项目 `runtime/cli` 相对路径。`cli-capabilities.json` 是来源快照，native_window_effective_verified=false，不能当微信或本次模型真实验收；`cli-tools-denied.json` 与 `mcp-empty.json` 是隔离策略。逐文件来源和两项本地差异见 [manifest](../vendor/qq-core-manifest.json)。Python 依赖另锁于 [uv.lock](../uv.lock)。
