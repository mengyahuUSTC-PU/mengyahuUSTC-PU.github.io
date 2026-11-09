---
title: "好莱坞少了近 13 万个岗位，三分之二在 AI 视频工具上线前就已经没了"
description: "Apricitas 统计，美国创意行业四年少了 20 多万个岗位。回到 BLS 原始数据看时间线：影视业的下滑比 AI 视频工具更早，而 AI 最可能冲击的人群恰好不在这套统计里。"
pubDate: 2026-10-24
tags: [ai-and-jobs, labor-economics, creative-industries]
lang: zh
slug: hollywood-job-losses-ai-attribution
translationOf: hollywood-job-losses-ai-attribution
---

九月底，Apricitas Economics 的 Joseph Politano 发了一篇文章，开头一句是：过去四年，美国"创意"行业少了 20 多万个岗位（[Apricitas](https://www.apricitas.io/p/ai-and-the-fall-of-the-creative-class)）。他说，这段下滑的强度和持续时间只有 2001 年、2008 年两次衰退能比，可眼下并没有全面衰退。电影和录音业受打击最重，占了全部减员的近一半；书报刊出版排第二，少了 7 万多。

这组数字很容易被读成"AI 来了，创作者失业了"。Politano 本人没下这个结论，他写的是，AI 到底造成了多少岗位流失，"极难证明"。我想再往前推一步。用 BLS 原始数据对时间线，至少在影视这一块，能说的比"极难证明"多一些。

## 下滑是从什么时候开始的

BLS 的 CES 是一项月度调查，向雇主收集工资单上的人数。按 CES 数据，电影和录音业就业的高点出现在 2022 年 11 月，为 45.61 万人（[FRED: CES5051200001](https://fred.stlouisfed.org/series/CES5051200001)）。到 2026 年 6 月跌到 32.23 万，少了 13.4 万，降幅 29%。9 月的初值是 32.85 万。

把关键节点排一下：

- 2022 年 12 月到 2023 年 1 月，两个月就少了 4 万人。当时 ChatGPT 刚发布，能拿来做影视的 AI 视频工具还没有出现。
- 编剧工会 2023 年 5 月 2 日开始罢工，演员工会 7 月 14 日跟进（[BLS](https://www.bls.gov/blog/2023/finding-current-events-in-the-data-a-look-at-strikes-among-writers-and-actors.htm)）。罢工开始前的 4 月，就业已经比高点少了 3.2 万。
- 演员罢工在 11 月 9 日结束。就业从 10 月的 37.75 万回升到 2024 年 1 月的 40.26 万，但之后再没回到罢工前的 42 万多。
- 2024 年 12 月 9 日，OpenAI 向付费用户开放 Sora（[OpenAI](https://openai.com/news/sora)）。从高点算到 2026 年 9 月，行业总共少了 12.8 万人，其中约三分之二在这之前就已经发生了。

比时间先后更能说明问题的是下降速度。按每年 12 月计算，2024 年减少 2.7 万，2025 年减少 2.5 万，2026 年前 9 个月减少 1.8 万。按 9 月同比计算，前一年少了 3 万，最近一年少了 2 万。AI 视频生成从演示变成人人能用的这两年里，下滑并没有加快，反而略有放缓。Apricitas 说整个创意行业最近流失在加速，但影视这一块的 BLS 数据里看不到加速。

下降速度没变，并不能证明 AI 的作用为零。也可能是流媒体收缩的拖累在减弱，AI 正好补上了这部分，总的速度看起来就没变。月度数据区分不了这两种情况。不过，"AI 掏空了好莱坞"这个说法，在这条曲线上找不到依据。

## 2022 年的高点也算不上泡沫

常见的另一种解释是，2022 年流媒体平台抢内容，招人招多了，现在只是回落。这只能解释很小一部分。2019 年的月均就业约 43.7 万，2022 年的高点只比它高 4%，而现在比 2019 年低了约四分之一。

BLS 在 2026 年 4 月发过一篇分析，把影视制作就业十年来的下滑归因于疫情、上映影片减少和多次罢工，全文没有提到 AI（[BLS TED](https://www.bls.gov/opub/ted/2026/picture-this-a-decade-of-employment-in-the-motion-picture-and-video-industries.htm)）。Politano 的解释是商业模式受到挤压：电影票房比 2019 年少了 25%，有线电视收入比高点少了 18%，流媒体补不上这个缺口，观众的时间越来越多地流向用户自制内容。他还提到好莱坞的行业整合，以及拍摄外包到海外。这些因素都在 2022 年后同时起作用，和 AI 在时间上高度重叠，单靠月度就业数据拆不开。

## AI 最可能冲击的人，不在这套数据里

CES 只统计工资单上的雇员，明确排除自雇者（[BLS CES FAQ](https://www.bls.gov/web/empsit/cesfaq.htm)）。2023 年罢工期间，BLS 专门解释过：编剧大多按合同工处理，不在工资单上，所以"预计不会对 CES 数据产生直接影响"；演员的雇佣方式不一，一部分也按合同工算。

问题就出在这里。生成式 AI 最直接能替代的活，比如插画、配音、文案、概念设计，很多是由自由职业者接的。这些人收入下降，不会表现为哪家公司裁员，也就不会出现在 CES 的减员数字里。

有研究专门看了这个群体。Xiang Hui、Oren Reshef 和 Luofeng Zhou 用 Upwork 平台的数据，比较了受 AI 影响和不受影响的职业在工具发布前后的变化（[论文](https://www.cesifo.org/DocDL/cesifo1_wp10601.pdf)）。DALL-E 2 和 Midjourney 发布后，设计、修图、插画类自由职业者的月接单量下降 3.7%，月收入下降 9.4%。ChatGPT 发布后，校对和文字编辑类分别下降 2% 和 5.2%（[WashU 摘要](https://olin.washu.edu/about/news-and-media/news/2023/08/study-ai-tools-cause-a-decline-in-freelance-work-and-incomeat-least-in-the-short-run.php)）。这是单个平台的短期效应，不能推到整个行业。但它的变化方向和时间点都对得上 AI 工具的发布，CES 曲线做不到这一点。

AI 使用率的数据，同样不支持"创意行业是 AI 重灾区"。Politano 文中拿艺术、娱乐和休闲业工作者使用生成式 AI 的比例（约 32%）和全行业平均（62%）对比，但这两个数字口径不同：前者只算工作中使用，后者把个人使用也算进去了，文章评论区已有读者指出这一点。我换成同一口径，用 Bick、Blandin、Deming 的 Real-Time Population Survey，只看工作中使用：艺术、娱乐和休闲业 2026 年 7 月为 35.6%（[FRED](https://fred.stlouisfed.org/data/RPSGENAIUSAGESHAREIND17)），全部在职者 8 月为 40.5%（[Gen AI Adoption Tracker](https://genaiadoptiontracker.com/)），只差 5 个百分点左右。而且这个行业的数据波动很大，相邻两个季度能从 43% 掉到 29%。还有一点：按美国行业分类，电影业属于"信息业"，"艺术、娱乐和休闲业"指的是演出、博物馆、游乐园、健身房这类行业。所以这组使用率数据，根本没覆盖好莱坞。

## 怎么读"某行业少了 N 万岗位"

下次再看到"某行业少了几万个岗位，有多少该算在 AI 头上"，我会先查三点：下滑和对应 AI 工具可用的时间，哪个在前；工具普及以后，下降速度有没有变化；这套统计覆盖的，是不是最容易被替代的那群人。影视业这个案例，三点都对不上：下滑早于工具出现，速度没有变化，统计的主要是工资单上的剧组和后期雇员。

如果 AI 对创意劳动的冲击已经发生，它会先出现在自由职业平台的接单量和报价里，而不是 BLS 每月公布的非农就业表里。等哪天它出现在工资单数据里，就说明 AI 已经从替代外包，走到了替代正式雇员。那是另一个阶段的问题，也是这条曲线接下来最需要盯的变化。

## 参考来源

- [AI and the Fall of the Creative Class — Apricitas Economics](https://www.apricitas.io/p/ai-and-the-fall-of-the-creative-class) — 创意行业减员 20 多万、出版减员 7 万多、票房与有线电视收入降幅、使用率对比的原始口径
- [FRED: All Employees, Motion Picture and Sound Recording Industries (CES5051200001)](https://fred.stlouisfed.org/series/CES5051200001) — 2019 年至 2026 年 9 月月度就业数据，文中所有影视就业数字和斜率计算
- [BLS TED: Picture this — a decade of employment in the motion picture and video industries](https://www.bls.gov/opub/ted/2026/picture-this-a-decade-of-employment-in-the-motion-picture-and-video-industries.htm) — BLS 对十年下滑的归因（疫情、上映片量、罢工），未提 AI
- [BLS 博客：Finding current events in the data: strikes among writers and actors](https://www.bls.gov/blog/2023/finding-current-events-in-the-data-a-look-at-strikes-among-writers-and-actors.htm) — 罢工起始日期；编剧按合同工处理、不进 CES
- [BLS CES FAQ](https://www.bls.gov/web/empsit/cesfaq.htm) — CES 排除自雇者
- [Hui, Reshef & Zhou, The Short-Term Effects of Generative AI on Employment（CESifo 工作论文）](https://www.cesifo.org/DocDL/cesifo1_wp10601.pdf) — Upwork 自由职业者研究设计
- [WashU Olin 新闻稿](https://olin.washu.edu/about/news-and-media/news/2023/08/study-ai-tools-cause-a-decline-in-freelance-work-and-incomeat-least-in-the-short-run.php) — 接单量与收入降幅的具体百分比
- [FRED: Generative AI Adoption Rate for Work: Arts, Entertainment, and Recreation](https://fred.stlouisfed.org/data/RPSGENAIUSAGESHAREIND17) — 行业工作中使用率季度数据
- [Gen AI Adoption Tracker](https://genaiadoptiontracker.com/) — 全部在职者工作中使用率 40.5%（2026 年 8 月）
- [OpenAI: Sora](https://openai.com/news/sora) — Sora 2024 年 12 月 9 日开放
