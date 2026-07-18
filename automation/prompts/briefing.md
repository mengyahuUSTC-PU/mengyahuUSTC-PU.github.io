# 任务：每日 AI 快讯写作

你会收到选题筛选输出的 `briefing_items`。先阅读 editorial-baseline.md 的编辑方针，然后写当日快讯。

## 要求

- 中文先行，写完中文版再写英文版（英文版是重写，不是直译）
- 每条 2–4 句：第一句说清发生了什么，后面给一句作者判断（为什么重要 / 意味着什么），不是复述摘要
- 条目按重要性排序，最重要的展开稍多
- 结尾一段「今日一句话」：当日最值得记住的一个判断
- 某来源当日抓取失败时，在文末以一行小字标注（如「注：今日 X 源抓取失败，未覆盖」）
- 不逐条罗列所有输入：不值得写的条目可以丢弃

## 输出格式

两个完整的 Markdown 文件内容，用分隔符隔开：

```
===ZH===
---
title: AI 快讯：<日期或当日最大事件做钩子>
description: <一句话>
pubDate: <YYYY-MM-DD>
tags: [briefing]
lang: zh
slug: briefing-<YYYY-MM-DD>
translationOf: briefing-<YYYY-MM-DD>
---

<正文>

===EN===
---
title: <English title>
description: <one line>
pubDate: <YYYY-MM-DD>
tags: [briefing]
lang: en
slug: briefing-<YYYY-MM-DD>
translationOf: briefing-<YYYY-MM-DD>
---

<body>
```
