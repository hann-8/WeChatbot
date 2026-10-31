# WX-AKASHA-ALL 实施与部署报告

2026-10-31，负责人本会话 Codex。返回 [PROGRESS](../PROGRESS.md) / [实施交接](../tracks/tasks/WX-AKASHA-ALL/HANDOFF.md)。状态 ready_for_user_test：全部接线/必要检查/受管部署完成，实际SSE/WS正常，交用户自然实测；尚未把连接正常当真实聊天验收。

## 实现

- 固定 Akasha 9dbe933 原始副本保留。6个关键源码文件与固定提交公开内容一致（规范化 CRLF/LF 后比较）；运行副本只加载项目 overlay 及 main.py 初始 health 地址小补丁，UIA/WeFlow/AstrBot 核心不改。
- WeFlow 维护分支 334456777/WeFlow v5.0.1，原发布包摘要保持；专属 home、18108 向导与5031桌面 SSE/API。账号/密钥由现成向导保存，不在日志/报告输出。
- 确定性 namespace ID、完整原消息/成员/媒体关联、指定会话/私聊/黑名单前置过滤、batch来源保留、起始基线/去重；文本@明确 text-derived，无伪造原生 At。
- 实际 UIA bool/异常之后回 OneBot 结果，成功只记 local_reported；失败/部分/结果连接丢失留 unknown 并暂停对应会话，重启保留，不重试。
- 独立 akasha-wechat/11229；QQRouter 各钩子按注册平台和实际来源分派，复用同一业务方法/provider/模型队列/Attention/ReplyPlan/MemoryStore，不复制QQ凭据或伪造QQ票据，不跨平台转发原文。
- schema2 全文/模型同次增改删/原子写与真实回执沿用现有服务。配对仅本机显式 qq_session/actor_links；facts_only、shared_context 同批实现，未配对独立。
- 当前消息图片按完整 serverId 精确读取，一次性本机 cap，现有归一化/原生同轮识图；失败不读旧图，不启动 llava/caption。
- 表情仅现有登记目录；adaptive、free/叫名/续聊、成员公开资料、可信wxid owner与本机控制已接线。原生@关闭，GIF仅首帧；语音/视频/任意文件/B站退役分支准确关闭/提示。
- 524288可见UTF-8政策及现有模型/low、thinking=false、reserves/历史、两工具3调用/4步骤/90秒/单8000总12000字节保持。新增微信来源私密ID按任务传入现有工具策略，其他工具/MCP关闭，无额外模型/重试/自动切后端。
- 单配置 config/local/akasha.json 和 Start-Akasha.ps1 的 prepare/setup/api/start/status/pause/resume/reset/memory-status/resolve-unknown/stop；18766 本机面板。账号配置/桥接/WeFlow日志、附件、密钥、配对与运行状态均忽略。

## 检查证据

| 检查 | 结果 | 边界 |
| --- | --- | --- |
| 当前 native/QQ/schema2 定向套件 | 34通过 | 旧QQ文字/free/owner/表情/记忆与CLI工具协议等组合；无真实生成/群发 |
| 微信实际 AstrBot 类/桥接组合 | 3通过 | 当前bridge→实际适配类/路由/provider元数据→替身模型→UIA替身，两轮连续、实际记忆回执、短期reset、来源/失败/unknown/batch |
| 微信当前图/共享上下文 | 3通过 | 现有normalizer、gateway实际NativeImage同轮，一次cap失败零模型；显式共享/未配对隔离 |
| 额外旧 test_transport_router | 17运行，10失败/2错误 | 在未改的42911af隔离副本完全复现；旧私有health合同与现行官方Snow主线不一致，不冒充通过，不改旧内核来迎合 |
| 依赖/语法 | pip check及相关compile通过 | 不代表账号/微信或模型已回复 |
| 锁定CLI真实零生成握手 | passed；real_generations=0，positive_next_calls=0，negative_users=[0,0] | 现有check/probe/activate，当轮实际binding与active配对，operator_trial，质量待用户实测 |

本轮 agent 未主动调用真实模型生成/WebSearch/WebFetch或微信/QQ群样本发送。替身或元数据检查不证明用户已见消息。

## 部署与保护

QQ开工本地/实时远端main=42911af；微信=938187c。QQ隔离 codex/wx-akasha-all 实现后普通快进 main；已知微信九份规划差异保留。两根 Git 与运行回执在交接继续更新。

受管停止/当前配对后增量注册微信平台，保留QQ6199/provider/账号/权限。Akasha存在时停止重跑旧AstrBot全量配置生成器，仅同步自有插件和新增平台。精确配置/插件备份和保护摘要在QQ忽略的 state/akasha-deployment；微信身份记录在 state/akasha-wechat。普通 Start 必要时调用既有受管QQ启动入口，不按进程名结束服务；Stop不退出微信，不结束外部手动进程。

用户已完成所选机器人账号/数据库与图片密钥保存；公开API唯一定位原指定群，未扩大范围，私聊保持关闭。用户明确保存 facts_only 配对及1条actor_link，并回复“配对已保存”。同一home切换5031，实际连库/SSE、Akasha→AstrBot11229 WS、UIA初始化和gateway_ready均正常；当前配置摘要已实际加载，共享MemoryStore检查200、0条。原QQ connected/online/ready，全部保护检查通过，free/adaptive/vision/memes/memory均保留。启动核对时local_reported=0、unknown为空；未主动生成/发样本，具体效果由用户自然群测。

## 回滚

运行 Start-Akasha.ps1 stop，仅停止身份匹配的微信项目进程。需要撤销AstrBot接入时，在其受管停止后恢复 state/akasha-deployment 中精确平台/自有插件备份，再正常启动；不要恢复整份旧QQ运行数据。保留WeFlow home/密钥、配对、新增记忆、unknown和其他用户修改，不退出/注销微信，不删除聊天数据或用空库覆盖记忆。

最终运行核对时间：2026-10-31T11:05:04.308079+08:00。源QQ当前绑定1c8d1f3724243023ef4f3ba11e39861c4f19df8061308480f9dfe45aef94a8cc有效；管理/配对页面和启动名称匹配检查已部署。两处main普通push后核对SHA，最终SHA见会话回执。
