---
title: "点一下\u201C分享\u201D,你就发布了:Claude 对话是怎么进 Google 搜索的"
description: "病历、孩子的电话、加密货币钱包密钥,都能在 Google 里搜到。还原 Claude 分享链接进入搜索索引的完整链条:这是同一个设计盲点三年里第五次出事。"
pubDate: 2026-08-04
tags: [privacy, trust-and-safety]
lang: zh
slug: claude-share-links-google-indexed
translationOf: claude-share-links-google-indexed
---

7 月 25 日,周六,有 Reddit 用户在 Google 里输入了一个再普通不过的检索指令:`site:claude.ai/share`。返回的是数以百计陌生人的 Claude 对话和 Artifacts([VentureBeat](https://venturebeat.com/technology/uh-oh-some-claude-shared-conversations-and-artifacts-appear-to-be-indexed-and-publicly-accessible-on-google-search))。7 月 27 日 [404 Media](https://www.404media.co/tons-of-peoples-claude-chats-and-creations-are-exposed-on-google/) 跟进报道,里面翻出来的东西包括:带患者姓名的病历和临床试验结果、孩子的姓名和电话号码、公司内部文件、员工绩效评估、加密货币钱包密钥,还有按使用政策本不该产出的色情对话([TechCrunch](https://techcrunch.com/2026/07/27/psa-your-claude-shared-chats-and-artifacts-may-have-ended-up-on-google/)、[Malwarebytes](https://www.malwarebytes.com/blog/privacy/2026/07/shared-claude-chats-were-searchable-on-google))。

报道发出当天下午,TechCrunch 复测时 Google 上的结果已被清空;据 Malwarebytes 转述,Wired 发现 Bing 上还残留着一部分。

Anthropic 发言人 Amie Rotherham 对 TechCrunch 的回应是:这些分享链接无法被猜出,除非用户自己把它们传播出去,否则不会被人发现;当有人分享一段对话,就是在把内容公开,和其他公开网页一样,它可能被第三方服务存档。

这话字面上都对。问题在于"分享"这两个字,用户理解的和产品实现的是两回事。

## "分享"到底做了什么

按 [Anthropic 官方帮助文档](https://support.claude.com/en/articles/10593882-share-and-unshare-chats),点击分享按钮后,系统为当前对话生成一个快照页面,任何拿到链接的人都能查看;之后新增的消息不会同步,除非重新分享。撤销的入口在 Settings > Privacy > Shared chats,那里能看到自己所有分享过的对话。

文档里有个细节值得对照:Team 和 Enterprise 版的分享只对同组织成员开放。企业客户的分享被当成权限问题处理,消费者版没有这一层。

还有一件事我专门核对过:截至 8 月 4 日,这份文档从头到尾没有一处提到搜索引擎,也没提第三方存档。用户能读到的全部承诺,是"有链接的人可以查看"。

## 从一次点击到 Google 结果,中间发生了什么

链条第一环是"有链接才能看"这个模型本身。不可猜测的长 URL 在安全设计里叫 capability URL:链接即凭证,拿到就能访问。它成立的前提是链接不流动。但链接天然会流动——贴进 Reddit 帖子、群聊、邮件,被聊天软件抓去生成预览卡片,被存档服务收录。只要在任何公开角落出现过一次,搜索引擎的爬虫就能顺着找过来。

已证实的泄露通道,是用户自己把链接贴到了公开场合。但这里有一处未解的争议:去年 9 月的那次事故([Forbes](https://www.forbes.com/sites/iainmartin/2025/09/08/hundreds-of-anthropic-chatbot-transcripts-showed-up-in-google-search/),当时 Google 收录了近 600 条 Claude 对话,包括 Anthropic 自家团队的内部 prompt 和员工姓名邮箱)里,至少有一名用户告诉 Forbes,自己那条工作对话的链接从没在任何地方公开贴过。链接到底怎么泄露的,双方各执一词。

第二环出在防堵的手法上。要看懂这一步哪里出了错,得先把 Google 搜索的运作方式从头讲一遍,假设你完全没接触过这套机制。

你在 Google 搜索时,Google 并不是当场跑遍全网找答案,而是在翻一本它提前编好的巨大地址簿:哪个网址是什么内容,提前登记在册,搜索就是查册。为了编这本地址簿,Google 派出一个自动程序(俗称"爬虫")在网上挨家挨户串门:顺着网页之间的链接访问一个个页面,把内容读下来。

关键的一点是,"上门读过内容"和"被登记进地址簿"是两件事。只要某个网址在别的公开网页上被链接过,Google 就知道了它的存在,可以直接把这个网址登记进地址簿,哪怕爬虫从没读过这个页面。这时搜索结果里出现的是一条没有摘要的链接,但链接照样能点开。

网站手里有两个工具,管的环节不一样:

- robots.txt 是贴在大门口的告示,写着"爬虫请勿入内"。正规爬虫看到会照办,不进门读内容。但它管不了地址簿:Google 从别的网页知道了这个网址,照样可以登记。
- noindex 是写在房间里面的纸条,意思是"请不要把本页登记进地址簿"。Google 读到这行字,才会把这个页面排除在搜索结果之外。而它写在页面内部,爬虫必须进门才看得到。

2025 年那次事故后,Anthropic 的补救是"不向搜索引擎提供分享对话的目录或 sitemap,并主动阻止爬虫抓取本站"(Forbes),也就是选了第一个工具:在门口贴告示。把上面两条放在一起,问题就出来了:告示把爬虫挡在门外,爬虫永远看不到屋里那张 noindex 纸条;而光靠门口的告示,又拦不住网址被登记进地址簿。想加一道防线,结果让真正管用的那道防线失效了。这不是我的推断,[Google 官方文档](https://developers.google.com/search/docs/crawling-indexing/block-indexing)专门警告过这种用法:想让 noindex 生效,页面就不能被 robots.txt 挡住。

所以正确的修法是反过来:把门打开(允许爬虫抓取),同时在每个分享页面里写上 noindex 纸条。我 8 月 4 日抓取了 [claude.ai 当前的 robots.txt](https://claude.ai/robots.txt):/chat/、/settings 等路径都在"请勿入内"清单里,唯独 /share 不在,爬虫可以进门。这和正确修法的前一半对得上。后一半,也就是分享页面里有没有那行 noindex,我手头本来没有现成的分享链接,于是当天自己新建了一条来验证:抓取这个分享页的源码,head 里确实写着 `<meta name="robots" content="noindex, nofollow">`。两半都对上了:截至 8 月 4 日,Claude 分享页挡收录的方式,已经是 Google 文档说的正确做法。

## 第五次了

同样的事故,行业里数得出来的至少五次。

2023 年 9 月,SEO 顾问 Gagan Ghotra 发现 Google 收录了 Bard 的分享对话([Gigazine](https://gigazine.net/gsc_news/en/20230928-google-bard-share-conversations-index/))。Google 搜索联络官 Danny Sullivan 回应"我们无意让这些分享对话被收录,正在屏蔽",之后补上了 robots.txt 规则。

2025 年夏天轮到 ChatGPT。那次用户至少明确勾选过一个"让这条对话可被发现"的选框,但 Fast Company 仍检索到超过 4500 条被收录的对话,里面有简历,也有情感倾诉([Tech Digest](https://www.techdigest.tv/2025/08/openai-disables-chat-discoverability-after-private-conversations-found-in-google-search.html))。OpenAI 首席信息安全官 Dane Stuckey 8 月 1 日宣布砍掉整个功能:"这个功能给了用户太多机会,去不小心分享他们本不想分享的东西"([Malwarebytes](https://www.malwarebytes.com/blog/news/2025/08/openai-kills-short-lived-experiment-where-chatgpt-chats-could-be-found-on-google))。

2025 年 8 月,Grok。[Forbes](https://www.forbes.com/sites/iainmartin/2025/08/20/elon-musks-xai-published-hundreds-of-thousands-of-grok-chatbot-conversations/) 报道约 37 万条对话被 Google 收录:分享按钮直接生成公开页面,用户没有收到任何提示,泄露内容包括密码和用药咨询,连用户上传的图片和表格都能顺着分享页拿到。

再加上 Claude 的 2025 年 9 月和这一次。四家公司,四种实现,从 Grok 的一声不吭到 ChatGPT 的明确勾选框,结果殊途同归。勾选框也没能救 ChatGPT,因为用户不知道"可被发现"意味着什么。Meta AI 的 Discover 信息流则是另一个变体:把公开直接做成了产品形态(Malwarebytes)。

## 盲点在哪

用户点分享时的心理模型是"把这个结果发给某个人看",产品实现是"生成一个永久公开的网页"。这中间差着一整个出版动作。普通网页是作者写给公众的;聊天记录不一样,人对着聊天框说的话接近自言自语,病史、财务、情绪都在里面。我在 7 月 23 日写过[《病历交给 ChatGPT 的那一刻,HIPAA 的保护就结束了》](/zh/chatgpt-health-hipaa-gap):数据交给聊天机器人,就离开了医疗隐私法的覆盖范围。这次的事故是同一件事的另一面,数据不但出了监管边界,还直接进了搜索索引。

做信任与安全工作有一条老经验:用户不读文档,唯一有效的告知位置是动作发生的那一刻。分享弹窗里写不写"这是一个公开网页,可能被搜索引擎和存档服务收录",直接决定用户按不按下去。目前 Anthropic 连帮助文档里都没有这句话。

还有一个多数人想不到的点:撤销分享只能阻止后续访问,撤不回已经被存档的副本。Anthropic 自己的声明也承认公开内容"可能被第三方服务存档"。archive 类服务抓走的快照,不归任何一家 AI 公司管。

## 判断

给用户的三条:

- 把每一个分享链接当成公开发表。发出去之前问自己:这段内容登在博客上我接受吗?
- 现在去 Settings > Privacy > Shared chats 过一遍历史分享,不需要的撤掉。撤销挡不住已存档的副本,但能挡住之后的访问。
- 真正敏感的东西不进对话。钱包密钥这类内容,不该出现在任何云端聊天框里,分不分享都一样。

给做产品的人:阻止收录靠 noindex,别靠 robots.txt,两者的区别 Google 文档写了很多年;"公开网页、可能被搜索引擎收录"这句话应该放进分享弹窗,而不是藏在帮助中心;给用户一个集中管理已分享内容的页面,Anthropic 这一点做了,值得肯定。

最后的判断:Anthropic 只是最新一家。同一个设计决定,把"分享"实现成"发布"却不把话说透,三年里第五次出事。只要分享按钮生成的还是永久公开 URL,而弹窗文案还停留在"有链接的人可以查看",下一次上新闻的只是换一个 logo。

## 参考来源

- [404 Media: Tons of People's Claude Chats and Creations Are Exposed on Google](https://www.404media.co/tons-of-peoples-claude-chats-and-creations-are-exposed-on-google/) — 原始披露报道(正文有付费墙,事实经 TechCrunch、Malwarebytes 交叉核对)
- [TechCrunch: PSA: Your Claude shared chats and Artifacts may have ended up on Google](https://techcrunch.com/2026/07/27/psa-your-claude-shared-chats-and-artifacts-may-have-ended-up-on-google/) — 时间线、曝光内容清单、Anthropic 发言人 Amie Rotherham 声明、Google 结果清除时间
- [VentureBeat: Some Claude shared conversations and Artifacts appear to be indexed on Google Search](https://venturebeat.com/technology/uh-oh-some-claude-shared-conversations-and-artifacts-appear-to-be-indexed-and-publicly-accessible-on-google-search) — 7 月 25 日 Reddit 发现、收录规模"数以百计"
- [Malwarebytes: Shared Claude chats were searchable on Google](https://www.malwarebytes.com/blog/privacy/2026/07/shared-claude-chats-were-searchable-on-google) — 曝光内容、Bing 残留(转述 Wired)、Meta AI 对比、用户自查路径
- [Anthropic 帮助文档: Share and unshare chats](https://support.claude.com/en/articles/10593882-share-and-unshare-chats) — 分享功能机制、快照逻辑、撤销路径、Team/Enterprise 差异;已核实文档未提及搜索引擎
- [Forbes (2025-09-08): Hundreds Of Anthropic Chatbot Transcripts Showed Up In Google Search](https://www.forbes.com/sites/iainmartin/2025/09/08/hundreds-of-anthropic-chatbot-transcripts-showed-up-in-google-search/) — 2025 年近 600 条收录事故、Anthropic robots.txt 说法、用户否认公开贴过链接
- [Google Search Central: Block Search indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing) — robots.txt 与 noindex 的互斥机制
- [claude.ai/robots.txt](https://claude.ai/robots.txt) — 本人 2026-08-04 抓取,确认 /share 无屏蔽规则
- [Gigazine: Bard shared conversations indexed by Google Search](https://gigazine.net/gsc_news/en/20230928-google-bard-share-conversations-index/) — Bard 2023 事故、Gagan Ghotra、Danny Sullivan 回应
- [Tech Digest: OpenAI disables chat discoverability](https://www.techdigest.tv/2025/08/openai-disables-chat-discoverability-after-private-conversations-found-in-google-search.html) — ChatGPT 4500+ 条(Fast Company 统计)、"Make this chat discoverable"勾选框
- [Malwarebytes (2025-08): OpenAI kills "short-lived experiment"](https://www.malwarebytes.com/blog/news/2025/08/openai-kills-short-lived-experiment-where-chatgpt-chats-could-be-found-on-google) — Dane Stuckey 声明原文、8 月 1 日下线时间
- [Forbes (2025-08-20): Elon Musk's xAI Published Hundreds Of Thousands Of Grok Chatbot Conversations](https://www.forbes.com/sites/iainmartin/2025/08/20/elon-musks-xai-published-hundreds-of-thousands-of-grok-chatbot-conversations/) — Grok 约 37 万条、无提示发布、上传文件可访问

<!-- 核查点(仅供 PR 审核,不渲染进正文):noindex 已于 2026-08-04(美西)验证。作者新建的分享链接 https://claude.ai/share/7a6dda9a-abb0-4d9f-81a8-6bd3f663587f,经代理取得未渲染的原始 HTML(HTTP 200),head 内含 <meta name="robots" content="noindex, nofollow">;并已确认抓到的是 Claude 应用页本身(资源加载自 assets-proxy.anthropic.com、og:description 为 "Shared via Claude"),而非 Cloudflare 拦截页(拦截页也带 noindex,故做了此项排除)。 -->
