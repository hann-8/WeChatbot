# WX-01 独立离线核心报告

返回[PROGRESS](../PROGRESS.md) / [TASKS](../TASKS.md) / [交接](../tracks/tasks/WX-01/HANDOFF.md)。2026-10-23，Asia/Shanghai；session `WX-01-offline-core-20261023`。

## 结论与证据等级

WX-01 **已实现、离线通过**。41 项本项目业务测试全部通过，包含真实固定 runner 的底层替身闭环；不借用 QQ 测试数量。真实微信、UI、账号身份、真实 @、跨重启站点消息 ID、图片像素、发送接受结果、真实模型效果及长期运行均 **unverified**；没有完整真实验收或部署。

本轮真实微信/UI/登录/数据库/剪贴板/键鼠/防睡眠操作 0；真实模型生成 0、SSH 0、对外聊天发送 0。CodeBuddy 原可执行工件仅复制/hash 核验，未执行。未安装或导入 pyweixin/pywechat/OpenClaw；未启动健康监听或服务。测试只绑定本机临时 socket 验证端口冲突。

## 实现范围

独立 Python 3.12.14 环境和 uv.lock（23 个解析包，含项目自身）；本项目没有 QQ editable/软链、AstrBot/QQ 运行实例或端口连接。五份中文逐参数模板、独立中性人设、代码拥有的严格 schema 和只读 inspect；默认群名单空、私聊关闭、mock、enabled/sends=false、mentions/single，其他功能关闭。只保留必要文本 runner 运行依赖，没有接入媒体/联网工具。

NormalizedEvent v1 拒绝未知/重复字段、超限、非法 ID/控制字符/非有限数值；每批最多 32 条/64KiB。传输/绑定能力摘要和账号→可信身份→黑名单→会话授权→自身回环/序列/代际/去重→触发→窗口/模型/历史。可信身份和能力来自绑定 mock adapter，不接受入站 caller 写 passed；生产资格恒 false。真实 @ 未知/正文 @ 均不触发，图片句柄不兑换。新增 `direct.allowed_conversations` 与计划的 sender 白名单配合，确保私聊双方绑定均受限。

独立 Store 单 owner 锁、SQLite FULL 同步/事务，去重/投递/有限历史全部只在项目 state；历史按账号/类型/会话/发送者隔离。一个全局生成槽、最多 5 个排队任务；冻结目标/账号/能力摘要/代际和停言 generation，出站前再次复核。群停言同条优先/无确认，后续可信新 @ 恢复；重连保留、owner 重启复位。free/adaptive 未实现且拒绝启用。

投递 prepared→submitted→accepted/failed/unknown；模型前写 prepared，提交前写 submitted。确定 ACK 与历史同一事务；无关联 trace、none ACK、提交后目标变化/取消/异常均 unknown，不新增 assistant 历史、不重试。重启 prepared/submitted→unknown，只恢复状态。unknown 阻断对应目标，清理 unknown 阻断全局模型；没有清账命令。单气泡纯文本最多 8000 字符，原 runner/过滤器拒绝工具内容。

## 固定源码复用和新 root

源 commit `dd9373029412137023124751d75883824122c784`，通过 `git ls-tree/git show` 导出已跟踪 `src/qqbot_gateway/` 和四份必要公开配置，不读取 QQ 工作区活动配置/秘密/历史/图库，不修改 QQ 仓库。63 个文件逐一记录源 SHA-256、本地 SHA-256 和变更原因于 [manifest](../vendor/qq-core-manifest.json)；61 个与源字节相同，两项本地差异：

1. `workbuddy_cli_runner.py`：CLI 锁相对路径以传入新 root 解析；加入 subprocess spawn 注入接缝，原默认语义保留，微信 facade 强制离线替身。
2. `versions.lock.json`：裁去 QQ/AstrBot/NapCat 部署项及全局绝对路径，只保留公开 CLI 文本版本和本项目相对工件路径；Node/入口/bundle 均记录 hash。

模型 facade 只调用 create_runner/InputBudget、文本过滤与清理，不运行旧 QQ config loader/gate/main。CleanupOwner 借用的 configuration_lock 是新 root 的本地文件锁，不加载 QQ 数字身份配置。所有历史/请求临时目录/清理台账在独立 root。清除每次 runner 调用的图片 ContextVar，避免同进程遗留媒体污染文本请求。

CLI：一次 synthetic spawn/一次用户输入；实际原 runner 构造 tools 空、strict 空 MCP、工具拒绝、无 session persistence、setting-sources none、进程局部记忆禁用参数，解析 init/result 并完成原 CleanupOwner。测试没有创建 OS 子进程，synthetic pid 不存在，无进程被终止。Ollama：原 runner 经显式假 transport 走 tags/chat/native payload 和 unknown marker，0 SSH，连接配置未读。模板 digest 为空仅用于离线工件；不是家庭模型可用性证明。

CLI `auto` 不传 effort；显式档位的当前控制握手沿用源语义，本轮未验真实档位效果。原生窗口必须 null；输入预算是保守 wire 字节计量，不等于原生 tokenizer 或额度保证。未声称复制出的 CLI 真实运行依赖完整。

## 验证命令与结果

在项目根使用独立 `.venv`：

| 命令 | 结果 |
| --- | --- |
| `python -m unittest discover -s tests -v` | 41 项通过，最终运行 4.374s |
| `python scripts/check_snapshot.py` | 63 文件 hash 通过、仅 2 本地差异，3 工件 hash 通过，executed=false |
| `python -m wechatbot inspect` | valid；mock；enabled=false；sends=false；production=false；真实身份/@/投递未验 |
| `uv lock --check` | 23 包锁一致 |

测试覆盖：未授权/黑名单/私聊关闭先于窗口/生成/历史，图片不兑换；同名/改名、可信 @ 与正文 @、错账号/旧代际/序列、自发回环、稳定去重/同文不同 ID/重启去重；群私聊与成员历史隔离、有限历史、实际预算前置；排队串行/队列满/排队取消、模型 pending 取消、停言与目标/账号变化作废；投递取消/none ACK/错 trace/unknown、pending 跨重启无重放、部分模型输出/工具拒绝/清理 unknown；严格配置/路径/本机端口冲突/零副作用只读状态。

开发中修复的决定性问题：将活动 prepared 与未知 unknown 一并在 gate 阻断，导致同目标排队失效；现 gate 只提前阻断 unknown，串行获得锁后再次复核所有未决状态，prepare 仍拒绝并发 side effect。最终串行历史测试证明三个任务按 1/3/5 条消息输入依次执行。

## 边界、Git 和后续

`state/runtime/.venv` 等全忽略，无新 secrets/local 配置。容量上限和回滚见 [README](../README.md)；不自动裁掉 unknown，不自动保留期清理。真实传输未实现；代码中的 `pyweixin` 只是候选枚举，不能启用生产。没有把源码支持/mock ACK 写成微信能力已通过。

本项目本地初始化分支 `codex/bootstrap`，只纳入审阅过的 WX-01 文件及原七份引导文档。没有 remote，未创建或推断远端，未推送。当前提交号以 `git log -1` 和本次交付消息为准；被忽略的本机工件/合成清理状态保留。

WX-02 未领取。下一步只能等待用户另行指令；如领取仍先 mock/inspect，真实观察、登录、模型、发送分别受后续明确授权约束。
