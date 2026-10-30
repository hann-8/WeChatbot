# WX-WXA-02 准备与试用报告

返回[PROGRESS](../PROGRESS.md) / [HANDOFF](../tracks/tasks/WX-WXA-02/HANDOFF.md)。

当前更新（2026-10-30）：用户自报账号已准备并登录微信4.2.0.11，先测一个指定群，接受更换兼容版本。账号阻塞解除；当前兼容/会话绑定/真实收发未验。后续按[统一迁移计划](QQ-TO-WECHAT-MIGRATION-PLAN.md)同轮准备入口，由用户实测；不把旧安装器元数据差异当永久阻断。

下列为27日准备阶段的历史事实：当时账号未准备、无会话绑定、真实试用未开始。30日只同步用户状态和新安排，没有运行微信或模型。

- 项目环境 `wxauto4` 版本 41.1.7；`inspect` 返回 dependency_present=true、production_eligible=false。试用台账 pending=false。无真实导入/构造。
- 从计划指定的第三方 [SiverKing Release](https://github.com/SiverKing/wechat4.0-windows-versions/releases/tag/v4.1.8.107) 下载 `weixin_4.1.8.107.exe` 至本机临时目录，233506664 字节，SHA-256 `b79aa3fdfd208d64f38fcc354684f9af213c05993c6f603521f2813930362b90`，与计划所记一致；这只证明与归档工件一致。Authenticode 状态 Valid，证书发布者 Tencent Technology (Shenzhen) Company Limited。
- 文件版本 `4.1.8.1000`、产品版本 `4.1.8.0`，与计划要求核实的 `4.1.8.107` 不一致；它们可能是安装器版本而非安装后客户端版本，但目前没有证据确认。按计划版本不符不运行；未安装或替换客户端，兼容性未验。临时工件路径 `C:/Users/yutha/AppData/Local/Temp/WeChatbot-WX-WXA-02/weixin_4.1.8.107.exe`，不提交。
- 指定会话、新消息接收、SendMsg 调用、框架本地返回、操作者观察均未执行；服务端 ACK 未验证，模型调用 0。未退出或操作微信。

30日后不重复询问账号/换版意愿。用户正常准备公开配套客户端、指定群和测试发送者，真实值只写本机忽略绑定；安装器标签与文件版本差异仅保留为历史线索，当前客户端版本与公开API效果才是实际依据。旧[WX-WXA-01报告](WX-WXA-01-REPORT.md)和[挑战计划](WXAUTO4-IMPLEMENTATION-PLAN.md)留作历史；新连续入口按统一计划交付，已有未决不删除、不重发。
