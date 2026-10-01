---
title: "攻击者没破解加密，他们让模型把保密推理念了出来"
description: "OpenAI 披露归因于月之暗面关联人员的协同蒸馏行动。拆开看：一个为隐私设计的功能被用成了提取管道，而这份披露能证明什么、不能证明什么，得分开说。"
pubDate: 2026-09-30
tags: [ai-safety, distillation, us-china]
lang: zh
slug: openai-reasoning-extraction-campaign
translationOf: openai-reasoning-extraction-campaign
---

9 月 30 日，OpenAI 发布了一份不常见的安全披露（[官方公告](https://openai.com/index/disrupting-a-coordinated-model-distillation-campaign/)）：一场有组织的「对抗性蒸馏」行动——系统性、未经授权地套取模型输出和推理过程，去训练或改进另一个模型——从 7 月第一周开始低调运转，7 月 24、25 日冲上峰值，4000 多个账号发出约 1.6 万条同模式请求；扩大排查后，使用相似提示模板的账号超过 1.5 万个。7 月 28 日，OpenAI 称行动被完全切断。归因只有一句，但分量最重：核心账号集群指向「与月之暗面（Moonshot AI，Kimi 开发商）相关的个人」（[CyberScoop](https://cyberscoop.com/openai-moonshot-ai-model-distillation-attack/)）。

这份披露里最值得拆的，是 OpenAI 特意澄清的一句话：攻击者「没有破解我们的加密，没有入侵数据库，也没有直接接触存储的用户对话」。那他们做了什么？手法一句话说完：把 A 会话返回的加密推理内容拷出来，贴进 B 会话，请模型「解密并转录」。要看懂这句话为什么能成立，得先回答两个问题：推理为什么藏着？藏着的推理为什么会以加密形式出现在用户手里？

## 藏起来的推理是最高效的训练数据

2024 年 9 月 o1 发布时，OpenAI 在权衡「用户体验、竞争优势和思维链监控的可能性」之后，决定不向用户展示原始思维链（[官方博客](https://openai.com/index/learning-to-reason-with-llms/)）。「竞争优势」指的就是防蒸馏：原始推理轨迹能被对手直接拿去当训练数据。

这个担心有实证。斯坦福等机构的 s1 实验只用 1000 条精选推理轨迹微调 Qwen2.5-32B，竞赛数学成绩就超过了 o1-preview，最多高出 27 个百分点（[arXiv:2501.19393](https://arxiv.org/abs/2501.19393)）。推理轨迹的样本效率高到这个程度，峰值期约 1.6 万条的提取量就不是零敲碎打，而是生产线的进料速度。模型的最终回答人人可见，各家水平也在拉平；中间那段推理才是闭源实验室花钱最多、也最不愿外流的东西。

## 隐私功能撞上了 IP 防线

那「加密推理内容」又是什么？它来自另一条产品需求：隐私。OpenAI 的 Responses API 有无状态模式，服务启用「零数据保留」（zero data retention，服务端不存任何对话数据）的企业客户。服务器不存对话，多轮推理的上下文就只能由客户端保管，于是 API 把推理内容加密后交给客户，下一轮请求原样传回，服务端解密、放回模型上下文，推理接着跑（[API 文档](https://developers.openai.com/api/docs/guides/reasoning)）。

注意这个设计的含义：一段本不出门的保密推理，现在以密文形式存放在客户手里，而且协议承诺「传回来就解开」。攻击者做的，是把这段密文带进另一个会话传回去——服务端照常解密进上下文，再诱导模型把上下文里的内容转述出来。模型没有破解任何密码，它只是把自己「看到」的东西念了出来。具体哪一道校验失守，OpenAI 没有细说，但修复清单透露了攻击面：封堵的重放路径横跨账号、工作区、模型家族三个维度，说明加密推理内容此前没有严格绑定在生成它的那个会话上。

这是一次设计目标的对撞：零数据保留是对企业客户的隐私承诺，隐藏思维链是对竞争对手的防线，两者在「加密推理内容」这一个设计点上迎面相遇，开了口子。

## 检测靠的是模式，不是单条请求

单看任何一条请求都不构成违规证据：把一段密文贴进对话请模型转录，外观上和无数正常用法没有区别。OpenAI 真正的识别依据是跨账号关联——1.5 万个账号共用相似的提示模板。相应地，修复动作也全在运营层面：封禁账号、封堵重放路径、增加流式输出检测、收紧注册控制，并通过前沿模型论坛（Frontier Model Forum，前沿实验室间的安全信息共享组织）和政府渠道把检测指标分发给同行。防蒸馏不像修一个 bug，修完就结束；它是一条要长期运营的对抗线。

## 这份披露证明了什么，没证明什么

OpenAI 给归因上了两道限定：不确定观察到的所有操作者是否同一行为体；这是公司自己的判断，不是司法认定。月之暗面此前一直否认蒸馏指控，称模型性能来自架构层面的原创改动（据 [SCMP 报道](https://www.scmp.com/tech/tech-war/article/3361625/global-ai-experts-push-back-us-distillation-claims-against-moonshots-kimi-k3-model)）。还有一条时间线要摆清楚：Kimi K3 7 月中旬就发布了（[我当时写过它的发布节奏](/zh/kimi-k3-open-weight-audit-gap)），而这次提取的峰值在 7 月 24、25 日。所以即使归因全部坐实，这份披露证明的也是「7 月有人在成规模地套推理轨迹」——这批材料只可能流向未来的模型，接不上白宫 7 月「K3 靠蒸馏美国模型建成」的那条指控（那条指控的证据成色，我在[制裁开源权重一文](/zh/sanctioning-open-weight-models)里拆过）。两件事经常被混在一起报道，分开才看得清。

把它放回九月的序列里，结构性的信号更清楚。Anthropic 的威胁情报报告已把模型蒸馏与生物滥用、网络攻击并列为滥用类目（[我 9 月 10 日的快讯](/zh/briefing-2026-09-10)），并指控月之暗面把 Kimi 用户请求转发给 Claude、收集两千三百多万条回复用于训练（[9 月 11 日快讯](/zh/briefing-2026-09-11)）；现在 OpenAI 交出了自己的版本。当开放权重基座加后训练就能贴近闭源第一梯队——Cognition 拿 K3 训出的 SWE-2 离 Fable 5.1 不到 1 分——闭源实验室最需要守住的资产正从权重移向推理轨迹。麻烦在于，推理轨迹必须流经产品接口才能变成收入，要守的东西和要卖的东西走在同一条管道里。接下来我会盯一个点：零数据保留这类隐私功能会不会因此收缩——企业客户的隐私需求和厂商的防蒸馏需求，下一次会在哪个设计点相撞。

## 参考来源

- [OpenAI: Disrupting a coordinated model-distillation campaign](https://openai.com/index/disrupting-a-coordinated-model-distillation-campaign/) — 事件披露本体：时间线、数字、归因、修复措施（页面对自动抓取返回 403，细节经下列三方交叉核实）
- [CyberScoop: OpenAI reveals 'novel' encryption bypass used in distillation attack](https://cyberscoop.com/openai-moonshot-ai-model-distillation-attack/) — 攻击手法、「未破解加密」原话、时间线与数字
- [HyperAI 报道](https://hyper.ai/en/stories/2bbb9ba9b71cbef4ce38852a5f1d9d46) — 披露日期（9 月 30 日）、数字、信息共享渠道交叉核实
- [MIXED News 报道](https://mixed-news.com/en/openai-moonshot-ai-reasoning-extraction-campaign) — 归因限定措辞（「不确定是否单一行为体」「公司自身判断」）
- [OpenAI: Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/) — o1 隐藏原始思维链的官方理由（原话另经 [Simon Willison 2024 年逐字引用](https://simonwillison.net/2024/Sep/12/openai-o1/)核对）
- [OpenAI Reasoning 文档](https://developers.openai.com/api/docs/guides/reasoning) — encrypted_content、无状态模式、零数据保留机制
- [arXiv:2501.19393 (s1: Simple test-time scaling)](https://arxiv.org/abs/2501.19393) — 1000 条推理轨迹微调 Qwen2.5-32B 超 o1-preview 的数据
- [SCMP: Global AI experts push back on US 'distillation' claims](https://www.scmp.com/tech/tech-war/article/3361625/global-ai-experts-push-back-us-distillation-claims-against-moonshots-kimi-k3-model) — 月之暗面否认表述（未能直接抓取，见核查点）
- 本站旧文：[Kimi K3 发布与安全评估缺口](/zh/kimi-k3-open-weight-audit-gap)、[制裁挡不住模型](/zh/sanctioning-open-weight-models)、[9 月 10 日快讯](/zh/briefing-2026-09-10)、[9 月 11 日快讯](/zh/briefing-2026-09-11)
