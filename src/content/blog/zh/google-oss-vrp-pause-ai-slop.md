---
title: "AI 没有攻破 Google,但挤爆了它的收件箱"
description: "Google 暂停开源漏洞赏金:AI 把写一份像样的漏洞报告的成本压到接近零,验证成本却一分没降。这道不对称的算术题,正在拆负责任披露的地基。"
pubDate: 2026-10-04
tags: [ai-security, open-source, bug-bounty]
lang: zh
slug: google-oss-vrp-pause-ai-slop
translationOf: google-oss-vrp-pause-ai-slop
---

10 月 1 日,Google 安全团队[在 X 上公告](https://x.com/GoogleVRP/status/2105689195180179605):开源软件漏洞赏金计划(OSS VRP,即 Google 付钱奖励外部研究者报告其开源项目安全漏洞的项目)暂停接受产品漏洞提交。原因只有一句话:「自动化提交显著增加,其中绝大多数是无效的」([TechCrunch](https://techcrunch.com/2026/10/04/google-froze-its-open-source-bug-bounty-program-due-to-a-significant-rise-in-ai-submissions/) 转引官方说明)。供应链类报告和已提交的存量报告不受影响,新方案要等到 2027 年一季度才有说法。

Google 不是第一个撑不住的。curl 的赏金计划今年 1 月 31 日关闭,运行了近七年,[累计确认 87 个漏洞、发出超过 10 万美元奖金](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/)。维护者 Daniel Stenberg 给出的数据很具体:常年里提交报告的确认率在 15% 以上,2025 年跌到 5% 以下;同年[约 20% 的提交是 AI 生成的垃圾报告](https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/)——幻觉出来的函数、不存在的攻击路径,格式却无可挑剔。

## 一道算术题

赏金计划有一个从没写进规则里的隐含假设:写一份像样的漏洞报告需要真功夫,所以提交量天然有限,信噪比天然有底。

AI 把等式左边清零了。一条 prompt 就能产出带调用栈、带复现步骤、带修复建议的报告,表面专业度和真实发现在初筛时无法区分。等式右边纹丝不动:curl 的安全团队只有 7 个人,每份报告要 3 到 4 人评审,每人花 30 分钟到 3 小时。生成端成本归零,验证端按报告数量线性烧人力,这个剪刀差没有上限。

再叠加彩票结构:curl 对 critical 级漏洞最高赏 1 万美元。只要提交免费,哪怕命中率百分之一,期望收益也是正的。Stenberg 说得直白,关掉赏金的主要目的就是「去掉提交垃圾的激励」。

## 真正坏掉的是信任,不是工作量

负责任披露(研究者发现漏洞后先私下告知厂商、留出修复窗口,再公开)主要靠一个社会契约运转:提交者先自己验证,再去占用维护者的注意力。过去这个契约由成本自动执行,写不出像样报告的人根本到不了维护者面前。现在,报告「看起来可信」不再携带任何关于提交者是否尽职的信息,两个信号彻底脱钩。

反例恰好也来自 curl。2025 年 9 月,研究员 Joshua Rogers 用 AI 扫描工具(ZeroPath 等)向 curl 提交了[约 50 个真实问题](https://www.theregister.com/2025/10/02/curl_project_swamped_with_ai/),Stenberg 公开称赞这批发现「truly awesome」。Google 自己的 Big Sleep agent 同年在 FFmpeg、ImageMagick 等项目里找到 20 个漏洞,还抢在攻击者利用之前发现了 SQLite 的 CVE-2025-6965([Google 官方博客](https://blog.google/innovation-and-ai/technology/safety-security/cybersecurity-updates-summer-2025/));Google 明确说明,Big Sleep 的每份报告在提交前都经人类研究员核实。

同样是 AI 找漏洞,差别只有一个:Rogers 和 Big Sleep 的流程里,报告发出之前有人做了验证,并为结论署名担责。Google 暂停的不是「AI 参与找漏洞」,是「验证成本转嫁给接收方」这种提交模式。

## 修复方向:把验证成本推回提交端

几条路径已经能看到苗头,共同点都是让提交者先付出点什么:

- **可机器验证的证据**。要求报告附上可复现的触发用例或攻击验证代码(PoC),先过自动复现这道闸,人工只看过了闸的。对内存安全类漏洞这条可行性最高,逻辑类漏洞更难自动判定,覆盖不了全部。
- **信誉记账**。提交历史公开,误报率高的账号降权。HackerOne 现有的信誉分是雏形,但新注册账号可以无限重开,信誉清零再来的成本接近于零,挡不住专门薅赏金的小号。
- **分级入口**。有记录的研究者走快速通道,匿名首次提交者进低优先级慢队列。代价是对新人不友好,而赏金计划的历史价值之一恰恰是给了无名研究者入场券。

三条都有真实代价,没有哪条是白捡的。但方向一致:匿名、零门槛、按件付费的提交模式,建立在「写报告很贵」这个已经失效的前提上。

Google 把答案押后到了 2027 年一季度。值得盯住的观察点是:新方案里会不会出现提交前自动复现或信誉门槛这类设计。Google 是少数有能力为此建基础设施的玩家,它给出的方案,大概率会成为整个行业照抄的模板。

## 参考来源

- [Google VRP 官方 X 公告](https://x.com/GoogleVRP/status/2105689195180179605) — 暂停范围(产品漏洞提交暂停、供应链与存量报告不受影响)、替代渠道
- [TechCrunch 报道](https://techcrunch.com/2026/10/04/google-froze-its-open-source-bug-bounty-program-due-to-a-significant-rise-in-ai-submissions/) — 官方解释原文「significant rise in automated submissions」、2027 年一季度更新承诺
- [Daniel Stenberg: The end of the curl bug-bounty](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/) — 关闭日期、87 个确认漏洞、10 万美元累计奖金、确认率 15%→5%、「去掉激励」表述
- [Daniel Stenberg: Death by a thousand slops](https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/) — 2025 年约 20% 提交为 AI slop、7 人团队、每份报告 3-4 人各 30 分钟至 3 小时
- [The Register: Curl project, swamped with AI slop, finds not all AI is bad](https://www.theregister.com/2025/10/02/curl_project_swamped_with_ai/) — Joshua Rogers 用 ZeroPath 等工具提交约 50 个真实问题
- [Google 官方博客:AI 安全进展](https://blog.google/innovation-and-ai/technology/safety-security/cybersecurity-updates-summer-2025/) — Big Sleep 发现 CVE-2025-6965、20 个开源项目漏洞、人工核实流程
