# WX-AKASHA-ALL 实施交接

返回[PROGRESS](../../../PROGRESS.md) / [TASKS](../../../TASKS.md)，继承根AGENTS。总报告见[实施报告](../../../docs/WX-AKASHA-ALL-REPORT.md)，使用见[README](../../../README.md)。对应[QQ交接](E:/CodexWS/QQbot_Snowluma/tracks/laptop-workbuddy/tasks/WX-AKASHA-ALL/HANDOFF.md)。

状态：active，等待本次操作者账号向导/真实映射，完成后同任务继续；不是另一轮规划或已完成微信验收。负责人本会话Codex，session WX-AKASHA-ALL-20261031，开始2026-10-31T10:25:51+08:00。只领取WX-AKASHA-ALL，未派代理。

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

QQ实现从codex/wx-akasha-all普通快进main，当前已push并核远端42a145fc9b3420ce67008dba0a3ecdf864ba2862；QQ工作区干净。精确配置/插件备份、保护摘要、技术配对与加载回执在QQ忽略的state/akasha-deployment。微信实施及已知规划正在main审阅提交；不发布本机数据。

WeFlow setup(18108)和本机panel(18766)已按创建身份运行；桌面API/bridge尚未启动，未读库/收发。用户问“哪有向导，是URL吗”，已回复http://127.0.0.1:18766点击“打开带本机授权的WeFlow向导”，/setup会302到18108并自动携带本机令牌，不输出token。实际检查页面/配置路由200，跳转302。尚未检测到WeFlow保存的config.json。

## 剩余同任务动作

1. 等用户在现成WeFlow向导选择机器人账号/目录并取钥保存，必要退出/登录/系统授权由其操作；只问具体错误，不重问读库意愿。不要打印config/key/token或原始亲友消息。
2. 同home切到5031桌面API，通过公开会话元数据定位原已授权群；用户在本机选一次实际QQ会话配对及scope/actor_links，不凭同名合并，实际ID只存忽略配置。未配对也可独立聊天。
3. 配置保存后以Start加载当前配置摘要；脚本会复用或受管重启当前AstrBot，不另开第二份。核对WeFlow连库/SSE/11229 WS/受管UIA状态、真实加载的profile与0生成元数据；只交用户自然群测，不造真实生成/发送样本。
4. 更新报告/PROGRESS/TASKS与两根Git/部署回执。真实连接可交用户实测；正常反馈就接受，有具体故障继续本任务修。

当前全部归属：原九份规划文档＋本交接/报告，Start-Akasha.ps1、adapters/akasha/{source.json,project_bridge.py,project_entry.py}、scripts/akasha.py、config/examples/akasha.json、tests/test_akasha_all.py；QQ实际文件见对应交接/提交。所有后续修改保留用户差异，不恢复空库或退出微信。
