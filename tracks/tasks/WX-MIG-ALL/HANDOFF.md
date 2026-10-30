# WX-MIG-ALL 批量文字版迁移交接

返回[PROGRESS](../../../PROGRESS.md) / [TASKS](../../../TASKS.md) / [统一计划](../../../docs/QQ-TO-WECHAT-MIGRATION-PLAN.md) / [报告](../../../docs/WX-MIG-ALL-REPORT.md) / [使用说明](../../../README.md)。继承根AGENTS。

## 当前状态

2026-10-30 Asia/Shanghai，session WX-MIG-ALL-20261030，负责人本会话Codex，22:37登记。**实现与必要检查completed，等待用户实测**。main基线33c18f0，上轮十份规划成果保留并审阅，同本任务交付。未操作真实微信/安装器，未调用真实CLI模型/工具服务/SSH或群发送；无真实兼容/收发验收声明。

唯一任务WX-MIG-ALL，未分领MIG-01/02/03。按授权普通commit/push main，远端SHA在最终答复核对，不建分支/force。源SnowLuma42911af只读无改动。

## 已实现与文件归属

- src/wechatbot/chat_session.py、chat_model.py、chat_policy.py、wxauto4_chat.py：单绑定群连续文字、精确允许昵称/黑名单、基线去重、单并发队列、本机控制、八轮RAM、真实local_reported/unknown语义、schema2全文记忆及原生联网小包装；仍用原transports/wxauto4_adapter.py三个公开API，不伪造生产事件/QQ身份。
- config/defaults、config/examples、config/README、models policy：524288可见UTF-8字节/low/thinking=false、memory/web准备true，其他能力关闭；本机config/local与secrets空模板忽略。微信persona/后端/模型/账号不替换，家庭连接不复制。
- docs/WX-MIGRATION-SOURCE-MAP.json所列共用模块及三份插件；公开capabilities、framework四字段、types锁定；scripts/check_snapshot.py/prepare_cli.py、versions锁与vendor manifest。74项混合快照，未用旧文件保留旧来源，微信相对Node/entry与spawn替身接点合并。
- Start-WeChatbot.ps1一个入口；README、报告、PROGRESS/TASKS及上轮已知规划文档同步。tests/test_chat_migration.py、test_native_guard.py及固定源合成SDK fixtures；offline_backend和test_core适配low元数据握手。

## 检查和边界

最终60项通过（8迁移组合＋1实际插件合成SDK/9限定变体＋41原严格核心＋10挑战工具）。源码/工件74项摘要与framework_upper=8985、compileall、默认启动inspect与旧trial mock通过。inspect 0微信/0生成/0发送；Node仅运行合成SDK host，不启动CLI或联网服务。初次发现内部JSON被single输出当文字及旧stdin断言不适应low握手，已同轮修正并通过。

保存失败保原件并真实回执、跨会话隔离、reset后新Store全文读回和增改删、当前问题/全文记忆不裁、旧历史整轮裁、两轮单任务单发送、unknown不重试/重启保留、错群/pause旧结果不保存/发送、HTTP(S)/参数封套/工具裁剪与限制均有定向替身证据。没有全库、长稳、媒体或生产矩阵。

## 本机准备与下一步

当前后端codebuddy_cli；Python3.12.14、wxauto4 41.1.7依赖存在，相对CLI Node/entry/bundle/types齐全。config/local五文件和secrets/wxauto4-chat.local.json为空模板；真实名字只由用户填本机，不入报告/Git。旧挑战未决不清理。

安装器已存在于C:/Users/yutha/AppData/Local/Temp/WeChatbot-WX-WXA-02/weixin_4.1.8.107.exe，233506664字节，SHA256 b79aa3fdfd208d64f38fcc354684f9af213c05993c6f603521f2813930362b90，Tencent签名Valid；未运行。文件/产品元数据差异不永久阻断。用户正常退出/安装/登录，安装后看客户端版本与公开API表现；当前4.2.0.11兼容未验。

下一步只由用户：按README正常换版/登录，填一个群和允许昵称、手动打开群，Start-WeChatbot.ps1先inspect再-Live，等baseline_ready后实测。正常就接受，不再加无关验收轮次。本会话交付后停止；后续有具体故障就在本范围修复。回滚保留未决/记忆/用户数据，不退出微信，不操作QQ。
