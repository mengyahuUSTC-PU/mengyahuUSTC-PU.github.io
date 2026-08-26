---
title: "第一代芯片就超过 Blackwell?先看清 Jalapeño 这份跑分是谁交的卷"
description: "OpenAI 公布自研推理芯片 Jalapeño 首批跑分:每瓦性能和延迟全面领先 Nvidia 现役系统。数字由 OpenAI 自己提供、场景只测了一小块,但即便打折,它改变的也是 2027 年的算力谈判桌。"
pubDate: 2026-08-25
tags: [ai-chips, openai, inference]
lang: zh
slug: openai-jalapeno-first-benchmarks
translationOf: openai-jalapeno-first-benchmarks
---

8 月 25 日,OpenAI 公布了自研推理芯片 Jalapeño 的第一份跑分([官方公告](https://openai.com/index/jalapeno-first-results/),公告细节经 [SemiAnalysis](https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia)、[TechCrunch](https://techcrunch.com/2026/08/25/openais-jalapeno-chip-is-built-for-fast-inference-at-scale-benchmarks-show/)、[The Register](https://www.theregister.com/systems/2026/08/25/openais-upcoming-jalapeno-chip-looks-like-itll-be-an-inference-beast/5292052) 等多方交叉核实)。数字很扎眼:对比 Nvidia 现役旗舰 Blackwell 系统,Jalapeño 在峰值吞吐下每瓦多完成 1.5 到 1.9 倍的推理工作,端到端延迟低 1.7 到 3.6 倍,交互式任务快 2.1 到 4.1 倍。SemiAnalysis 创始人 Dylan Patel 的评价被到处引用:"第一代芯片通常没有竞争力,但 OpenAI 在赢 Blackwell,甚至 Rubin。"

芯片行业的常识恰恰是第一代自研芯片交学费:流片延期、良率爬坡、软件栈拖后腿,能跑通就算成功。所以这份成绩单只有两种解释:要么 OpenAI 破了常规,要么卷子本身有需要说明的地方。看完材料,我的结论是两者都对。

## 卷子是谁交的

先把测试本身拆开。这次用的是 SemiAnalysis 的公开基准 InferenceX,它衡量的是服务一条 AI 请求的完整过程(从收到请求到吐完全部回答),而非某个单点算力指标,测试覆盖 GPT-OSS 120B、DeepSeek R1、Kimi K2.5 三个开放权重模型。听起来足够第三方,但 SemiAnalysis 在自己的文章里写得很清楚:**全部数字由 OpenAI 提供**,SemiAnalysis 只是到 OpenAI 实验室现场验证了部分运行,没有独立跑完整套 InferenceX。相当于考生在自己家里答卷,监考老师上门抽查了几道题的演算过程。抽查比没有强,但这不是独立复测。

场景也窄。目前只测了 8k 输入、1k 输出的单一负载,而专门衡量长上下文、多轮 agent 任务的 AgentX 部分没有任何公开结果。生产环境里的推理远比 8k/1k 复杂:多轮对话、请求路由、缓存管理,这些都还没进考卷。

对比对象同样要打个折。Blackwell 是 2024 年就发布的现役产品,而 Jalapeño 目前只有工程样品(流片回来用于调试验证的样品,不是量产版),按 [TechCrunch 的报道](https://techcrunch.com/2026/08/25/openais-jalapeno-chip-is-built-for-fast-inference-at-scale-benchmarks-show/),2026 年底才极小批量部署,2027 年放量。到那时它面对的已经是 Nvidia 下一代 Rubin 平台,首批 1 吉瓦定于 2026 下半年上线。OpenAI 硬件负责人 Richard Ho 自己也承认这一点。

不过给成绩单打完折,剩下的仍然可观。SemiAnalysis 指出,更公平的对比是同样用 HBM4 内存的 Rubin,而按其现场看到的数据,Jalapeño 在每兆瓦 token 产出上仍然领先,并且对手系统开启了多 token 预测(一种让模型一次猜多个 token 再快速验证的推理加速软件手段),Jalapeño 还没用上这项优化。Ho 的原话是:"结果显示了对现有最先进水平非常、非常显著的性能推进。"

## 为什么第一代就能赢:推理只吃带宽

要理解 Jalapeño 为什么可能真的赢了,得先说清训练和推理的区别。训练是造模型,吃浮点算力;推理是把造好的模型跑起来回答请求。生成式模型每产出一个 token,都要把上百 GB 的模型权重从显存搬进计算单元过一遍,算力单元大部分时间在闲着等数据。推理的瓶颈是内存带宽,不是算力。

Jalapeño 的规格印证了这个取舍(据 SemiAnalysis 和 The Register 披露):台积电 3nm 制程,单芯片 216GB HBM4(第四代高带宽内存,把内存颗粒直接堆叠在芯片旁边以缩短数据路径),带宽 15.4TB/s,片上另配大容量 SRAM 缓存,用来就近存放 KV cache——对话上下文的中间计算结果,长对话和 agent 任务里每生成一个 token 都要反复读取的那部分数据。Ho 说得直接:"我们设计 Jalapeño 就是为了最小化数据搬运和通信延迟。"反倒是 13.4 PFLOPS 的 4-bit 算力并不突出,The Register 算过,竞品的算力比它高 1.5 到 2 倍。这颗芯片没打算在算力上压过谁,筹码全押在搬数据上。

第一代就敢做这么极端的取舍,原因只有一个:OpenAI 只需要伺候自家模型。通用 GPU 要兼顾所有客户的所有负载,自研芯片只对自己的负载特征负责,连编译器和底层算子优化都可以让自家前沿模型来写。Patel 的判断值得转述:如果 Jalapeño 成功,说明行业对通用编程模型和通用编译器的执念,正在被"前沿模型自己写底层软件"的能力替代。CUDA 生态的壁垒对"只跑自家模型的实验室"正在变薄,尽管对其余所有客户依然存在。

## 真正的账本:成本表与谈判桌

推理的单位经济学大致是:每百万 token 的成本 ≈(芯片折旧 + 电力散热 + 机房摊销)÷ token 产出。数据中心如今按供电容量规划,电是硬约束,所以"每瓦性能"直接决定同一座机房能产出多少 token。1.5 到 1.9 倍的每瓦提升,意味着同样的电至少多卖一半的 token。

另一半账在采购价上。Nvidia 公司整体毛利率近年长期在七成上下,买卡支出的大头是 Nvidia 的利润。自研芯片按 Broadcom 的开发和代工成本拿货,即便每瓦性能只是打平,单是绕开这层毛利,每 token 的折旧成本就能砍掉一大截。两个杠杆叠加,才是 OpenAI 做芯片的完整算术。

但近两年内,量变不了天。Jalapeño 年底才小批量,与 Broadcom 的 [10 吉瓦自研加速器合作](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/)要到 2029 年底才建完。同期 OpenAI 手里还压着与 Nvidia [至少 10 吉瓦的合作意向](https://openai.com/index/openai-nvidia-systems-partnership/)(Nvidia 拟随部署进度渐进投资至多 1000 亿美元),以及与 AMD 的 [6 吉瓦协议](https://ir.amd.com/news-events/press-releases/detail/1260/amd-and-openai-announce-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus)(附带最多 1.6 亿股认股权证)。三份协议放在一起看就明白:Jalapeño 短期内改变的不是采购结构,而是谈判位置。一颗被第三方现场看过、确实能打的自研芯片,是采购谈判里最硬的外部选项。

Google 用 TPU 走过同一条路:TPU 在 2016 年公开时已内部使用一年多,此后 Google 从没停止采购 Nvidia,但内部大负载逐步转到自家芯片上,之后的每一单采购都带着"我可以不买"的底气。差别在于 Google 还能把 TPU 放进云上外售,而 OpenAI 的芯片目前纯自用,议价是唯一的即期收益。

还有一层对 agent 产品的直接意义。那组 2.1 到 4.1 倍的交互式任务提速,以及 DeepSeek R1 在单用户独占时超过 700 token/秒的单流速度,恰好踩在 agent 的痛点上:agent 任务是长串行链条,一步生成完才能走下一步,模型输出快一倍,整条链就快一倍,响应体验和单位任务成本同时改善。讽刺的是,专测长上下文多轮 agent 场景的 AgentX 恰恰没有公布结果。宣传上最受益的场景,正是数据上最空白的场景。这一块我没能在任何信源里找到补充数据,只能等 OpenAI 或 SemiAnalysis 放出。

## 该盯什么

接下来值得盯三个信号。一是 AgentX 和长上下文数据何时公布,在此之前,agent 场景的收益只能按存疑处理。二是 2027 年的放量规模和良率:SemiAnalysis 称改进版 B0 芯片已送代工、预计性能再提升约 25%,但第一代芯片死在量产环节的远比死在跑分环节的多。三是价格动作:推理成本若真降下来,会先出现在 OpenAI 自家 agent 产品的毛利上,然后才传导到 API 价签。

对 Nvidia,这份跑分短期不动摇收入,OpenAI 自己还签着 10 吉瓦的采购意向。它动摇的是定价假设。过去 Nvidia 的七成毛利建立在"没有可信替代品"之上;当最大的客户拿出一颗第三方看过、每瓦性能领先的自研芯片,这个毛利率就从技术定价变成了谈判定价。跑分可以打折,这件事打不了折。

## 参考来源

- [Jalapeño's first results show industry-leading speed and efficiency in AI inference](https://openai.com/index/jalapeno-first-results/) — OpenAI 官方公告(核心数字出处,细节经下列多方交叉核实)
- [OpenAI Jalapeño: Better Than Nvidia Blackwell](https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia) — InferenceX 测试方法、验证范围与保留意见、芯片规格、B0 步进、Patel 评论
- [OpenAI's Jalapeño chip is built for fast inference at scale, benchmarks show](https://techcrunch.com/2026/08/25/openais-jalapeno-chip-is-built-for-fast-inference-at-scale-benchmarks-show/) — Richard Ho 原话、部署时间表
- [OpenAI's upcoming Jalapeño chip looks like it'll be an inference beast](https://www.theregister.com/systems/2026/08/25/openais-upcoming-jalapeno-chip-looks-like-itll-be-an-inference-beast/5292052) — 芯片规格、与竞品算力/内存对比、专用化风险分析
- [OpenAI's first custom chip "Jalapeño" reportedly beats Nvidia's Blackwell and Rubin in inference benchmarks](https://the-decoder.com/openais-first-custom-chip-jalapeno-reportedly-beats-nvidias-blackwell-and-rubin-in-inference-benchmarks/) — 官方公告数字转述、与 Rubin 的对比及多 token 预测细节
- [OpenAI unveils its first custom chip, built by Broadcom](https://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom/) — 6 月首次发布背景、自研动机
- [OpenAI and Broadcom announce strategic collaboration to deploy 10 gigawatts of OpenAI-designed AI accelerators](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/) — 10GW 合作条款与时间表
- [OpenAI and NVIDIA announce strategic partnership to deploy 10 gigawatts of NVIDIA systems](https://openai.com/index/openai-nvidia-systems-partnership/) — Nvidia 10GW 意向与至多 1000 亿美元投资、Rubin 首吉瓦时间表
- [AMD and OpenAI Announce Strategic Partnership to Deploy 6 Gigawatts of AMD GPUs](https://ir.amd.com/news-events/press-releases/detail/1260/amd-and-openai-announce-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus) — AMD 6GW 协议与认股权证
