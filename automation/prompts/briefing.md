# 任务：每日 AI 快讯写作

你会收到选题筛选输出的 `briefing_items`。先阅读 editorial-baseline.md 的编辑方针，然后写当日快讯。

## 要求

- 中文先行，写完中文版再写英文版（英文版是重写，不是直译）
- **条目式排版，每条独立成块**：
  - 小标题一行：`### [事件短标题](一手来源 URL)` ——**标题链接必须是一手来源**：模型/产品发布挂官方公告页（用 WebSearch/WebFetch 去找，别偷懒用抓取源给的链接），论文挂 arXiv 原文，事故挂当事人原帖或原始披露
  - 聚合类博主（如 Simon Willison）的链接只能以 `（另见 [xx](url)）` 出现，或在引用**他本人原创测评**时使用
  - 正文 2–4 句：第一句说清发生了什么，后面给作者判断（为什么重要 / 意味着什么），不是复述摘要
  - 一条涉及多个来源时，把其余链接以 `（另见 [xx](url)）` 形式带上
- **杜绝幻觉**：每一个事实断言都必须能对应到输入条目的 URL；输入里没有的细节不要编，拿不准就删
- 条目按重要性排序，最重要的放最前、展开稍多；相关条目可合并为一条
- 结尾一段「**今日一句话**」：当日最值得记住的一个判断
- 某来源当日抓取失败时，在文末以一行小字标注（如「注：今日 X 源抓取失败，未覆盖」）
- 不逐条罗列所有输入：不值得写的条目可以丢弃

## 执行约束

**最终回复只包含两个文件的内容和分隔符**：不要解说、不要提问、不要描述你做了什么、不要尝试自己写文件。

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
