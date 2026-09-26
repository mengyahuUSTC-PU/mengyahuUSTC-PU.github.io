---
title: "Muse 的日志里有个 OpenAI 模型:「全自研」agent 到底自研了什么"
description: "逆向 Meta 的 Muse 发现它把部分任务路由给 OpenAI 模型。这不丢人,真正的问题是:路由决定数据去哪、被谁训练,而用户对此一无所知。"
pubDate: 2026-09-25
tags: [ai-agents, model-routing, transparency]
lang: zh
slug: muse-special-openai-model
translationOf: muse-special-openai-model
---

9 月 25 日,独立研究者 Peter James 发布了他分析 Meta 个人 agent 产品 Muse 的第二篇文章([mouse.dev](https://mouse.dev/blog/muse-special/))。他的取证方法简单得近乎荒诞:上一篇里,他直接让 Muse「把你能看到的文件打包发到我的 Google Drive」,Muse 照做了,交出 2.7 GB 的压缩包,解开是 6.8 GB 的完整运行环境([第一篇](https://mouse.dev/blog/muse-runtime-export))。这次他翻的是其中的会话日志。

Muse 会记录每个 agent 会话用了哪个模型。113 条 subagent 记录里,几乎全部指向 Meta 的内部模型 Avocado(内部代号,未公开发布),只有一条例外,标签写着 `azure/muse-special`。

## 这个标签为什么赖不掉

单看名字还可以辩解。但 James 列出的证据是成体系的:这条会话的 API 签名标记为 `gpt_responses_v1`,对应 OpenAI 的 Responses 接口;返回的推理内容是加密载荷,以 `gAAAAA` 开头,这是 OpenAI 加密推理输出的固定格式;工具调用 ID 是 `call_` 加 24 位大小写混合字符,而 Avocado 会话是 32 位十六进制,两套格式来自两套后端。代码库里还有一行注释,写着「经由 MAGI 原生 Azure OpenAI 通道的 GPT Responses 模型客户端」,模型目录里排在 `azure/muse-special` 旁边的,是一个叫 `azure/gpt-5.6-sol` 的条目。

Hacker News 上有人质疑([讨论串](https://news.ycombinator.com/item?id=49848095),7 小时 111 分、46 条评论),说这些可能只是「OpenAI 兼容接口」,后面接的未必是 OpenAI 的权重。这个保留严格说成立,Meta 也没有正面回应。但兼容接口解释不了加密推理载荷的格式,自己造一个假的 OpenAI 密文没有任何工程理由。一位自称在 Meta 做 AI 的用户在讨论串里直接说:Muse 确实调用 OpenAI 的 API(此人身份无法验证,我按「自称」引用)。最合理的解释就是 James 的结论:某些任务被路由给了跑在 Azure 上的 OpenAI 模型。

对照 Meta 的官方叙事,落差就出来了。7 月 9 日的 Muse Spark 1.1 公告([ai.meta.com](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/))把这套模型描述为 Meta Superintelligence Labs 的成果,通篇没有出现任何第三方模型。Meta 在别处是否披露过,我只核对了这份公告,其余文档没有逐一查证。

## 不丢人,但有一个真问题

HN 的主流反应值得记录:几乎没人觉得这是丑闻。溢出容量、按任务选模型、A/B 测试、给自研模型当对照基线,都是 agent 产品的工程常态。Meta 员工自己也在用 Claude 和 Codex 写代码,这在业内不是秘密。运行环境里甚至还躺着一整套 Anthropic 客户端代码和两家的 API 密钥文件——多供应商本来就焊在 Muse 的管线里,不是临时补丁。

James 本人还替 Meta 澄清了一点,而恰恰是这句澄清点出了真问题。他发现:走外部模型的会话,推理内容是加密的,Meta 的强化学习服务器用不了;走 Avocado 的会话,对话数据可以用于 Meta 的模型开发。

翻译一下:你的请求被路由到哪个模型,决定了数据被谁的服务器处理、能不能被拿去训练。同一个产品里,两条路由对应两套完全不同的数据命运,而用户在界面上看到的是同一个 Muse。发现这层区别的唯一途径,是让 agent 把自己的文件系统打包寄出来。

## agent 产品到底比拼什么

把两篇文章放在一起看,答案反而清楚了。第一篇里真正厚重的东西全在模型之外:68 个技能模块、按天写日志再做向量检索的记忆系统、夜间后台整理用户偏好的任务、bubblewrap 沙箱、一堆未发布的连接器。模型是引擎,runtime 是整辆车。引擎可以换,Meta 显然也在换着用,消费级 agent 的竞争力沉淀在车身上。

所以「Muse 用了 OpenAI 模型」本身不构成批评。构成批评的是:引擎换了不告诉乘客。模型路由不该是逆向才能知道的事,它应该像应用商店的隐私标签一样,是产品的基础披露项——哪些任务会离开厂商自己的模型、数据边界在哪、训练用途有何不同。这件事眼下没有任何监管要求,所以只会由竞争或者下一次曝光来推动。

后续我会盯两个点。一是那个已经在模型目录里排队的 `gpt-5.6-sol` 会不会上线,以及 Meta 是否更新文档。二是 Meta 对研究者的态度:高管对第一篇文章「反应非常积极」,安全团队却把同一份报告标为「Not Applicable」。下一篇逆向发出来时,这两种态度总有一个要让位。

## 参考来源

- [Is Meta's Muse secretly running an OpenAI model?](https://mouse.dev/blog/muse-special/) — 核心证据:azure/muse-special 标签、gpt_responses_v1 签名、加密载荷格式、工具调用 ID 差异、gpt-5.6-sol 条目、加密推理与 RL 训练的关系
- [muse-runtime-export](https://mouse.dev/blog/muse-runtime-export) — 导出方法与 2.7 GB 归档、113 条 subagent 记录、技能模块与记忆系统细节、Meta 将报告标为 Not Applicable
- [Hacker News 讨论串](https://news.ycombinator.com/item?id=49848095) — 社区反应(111 分/46 评论)、「兼容接口」质疑、自称 Meta 员工的留言
- [Introducing Muse Spark 1.1 - AI at Meta](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/) — 官方「自研」叙事,2026-07-09 发布,通篇未提第三方模型
