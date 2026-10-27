# 微信框架选型决定

2026-10-27：选型已进入[独立详细规划任务](../WX-WXAUTO4-PLAN/HANDOFF.md)，完整范围/接口/验收与medium指令见[实施计划](../../../docs/WXAUTO4-IMPLEMENTATION-PLAN.md)。本文26日选型仍作依据；下述“本轮不提交/无remote”是前轮历史。用户现已授权本次审阅文档commit/push，并明确要求创建public的WeChatbot，已建[hann-8/WeChatbot](https://github.com/hann-8/WeChatbot)作为origin。尚无安装/更换客户端/真实收发/模型结果。

返回[PROGRESS](../../../PROGRESS.md) / [TASKS](../../../TASKS.md)。继承[AGENTS](../../../AGENTS.md)，依据[框架优先约束](../WX-PLAN-ALIGN/HANDOFF.md)和[PLAN](../../../docs/PLAN.md)。

当前续作：`WX-FRAMEWORK-DECISION-practical-20261026`，2026-10-26 18:44（Asia/Shanghai）登记，负责人本会话Codex；按用户“以能用为优先、不必限定注入”完成选型和试用顺序修订，文档校验通过，未实施、未领取WX-03。原25日结论保留作历史，不再把完整源消息ID/服务端回执作为任何小范围试用的前提。

续作归属仍为AGENTS、PLAN、RESEARCH、IMPLEMENTATION_GUIDE、PROGRESS、TASKS、本交接。起始HEAD=`a66319d`，无remote；保留前轮所有未提交文档，不改src/config/tests/vendor/锁，不安装或操作微信，不调用模型，不提交/推送。此前有界只读版本查询未得到信息，随后用户已提供当前微信`4.1.15.13`并明确接受换版；这是用户提供的信息，没有读取UI、账号目录或数据库，也不把答复当作客户端更换已完成。

续作计划：以现成免费接口、客户端兼容和小范围可用性作比较；确认WeChatFerry的版本/维护/账号受限反馈；给出一个首选及简短试用步骤；同步旧冻结结论，校验文档。成功标准是能分清“值得试用”与“已验证可用”，不因不完整回执否决所有尝试，也不扩大到改框架内部。

## 2026-10-26当前决定与依据

首选组合确定为`wxauto4 41.1.7`免费版＋微信`4.1.8.107`，目标是单会话、人工可观察的基本文字收发；不限定进程注入，不新造完整机器人框架。免费版[官方文档](https://docs.wxauto.org/docs/install.html)列兼容到微信`4.1.8.107`；[PyPI 41.1.7](https://pypi.org/project/wxauto4/41.1.7/)于2026-09-01发布，有现有Python3.12 Windows x64工件。用户提供的当前版本`4.1.15.13`不在官方免费支持说明内，用户已接受换版，不再询问换版意愿；不为保留当前版本修改框架。安装/客户端更换和实际兼容测试仍未执行，后续按具体实施任务范围推进。

现成接口包括`ChatWith`、`GetSession`、`ChatInfo`、`SendMsg`、`GetAllMessage`。官方[WeChat类](https://docs.wxauto.org/docs/class/WeChat.html)把`AddListenChat`、`GetNextNewMessage`标为Plus；免费版首期不承诺后台多群监听，只规划当前指定会话的有界检查。没有购买、激活或默认转Plus的授权。旧GitHub仓库“停止更新”与正式包仍能获取是两件事，不据前者断言软件整体不能用。

WeChatFerry作为备选保留：官方[v39.5.2](https://github.com/lich0821/WeChatFerry/releases/tag/v39.5.2)于2026-03-28发布，配套微信3.9.12.51；当前仓库归档。维护者[2026-05-14回复](https://github.com/lich0821/WeChatFerry/issues/423#issuecomment-4455679595)仍说能用。[#126](https://github.com/lich0821/WeChatFerry/issues/126)是2024-02-02用户报告账号受限并经验证解封，不能据此推断所有账号都会封禁、当前封禁率或归档原因。若用户已有匹配旧客户端且可正常登录，值得考虑，不先判不能用；本轮不下载旧版或打登录绕过补丁。

Akasha已有AstrBot/OneBot桥接，但当前收发依赖WeFlow数据库与桌面发送，额外依赖更多，不作为首个最小文本试用的推荐。mosheng Hook和pyweixin的旧审阅保留，不再以“只有这个候选但一律不许试”锁住后续；也不将其缺口转成私有fork任务。

## 最小试用顺序（仅规划，未执行）

1. 确认客户端版本与免费包兼容；不兼容时报告具体版本，调整选型，不先改框架或自动买Plus/降级。
2. 后续用户明确一个目标会话及动作后，先读取新自造文本并发送一条自造文本，0模型；操作者观察实际目标与结果。只用公开接口，不扫描全部联系人/旧历史/数据库，不抢其他会话或管理附着客户端进程。
3. 基本收发成立后，才规划一次模型回复；复用独立的模型调用代码，不连接QQ运行端口/状态。不先做图片、free、多群、长期记忆或24h承诺。
4. 结果分别记录本地提交、人工观察、实际API确认；没有服务端ACK不等于不能试，也不把UI提交标成服务器接受。unknown不自动重发，重启不重放；临时ID/昵称只能标相应级别。
5. 真实@不足时不称可信@，此次不改变群自动触发；后续若采用文本唤醒需明确为文本规则。黑名单/授权不能被悄悄绕过，但首次0模型收发试验不需先实现全部自动群聊功能。

以上是在用户最新指令下拆分“首次受控试用”和“完整自动群聊接受”，不是扩大本轮真实授权。当前src/config/默认mock仍未修改，真实通道/模型关闭；仅文档改变，不需要运行回滚或清账。旧25日“必须等上游补齐再做任何试用”不再有效。

续作验证：七份归属文档写后重读，57个本地链接、配对围栏及根入口/台账双向链接通过，`git diff --check`通过；src/config/scripts/tests/vendor/项目依赖锁相对HEAD无差异。没有安装或导入wxauto4，没有新业务测试/真实观察/发送/模型结果；历史70项不计为本轮验证。既有未提交修改均保留，本轮仍未提交、无remote、未推送。

以下25日内容为历史检查点，不再是当前候选排序或全部试用门槛。

## 目标、范围与文件归属

用户明确“不太理解选哪个框架，你来决定”。本项负责给出单一后续候选、核实其原生收发接口与已知差额、规定进入实施条件；目标仍为个人亲友群，不更换成官方Bot私聊产品，不把注入方式当稳定性证据。

文件归属：AGENTS、PLAN、RESEARCH、IMPLEMENTATION_GUIDE、PROGRESS、TASKS、本交接。起始本地 `codex/bootstrap` HEAD=`a66319d`、无 remote；保留前轮已知未提交的五份文档（含 WX-PLAN-ALIGN 交接）。不提交/推送，不改 src/config/tests/vendor/锁，不安装、编译、注入、登录、读微信数据库或执行真实收发/模型；公开源码只读。

计划：核对候选现有 Webhook/发送接口，按真实源码而非旧笔记作决策；记录固定版本及身份/@/消息ID/发送结果/配置与许可差额；同步各入口后复读和检查文档。成功标准是决定明确、候选与可部署资格分开、没有把差额转换成改写框架核心的任务。

## 2026-10-25历史决定

后续唯一候选为[mosheng20205/WechatHook4.1.10.27](https://github.com/mosheng20205/WechatHook4.1.10.27/tree/713ec7d6f01d858e067a623c9bf2cda64d0d3e19)，固定复核commit `713ec7d6f01d858e067a623c9bf2cda64d0d3e19`，仅声明适配Windows微信`4.1.10.27`。分支API确认该commit及2026-07-18提交时间，不把树对象/文件blob或最近star时间冒充维护提交。

选择理由是原生DLL Hook、已有外部Webhook与HTTP文本发送，比继续用UI原语拼装收发更接近用户希望的接入形态。此为候选收敛，**当前版本不进入实施，没有可启用的真实后端**。pyweixin保留代码/探针/报告，不再新增provider或真实适配投入；不删除离线核心，不改默认mock或能力资格，不将iLink私聊替换成亲友群产品。

## 固定源码证据与差额

| 项目 | 本次静态证据 | 判断 |
| --- | --- | --- |
| 外部接收接口 | [回调3668–3701](https://github.com/mosheng20205/WechatHook4.1.10.27/blob/713ec7d6f01d858e067a623c9bf2cda64d0d3e19/src/inline_weixin_dll_load.cpp#L3668)读取`recv_url`，输出selfwxid/fromid/toid/room/sender/msgtype/msg | 已有源码，不是还需我们写接收Hook；未运行验证 |
| 群内发送者 | [拆分3991–4016](https://github.com/mosheng20205/WechatHook4.1.10.27/blob/713ec7d6f01d858e067a623c9bf2cda64d0d3e19/src/inline_weixin_dll_load.cpp#L3991)从传输群正文前缀拆成员；缺前缀则sender退回群ID | 修正旧笔记“成员字段未接入”的不完整描述；不等于实际绑定/可信性通过，fallback不能作成员身份 |
| 源消息ID | 同一回调第3691行把`msgsvrid`写死为0，time来自`GetTickCount64` | 不符合现有稳定消息ID/去重合同；不能把本地序列或正文hash升级为服务端ID |
| 真实入站@ | 已核回调没有输出结构化mention或msgsource XML字段 | 无已证可信@，mentions群路径保持关闭；不改为正文匹配或全回复 |
| 文本发送结果 | [README第142行及215–219行](https://github.com/mosheng20205/WechatHook4.1.10.27/blob/713ec7d6f01d858e067a623c9bf2cda64d0d3e19/README.md#L142)明确`/SendTextMsg`仅表示本地入队 | 不能当微信服务端接受或对端送达；无关联接受证据时仍为unknown，不自动补发 |
| 加载副作用/监听 | [初始化5819–5886](https://github.com/mosheng20205/WechatHook4.1.10.27/blob/713ec7d6f01d858e067a623c9bf2cda64d0d3e19/src/inline_weixin_dll_load.cpp#L5819)实际绑定`0.0.0.0`并安装联系人/SQLite等观察Hook，README写127.0.0.1；自动回复会加载已有磁盘配置 | 未证明能通过正式配置收敛到项目允许范围；不能只凭README视作仅本机/无额外读取，也不通过私改核心解决 |
| 许可/版本/稳定性 | API项目license为空，本次完整树未见根项目许可证，只有第三方MinHook许可；目标客户端版本固定，未核本机版本 | 不把公开仓库或第三方许可当完整授权；未证明本机兼容、长稳、重登/账号切换，也不降级客户端试跑 |

源码文件blob：`inline_weixin_dll_load.cpp=79c864e5221f6d964533d3ad415e21f4bab6c2bc`，`README.md=abe40ed3a6f00f1313052a010374cdff3df36b19`。没有下载/运行DLL、客户端或依赖，没有把上游自述真机验证当本项目接受结果。

## 2026-10-25旧规则（26日已修订试用条件）

本次到候选收敛与差额报告结束。当前没有进入Hook适配实施的任务；不继续泛化搜索、反复安装试错、编译注入、做新偏移逆向、补发消息、补接内部回执或私有fork。稳定消息ID、可信@及可靠文本接受不能由关闭图片/free等附加功能替代。

只有后续上游版本/现有正式接口与配置提供上述必要能力及清晰许可，才以新的固定证据复核；不为维持本次候选决定修改源码或降低既有合同。复核通过后另行规划项目侧薄适配与AstrBot/现有模型层复用，再由用户给实施指令；真实对象/动作仍另行明确。若持续缺少最小能力，维持停在缺口报告，候选收敛不产生部署义务。

预期运行默认值不变：mock、enabled/sends=false、群空、私聊关闭、mentions/single，模型/图片/联网关闭；没有新增可启用transport枚举。文档决策可撤回到既有离线mock状态，无运行迁移或清账动作。

## 2026-10-25验证与交付

七份归属文档写后重读，57个本地链接、配对代码围栏、根入口/台账与本交接双向链接检查通过，`git diff --check`通过。src/config/scripts/tests/vendor/项目依赖锁相对HEAD无差异；未运行业务测试，历史70项不算本轮结果。前轮WX-PLAN-ALIGN交接保持原样，其他前轮文档仅按本次归属增量同步；没有其他已跟踪文件变更。

本地HEAD仍为`a66319d`，未提交、无remote、未推送。决策/差额报告已交付，候选的真实接入、稳定性及所有本机能力均未验证；没有待自动推进的实施步骤。
