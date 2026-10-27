# wxauto4 详细规划交接

返回[PROGRESS](../../../PROGRESS.md) / [TASKS](../../../TASKS.md)。继承[AGENTS](../../../AGENTS.md)。

状态：completed，仅详细规划与文档交付；session `WX-WXAUTO4-PLAN-20261027`，2026-10-27 19:05（Asia/Shanghai）起，负责人本会话 Codex。用户指定本轮sol/max规划，完成后交medium实施；不检测或切换会话设置。

最新续作：`WX-WXAUTO4-PLAN-terra-20261027`，19:51（Asia/Shanghai）起，用户希望用`gpt-6.1-terra/medium`试落地。按TASKS登记仅改六份文档，起点`fa12125`且工作区干净；AGENTS与三段当前复制指令改为Terra，首项仍WX-WXA-01且未领取，范围/验收/机器人CodeBuddy后端不变。本次不实施或自动切换模型，沿既有授权commit/push核SHA。

OpenAI Docs复核：[官方选型建议](https://learn.chatgpt.com/docs/model-selection)将Terra列为有明确目标、可验结果的代码/界面任务可试选项；[模型页](https://developers.openai.com/api/docs/models/gpt-6.1-terra)列有medium。判断本项目首项值得试是基于其已确定的接口/验收，不是Terra对本仓库的既有成功证据；用真实交付与回归结果评价，不额外运行模型对比工程。

模型续作验证：六份文档写后复读、66个本地链接/围栏/UTF-8 LF与diff检查通过；三段当前指令全部使用Terra medium，业务代码/运行配置/依赖未变，不重跑业务测试。续作文档提交说明`docs: allow Terra medium for wxauto4 implementation`；基线规划提交为`fa12125`，本次提交SHA按最终本地HEAD/远端分支实际读取并核对，完成后停止。

目标：把已选wxauto4免费版41.1.7＋微信4.1.8.107落实为最小文字收发、薄适配和模型复用的可执行计划，明确每次实施的文件/接口/验收/停止点，交付可复制medium指令。本轮不安装、更换客户端、登录、观察微信、收发消息、执行模型或改业务代码。用户当前4.1.15.13且已接受换版，不重复确认换版意愿。

文件归属与起点见[TASKS登记](../../../TASKS.md)。起始为 `codex/bootstrap` / `a66319d`、无remote；前轮六份已跟踪文档差异与两份交接均已识别为本会话成果，保留并审阅后纳入本次11份文档检查点。最初缺地址已询问，随后用户给出建仓授权；不使用QQ远端。

后续授权已解决远端：用户明确要求在其GitHub创建public的WeChatbot。2026-10-27已建立[hann-8/WeChatbot](https://github.com/hann-8/WeChatbot)，private=false；本地origin=`https://github.com/hann-8/WeChatbot.git`，创建后远端heads为空。连接器无建仓接口，使用本机Git已有同账号凭据调用GitHub官方API；凭据未写入文件/输出。待发布133个当前文件和145个历史blob未见受保护路径或常见秘密模式命中。只发布审阅文档及原有已跟踪源码/合成模板/许可，忽略运行工件与私人数据。

工作顺序：核对官方免费API、Python/客户端配套与当前项目合同；决定首次试用最短路径；写详细计划及medium指令；同步根进度/工作线/任务台账，写后重读、核链接及差异；提交已审阅文档。远端存在且地址明确时才推送并核对SHA。

成功标准：新session从根入口能直达本计划，只领取一项即可实施；不要求先复刻QQ功能或证明全部生产能力，不伪造身份/@/消息ID/服务端ACK；公开接口不足时停在具体缺口，不改上游内部。已规划/源码或文档支持/离线/真实各自标明。

已完成主要规划：[独立计划](../../../docs/WXAUTO4-IMPLEMENTATION-PLAN.md)写明公开API/固定工件、两模块薄封装、人工监督试用的输入/基线/一次动作/结果等级、三个独立任务与退出方式；[medium指令](../../../docs/IMPLEMENTATION_GUIDE.md)包含三段独立复制文本，首推WX-WXA-01。选择暂不加AstrBot，保留旧离线Gate，后续直接复用本项目固定runner。当前默认mock/代码未变；三项实施均未领取。

公开复核：官方安装/WeChat/Chat/Message文档、PyPI 41.1.7 JSON和客户端版本归档Release元数据。确认免费版边界、UI ID会变及wheel/客户端asset摘要；本轮不下载包/客户端、不import wxauto4、不操作微信。摘要与接口文档支持不等于安装签名或本机兼容已验。

验证：11份归属/纳入检查点文档写后复读，99个本地链接、成对围栏、全部工作线根入口/返回链接、UTF-8无BOM/LF、git diff --check均通过；src/config/scripts/tests/vendor/pyproject.toml/uv.lock相对起点无差异。没有新业务测试，历史70项不作为本轮结果；没有下载/安装包或微信客户端、登录/观察/收发/模型/SSH，运行配置保持原样。

Git检查点：初版详细规划为`fa12125`（提交说明`docs(wxauto4): plan supervised text trials`），最新Terra续作接在其后；origin见上，发布分支`codex/bootstrap`。本地SHA从`git rev-parse HEAD`取，远端从`git ls-remote origin refs/heads/codex/bootstrap`取，实际交付答复报告一致性；不预写提交自身SHA。前轮差异均在本任务逐文件复核范围，没有未审阅源码/秘密混入。

下一步由用户在界面选择gpt-6.1-terra及medium后按[当前首段指令](../../../docs/IMPLEMENTATION_GUIDE.md)领取WX-WXA-01；该项只做试用工具/可选依赖/离线验证。真实会话和客户端动作留给另行明确的WX-WXA-02，模型留给WX-WXA-03。本轮到文档/Git结束，不自动开始任何实施。
