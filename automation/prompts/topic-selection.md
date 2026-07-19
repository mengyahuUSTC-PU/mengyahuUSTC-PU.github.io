# 任务：选题筛选

你会收到一份当日抓取的原始条目池 JSON（字段：source / title / url / summary / published）。
先阅读 editorial-baseline.md 的编辑方针，然后从池中筛出**最值得写的条目**。

## 筛选标准

1. 与品牌相关：AI 安全与治理（权重最高）、AI 前沿进展、行业趋势；偶尔可选真正重大的其他科技条目
2. 有「作者能加增量」的空间：能给出机制解释、工程判断或亲历视角的优先；纯官宣稿低优先
3. 时效性：突发大事优先；常绿深度话题不受时效限制
4. 去重：同一事件多个来源只保留信息最全的一条
5. **来源多样性**：briefing_items 中来自同一来源（尤其是聚合类博主如 Simon Willison）的条目不得超过 2 条；同一事件优先选一手来源的条目而非博主转述

## 输出格式（严格 JSON，不要输出其他文字）

```json
{
  "briefing_items": [
    {"title": "", "url": "", "source": "", "one_liner": "一句话中文摘要", "why": "为何值得进快讯"}
  ],
  "deep_dive_candidates": [
    {"rank": 1, "title": "", "url": "", "source": "", "one_liner": "", "why": "为何值得写深度：作者能提供什么增量视角", "angle": "建议的切入角度"}
  ]
}
```

- `briefing_items`：5–10 条，进当日快讯
- `deep_dive_candidates`：2–4 条，按值得写的程度排序，供用户挑选
- 全部为空时输出两个空数组，并可在 `note` 字段说明当日无可写内容
