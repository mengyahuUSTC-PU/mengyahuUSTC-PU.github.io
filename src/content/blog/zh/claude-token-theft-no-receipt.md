---
title: "你没在用 Claude，额度却在掉：一场没有账单的盗刷"
description: "infostealer 偷走的不是密码，是你已登录的会话。拆解 Claude 订阅额度盗用的攻击链，以及为什么这类盗刷比信用卡盗刷更难被发现。"
pubDate: 2026-09-08
tags: [ai-security, account-security, infostealer]
lang: zh
slug: claude-token-theft-no-receipt
translationOf: claude-token-theft-no-receipt
---

8 月 4 日，英国东萨塞克斯的独立 AI 顾问 Grant De Swardt 注意到一件小事：他没在干活，Claude 的用量条却从 45% 涨到了 55%（[TechCrunch](https://techcrunch.com/2026/09/08/hackers-are-stealing-claude-tokens-from-subscribers/)）。他订的是每月 200 美元的 Max 档。不久后 Anthropic 暂停了他的账户、作废了所有会话，退了 44.49 英镑，并告诉他：他的账户被一个疑似未经授权的外部服务用来处理别人的活动，至于对方是怎么拿到访问权的，Anthropic 没能确定。

他不是个例。Reddit 上的相关帖子聚集了大量同样遭遇的用户：有人的用量在 12 分钟内从 0 冲到 49%；有人连续三天额度被烧光；还有人的账户在本人不知情的情况下被升级到了更贵的档位并扣了费。Anthropic 随后向受影响用户发邮件确认：「我们最近发现一个恶意行为者，正在用常见的 infostealer 恶意软件从用户电脑上窃取 Claude 登录会话，再用这些会话访问账户、消耗用量。」（[BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-warns-infostealer-malware-is-hijacking-claude-sessions-to-drain-usage/)）

这件事最值得拆的地方不在「账号被盗」本身。账号被盗是老故事。新的是攻击者图的东西：偷走的是登录会话，掏空的是一种预付费的计算额度。这种消耗不产生新的银行交易，套餐内的用量也没有逐会话的明细，没有银行风控替你盯着。额度被人蹭了，你多半不知道。

## 被偷的不是密码，是「已经登录」这个状态

先把机制讲清楚，假设你完全没有安全背景。

你登录 Claude 时要输密码，可能还要过两步验证（2FA），比如手机收个验证码。这相当于在大门口查身份证。查完之后，网站不会每次操作都重新查一遍，而是在你的浏览器里存一小段数据，叫会话 cookie（session cookie），相当于查验后发给你的手环：接下来你每次请求，只要出示手环，网站就认定「这是刚才那个人」（[OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)）。

infostealer（信息窃取类恶意软件）干的事，就是潜入你的电脑，把浏览器里存的手环整个复制走。攻击者拿到手环后，不需要你的密码，也不需要过两步验证，因为在网站看来，他就是「已经登录的你」。安全行业管这叫会话劫持（session hijacking）：拿到有效的会话 cookie，就能完整冒充这个用户（[OWASP](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/09-Testing_for_Session_Hijacking)）。这就是为什么此类攻击能绕过 2FA：2FA 守的是大门，而攻击者是直接从你口袋里摸走了手环。根据 Anthropic 发给用户的邮件，这次涉及的都是安全圈的老面孔：Windows 上的 Vidar、LummaC2、StealC、RedLine、Acreed，以及少量 Mac 用户中招的 Atomic Stealer（[Search Engine Journal](https://www.searchenginejournal.com/anthropic-warns-hackers-are-stealing-claude-sessions-to-hijack-accounts/587566/)）。感染途径也是老一套：Reddit 上有受害者承认，中招前下过盗版游戏（[Search Engine Journal](https://www.searchenginejournal.com/anthropic-warns-hackers-are-stealing-claude-sessions-to-hijack-accounts/587566/)）。

攻击链还有关键一步。据 TechCrunch 报道，被盗的 Claude 会话密钥被用来「铸造未经授权的 Claude Code OAuth token」。翻译一下：攻击者拿着浏览器会话，去给 Claude Code（Anthropic 的编程 agent 工具，[官方文档](https://code.claude.com/docs/en/overview)）签发了程序化访问凭证，也就是一把可以写进脚本里用的钥匙，让盗刷不必有人守着浏览器窗口。两种凭证各自的有效期和权限范围，公开报道没有披露。12 分钟烧掉 49% 额度这种速度，我的推断是手动聊天聊不出来，更像脚本化跑 agent 任务的消耗节奏；报道没有取证攻击者具体跑了什么负载，这一点是推断，不是坐实的事实。

## 为什么受害者几乎不可能自己发现

把这次盗刷和传统信用卡盗刷对比，差别立刻出来。

信用卡被盗刷，你有三层保护：银行风控会标记异常交易；月底账单上每一笔消费都有商户名和金额，监管机构提醒消费者盯紧账单，正是因为盗刷会在这里现形（[CFPB](https://www.consumerfinance.gov/consumer-tools/bank-accounts/watch-accounts-closely-when-card-data-is-hacked/)）；发现未授权扣费还能发起争议（chargeback），核实属实后这笔钱必须从账单上撤掉（[CFPB](https://www.consumerfinance.gov/ask-cfpb/how-do-i-dispute-a-charge-on-my-credit-card-bill-en-61/)）。这套体系是几十年欺诈损失堆出来的。

订阅制 AI 额度被盗刷，三层几乎全部失效。第一，攻击者通常不产生新的扣费。钱你早就付了，他消耗的是预付额度；套餐内的用量根本不走你的卡，只有单独购买的用量积分（usage credits）才会产生额外扣费（[Claude Help Center](https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans)）。银行侧看不到新增交易，风控无从谈起。例外是前面那位账户被擅自升级的用户，确实被多扣了钱，但那笔扣费在银行看来也只是 Anthropic 的一笔正常订阅扣款，同样触发不了风控。第二，没有逐任务的明细。Claude 设置里确实有一个用量页面，能看到整体消耗和历史（[Claude Help Center](https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans)），但订阅用户拿到的只是汇总数字：没有逐会话的列表，看不到跑了什么任务、每次烧了多少。De Swardt 之所以发现，纯粹因为他碰巧在没干活的时候盯了一眼用量条；一个每天把额度用到七八成的重度用户，被人蹭走两三成额度，未必察觉得到。他对 TechCrunch 说得直白：Anthropic 没有给用户提供「能看到是什么在消耗 token 的工具」，没有逐项明细，订阅用户就没有办法保护自己。第三，没有制度化的追回机制。算力是即时消费品，token 烧掉就是烧掉了；De Swardt 拿到的 44.49 英镑退款是 Anthropic 的个案处置——官方支持页面也只说团队可以「核查退款资格」（[Anthropic Help Center](https://support.claude.com/en/articles/9015913-how-to-get-support)），不是用户可以像信用卡拒付那样主张的成文争议流程。

Anthropic 的检测倒是起了作用：是它主动发现异常、登出用户、发的邮件。但当 TechCrunch 问及用户自己该怎么识别滥用时，Anthropic 拒绝置评。平台看得到的，用户看不到。这个信息差就是当前订阅制 AI 产品安全模型的最大缺口。

至于攻击者偷额度干什么，Anthropic 和各家报道都没有点明，这一点我只能按机制推演，无法验证。最顺的变现路径有两条。一是转售：被盗 AI 账号在黑市早有先例，Group-IB 在 2023 年就发现超过 10 万台被 infostealer 感染的设备上保存的 ChatGPT 账号凭证在暗网市场流通（[Group-IB](https://www.group-ib.com/media-center/press-releases/stealers-chatgpt-credentials/)），偷来的额度是零成本货源。二是自用，跑爬虫清洗、批量内容生成这类本来要花 API 钱的负载。infostealer 偷来的凭证历来按「日志包」（stealer logs）在暗网市场和 Telegram 频道批量出售（[Flare](https://flare.io/learn/resources/blog/stealer-logs-and-corporate-access/)）；Claude 会话是不是已经成了日志包里新添的一个值钱字段，我没有黑市交易记录可以证实，但机制上顺理成章。

还有一个细节值得如实记下：De Swardt 说他扫描后没有在自己电脑上找到任何感染证据。Anthropic 的邮件里也提到另一种可能：账户连接了未经授权的外部服务。也就是说，具体到每个受害者，会话到底是被本机恶意软件偷走、还是从某个第三方工具泄漏的，并没有逐一坐实。这次事件的整体归因（infostealer）来自 Anthropic，但个案层面存在没对上的地方。

## 你现在该做什么

如果你是 Claude 订阅用户（或任何 AI 订阅产品的用户），有几个动作值得今天就做：

**先杀毒，再改密码。顺序不能反。** 这是 Anthropic 邮件里反复强调的点：登出只能作废已被偷走的会话，杀不掉电脑里的恶意软件。如果 infostealer 还在，你改的新密码、新登录的会话会立刻再次被偷。先用杀毒软件全盘扫描并清除，确认干净后再改密码、重新登录。

**检查活跃会话。** Claude 设置里可以查看所有已登录的设备、浏览器和大致位置（[官方指引](https://support.claude.com/en/articles/13124001-managing-your-active-sessions)），看到不认识的位置或设备，立即终止。

**盯用量条的两个异常信号。** Anthropic 邮件里给出的典型症状是：额度看起来「回满了，然后在你没用的时候掉下去」。另一个信号是你明明没干活、用量却在涨。养成偶尔在空闲时瞄一眼的习惯。在平台给出逐项明细之前，用户侧的检测手段就是这根用量条、设置里的汇总用量页，加上前一条说的活跃会话列表，没有更多了。

**把邮箱当成同等重要的阵地。** 你的 Claude 账户挂在邮箱上，攻击者一旦拿下邮箱，就可能顺着找回密码的流程接管挂在这个邮箱上的各种账户（[NCSC](https://www.ncsc.gov.uk/guidance/recovering-a-hacked-account)）。改邮箱密码、登出其他设备、开启两步验证。Anthropic 这次替受影响用户移除了保存的支付方式；Malwarebytes 提醒，要等上面的清理步骤全部做完、确认电脑干净之后，再把支付方式加回去。发现持续异常可以联系 usersafety@anthropic.com。

**别碰盗版和破解工具。** 这轮受害者里，公开追溯到感染源的那一例，起点是一款盗版游戏。盗版和破解软件一直是 infostealer 的标准分发渠道；微软对 Lumma Stealer 的分析就描述了把正版应用的破解版和恶意软件打包、经文件分享平台传播的手法（[Microsoft](https://www.microsoft.com/en-us/security/blog/2025/05/21/lumma-stealer-breaking-down-the-delivery-techniques-and-capabilities-of-a-prolific-infostealer/)）。

最后说个判断。订阅制 AI 额度正在变成一种真实的、可被盗窃的资产类别，但围绕它的安全基础设施还停留在「一根百分比条」的水平。信用卡体系用几十年学会了给用户逐笔明细和拒付权，我判断 AI 订阅平台迟早也要走到这一步：逐会话的用量日志、异常消耗告警、可撤销的细粒度凭证。在那之前，用户侧能做的只有上面这些，而平台侧欠的账，De Swardt 已经点明了：订阅用户没有办法保护自己。他后来换去了 Cursor。在我看来，赶走用户的未必是安全事故本身，而是出了事之后什么都看不到。

## 参考来源

- [Hackers are stealing Claude tokens from subscribers — TechCrunch](https://techcrunch.com/2026/09/08/hackers-are-stealing-claude-tokens-from-subscribers/) — De Swardt 案例细节（日期、用量变化、退款金额、访问来源未能确定）、session key 铸造 OAuth token 的机制、Reddit 受害者汇总、Anthropic 拒绝置评识别方法
- [Anthropic warns infostealer malware is hijacking Claude sessions to drain usage — BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-warns-infostealer-malware-is-hijacking-claude-sessions-to-drain-usage/) — Anthropic 邮件原文引语、恶意软件家族名单、官方处置措施（登出、移除支付方式、退款）
- [Infostealers are hijacking Claude accounts at users' expense — Malwarebytes](https://www.malwarebytes.com/blog/news/2026/09/infostealers-are-hijacking-claude-accounts-at-users-expense/) — 用户防护步骤顺序（先杀毒再改密码）、清理完成后再重新绑定支付方式的建议、usersafety@anthropic.com 联系渠道
- [Anthropic Warns Hackers Are Stealing Claude Sessions To Hijack Accounts — Search Engine Journal](https://www.searchenginejournal.com/anthropic-warns-hackers-are-stealing-claude-sessions-to-hijack-accounts/587566/) — 确认 Anthropic 声明出自发给用户的邮件（经 Reddit 流出）而非公开公告、恶意软件家族名单交叉印证、盗版游戏感染源案例
- [Claude Code overview — Anthropic docs](https://code.claude.com/docs/en/overview) — Claude Code 作为 Anthropic 的编程 agent 工具，支持脚本化与自动化使用
- [Managing your active sessions — Claude Help Center](https://support.claude.com/en/articles/13124001-managing-your-active-sessions) — 活跃会话管理的官方指引
- [Manage usage credits for paid Claude plans — Claude Help Center](https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans) — 套餐内用量与单独计费的用量积分的区别、设置里的用量页面
- [How to get support — Anthropic Help Center](https://support.claude.com/en/articles/9015913-how-to-get-support) — 支持团队逐案核查退款资格
- [Session Management Cheat Sheet — OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) 与 [Testing for Session Hijacking — OWASP](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/09-Testing_for_Session_Hijacking) — 会话 cookie 维持登录状态、被盗会话可完整冒充用户的机制说明
- [Watch accounts closely when card data is hacked — CFPB](https://www.consumerfinance.gov/consumer-tools/bank-accounts/watch-accounts-closely-when-card-data-is-hacked/) 与 [How do I dispute a charge on my credit card bill? — CFPB](https://www.consumerfinance.gov/ask-cfpb/how-do-i-dispute-a-charge-on-my-credit-card-bill-en-61/) — 账单监控建议、信用卡账单争议与未授权扣费撤销机制
- [Recovering a hacked account — NCSC](https://www.ncsc.gov.uk/guidance/recovering-a-hacked-account) — 邮箱失守为何会波及挂在它名下的各种账户
- [Over 100K compromised ChatGPT accounts found on dark web marketplaces — Group-IB](https://www.group-ib.com/media-center/press-releases/stealers-chatgpt-credentials/) — 被盗 AI 账号在暗网市场流通的先例
- [Stealer Logs & Corporate Access — Flare](https://flare.io/learn/resources/blog/stealer-logs-and-corporate-access/) — stealer logs 在暗网市场与 Telegram 频道按包批量交易的研究
- [Lumma Stealer: breaking down the delivery techniques of a prolific infostealer — Microsoft](https://www.microsoft.com/en-us/security/blog/2025/05/21/lumma-stealer-breaking-down-the-delivery-techniques-and-capabilities-of-a-prolific-infostealer/) — 破解/盗版软件作为 infostealer 分发渠道
