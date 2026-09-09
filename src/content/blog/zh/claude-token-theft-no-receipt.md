---
title: "你没在用 Claude，额度却在掉：一场没有账单的盗刷"
description: "infostealer 偷走的不是密码，是你已登录的会话。拆解 Claude 订阅额度盗用的攻击链，以及为什么这类盗刷比信用卡盗刷更难被发现。"
pubDate: 2026-09-08
tags: [ai-security, account-security, infostealer]
lang: zh
slug: claude-token-theft-no-receipt
translationOf: claude-token-theft-no-receipt
---

8 月 4 日，英国东萨塞克斯的独立 AI 顾问 Grant De Swardt 注意到一件小事：他没在干活，Claude 的用量条却从 45% 涨到了 55%（[TechCrunch](https://techcrunch.com/2026/09/08/hackers-are-stealing-claude-tokens-from-subscribers/)）。他订的是每月 200 美元的 Max 档。不久后 Anthropic 暂停了他的账户、作废了所有会话，退了 44.49 英镑，并告诉他：有人拿着他的登录会话在替他「用」Claude。

他不是个例。Reddit 上的相关帖子聚集了大量同样遭遇的用户：有人的用量在 12 分钟内从 0 冲到 49%；有人连续三天额度被烧光；还有人的账户在本人不知情的情况下被升级到了更贵的档位并扣了费。Anthropic 随后向受影响用户发邮件确认：「我们最近发现一个恶意行为者，正在用常见的 infostealer 恶意软件从用户电脑上窃取 Claude 登录会话，再用这些会话访问账户、消耗用量。」（[BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-warns-infostealer-malware-is-hijacking-claude-sessions-to-drain-usage/)）

这件事最值得拆的地方不在「账号被盗」本身。账号被盗是老故事。新的是被偷的东西：不是信用卡号，不是密码，而是一种预付费的计算额度。这类资产没有账单、没有明细、没有银行风控替你盯着。它被偷了，你多半不知道。

## 被偷的不是密码，是「已经登录」这个状态

先把机制讲清楚，假设你完全没有安全背景。

你登录 Claude 时要输密码，可能还要过两步验证（2FA），比如手机收个验证码。这相当于在大门口查身份证。查完之后，网站不会每次操作都重新查一遍，而是在你的浏览器里存一小段数据，叫会话 cookie（session cookie），相当于查验后发给你的手环：接下来你每次请求，只要出示手环，网站就认定「这是刚才那个人」。

infostealer（信息窃取类恶意软件）干的事，就是潜入你的电脑，把浏览器里存的手环整个复制走。攻击者拿到手环后，不需要你的密码，也不需要过两步验证，因为在网站看来，他就是「已经登录的你」。这就是为什么此类攻击能绕过 2FA：2FA 守的是大门，而攻击者是直接从你口袋里摸走了手环。根据 Anthropic 发给用户的邮件，这次涉及的都是安全圈的老面孔：Windows 上的 Vidar、LummaC2、StealC、RedLine、Acreed，以及少量 Mac 用户中招的 Atomic Stealer（[Search Engine Journal](https://www.searchenginejournal.com/anthropic-warns-hackers-are-stealing-claude-sessions-to-hijack-accounts/587566/)）。感染途径也是老一套：Reddit 上有受害者承认，中招前下过盗版游戏（[Malwarebytes](https://www.malwarebytes.com/blog/news/2026/09/infostealers-are-hijacking-claude-accounts-at-users-expense/)）。

攻击链还有关键一步。据 TechCrunch 报道，被盗的 Claude 会话密钥被用来「铸造未经授权的 Claude Code OAuth token」。翻译一下：浏览器会话是短效凭证，随时可能过期；但攻击者可以拿它去给 Claude Code（Anthropic 的编程 agent 工具）签发程序化访问凭证。这一步把「临时手环」升级成了「可以写进脚本里反复用的钥匙」，让盗刷可以自动化、批量化地跑，而不用人守着一个浏览器窗口。12 分钟烧掉 49% 额度这种速度，靠人手动聊天是聊不出来的，只有脚本化地跑 agent 任务才做得到。

## 为什么受害者几乎不可能自己发现

把这次盗刷和传统信用卡盗刷对比，差别立刻出来。

信用卡被盗刷，你有三层保护：银行风控会拦截异常交易；月底账单上每一笔消费都有商户名和金额；发现问题还能拒付（chargeback）把钱追回来。这套体系是几十年欺诈损失堆出来的。

订阅制 AI 额度被盗刷，三层全部不存在。第一，攻击者不产生任何新的扣费。钱你早就付了，他消耗的是预付额度，银行侧从头到尾看不到任何异常交易，风控无从谈起。第二，没有明细。Claude 订阅用户能看到的只有一根用量百分比条，看不到「几点几分、哪个会话、跑了什么任务、烧了多少」。De Swardt 之所以发现，纯粹因为他碰巧在没干活的时候盯了一眼用量条；一个每天把额度用到七八成的重度用户，被人蹭走两三成额度，大概率永远不会察觉。他对 TechCrunch 说得直白：没有逐项的用量明细，「这些人没有办法保护自己」。第三，token 烧掉就是烧掉了，算力是即时消费品，不存在拒付。

Anthropic 的检测倒是起了作用：是它主动发现异常、登出用户、发的邮件。但当 TechCrunch 问及用户自己该怎么识别滥用时，Anthropic 拒绝置评。平台看得到的，用户看不到。这个信息差就是当前订阅制 AI 产品安全模型的最大缺口。

至于攻击者偷额度干什么，Anthropic 和各家报道都没有点明，这一点我只能按机制推演，无法验证。最顺的变现路径有两条：一是转售，市面上一直存在倒卖各类 AI 订阅访问权的灰色服务，偷来的额度是零成本货源；二是自用，跑爬虫清洗、批量内容生成这类本来要花 API 钱的负载。infostealer 偷来的凭证历来是按「日志包」在黑市批量出售的，Claude 会话大概率只是包里新添的一个值钱字段。

还有一个细节值得如实记下：De Swardt 说他扫描后没有在自己电脑上找到任何感染证据。Anthropic 的邮件里也提到另一种可能：账户连接了未经授权的外部服务。也就是说，具体到每个受害者，会话到底是被本机恶意软件偷走、还是从某个第三方工具泄漏的，并没有逐一坐实。这次事件的整体归因（infostealer）来自 Anthropic，但个案层面存在没对上的地方。

## 你现在该做什么

如果你是 Claude 订阅用户（或任何 AI 订阅产品的用户），有几个动作值得今天就做：

**先杀毒，再改密码。顺序不能反。** 这是 Anthropic 邮件里反复强调的点：登出只能作废已被偷走的会话，杀不掉电脑里的恶意软件。如果 infostealer 还在，你改的新密码、新登录的会话会立刻再次被偷。先用杀毒软件全盘扫描并清除，确认干净后再改密码、重新登录。

**检查活跃会话。** Claude 设置里可以查看所有已登录的设备和浏览器（[官方指引](https://support.claude.com/en/articles/13124001-managing-your-active-sessions)），看到不认识的位置或设备，立即终止。

**盯用量条的两个异常信号。** Anthropic 邮件里给出的典型症状是：额度看起来「回满了，然后在你没用的时候掉下去」。另一个信号是你明明没干活、用量却在涨。养成偶尔在空闲时瞄一眼的习惯，目前这是用户侧唯一的检测手段。

**把邮箱当成同等重要的阵地。** 你的 Claude 账户挂在邮箱上，邮箱失守等于全部失守。改邮箱密码、登出其他设备、开启两步验证。Malwarebytes 还建议：确认电脑干净之前，先把账户里保存的支付方式删掉（Anthropic 这次也替受影响用户移除了保存的支付方式），发现持续异常可以联系 usersafety@anthropic.com。

**别碰盗版和破解工具。** 这轮受害者里已确认的感染源就是盗版游戏。infostealer 最主要的分发渠道从来都是「免费的付费软件」。

最后说个判断。订阅制 AI 额度正在变成一种真实的、可被盗窃的资产类别，但围绕它的安全基础设施还停留在「一根百分比条」的水平。信用卡体系用几十年学会了给用户逐笔明细和拒付权，AI 订阅平台迟早也要走到这一步：逐会话的用量日志、异常消耗告警、可撤销的细粒度凭证。在那之前，用户侧能做的只有上面这些，而平台侧欠的账，De Swardt 那句「这些人没有办法保护自己」已经说清了。他后来换去了 Cursor。用户不一定会为安全事故本身离开，但一定会为「出了事却什么都看不到」离开。

## 参考来源

- [Hackers are stealing Claude tokens from subscribers — TechCrunch](https://techcrunch.com/2026/09/08/hackers-are-stealing-claude-tokens-from-subscribers/) — De Swardt 案例细节（日期、用量变化、退款金额）、session key 铸造 OAuth token 的机制、Reddit 受害者汇总、Anthropic 拒绝置评识别方法
- [Anthropic warns infostealer malware is hijacking Claude sessions to drain usage — BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-warns-infostealer-malware-is-hijacking-claude-sessions-to-drain-usage/) — Anthropic 邮件原文引语、恶意软件家族名单、官方处置措施（登出、移除支付方式、退款）
- [Infostealers are hijacking Claude accounts at users' expense — Malwarebytes](https://www.malwarebytes.com/blog/news/2026/09/infostealers-are-hijacking-claude-accounts-at-users-expense/) — 用户防护步骤顺序（先杀毒再改密码）、usersafety@anthropic.com 联系渠道、盗版游戏感染源案例
- [Anthropic Warns Hackers Are Stealing Claude Sessions To Hijack Accounts — Search Engine Journal](https://www.searchenginejournal.com/anthropic-warns-hackers-are-stealing-claude-sessions-to-hijack-accounts/587566/) — 确认 Anthropic 声明出自发给用户的邮件（经 Reddit 流出）而非公开公告、恶意软件家族名单交叉印证
- [Managing your active sessions — Claude Help Center](https://support.claude.com/en/articles/13124001-managing-your-active-sessions) — 活跃会话管理的官方指引
