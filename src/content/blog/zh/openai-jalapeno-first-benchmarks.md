---
title: "第一代芯片就超过 Blackwell?先看清 Jalapeño 这份跑分是谁交的卷"
description: "OpenAI 公布自研推理芯片 Jalapeño 首批跑分:每瓦性能和延迟全面领先 Nvidia 现役系统。数字由 OpenAI 自己提供、场景只测了一小块,但即便打折,它改变的也是 2027 年的算力谈判桌。"
pubDate: 2026-08-25
tags: [ai-chips, openai, inference]
lang: zh
slug: openai-jalapeno-first-benchmarks
translationOf: openai-jalapeno-first-benchmarks
---

8 月 25 日,OpenAI 公布了自研推理芯片 Jalapeño 的第一份跑分([官方公告](https://openai.com/index/jalapeno-first-results/);[SemiAnalysis](https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia)、[TechCrunch](https://techcrunch.com/2026/08/25/openais-jalapeno-chip-is-built-for-fast-inference-at-scale-benchmarks-show/)、[The Register](https://www.theregister.com/systems/2026/08/25/openais-upcoming-jalapeno-chip-looks-like-itll-be-an-inference-beast/5292052) 当天均有报道,三家中只有 SemiAnalysis 提到做过现场验证,后面细说)。数字很扎眼:对比 Nvidia 现役旗舰 Blackwell 系统,Jalapeño 在峰值吞吐下每瓦多完成 1.5 到 1.9 倍的推理工作,端到端延迟低 1.7 到 3.6 倍,交互式任务快 2.1 到 4.1 倍。SemiAnalysis 的结论很直接:第一代芯片通常没有竞争力,而 OpenAI 在赢 Blackwell,甚至 Rubin。

芯片行业的常识恰恰站在这些数字的对面:第一代自研芯片通常没有竞争力,SemiAnalysis 那句判断的前半句说的就是这条行规。所以这份成绩单有两种解释:要么 OpenAI 破了常规,要么卷子本身有需要说明的地方。看完材料,我的结论是两者都对。

## 卷子是谁交的

先把测试本身拆开。这次用的是 SemiAnalysis 的公开基准 InferenceX,按 OpenAI 公告的说法,它衡量的是服务一条 AI 请求的完整过程(从收到请求到吐完全部回答),而非某个单点算力指标,测试覆盖 GPT-OSS 120B、DeepSeek R1、Kimi K2.5 三个开放权重模型。听起来足够第三方,但 SemiAnalysis 在自己的文章里写得很清楚:**全部数字由 OpenAI 提供**,SemiAnalysis 只是到 OpenAI 实验室现场验证了部分运行,没有独立跑完整套 InferenceX。相当于考生在自己家里答卷,监考老师上门抽查了几道题的演算过程。抽查比没有强,但这不是独立复测。

场景也窄。目前只测了 8k 输入、1k 输出的单一负载,而专门衡量长上下文、多轮 agent 任务的 AgentX 部分没有任何公开结果。生产环境里的推理远比 8k/1k 复杂:多轮对话、请求路由、缓存管理,这些都还没进考卷。

对比对象同样要打个折。Blackwell 是 [2024 年 3 月就发布](https://nvidianews.nvidia.com/news/nvidia-blackwell-platform-arrives-to-power-a-new-era-of-computing)的现役产品,而 Jalapeño 目前只有工程样品(流片回来用于调试验证的样品,不是量产版),按 [TechCrunch 的报道](https://techcrunch.com/2026/08/25/openais-jalapeno-chip-is-built-for-fast-inference-at-scale-benchmarks-show/),2026 年底才极小批量部署,2027 年放量。到那时它面对的已经是 Nvidia 下一代 Rubin 平台,首批 1 吉瓦定于 2026 下半年上线。OpenAI 硬件负责人 Richard Ho 也对 TechCrunch 承认了这一点:等 Jalapeño 全面部署时,对手可能已经前进了一大截。

不过给成绩单打完折,剩下的仍然可观。SemiAnalysis 指出,更公平的对比是同样用 HBM4 内存的 Rubin,而按其现场看到的数据,Jalapeño 在每兆瓦 token 产出上仍然领先,并且对手系统开启了多 token 预测(一种让模型一次猜多个 token 再快速验证的推理加速软件手段),Jalapeño 还没用上这项优化。Ho 的原话是:"归根结底,这些结果显示了非常、非常显著的性能推进。"

## 为什么第一代就能赢:解码只吃带宽

要理解 Jalapeño 为什么可能真的赢了,得先说清训练和推理的区别。训练是造模型,吃浮点算力。推理是把造好的模型跑起来回答请求,它又分两段:读入问题的预填充(prefill)阶段同样吃算力,逐个往外吐 token 的解码阶段则主要受内存带宽约束,[OpenAI 的公告](https://openai.com/index/jalapeno-first-results/)里也是按这两段分开讲的。解码时,通常每产出一个 token 都要把模型权重从显存搬进计算单元过一遍(稠密模型是全部权重,MoE 这类稀疏模型是被激活的那部分),算力单元大部分时间在闲着等数据。解码的瓶颈是带宽,不是算力。

Jalapeño 的规格(据 SemiAnalysis 和 The Register 披露)读起来就是押在这一点上的赌注:台积电 N3P 制程,单封装 216GB HBM4(第四代高带宽内存,把内存颗粒直接堆叠在芯片旁边以缩短数据路径),带宽 15.4TB/s,片上另配大容量 SRAM 缓存。OpenAI 称,包括 KV cache 在内的模型状态可以显式放置、留在芯片本地。KV cache 是对话上下文的中间计算结果,长对话和 agent 任务里每生成一个 token 都要反复读取的那部分数据。公告给出的设计目标,就是最小化数据搬运和通信延迟。反倒是原始算力不是这颗芯片的故事:SemiAnalysis 引用的 13.4 PFLOPS 4-bit 算力属于后续的 B0 步进,并非跑出这份成绩的 A0 芯片;The Register 算过,竞品机架系统的原始算力比它高 1.46 到 2 倍。这颗芯片没打算在算力上压过谁,筹码全押在搬数据上。

第一代就敢做这么极端的取舍,是因为它只对推理负责,不必像通用 GPU 那样同时兼顾训练和五花八门的客户负载。但有个容易想当然的误解要澄清:SemiAnalysis 特意指出,"Jalapeño 只能跑 OpenAI 自家模型"的说法是错的,它是能运行多种模型和负载的通用推理芯片,这次公开测试的三个模型就全是外部开放权重模型。OpenAI 真正独有的优势在软件:官方公告称,自家前沿模型参与了模型到芯片的映射、调度和底层 kernel 优化,选定的 GPT-OSS attention 和 MoE 模块的 AI 生成实现,比人工专家写的版本快 1.5 到 1.8 倍。SemiAnalysis 的判断值得转述:如果 Jalapeño 成功,说明行业对通用编程模型和通用编译器的执念,正在被"前沿模型自己写底层软件"的能力替代。至于 CUDA 生态的壁垒是否因此松动,SemiAnalysis 给的只是一个分析性判断,还不是已经发生的事实。

## 真正的账本:成本表与谈判桌

推理的单位经济学大致是:每百万 token 的成本 ≈(芯片折旧 + 电力散热 + 机房摊销)÷ token 产出。SemiAnalysis 称,OpenAI 当前的瓶颈是数据中心供电,不是预算,电是硬约束,所以"每瓦性能"直接决定同一座机房能产出多少 token。1.5 到 1.9 倍的每瓦提升,按同一测试口径换算,意味着同样的电至少多产一半的 token。

另一半账在采购价上。Nvidia 公司整体毛利率近年在七成到七成五之间([FY2025 全年 GAAP 毛利率 75%](https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2025/default.aspx))。这是公司整体口径,不能直接换算成某一张加速卡的利润,但足以说明买卡的价格里含着可观的利润空间。自研路线绕的正是这道毛利:Broadcom 自己也要赚一层,只是 SemiAnalysis 认为它低于 Nvidia 的水平,总拥有成本的优势有一部分正来自这个毛利差。具体能省多少,OpenAI 没有披露。每瓦性能和采购价两个杠杆叠加,才是 OpenAI 做芯片的完整算术。

但放量还要等上几年。Jalapeño 年底才小批量,与 Broadcom 的 [10 吉瓦自研加速器合作](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/)要到 2029 年底才建完。账本的 Nvidia 一侧已经改写过一次:2025 年 9 月签下的[至少 10 吉瓦 Nvidia 系统合作意向](https://openai.com/index/openai-nvidia-systems-partnership/)(Nvidia 原拟随部署进度渐进投资至多 1000 亿美元),在 2026 年 2 月被重组。据[《金融时报》报道](https://finance.yahoo.com/news/nvidia-close-finalizing-30-billion-002456305.html),它变成了 Nvidia 在 OpenAI 最新一轮融资中约 300 亿美元的直接持股,而 OpenAI 预计会把这笔新资金的大部分花在 Nvidia 芯片上。再加上与 AMD 的 [6 吉瓦协议](https://ir.amd.com/news-events/press-releases/detail/1260/amd-and-openai-announce-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus)(附带最多 1.6 亿股认股权证),我的看法是:Jalapeño 短期内改变的更多是 OpenAI 的谈判位置,而非采购结构。一颗被第三方现场抽查过、账面确实能打的自研芯片,是采购谈判里最硬的外部选项。

Google 用 TPU 走过类似的路:TPU 在 [2016 年公开时已在内部数据中心运行一年多](https://cloud.google.com/blog/products/ai-machine-learning/google-supercharges-machine-learning-tasks-with-custom-chip)。Google 云上至今仍在采用 Nvidia 新一代 GPU(如[基于 Blackwell GB200 NVL72 的实例](https://www.tomshardware.com/tech-industry/artificial-intelligence/google-cloud-launches-first-blackwell-ai-gpu-powered-instances-72-way-gb200-with-72-b200-gpus-and-36-grace-cpus)),但按 Google [自己的说法](https://cloud.google.com/blog/transform/ai-specialized-chips-tpu-history-gen-ai),TPU 已是其几乎所有产品里 AI 负载的骨干。Google 不披露 GPU 采购是怎么谈的,但很难想象那些订单上桌时,背后没有这颗自研替代品撑着,这一句是我的推断。差别在于 Google [从 2017 年起把 TPU 放进云上外售](https://cloud.google.com/blog/topics/inside-google-cloud/google-cloud-offer-tpus-machine-learning),而 OpenAI 的芯片目前只计划部署在自家基础设施里;官方把收益算在响应速度、成本和运营弹性上,议价筹码则是最直接的即期收益。

还有一层对 agent 产品的直接意义。那组 2.1 到 4.1 倍的交互式任务提速,以及 DeepSeek R1 在单用户独占时超过 700 token/秒的单流速度,恰好踩在 agent 的痛点上:agent 任务是长串行链条,一步生成完才能走下一步,OpenAI 自己也说延迟会沿着步骤累积。模型输出提速,链条里花在生成上的时间就等比例缩短;工具调用、网络等待这些环节不会跟着变快,整条链未必按同样倍数提速,但响应体验和单位任务成本都会实打实改善。讽刺的是,专测长上下文多轮 agent 场景的 AgentX 恰恰没有公布结果。宣传上最受益的场景,正是数据上最空白的场景。这一块我没能在任何信源里找到补充数据,只能等 OpenAI 或 SemiAnalysis 放出。

## 该盯什么

接下来值得盯三个信号。一是 AgentX 和长上下文数据何时公布,在此之前,agent 场景的收益只能按存疑处理。二是 2027 年的放量规模和良率:SemiAnalysis 称改进版 B0 芯片已送代工、预计每瓦性能再提升约 25%,但从工程样品到规模量产,良率和产能爬坡的关口都还在前面。三是价格动作:推理成本若真降下来,会不会反映到价签上。我的猜测是先体现在 OpenAI 自家 agent 产品的毛利里,再传导到 API 价格,这只是推演,目前没有公开定价计划可以佐证。

对 Nvidia,短期营收不是问题:即便按重组后的协议,OpenAI 也预计会把 Nvidia 那 300 亿美元中的大部分花回 Nvidia 芯片上,该买的还得买。我的判断是,这份跑分动摇的是定价假设:七成上下的毛利率,离不开客户手里没有可信替代品这个背景;当最大的客户拿出一颗第三方现场抽查过、按 OpenAI 提供的数据每瓦性能领先的自研芯片,这个毛利率就从技术定价变成了谈判定价。跑分可以打折,这件事打不了折。

## 参考来源

- [Jalapeño's first results show industry-leading speed and efficiency in AI inference](https://openai.com/index/jalapeno-first-results/) — OpenAI 官方公告(核心数字出处)
- [OpenAI Jalapeño: Better Than Nvidia Blackwell](https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia) — InferenceX 测试方法、验证范围与保留意见、芯片规格、B0 步进、分析与评论
- [OpenAI's Jalapeño chip is built for fast inference at scale, benchmarks show](https://techcrunch.com/2026/08/25/openais-jalapeno-chip-is-built-for-fast-inference-at-scale-benchmarks-show/) — Richard Ho 原话、部署时间表
- [OpenAI's upcoming Jalapeño chip looks like it'll be an inference beast](https://www.theregister.com/systems/2026/08/25/openais-upcoming-jalapeno-chip-looks-like-itll-be-an-inference-beast/5292052) — 芯片规格、与竞品算力/内存对比、专用化风险分析
- [OpenAI's first custom chip "Jalapeño" reportedly beats Nvidia's Blackwell and Rubin in inference benchmarks](https://the-decoder.com/openais-first-custom-chip-jalapeno-reportedly-beats-nvidias-blackwell-and-rubin-in-inference-benchmarks/) — 官方公告数字转述、与 Rubin 的对比及多 token 预测细节
- [OpenAI unveils its first custom chip, built by Broadcom](https://techcrunch.com/2026/06/24/openai-unveils-its-first-custom-chip-built-by-broadcom/) — 6 月首次发布背景、自研动机
- [OpenAI and Broadcom announce strategic collaboration to deploy 10 gigawatts of OpenAI-designed AI accelerators](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/) — 10GW 合作条款与时间表
- [OpenAI and NVIDIA announce strategic partnership to deploy 10 gigawatts of NVIDIA systems](https://openai.com/index/openai-nvidia-systems-partnership/) — 2025 年 9 月合作意向(后已重组)、Rubin 首吉瓦时间表
- [Nvidia close to finalizing $30 billion investment in OpenAI](https://finance.yahoo.com/news/nvidia-close-finalizing-30-billion-002456305.html) — 《金融时报》报道的 2026 年 2 月意向重组为约 300 亿美元股权投资
- [AMD and OpenAI Announce Strategic Partnership to Deploy 6 Gigawatts of AMD GPUs](https://ir.amd.com/news-events/press-releases/detail/1260/amd-and-openai-announce-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus) — AMD 6GW 协议与认股权证
- [NVIDIA Blackwell Platform Arrives to Power a New Era of Computing](https://nvidianews.nvidia.com/news/nvidia-blackwell-platform-arrives-to-power-a-new-era-of-computing) — Blackwell 2024 年 3 月发布
- [NVIDIA Announces Financial Results for Fourth Quarter and Fiscal 2025](https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2025/default.aspx) — FY2025 GAAP 毛利率 75%
- [Google supercharges machine learning tasks with TPU custom chip](https://cloud.google.com/blog/products/ai-machine-learning/google-supercharges-machine-learning-tasks-with-custom-chip) — TPU 2016 年公开时已内部运行一年多
- [Build and train machine learning models on our new Google Cloud TPUs](https://cloud.google.com/blog/topics/inside-google-cloud/google-cloud-offer-tpus-machine-learning) — 2017 年 TPU 向云客户开放
- [TPU transformation: A look back at 10 years of our AI-specialized chips](https://cloud.google.com/blog/transform/ai-specialized-chips-tpu-history-gen-ai) — TPU 是 Google 几乎所有产品 AI 负载的骨干
- [Google Cloud launches first Blackwell AI GPU-powered instances](https://www.tomshardware.com/tech-industry/artificial-intelligence/google-cloud-launches-first-blackwell-ai-gpu-powered-instances-72-way-gb200-with-72-b200-gpus-and-36-grace-cpus) — Google 云上持续采用 Nvidia 新一代 GPU
