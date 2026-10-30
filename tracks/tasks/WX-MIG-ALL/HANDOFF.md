# WX-MIG-ALL 批量文字版迁移交接

返回[PROGRESS](../../../PROGRESS.md) / [TASKS](../../../TASKS.md) / [统一计划](../../../docs/QQ-TO-WECHAT-MIGRATION-PLAN.md) / [报告](../../../docs/WX-MIG-ALL-REPORT.md) / [使用说明](../../../README.md)。继承根AGENTS。

## 当前状态

2026-10-31收尾completed，负责人本会话Codex，沿用WX-MIG-ALL-20261030。2026-10-31（Asia/Shanghai），用户先反馈“现在可以了”，随后反馈“测试ok，继续”。据此记录指定单群文字版启动恢复、整体试用OK并由用户接受；用户未逐项列出记忆/联网/本机控制结果，不扩写为这些专项全部实测通过，不称服务端ACK或长期稳定性证明。 实现起点main33c18f0，最新代码/诊断提交3277e37；本轮仅文档/忽略规则收尾。agent未运行真实微信/模型或发送，用户反馈与离线证据分别记录。

唯一任务WX-MIG-ALL，未分领MIG-01/02/03。按授权普通commit/push main，远端SHA在最终答复核对，不建分支/force。源SnowLuma42911af只读无改动。

## 已实现与文件归属

- src/wechatbot/chat_session.py、chat_model.py、chat_policy.py、wxauto4_chat.py：单绑定群连续文字、全体群成员可触发/黑名单、基线去重、单并发队列、本机控制、八轮RAM、真实local_reported/unknown语义、schema2全文记忆及原生联网小包装；仍用原transports/wxauto4_adapter.py三个公开API，不伪造生产事件/QQ身份。
- config/defaults、config/examples、config/README、models policy：524288可见UTF-8字节/low/thinking=false、memory/web准备true，其他能力关闭；本机config/local与secrets空模板忽略。微信persona/后端/模型/账号不替换，家庭连接不复制。
- docs/WX-MIGRATION-SOURCE-MAP.json所列共用模块及三份插件；公开capabilities、framework四字段、types锁定；scripts/check_snapshot.py/prepare_cli.py、versions锁与vendor manifest。74项混合快照，未用旧文件保留旧来源，微信相对Node/entry与spawn替身接点合并。
- Start-WeChatbot.ps1一个入口；README、报告、PROGRESS/TASKS及上轮已知规划文档同步。tests/test_chat_migration.py、test_native_guard.py及固定源合成SDK fixtures；offline_backend和test_core适配low元数据握手。

## 检查和边界

最终60项通过（8迁移组合＋1实际插件合成SDK/9限定变体＋41原严格核心＋10挑战工具）。源码/工件74项摘要与framework_upper=8985、compileall、默认启动inspect与旧trial mock通过。inspect 0微信/0生成/0发送；Node仅运行合成SDK host，不启动CLI或联网服务。初次发现内部JSON被single输出当文字及旧stdin断言不适应low握手，已同轮修正并通过。

保存失败保原件并真实回执、跨会话隔离、reset后新Store全文读回和增改删、当前问题/全文记忆不裁、旧历史整轮裁、两轮单任务单发送、unknown不重试/重启保留、错群/pause旧结果不保存/发送、HTTP(S)/参数封套/工具裁剪与限制均有定向替身证据。没有全库、长稳、媒体或生产矩阵。

## 本机准备与下一步

当前后端codebuddy_cli；Python3.12.14、wxauto4 41.1.7依赖存在，相对CLI Node/entry/bundle/types齐全。config/local五文件和secrets/wxauto4-chat.local.json已准备；真实名字由用户填本机，不入报告/Git。旧挑战未决不清理。

安装器已存在于C:/Users/yutha/AppData/Local/Temp/WeChatbot-WX-WXA-02/weixin_4.1.8.107.exe，233506664字节，SHA256 b79aa3fdfd208d64f38fcc354684f9af213c05993c6f603521f2813930362b90，Tencent签名Valid；未运行。文件/产品元数据差异不永久阻断。用户已自报换到4.1.8.107并反馈测试OK，agent未操作安装或客户端。

下一步：用户正常使用，遇到具体问题就在本任务范围修复，不新增完整验收轮次；媒体/成员/真实@/free仍延期。本轮仅记录接受并收尾，不操作实例/账号/配置/消息。_temp/与wxauto_logs/为新出现的本机工件，保留且补Git忽略，不读取内容、不删除或提交。

## 用户反馈续修：取消发送者白名单

2026-10-30 23:16 Asia/Shanghai，本会话Codex按用户反馈续修WX-MIG-ALL：取消连续聊天的发送者白名单，指定群全部成员可按前缀触发，保留黑名单和本机控制边界。归属src/wechatbot/chat_session.py、chat_model.py、chat_policy.py、wxauto4_chat.py、绑定模板及忽略的本机绑定、tests/test_chat_migration.py、README/AGENTS/计划/报告/PROGRESS/TASKS/当前HANDOFF。无真实通道操作。

续修完成：取消连续入口的发送者白名单，绑定群全部非黑名单成员可按bot前缀触发；旧allowed_senders读取时忽略，模板及本机文件移除。9项迁移定向检查通过，默认inspect仍0真实通道/模型/发送，未运行live。本机绑定格式已验证，用户填写的其他值保留。

## 用户实报启动失败续修

2026-10-30 23:21 Asia/Shanghai，本会话Codex续修WX-MIG-ALL启动故障：用户实报-Live在wxauto初始化附近失败，原入口吞掉异常。范围为启动诊断、必要公开API适配、替身检查及README/报告/当前交接/PROGRESS/TASKS；不自行执行live或操作微信。先补封闭元数据诊断再据具体证据修复，不把广告输出当兼容结论。

启动续修检查点：用户自报已换4.1.8.107；已修复入口吞掉全部异常的问题，startup_error会显示阶段/异常类型/安全代码帧与数值错误码，并写state/startup-last-error.json，不含异常原文/群名/消息。新增构造器失败与隐私反例，连同9项迁移检查共10项通过；默认inspect仍0真实操作。未重跑live，真实启动原因待用户提供新诊断，尚不声称已修复实际框架故障。

2026-10-31 00:15 Asia/Shanghai，本会话Codex继续WX-MIG-ALL收尾：用户反馈启动已恢复，随后明确“测试ok，继续”，记录本次单群文字版用户接受。归属AGENTS.md、PROGRESS.md、TASKS.md、README.md、docs/WX-MIG-ALL-REPORT.md、tracks/tasks/WX-MIG-ALL/HANDOFF.md及.gitignore。保留新出现的_temp/与wxauto_logs/本机工件，不读内容、不删除、不提交；仅补忽略。无代码/配置/运行实例改动，无新增验收。


本轮收尾验证：检查改动归属、Markdown本地链接、双向入口及git diff --check；仅文档与.gitignore，不重跑业务测试。按现有授权普通提交/push main核远端SHA。
