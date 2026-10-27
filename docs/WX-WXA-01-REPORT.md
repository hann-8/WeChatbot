# WX-WXA-01 离线交付报告

返回 [PROGRESS](../PROGRESS.md) / [HANDOFF](../tracks/tasks/WX-WXA-01/HANDOFF.md)。

实现独立的 wxauto4 单会话试用入口、工厂注入的公开接口适配、合成绑定和跨编号未决阻断台账；不修改旧 Gate、固定 runner 或默认配置。使用本项目 Python 3.12 环境安装 Windows 可选 extra，锁增加必要依赖，已有依赖版本无升级。wheel 大小与 SHA-256 与清单一致；未提交 wheel。固定 wheel 的公开 `wx.pyi` 支持 `WeChat(debug=False, resize=False)`，以及 `ChatInfo`、`GetAllMessage`、`SendMsg`；`param.py` 的 WxResponse 为 dict，status 为“成功”仅记框架本地报告，未决仍保留。公开文档与固定包实际行为仍须真机验证。wheel 无独立许可文件，条款见 [上游文档](https://docs.wxauto.org/)；不据此推断再分发许可。

离线检查：针对性 10 项、全套 80 项通过；固定快照检查 63 文件、2 处受控差异、工件 hash 通过；inspect 与合成 mock 通过。mock 的 send_invoked 仅指替身调用。未安装或切换微信客户端、未导入或构造真实 WeChat、未观察窗口、登录、收发、SSH 或调用模型。真实客户端兼容、身份、消息 ID、收发、恢复及服务端 ACK 全部未验。

命令（最后两项仅供后续明确授权的 WX-WXA-02，不在本任务运行）：

```powershell
.venv\Scripts\python.exe -m wechatbot.wxauto4_trial inspect
.venv\Scripts\python.exe -m wechatbot.wxauto4_trial mock
.venv\Scripts\python.exe -m wechatbot.wxauto4_trial run --mode live --binding secrets/wxauto4-trial.local.json
.venv\Scripts\python.exe -m wechatbot.wxauto4_trial observe --trial-id <试用编号>
```

绑定参照 `config/examples/wxauto4-trial.example.json`，使用独立忽略目录，设置唯一自造挑战和回复，并由操作者确认测试者同名无歧义。`observe` 只在操作者确实看到对应结果后标记人工观察，不发送，不表示服务端 ACK。框架可能使用焦点、键鼠或剪贴板；调用可能阻塞，120 秒仅轮询预算。窗口复核与发送不原子，显示名无法证明账号身份；ID 部分重建且仍有重叠不能保证被发现。切换会话、重建或同名歧义时操作者应停止试用。未决不自动重试或换编号解除；无观察结论则保留。当前试用不读取历史数据库、不连接模型。
