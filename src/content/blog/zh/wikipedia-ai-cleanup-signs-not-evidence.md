---
title: "维基百科的「AI 腔」清单，自己就写着：这些不算证据"
description: "我照着维基百科的 Signs of AI writing 页面给写作流程加了黑名单，回头细读才发现，维基百科自己处理 AI 内容时，只把人类几乎写不出来的痕迹当证据。"
pubDate: 2026-10-27
tags: [ai-detection, wikipedia, ai-writing]
lang: zh
slug: wikipedia-ai-cleanup-signs-not-evidence
translationOf: wikipedia-ai-cleanup-signs-not-evidence
---

今年 7 月底，有读者反馈，我的文章「一看就是 AI 写的」，读不下去。

我的写作流程确实用 AI 辅助，这话没法反驳，只能改。我照着英文维基百科的 [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) 页面给流程加了一张黑名单：不用 delve、tapestry，破折号全文最多一处，不写「不仅……更是……」，同一个词重复用也不硬换同义词。

上周 IEEE Spectrum [采访](https://spectrum.ieee.org/wikipedia-wikiproject-ai-writing-cleanup)了维基百科 AI 清理项目的创始成员 Ellia Lebleu，Hacker News 上拿了 443 分。我回头把那个页面从头读了一遍，才注意到它在开头就写明：这份清单是「观察，不是规则」。带这些特征的文字不一定出自 AI，因为模型本来就是用人写的东西训练的，其中就有维基百科。

我抄来当规则的东西，维基百科自己并不拿它当证据。

## 能删条目的证据只有三类

WikiProject AI Cleanup 起于 2023 年 12 月，当时编辑们在维基百科的 Discord 上发现一批条目带着同样的怪癖。今年 3 月，英文维基通过[指南](https://en.wikipedia.org/wiki/Wikipedia:Writing_articles_with_large_language_models)，禁止用大模型生成或改写条目正文，只留两个例外：让模型给自己写的内容挑拼写和语法错误，以及从其他语言版本翻译。

规则很严，执行时却按证据分档。最快的处理是快速删除，对应的 [G15 条款](https://en.wikipedia.org/wiki/Wikipedia:Criteria_for_speedy_deletion)只认三类证据：

- 写给用户的话留在了条目里，比如「这是您要的维基百科条目」、知识截止日期声明、没填的「[出生日期]」占位符；
- 不存在的引用：一点就失效的链接，校验位不对、WorldCat 也查不到的 ISBN，解析不了的 DOI；
- 技术残留：ChatGPT 特有的 oaicite 引用残码、turn0search0、被包进 Markdown 代码块的维基源码。

这三类有个共同点，人几乎写不出来。delve、三段式排比、破折号都不在其中。G15 原文写明，其他常见 AI 特征单独出现都不够，连作者本人承认用了大模型也不算。禁令指南也写着：有些编辑的文风本来就像模型输出，处罚要看「该编辑近期编辑的完整模式」，只凭文风不行。

文风特征只负责提醒编辑去查引用、查内容，定不了案。Signs 页面还专门提醒：别把特征当成问题本身去修，修掉症状只会让检测更难。

读到这句我有点尴尬。我那张黑名单，干的正是修症状。

## 误伤落在谁身上

Signs 页面有一节专讲「无效特征」，开篇就说，错误的 AI 指控会赶走新编辑，让社区里人人互相猜疑。Lebleu 在采访里说，绝大多数 AI 生成内容来自新手编辑。被清理的主要对象和最容易被误伤的人，是同一群人。

非母语写作者更吃亏。页面里有个细节：刻意避免重复用词常被当作 AI 特征，可非母语编辑也会这么写，意大利的学校就教学生别重复同一个词。我黑名单里「不硬换同义词」那条，放到这些作者身上就是误伤。

自动检测器的误伤是另一种机制。斯坦福 James Zou 团队 2023 年的[研究](https://arxiv.org/abs/2304.02819)用 7 个常用 GPT 检测器测了 91 篇托福作文，平均误报率 61.22%，测美国八年级学生的作文则几乎没有误判。91 篇托福作文里有 18 篇被 7 个检测器一致判为 AI。这些检测器主要看困惑度（perplexity），也就是一段文字对语言模型来说有多好预测。非母语作者词汇窄、句式变化少，文字好预测，就被当成机器写的。

同一篇论文做了反向实验：让 ChatGPT 把托福作文的用词改得更像母语者，误报率从 61.22% 降到 11.77%。

两件事放在一起，会推出一个别扭的结果。这是我的推论，没有研究直接测过：一位非母语作者不用 AI 润色，文字太好预测，困惑度检测器会把它判成 AI；用了 AI 润色，也就是维基百科允许的那种改错，文字里又可能多出人类审阅者盯着的词和句式。两套方法朝相反方向出错，被夹在中间的是同一个人。

维基百科这边用的检测器不是 2023 年那 7 个。Lebleu 和检测公司 Pangram 合作估算，2025 年底约 20% 的新条目和草稿是 AI 生成的，2026 年初降到 15%–16%。Pangram 在 ChatGPT 出现之前的维基内容上测试，零误报，所以这些数字被当作保守下限。但那批条目大多经过多人多年修订，和一个新手用第二语言写的初稿是两种文本。前者零误报，推不出后者也零误报。

## 对用 AI 写作的人

读者说「一看就是 AI」，是在文风层面下判断。这种判断有代价，读者真的会走。但词表会过期。Signs 页面自己说，被过度使用的词随模型更新而变化；它引用的一项 2026 年 7 月研究发现，受测模型里只有 Claude 用破折号比职业作者多。按词表改稿，追的是一个一直在移动的目标。

不会过期的是 G15 那一档：引用能不能打开，来源里有没有这句话。Lebleu 提到，有了检索增强生成，编造的引用少了，现在更常见的是来源真实存在，内容却撑不起正文里的论断。扫一眼看不出这种问题，认真的读者核对一次就会发现。对用 AI 辅助写作的人，读者扫一眼看到的是文风，核对之后才看到引用和论断对不对得上。

接下来我会盯维基媒体基金会在做的 Paste Check。它在编辑提交时标记从部分聊天机器人粘贴过来的文字，看的是文字怎么来的，不看读起来像什么。如果它管用，只是文风像 AI 的非母语作者就不会再被连带误伤。最难的是规则允许的那部分：用模型改错、用模型翻译，同样是把模型的输出粘进编辑框。Paste Check 在这里怎么划线，我还看不出来。

## 参考来源

- [How Wikipedia's Editors Keep the Online Encyclopedia Human-Written（IEEE Spectrum）](https://spectrum.ieee.org/wikipedia-wikiproject-ai-writing-cleanup) — Lebleu 访谈：项目起源、新手编辑是主要来源、Pangram 估算（20%→15–16%、零误报测试）、引用与论断不符、Paste Check
- [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) — 「观察，不是规则」、勿修症状、无效特征一节、非母语编辑与避免重复用词、破折号研究
- [Wikipedia:WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) — 项目目标与处理流程、2023 年 12 月起始
- [Wikipedia:Writing articles with large language models](https://en.wikipedia.org/wiki/Wikipedia:Writing_articles_with_large_language_models) — 禁令内容、改错与翻译两个例外、文风相似不能作为处罚依据
- [Wikipedia:Criteria for speedy deletion（G15）](https://en.wikipedia.org/wiki/Wikipedia:Criteria_for_speedy_deletion) — G15 的三类证据，其他特征和本人承认都不够
- [Liang et al., GPT detectors are biased against non-native English writers（arXiv:2304.02819）](https://arxiv.org/abs/2304.02819) — 7 个检测器、91 篇托福作文、61.22% 误报率、18 篇一致误判、润色后降至 11.77%、困惑度机制
