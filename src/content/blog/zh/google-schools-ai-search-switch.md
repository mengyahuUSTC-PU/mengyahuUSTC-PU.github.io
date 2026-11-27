---
title: "Google 早有不带 AI 的搜索，只是没放进学校的开关里"
description: "Google 让 K-12 学校在「开 AI」和「保搜索」之间二选一，可它自家的 Web 筛选早就能只显示链接。症结在管理后台的开关粒度。"
pubDate: 2026-11-04
tags: [ai-in-education, ai-governance, google]
lang: zh
slug: google-schools-ai-search-switch
translationOf: google-schools-ai-search-switch
---

11 月 3 日，Google 教育业务负责人 Chris Phillips 发了一篇博客（[Designing responsible AI for learning](https://blog.google/products-and-platforms/products/education/ai-learning-era-updates-2026/)）。核心一句：Gemini、Gemini Notebook、Gemini in Classroom 和 Google Search，"对 K-12 学生账号将完全关闭，直到学校管理员明确开启"。

单看这句，像是让步。Google 现行的管理员文档写的还是 Gemini in Classroom"对所有年龄段默认开启"（[Workspace 帮助](https://knowledge.workspace.google.com/admin/getting-started/editions/manage-access-to-gemini-in-classroom)）。7 月，Common Sense Media 在风险评估里向 Google 提的要求，正是对未成年人账号默认关闭搜索里的 AI 功能，并把开关交给学校和家长（[新闻稿](https://about.commonsensemedia.org/press-room/press-releases/googles-ai-search-poses-unacceptable-risk-to-kids-common-sense-media-finds)）。

麻烦在清单最后一项。Search 和 Gemini 列在一起，开关是捆着的。Phillips 对《纽约时报》说得很直白："Search and AI are deeply integrated."学校不开 AI，学生就用不了搜索，只会看到学校发出的"不可用"提示（[NYT](https://www.nytimes.com/2026/11/03/us/google-search-schools-restrict-ai.html)，这句话 [TechCrunch](https://techcrunch.com/2026/11/03/google-will-let-schools-disable-its-ai-tools-but-not-without-sacrificing-search/) 和 [EdWeek](https://www.edweek.org/technology/googles-new-rules-hand-schools-hard-choices-about-ai-and-search/2026/11) 都引用了）。

反应来得很快。据 TechCrunch 汇总，参议员 Sanders 称之为"勒索"，前 FTC 主席 Lina Khan 说这暴露了不受监管的垄断者掌控基础服务的危险（[TechCrunch](https://techcrunch.com/2026/11/04/google-faces-backlash-for-plan-that-would-turn-off-search-for-schools-that-restrict-ai/)）。DuckDuckGo CEO Gabriel Weinberg 直接贴出了把学校默认搜索引擎换成 DuckDuckGo 的[部署文档](https://start.duckduckgo.com/duckduckgo-help-pages/get-duckduckgo/deploy-duckduckgo)，附一句"get in touch for help"（[TechCrunch](https://techcrunch.com/2026/11/04/duckduckgo-pitches-itself-to-schools-amid-backlash-over-googles-ai-policy/)）。Google 在 X 上回应，说这些公告"给了学校更多选择，而不是更少"（[@NewsFromGoogle](https://x.com/NewsFromGoogle/status/2117714815477059722)）。

垄断之争会持续很久。我更关心一个能查证的问题：搜索和 AI 真的拆不开吗？

## "深度整合"整合的是哪一层

"搜索里的 AI"至少有两层，意思差得很远。

第一层是理解查询、给结果排序。Google 2019 年就公开说，BERT 参与了美国英文搜索里约十分之一查询的排序（[Google 博客](https://blog.google/products/search/search-language-understanding-bert/)）。这一层早就和搜索长在一起。没有学区要求关掉它，它也不会替学生写作业。

第二层是生成式回答：结果页顶部的 AI 摘要（AI Overviews），以及可以连续追问的 AI Mode。学校担心的是这一层。Common Sense 拿 180 份作业做测试，一半数学题、一半人文写作，AI Mode 每一份都给出了能直接上交的完整答案。同一道历史题换一次搜索，四成以上的答案出入很大（[报告 PDF](https://institute.commonsensemedia.org/sites/default/files/risk-assessments/csm-ai-risk-assessment-google-search-07142026_0.pdf)）。

把第二层单独去掉，Google 早有现成的做法。它的搜索帮助页写着：AI Overviews 等功能"无法关闭"，但用户可以在搜索后选 Web 筛选，"只显示文字链接，不含 AI Overviews 等功能"（[Google 搜索帮助](https://support.google.com/websearch/answer/14901683)）。Web 筛选 2024 年 5 月上线（[TechCrunch](https://techcrunch.com/2024/05/14/google-adds-web-search-filter-for-showing-old-school-text-links-as-ai-rolls-out)）。不带生成式回答的结果页，Google 已经给全球普通用户开放了两年多。

所以"深度整合"放在第一层说得通，放在第二层更像一个产品决定：Google 没有把 Web 视图做成管理员能锁定的选项。Phillips 的公告通篇没提 AI Overviews 和 AI Mode。EdWeek 的报道也写明，Google 不提供不带 AI 摘要的传统搜索，也没说以后会不会提供。

有一点我拿不准。按次选择的筛选器，要变成学生绕不开的账号级设置，工程上未必零成本。Google 同期在搜索里试点的 Guided Learning 也建在生成层上。但 Google 没有公开解释为什么做不到，"deeply integrated"这句话本身也回答不了这个问题。

## 学校实际失去的是什么

后台开关按"产品 × 组织单元"分配。Classroom 产品负责人 Brittany Siegal Mennuti 对 EdWeek 说，学区可以让一个年级完全不用 AI，另一个年级只开 Guided Learning，高年级开完整搜索。粒度能细到年级，细不到功能：哪个组禁用 AI，哪个组就没有搜索。

被拿掉的东西是有用的。当过教师和校长的 Common Sense 首席项目官 Yvette Renteria 对 EdWeek 说，没了搜索，学生就少了练习找来源、判断来源可不可信的机会。查资料、比来源、辨真假，正是学校最想教、也最怕 AI 摘要代劳的部分。

换引擎也没那么简单。按 Google 往年的数据，美国学校里约有 5000 万台 Chromebook（见 [TechCrunch](https://techcrunch.com/2026/11/04/duckduckgo-pitches-itself-to-schools-amid-backlash-over-googles-ai-policy/)）。账号、Classroom、浏览器是同一套体系，换掉默认引擎只解决了一部分。

有余力的学区会自己打补丁。EdWeek 提到，过滤软件商 Securly 提供屏蔽 Google 搜索 AI 内容的功能，弗吉尼亚州 Fairfax 县在测试一个隐藏 AI 摘要的 Chrome 扩展。还有 IT 教程教人把 AI Mode 的网址加进 Chrome 黑名单（[教程](https://googleadminbootcamp.com/block-gemini-ai-google-search/)）。这些都是非官方办法，Google 改一次页面就可能失效。没有专职 IT 的小学区，只剩两个整包选项。Renteria 也提醒过，这会拉大学区之间的差距。

## 判断

对做产品的人来说，这件事的关键在管理后台。AI 嵌进一个已经被当成基础设施的产品之后，"默认关闭"有没有意义，要看能关到多细。只能整个关掉，用户面对的就还是二选一。Google 这次从"默认开、关不掉"改成了"默认关、要关就连搜索一起关"，只走了一半。

Phillips 说会在"接下来几个月"向学校公布细节，EdWeek 报道搜索部分明年初生效。Blumenthal 和 Hawley 10 月致信 Pichai 提了九个问题，要求 11 月 2 日前答复，Google 11 月 3 日的声明一个都没回应。我会盯一个具体信号：明年初之前，管理后台里会不会出现一个等同于 Web 筛选的选项。如果一直没有，那就是 Google 选择不拆，而不是拆不开。

## 参考来源

- [Designing responsible AI for learning（Google 博客，Chris Phillips）](https://blog.google/products-and-platforms/products/education/ai-learning-era-updates-2026/) — 默认关闭的产品清单、生效节奏、Guided Learning 试点；公告未提 AI Overviews/AI Mode
- [Manage access to Gemini in Classroom（Google Workspace 帮助）](https://knowledge.workspace.google.com/admin/getting-started/editions/manage-access-to-gemini-in-classroom) — 现行默认对所有年龄开启
- [AI Overviews 帮助页（Google 搜索帮助）](https://support.google.com/websearch/answer/14901683) — 功能无法关闭；Web 筛选只显示文字链接、不含 AI Overviews
- [Understanding searches better than ever before（Google 博客，2019）](https://blog.google/products/search/search-language-understanding-bert/) — BERT 参与约十分之一美国英文查询的排序
- [Common Sense Media 新闻稿](https://about.commonsensemedia.org/press-room/press-releases/googles-ai-search-poses-unacceptable-risk-to-kids-common-sense-media-finds)与[风险评估报告](https://institute.commonsensemedia.org/sites/default/files/risk-assessments/csm-ai-risk-assessment-google-search-07142026_0.pdf) — 180 份作业全部被完成、历史题答案不一致、对 Google 的建议
- [TechCrunch：Google will let schools disable its AI tools, but not without sacrificing Search](https://techcrunch.com/2026/11/03/google-will-let-schools-disable-its-ai-tools-but-not-without-sacrificing-search/) — Phillips 对 NYT 的表态
- [TechCrunch：Google faces backlash…](https://techcrunch.com/2026/11/04/google-faces-backlash-for-plan-that-would-turn-off-search-for-schools-that-restrict-ai/) — 政界反应、Google 的 X 回应
- [TechCrunch：DuckDuckGo pitches itself to schools…](https://techcrunch.com/2026/11/04/duckduckgo-pitches-itself-to-schools-amid-backlash-over-googles-ai-policy/) — Weinberg 的表态、5000 万台 Chromebook
- [EdWeek：Google's New Rules Hand Schools Hard Choices About AI and Search](https://www.edweek.org/technology/googles-new-rules-hand-schools-hard-choices-about-ai-and-search/2026/11) — 生效时间、按年级分组、没有无 AI 的搜索选项、Renteria 观点、Securly/Fairfax 补丁、参议员信件未获回应
- [TechCrunch：Google adds 'Web' search filter（2024）](https://techcrunch.com/2024/05/14/google-adds-web-search-filter-for-showing-old-school-text-links-as-ai-rolls-out) — Web 筛选上线时间
- [Google Admin Bootcamp 教程](https://googleadminbootcamp.com/block-gemini-ai-google-search/) — 后台无 AI Mode 开关，用网址黑名单绕行
- [DuckDuckGo 部署文档](https://start.duckduckgo.com/duckduckgo-help-pages/get-duckduckgo/deploy-duckduckgo) — Weinberg 贴出的切换指南
