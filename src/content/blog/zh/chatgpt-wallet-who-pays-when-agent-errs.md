---
title: "Face ID 一刷，agent 买错的东西就成了你批准的交易"
description: "ChatGPT Wallet 让 agent 每次付款前都要你做一次生物识别。这一下保住了卡号，也让 agent 出的错更难算作“未授权交易”，争议只能走更窄的路。"
pubDate: 2026-11-13
tags: [ai-agents, agentic-commerce, ai-safety]
lang: zh
slug: chatgpt-wallet-who-pays-when-agent-errs
translationOf: chatgpt-wallet-who-pays-when-agent-errs
---

11 月 13 日，OpenAI 发布 ChatGPT Wallet：它的个人 agent dots 可以替用户付钱了（[OpenAI 公告](https://openai.com/index/introducing-chatgpt-wallet/)，[开发者社区官方帖](https://community.openai.com/t/introducing-chatgpt-wallet/1416044)）。首批只开放给美国 18 岁以上的 ChatGPT Pro 用户，要绑定美国发行的合格银行卡，合作方是 American Express、Mastercard 和 Visa。

我之前写过两篇相关的文章。一篇讲几乎没人愿意让 agent 下单，另一篇讲点了几十万次"允许"之后，人工审批为什么拦不住 agent。Wallet 把这两个问题直接落到了钱上。这次我只想问一件事：agent 买错了东西，或者被网页里藏的指令带偏了，这笔钱最后由谁来承担？

## 批准界面上能看到什么

按公告和多家媒体的描述，付款流程是这样的：卡只需要绑定一次。每次购买前，用户会看到三样东西：商品、总价、这次要扣的那张卡。确认后用 Face ID 或指纹验证，每次批准都会留下一条授权记录（[9to5Mac](https://9to5mac.com/2026/11/13/openai-launches-chatgpt-wallet-enabling-dot-agents-to-make-purchases/)，[PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2026/openai-gives-ai-agents-a-wallet-while-blocking-them-from-seeing-the-card/)）。

批准之后，卡组织发一个"网络令牌"给商家。它是一串替身卡号，有自己的号码、安全码和有效期，钱从你选的那张卡上扣，但商家和 agent 都看不到真实卡号。OpenAI 的开发者文档还规定，这次授权只对这一笔交易有效，商家不能把令牌存下来另作他用（[Accept payments 文档](https://developers.openai.com/commerce/guides/accept-payments)）。

这个设计解决了一个具体问题：agent 泄露卡号。dots 每个都跑在自己的云端电脑上，带一个浏览器（[TechCrunch](https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/)），会访问大量陌生网页。卡号不进 agent 的上下文，网页里的恶意指令就没法骗它把卡号念出来。

它解决不了的是另一个问题：agent 带着你去买了你本来不该买的东西。

## 三个场景，三种结局

公告对争议规则只有一句：Wallet "不影响卡片对合格争议（eligible disputes）的保护"。关键在"合格"两个字上。美国法律把银行卡争议分成几类，保护力度差别很大。

**场景一：尺码买错了。** 你让 dot 买双跑鞋，它选了 42 码，你在批准界面上没细看就刷了脸。商品、总价都显示过，你也批准了。按信用卡的 Regulation Z，"未授权使用"指的是没有实际、默示或表见授权的人刷了你的卡（[12 CFR 1026.12](https://www.consumerfinance.gov/rules-policy/regulations/1026/12/)）。这一单显然不算。商家按订单发了货，也不构成"账单错误"。剩下的只有商家自己的退货政策。

**场景二：被带到了假商店。** dot 比价时读到一个页面，页面里藏着指令，把它引到一家山寨网店。你看到的商品名和价格都正常，于是刷了脸，货却一直没到。这时候走"未授权"这条路基本没希望：授权记录里有你的生物识别验证。能走的是另一条。Regulation Z 把"未按约定交付"的商品列为账单错误，持卡人在收到第一份含这笔交易的账单后 60 天内书面通知发卡行即可，不必先找商家（[12 CFR 1026.13](https://www.consumerfinance.gov/rules-policy/regulations/1026/13/)）。

换成借记卡，情况就不同了。借记卡受 Regulation E 管，它的"错误"清单包括未授权转账、金额不对、记账错误等，没有"货没送到"这一项（[12 CFR 1005.11](https://www.consumerfinance.gov/rules-policy/regulations/1005/11/)）。这种情况能不能追回钱，要看发卡行和卡组织自己的规则。法律本身不兜底。

**场景三：货到了，是假货。** 你已经签收，属于质量争议。1026.13 明确把已接受商品的质量问题排除在账单错误之外。另一条路是 1026.12(c) 的"索赔与抗辩"，但它要求你先真诚地和商家协商，金额超过 50 美元，交易地还要在你所在的州或 100 英里以内。面对一家山寨网店，这几个条件都不好满足。

## 生物识别把风险挪到了哪里

三个场景放在一起看，规律很清楚。在美国卡片保护体系里，"未授权交易"受到的保护最强：信用卡持卡人最多承担 50 美元。"授权了但出了问题"那一类，保护就窄得多，还很看卡种。

Wallet 的每一次 Face ID 加一条记录，正是把交易稳稳放进"已授权"这一类。这样设计有商业上的理由：商家的风控系统得相信这笔单是真人批准的才肯接单，OpenAI 也在开发者文档里教商家怎么识别合法的 agent 订单。代价落在用户身上：agent 出的错，在法律上会被记成你的决定。

我在上一篇关于审批的文章里讨论过，人在连续点"允许"时会漏掉恶意请求。到了 Wallet 这里，漏看一次的后果变了，你漏看的那一下会作为生物识别签名记录在案。

prompt injection（网页里藏的指令劫持 agent）也不会很快消失。OpenAI 自己在 Atlas 浏览器的安全文章里写过，这是 agent 安全中的一个开放难题，预计还要"持续处理很多年"（[OpenAI](https://openai.com/index/hardening-atlas-against-prompt-injection)）。

## 今天要不要开、怎么用

Wallet 目前只对 Pro 用户开放。公告说以后会加入消费上限、品类规则和时间窗口，让用户可以预先批准 agent 的购买（[Android Authority](https://www.androidauthority.com/chatgpt-wallet-3735154/)）。在这些功能上线之前，额度只能靠卡本身来控制：

- 绑信用卡，不绑借记卡。理由就是上面场景二里 Regulation Z 和 Regulation E 的差别
- 单独用一张额度低的卡，并在发卡行 app 里打开每笔交易提醒
- 批准界面上列的是商品、总价和卡片。刷脸前先让 dot 告诉你商家名和网址，不认识的店就不批
- 留好订单确认邮件。60 天的争议期从账单日开始算，不是从你发现问题那天

照这些做法，我会在熟悉的大商家、金额不大的订单上用它。陌生网店、大额订单，还是自己去结账。

最值得看的是预批准功能上线的那一天。到那时，每笔交易的刷脸确认没了，agent 在你设定的规则内买了一件你并不想要的东西，算不算"授权"？Regulation Z 说，有没有授权由州法或其他适用法律来判断。OpenAI 和发卡行如果在推出预批准之前公布这类交易的争议规则，用户才知道自己预先签下的到底是什么。

## 参考来源

- [Introducing ChatGPT Wallet（OpenAI）](https://openai.com/index/introducing-chatgpt-wallet/) — 发布日期、适用范围、合作卡组织、争议保护表述
- [Introducing ChatGPT Wallet（OpenAI 开发者社区官方帖）](https://community.openai.com/t/introducing-chatgpt-wallet/1416044) — 首发经由 dots、Pro 美国用户、每笔安全验证、卡片保护表述
- [Accept payments（OpenAI 开发者文档）](https://developers.openai.com/commerce/guides/accept-payments) — 网络令牌、单笔授权、禁止复用凭证、风控信号
- [9to5Mac](https://9to5mac.com/2026/11/13/openai-launches-chatgpt-wallet-enabling-dot-agents-to-make-purchases/) — 批准界面显示内容、生物识别、授权记录、令牌机制
- [PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2026/openai-gives-ai-agents-a-wallet-while-blocking-them-from-seeing-the-card/) — 18 岁以上、美国发行卡片、未来完全委托的规划
- [Android Authority](https://www.androidauthority.com/chatgpt-wallet-3735154/) — 计划中的消费上限、品类与时间窗口预批准
- [TechCrunch：OpenAI launches dots](https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/) — dots 的发布背景
- [Hardening Atlas against prompt injection（OpenAI）](https://openai.com/index/hardening-atlas-against-prompt-injection) — prompt injection 是长期开放难题
- [12 CFR 1026.12（CFPB）](https://www.consumerfinance.gov/rules-policy/regulations/1026/12/) — 未授权使用定义、50 美元上限、索赔与抗辩条件
- [12 CFR 1026.13（CFPB）](https://www.consumerfinance.gov/rules-policy/regulations/1026/13/) — "未按约定交付"属于账单错误、排除质量争议、60 天通知期
- [12 CFR 1005.11（CFPB）](https://www.consumerfinance.gov/rules-policy/regulations/1005/11/) — 借记卡错误清单的范围
