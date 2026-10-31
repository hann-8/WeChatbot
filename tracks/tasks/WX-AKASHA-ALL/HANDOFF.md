# WX-AKASHA-ALL 实施交接

返回[PROGRESS](../../../PROGRESS.md) / [TASKS](../../../TASKS.md)，继承根AGENTS。总报告见[实施报告](../../../docs/WX-AKASHA-ALL-REPORT.md)，使用见[README](../../../README.md)。对应[QQ交接](E:/CodexWS/QQbot_Snowluma/tracks/laptop-workbuddy/tasks/WX-AKASHA-ALL/HANDOFF.md)。

状态：ready_for_user_test，实施/必要检查/受管部署完成，实际SSE/WS连接正常，交用户在已选群自然实测；具体故障继续本任务。不是质量已验收。负责人本会话Codex，session WX-AKASHA-ALL-20261031，开始2026-10-31T10:25:51+08:00。只领取WX-AKASHA-ALL，未派代理。

## 已完成与证据

- 起点微信main=938187c；保留已知九份规划差异与全部旧wxauto代码/本机配置。QQ开工main=42911af且干净，旧NapCat根未操作。
- 固定上游9dbe933的6个关键源码与公开固定提交规范化换行后相同，原始副本保留。运行副本只应用adapters/akasha overlay与初始health地址薄补丁，UIA/解密/登录/AstrBot核心不改。
- 微信稳定ID/完整源ID、前置范围过滤、batch成员来源、精确当前图、发送后按bool回结果、partial/unknown暂停且重启保留；无额外caption模型；只回源，不QQ↔微信原文转发。
- 现有AstrBot自有业务方法/provider/队列/Attention/ReplyPlan/MemoryStore已接线，显式facts_only/shared_context/actor_links，未配对独立；全文schema2与真实回执、原生两工具、受控表情/free/adaptive、成员、可信owner/本机控制、私聊默认关闭及不支持媒体的准确关闭均已实现。
- Start-Akasha.ps1及scripts/akasha.py提供prepare/inspect/setup/api/start/status/pause/resume/reset/memory-status/resolve-unknown/stop；单一本机config/local/akasha.json；18766面板可配置/控制/记忆管理。WeFlow home/密钥/token/附件/日志/状态仅忽略目录。现有旧绑定有指定群，blacklist为0项，未扩大范围。
- 当前34项native/QQ/schema2套件、3项实际AstrBot/provider＋替身链路、3项当前图/共享上下文组合均通过。额外旧transport_router 17项为10失败/2错误，原42911af隔离副本完全复现；已保存本机日志，临时baseline worktree已正常移除，未改旧合同迎合。
- 当前绑定1c8d1f3724243023ef4f3ba11e39861c4f19df8061308480f9dfe45aef94a8cc沿原check/probe/activate完成，CLI真实零生成握手passed、real_generations=0、positive_next_calls=0、negative_users=[0,0]；authorize-operator-trial配对，质量待用户实测。未主动真实模型生成/工具服务/群发样本。
- QQ侧已增量部署，6199与11229监听，QQ connected/online/channel_ready及router_ready=true，current_error=null；原QQ平台/provider/preferences与config/local/persona保护不变，memory/vision保留。日常实际启动路径已保留新增平台，并避免重跑旧全量AstrBot配置生成器。

## 当前运行/Git

QQ实现从codex/wx-akasha-all普通快进main，实施及当轮配对已交付，最终文档回执另行提交并核远端；QQ原平台/provider/preferences、config/local/persona保护检查通过，connected/online/channel_ready、router_ready=true，current_error=null。当前配置实际free/adaptive/vision/memes/memory均启用。精确备份和加载回执在QQ忽略的state/akasha-deployment。

用户通过18108向导保存所选机器人账号/数据库与图片密钥，已通过公开API唯一匹配原授权群（1个），保持私聊关闭；随后用户在18766明确保存facts_only及1条actor_link并回复“配对已保存”。实际ID/密钥只留忽略配置。5031连库/API及SSE端点200；Start已加载当前配置摘要并受管部署WeFlow与bridge，实际SSE=true、AstrBot WS=true、UIA初始化true、模型元数据零生成证明有效、gateway_ready=true；共享MemoryStore检查200，当前0条，未填造事实。启动检查时local_reported=0、unknown为空。

微信main已提交首个实现2422174，最终管理/选择与运行报告改动同轮审阅提交推送；两处最终SHA以会话回执为准，不在文档自引用。11份Markdown/104个本地链接、相关compile、依赖pip check、diff检查通过；真实适配类替身套件最终再次3通过。

## 用户实测与接续

直接在原选定群自然聊、问需要联网的问题、发当前图片、按需要要表情、记住自造称呼后reset再问；跨平台记忆按已选事实scope在另一端问。正常反馈就接受，具体故障在WX-AKASHA-ALL续修，不再规划/索部署授权。未主动执行真实模型生成/工具服务/发送样本；连接与零生成证明不代表模型已实际回答或用户已看见。

入口：Start-Akasha.ps1 start / stop / status，管理http://127.0.0.1:18766，单配置config/local/akasha.json。prepare/inspect/setup/api/pause/resume/reset/memory-status/resolve-unknown仍可用；Stop不退出微信或QQ，只管理有创建身份的微信项目进程。原生@关闭、GIF首帧、不支持媒体准确提示。不要自动重发unknown、复制库/key、清QQ记忆或回滚其他用户差异。

当前全部归属：原九份规划文档＋本交接/报告，Start-Akasha.ps1、adapters/akasha/{source.json,project_bridge.py,project_entry.py}、scripts/akasha.py、config/examples/akasha.json、tests/test_akasha_all.py；QQ实际文件见对应交接/提交。

2026-10-31T11:16:39.271914+08:00 WX-AKASHA-ALL具体故障续修，负责人本会话Codex：用户实报Start-Akasha.ps1 status向Python传空--session导致argparse失败。起点main=0cec96d，工作区干净。精确归属仅Start-Akasha.ps1、TASKS.md、本任务HANDOFF；改为仅非空Session才传该可选参数，验证真实status命令。无需重启服务、修改QQ/配置、模型生成或发送；沿原授权审阅提交并普通push。

续修结果：Start-Akasha.ps1仅在Session非空时追加--session和值；当前PowerShell直接运行.\Start-Akasha.ps1 status及Windows PowerShell5.1 -File调用均exit=0、返回状态JSON，SSE/WS仍true。未重启/生成/发送。验证同时看到当前会话有1项unknown且已暂停，保持原记录，不重发、不清账；这与本次参数错误分开。
