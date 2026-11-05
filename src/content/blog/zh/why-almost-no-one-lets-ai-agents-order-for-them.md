---
title: "Uber 一周只有 4 单 agent 叫车，先看这 4 单是怎么数出来的"
description: "DoorDash 和 Uber 先后在财报会上说外部 AI agent 只带来了几百单。但两家平台已经把 ChatGPT 里的订单引回自家 App 结账，还在和 agent 厂商谈接入条件。这个数字测的是平台自己设的窄口，不能直接读成用户不要 agent。"
pubDate: 2026-11-04
tags: [ai-agents, agentic-commerce]
lang: zh
slug: why-almost-no-one-lets-ai-agents-order-for-them
translationOf: why-almost-no-one-lets-ai-agents-order-for-them
---

11 月 4 日的 Uber 三季度财报电话会上，CFO Balaji Krishnamurthy 报了一组数字。万圣节那周是 Uber 今年单量最大的几周之一，Uber 和 Uber Eats 一共做了大约 3.2 亿单。其中由 AI agent 下的 Uber Eats 订单约 500 单，叫车只有 4 单（[电话会记录](https://www.fool.com/earnings/call-transcripts/2026/11/04/uber-uber-q3-2026-earnings-call-transcript/)）。

10 月底 DoorDash 的财报会上，CEO Tony Xu 给出的说法是："maybe several hundred orders in total from some of these third-party agents"，点名了 Muse、Instinct、Fo 等外部 agent（[TechCrunch](https://techcrunch.com/2026/10/30/doordash-said-its-only-received-several-hundred-orders-from-ai-agents/)）。DoorDash 同一季度的总单量是 9.93 亿（[财报新闻稿](https://www.sec.gov/Archives/edgar/data/0001792789/000179278926000062/proddashex991-pressrelease.htm)）。

两家公司、两个数字，量级一致，很容易得出一个结论：用户根本不想让 agent 替自己下单。我认为这个结论下得太早。这两个数字测的范围，是两家平台自己划定的。

## 订单被引回了自家 App

用户今天最可能接触到的"agent 下单"入口是 ChatGPT 里的应用。可是这个入口里，两家都没让 agent 走完最后一步。

Uber 帮助中心写得很直白：叫车可以在 ChatGPT 里规划行程，"then complete the ride request and payment process in the Uber app"（[Uber 帮助页](https://help.uber.com/en/riders/article/chatgpt-integration-for-rides?nodeId=afa53c91-a8e0-4306-b18f-9f742bf24252)）。Uber Eats 更严，ChatGPT 里只能看餐厅和菜单，选了菜就跳转到 Uber Eats 结账（[Uber Eats 帮助页](https://help.uber.com/ubereats/restaurants/article/chatgpt-integration-for-eaters?nodeId=7e56650b-9482-4a55-a560-1902ba2dd70e)）。DoorDash 2025 年 12 月上线的 ChatGPT 应用只做杂货，购物车在对话里生成，结账要"open your cart in the DoorDash app"（[DoorDash 公告](https://about.doordash.com/en-us/news/openai)）。

也就是说，一个用户在 ChatGPT 里说"帮我叫车去机场"，最后是在 Uber App 里点的确认、付的钱。这一单算不算"agent 订单"？两家都没在电话会上交代统计口径。CFO 的原话是"fulfilled from agents"，Xu 说的是"third-party agents"，加上他点名的都是 Muse、Instinct 这类独立 agent，我倾向于认为统计的是由外部 agent 直接完成下单的那部分，但这一点我没能验证。

如果这个推测成立，那么能被计入的订单有一个前提：用户已经把账户和付款权交给了一个外部 agent。而平台自己的主力集成恰恰把付款权留在了自家 App 里。这个数字很小，原因之一就是计入它的条件本来就窄。

## 接入条件还在谈

第二个原因是供给侧。Dara Khosrowshahi 在电话会上说，每一家 AI 公司都在找 Uber 谈，市面上已有 8 个主要 AI 助手，以后会超过 10 个，"we are really now negotiating the terms of trade"。他还说，直接的用户关系是 Uber AI 策略的核心，Uber 不想依赖任何一个渠道方。他之前在旅游行业（Expedia）待了多年，那个行业的流量入口长期握在 Google 这类搜索平台手里，他的原话是"I do not wanna go back there"。

DoorDash 的做法方向一致。它这一年接连推出了自己的 agent：6 月的 Ask DoorDash 对话下单，7 月的命令行工具，9 月可以发短信下单的 agent。对外开放的 MCP 接口（一种让外部 AI 工具调用服务的开放协议）目前是限量测试，只面向企业给员工订餐（[DoorDash 公告](https://about.doordash.com/en-us/news/doordash-ordering-connector)）。

把这两件事放在一起看：一个外部 agent 想替普通消费者在 Uber 或 DoorDash 下单，眼下还没有一条正式谈妥、面向消费者的通道。在这种条件下出现几百单，说明的是平台还没开门，用户想不想用，这个数字回答不了。

还有一层是我的推测：两位 CEO 在谈判期公开强调"几乎没人用"，对谈判本身也有用。等于告诉对方，你目前给我带不来什么量，条件不能开太高。

## agent 确实省不了多少时间

第三个解释来自需求侧，而且有一定道理。Khosrowshahi 给了两个时间：在 App 里叫一次车平均约 50 秒，在 Uber Eats 里重复下一单常点的外卖，中位数约 90 秒。

叫车是高频、目标明确、选项很少的任务。起点终点定了，剩下的只是选车型。对这种任务，agent 能省下的时间很有限，还多了一个风险：它理解错了怎么办。替你付钱的 agent 只要出一次错，比如叫错地址、点错菜，损失就落在用户身上，而 50 秒的 App 流程几乎不会出这种错。

不过这个论据由最有动机说"用户不需要外部 agent"的一方提出，只能当一方说法看。另外它只覆盖"重复下单"这一类场景。DoorDash 给自家短信 agent 宣传的卖点，是一单里同时满足多人不同忌口的团餐（[TechCrunch](https://techcrunch.com/2026/09/30/doordash-launches-an-ai-agent-you-can-text-to-order-food/)）。平台自己也清楚，agent 的价值在模糊、多约束的任务上，不在"再来一单"。

## 这组数字该怎么用

对做 agent 产品的人，这两个数字既不能证明需求不存在，也不能当作"市场还很早、空间巨大"的论据。它测的是外部 agent 在没有正式接入协议、付款权被平台留在自家 App 的条件下，从夹缝里走完全流程的单量。真正有参考价值的数字是 ChatGPT 里发起、跳转回 App 后完成的订单量，以及跳转环节流失了多少。两家都没公布。

对考虑把付款权交给 agent 的用户，现在的产品设计其实已经替你做了选择：主流集成里，最后确认付款的还是你自己。

接下来几个季度值得看的，不只是这个数字涨了多少。更要看的是两家怎么定义它：如果 Uber 和某家 AI 助手谈妥条件，或者 DoorDash 开始把自家短信 agent 的单量单独报出来，那时 agent 订单的口径大概率会改。数字突然变大，很可能只是口径变了，用户行为未必变了多少。

## 参考来源

- [Almost no one uses AI agents to book their Uber, company says（TechCrunch）](https://techcrunch.com/2026/11/04/almost-no-one-uses-ai-agents-to-book-their-uber-company-says/) — 选题来源，Uber 数字的背景
- [Uber Q3 2026 earnings call transcript（Motley Fool）](https://www.fool.com/earnings/call-transcripts/2026/11/04/uber-uber-q3-2026-earnings-call-transcript/) — 3.2 亿单、500 单、4 单、50/90 秒、"terms of trade"、不依赖单一渠道、旅游行业经历
- [DoorDash said it's only received 'several hundred' orders from AI agents（TechCrunch）](https://techcrunch.com/2026/10/30/doordash-said-its-only-received-several-hundred-orders-from-ai-agents/) — Tony Xu 原话、点名的外部 agent、DoorDash 自有 agent 时间线
- [DoorDash Q3 2026 财报新闻稿（SEC 8-K）](https://www.sec.gov/Archives/edgar/data/0001792789/000179278926000062/proddashex991-pressrelease.htm) — 季度总单量 9.93 亿
- [ChatGPT Integration for Rides（Uber 帮助中心）](https://help.uber.com/en/riders/article/chatgpt-integration-for-rides?nodeId=afa53c91-a8e0-4306-b18f-9f742bf24252) — 叫车在 Uber App 内完成请求和付款
- [ChatGPT Integration for Eaters（Uber 帮助中心）](https://help.uber.com/ubereats/restaurants/article/chatgpt-integration-for-eaters?nodeId=7e56650b-9482-4a55-a560-1902ba2dd70e) — ChatGPT 内只能浏览，下单付款跳转 Uber Eats
- [DoorDash Launches Grocery Shopping App Within ChatGPT（DoorDash）](https://about.doordash.com/en-us/news/openai) — 杂货应用，结账在 DoorDash App
- [DoorDash brings office ordering to the AI tools teams already use（DoorDash）](https://about.doordash.com/en-us/news/doordash-ordering-connector) — MCP 接口限量测试、仅面向企业
- [DoorDash launches an AI agent you can text to order food（TechCrunch）](https://techcrunch.com/2026/09/30/doordash-launches-an-ai-agent-you-can-text-to-order-food/) — 短信 agent 的团餐、忌口场景
