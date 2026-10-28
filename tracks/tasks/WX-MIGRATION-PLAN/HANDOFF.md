# WX-MIGRATION-PLAN：QQ业务向微信的功能迁移规划

返回[PROGRESS](../../../PROGRESS.md) / [TASKS](../../../TASKS.md) / [详细计划](../../../docs/QQ-TO-WECHAT-MIGRATION-PLAN.md) / [实施指令](../../../docs/IMPLEMENTATION_GUIDE.md)。继承根AGENTS；WX-WXA-02真实试用的旧归属与阻塞保留。

## 当前状态

completed，仅详细规划；代码未实施、业务测试未运行。2026-10-28 14:06（Asia/Shanghai）登记，session `WX-FEATURE-MIGRATION-PLAN-20261028`。用户追加明确：本轮commit/push可直接推主线，后续全部gpt-6.1-sol/medium；预算无更低硬限制时可48000。

## 基线与归属

- QQ main：`52866fe10cc654d2e12c5520f7afc5aa8bbe0179`。
- 微信试用基线：`29240978a298e3fd5a47a21af7eb10a670d48994`，原默认codex/bootstrap为`8ad1334a66ee9d3ff7cedc70b51ce4fa3dc085ac`，试用仅多两个已有提交。
- 六份文档：AGENTS/PROGRESS/TASKS、docs/IMPLEMENTATION_GUIDE.md、docs/QQ-TO-WECHAT-MIGRATION-PLAN.md、本HANDOFF。
- 初始临时规划分支仅作准备指针；用户随后要求直接主线，最终按普通快进codex/bootstrap交付，不force、不改默认名称，保留两个试用提交原作者/历史。
- 本机没有实际E:/CodexWS/WeChatbot；用GitHub固定提交及本地文档覆层审阅，不触碰另一台电脑未提交内容。初始TASKS与本HANDOFF已先登记并重读。用户随后要求本笔记本不留项目文件，远端核对后删除本轮本地覆层；云端环境单独创建，代码根以云端checkout为准。

## 已完成与决定

18个共享模块按Git blob比较，12个相同、6个不同；微信已有固定快照，不重新全量复制。首推WX-MIG-01人设/自然纯文本/监督模型接点，再02短期RAM与本机控制，后03显式单URL读取；adaptive、长期记忆/free/媒体/成员与搜索延后。

微信16384是当前输入政策值，配置可至131072；固定能力记录为CLI2.168.0/DeepSeek maxInputTokens1000000，原生有效窗口仍未实测。推荐代码准备采用48000可见UTF-8字节政策，各reserve2048，模型/auto/null保留。QQ角色正文19256字节/9585字符会被现有8000字符校验拒绝，计划同时改为最终预算校验，不强制删角色段落。

MIG-01代码准备可先于WXA-02真实通过；不关闭旧real_model_closed、不伪造NormalizedEvent/能力资格，不接真实GUI/模型。后续统一Sol/medium，旧Terra选择仅历史。详细字段、生效/回滚、文件和接续指令见计划。

## 验证与边界

只做两仓库源码/固定能力/分支关系读取、文档本地链接/围栏/任务ID/UTF-8 LF/差异与归属检查。业务测试、inspect/mock、客户端、登录、收发、模型、公共HTTP和SSH均未执行。历史80项不作为本轮验证数。

本轮新增提交仅六份Markdown，实际业务代码/local/persona/运行数据无变更；主线快进还包含两个既有试用提交，不能把它们称为本轮新实现。提交/远端SHA在会话交付中核对，不把本回执自身SHA写回造成自引用。

## 剩余与第一步

没有已领取的实施session。用户后续选Sol/medium时，只领取WX-MIG-01，先按真实项目PROGRESS/AGENTS/TASKS与本计划重查最新主线和工作区、登记精确归属，完成该项后停止。WXA-02账号和客户端版本证据仍待另定时段；不把阻塞转为本轮新任务，不自动开展测试。
