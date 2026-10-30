# 配置索引

返回[README](../README.md)。运行读取config/local五份完整YAML，绑定只放忽略的secrets/wxauto4-chat.local.json；[模板](examples/wxauto4-chat.example.json)。本机已建空模板，不含真实群名/昵称。

| 文件 | 作用 |
| --- | --- |
| [bot.yaml](examples/bot.yaml) | 旧严格mock平台/开关，默认关闭 |
| [chat.yaml](examples/chat.yaml) | 8轮历史，single；旧严格私聊/mentions保留，不给新入口伪造真实@ |
| [models.yaml](examples/models.yaml) | CLI/Ollama显式选择，单并发队列5；CLI 524288字节、low、overhead/output各2048、原生窗口null |
| [features.yaml](examples/features.yaml) | web/schema2全文记忆准备true，媒体/成员关闭 |
| [runtime.yaml](examples/runtime.yaml) | 旧发送/自启默认false，不记录正文；新入口仅显式-Live启动 |

web engine固定codebuddy_cli，最多3工具/4步骤、单结果8000/总12000字节，90秒由原任务/插件限制；仅WebSearch/WebFetch，MCP空。关闭web不关闭文字；选Ollama不自动切CLI。

memory enabled/learning_enabled为true，max_chars_per_group=50000、max_group_file_bytes=1048576、max_total_bytes=8388608、max_groups=16，可扩大。无关键词候选条数/240字节政策。reset不清长期记忆；库/密钥独立在微信state/secrets。

[persona.md](persona.md)本次保留。最终预算包含角色、当前请求和全文记忆；只裁完整旧历史，仍超限就本地失败，不删除角色、不截当前请求/记忆、不重试模型。

[versions.lock.json](versions.lock.json)锁相对Node/CLI路径、bundle/types摘要；[cli-capabilities.json](cli-capabilities.json)为公开静态模型资料，不代表真实验收。工件准备见根README。config/local、secrets、state、runtime、logs、cache均忽略，不复制QQ私密配置或家庭资料。
