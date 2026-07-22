---
title: "怎么制裁一个人人都能下载的文件？"
description: "财长 Bessent 威胁制裁『偷 IP』的中国开源模型。但芯片出口管制之所以能咬住，靠的是三个抓手——物理瓶颈、可追踪、可拦截。开源权重一个都没有。"
pubDate: 2026-07-21
tags: [ai-governance, us-china, open-source]
lang: zh
slug: sanctioning-open-weight-models
translationOf: sanctioning-open-weight-models
---

7 月 21 日，美国财政部长 Scott Bessent 在 Fox Business 的访谈里放了一句狠话：美国将仔细审查来自中国的开源 AI 模型有没有窃取知识产权，「如果我们看到海外模型在偷我们伟大公司的东西，我们有能力因为这种盗窃而制裁它们」（[TechCrunch](https://techcrunch.com/2026/07/21/us-threatens-sanctions-against-chinese-ai-models-over-ip-theft/)，[Bloomberg](https://www.bloomberg.com/news/articles/2026-07-21/bessent-says-us-will-scrutinize-chinese-ai-models-for-ip-theft)）。

先把一件事说清楚：这句话里，指控本身没有一个字是新的。「中国偷美国知识产权」是美国对华经贸政策讲了快十年的主线——2018 年 3 月，美国贸易代表办公室（USTR）的 301 调查报告认定中国在技术转让和知识产权上的做法「不合理、具歧视性」，那轮贸易战关税就是以此为法律依据开征的（[USTR](https://ustr.gov/about-us/policy-offices/press-office/press-releases/2018/march/section-301-report-chinas-acts)）。落到 AI 上还有刑事判例：前 Google 工程师 Linwei Ding 被控向中国公司转移 Google AI 超算基础设施的机密文件，2026 年 1 月被联邦陪审团裁定经济间谍罪和窃取商业机密罪全部成立，司法部称这是美国首例与 AI 相关的经济间谍定罪（[DOJ](https://www.justice.gov/usao-ndca/pr/former-google-engineer-found-guilty-economic-espionage-and-theft-confidential-ai)）。专门冲着中国 AI 模型来的「偷 IP」说法，也已经喊了一年半：2025 年 1 月底 DeepSeek 引爆市场那一周，白宫 AI 顾问 David Sacks 就公开说有「大量证据」表明 DeepSeek 蒸馏了 OpenAI 的模型（[Fortune](https://www.fortune.com/2025/01/29/deepseek-openais-what-is-distillation-david-sacks)）；商务部长提名人 Howard Lutnick 在参议院听证会上说得更直白——「他们偷了东西，他们闯了进来，他们拿走了我们的 IP」（[Washington Times](https://www.washingtontimes.com/news/2025/jan/29/commerce-secretary-nominee-howard-lutnick-lashes-c/)）；参议员 Josh Hawley 随即提出法案，要全面禁止美中之间的 AI 技术进出口与合作研究（[Hawley 官网](https://www.hawley.senate.gov/hawley-introduces-legislation-to-decouple-american-ai-development-from-communist-china/)）；海军、NASA、商务部和众议院则先后把 DeepSeek 逐出政府设备（[NBC News](https://www.nbcnews.com/business/business-news/us-lawmakers-move-ban-deepseek-government-devices-chinese-surveillance-rcna190965)）。一年半下来，真正落地的只有政府设备禁令，Hawley 的法案至今没有下文。所以 Bessent 带来的增量只有一个：**工具换了**。此前摆上台面的是设备禁令、立法提案、出口管制；把财政部的制裁权直接对准开源模型，据公开检索未见更早的先例。这篇文章要讨论的，正是这件新工具好不好使。

时点也不难读懂。Moonshot 的 Kimi K3 正在编程和 agent 任务上追赶 OpenAI 和 Anthropic 的旗舰模型；一周前，白宫 AI 顾问 David Sacks 公开警告中国开放权重模型正把中国推到前面（[Axios](https://www.axios.com/2026/07/17/sacks-kimi-open-source-weights-trump)）；一天前，Axios 报道政府内部正在辩论如何限制中国开源模型——考虑的工具包括实体清单、政府采购规则、行政令，而不是一刀切的禁令（[Axios](https://www.axios.com/2026/07/20/ai-us-china-open-source-kimi)）。另据 Bloomberg，美中计划 9 月举行特朗普任内首次官方 AI 对话。财长这句话，既是政策试探，也是谈判前的筹码。

但把这句话当真、往下推演一步，就会撞上一个财政部似乎还没想清楚的问题：**制裁的对象是一个权重文件——它可以被任何人免费下载、复制、微调。芯片管制那套剧本，抄不到这里来。**

## 「偷 IP」指的是什么

Bessent 说的不是黑客入侵，而是「蒸馏」（distillation）：用一个强模型的输出当训练数据，去调教自己的模型——相当于让学生模型大量「抄」老师模型的答案，把能力低成本地转移过来。这条指控主要落在 DeepSeek 头上，公开证据有几层，成色各不相同。

最实的一层是访问记录：2025 年初，Microsoft 安全团队发现疑似与 DeepSeek 有关的账号通过 OpenAI 的 API 大规模抽取数据，OpenAI 随后展开调查（[The Hill](https://thehill.com/policy/technology/5113470-openai-deepseek-data-theft/)）。这类证据看的是谁在什么时候调了多少 API，跟模型输出像不像无关。

另一层是输出相似。DeepSeek V3 上线时被用户发现会自称 ChatGPT，连讲的笑话都和 GPT-4 一样（[TechCrunch](https://techcrunch.com/2024/12/27/why-deepseeks-new-ai-model-thinks-its-chatgpt/)）。但零星几个样本的雷同本身说明不了蒸馏：各家模型抓取的是同一片公开互联网，GPT-4 的输出早已大量混进网络语料，个别任务上撞车，很可能只是训练数据重合。真要指向蒸馏，得看大规模、跨任务的系统性相似。这方面有研究做过：一篇被 ACL 2025 接收的论文《Quantification of Large Language Model Distillation》用两个指标量化主流模型「像 GPT-4o 的程度」——一是模型会不会在身份问题上答错（比如自称 ChatGPT、说自己由 OpenAI 开发），二是大规模提示下的响应相似度。结果 DeepSeek-V3、Qwen-Max、GLM-4-Plus 两项得分都最高，而同为中国模型的豆包和美国的 Claude 几乎测不出可疑信号（[arXiv](https://arxiv.org/abs/2501.12619)）。这说明相似确实是系统性的，也说明它并非中国模型的普遍属性；但论文测的终究是相似度——高相似可以来自蒸馏，也可以来自数据重合，它能加重嫌疑，坐实不了「盗窃」。

国会层面的正式指控出现在 2025 年 4 月：美国众议院中共问题特别委员会发布 DeepSeek 调查报告，OpenAI 向委员会表示，DeepSeek 输出的「推理结构与措辞模式」与自家模型相似，并称对 DeepSeek 违反其禁止蒸馏的使用条款「有高度信心」（[委员会报告](https://chinaselectcommittee.house.gov/media/reports/deepseek-unmasked-exposing-the-ccp-s-latest-tool-for-spying-stealing-and-subverting-us-export-control-restrictions)）。但支撑这份「高度信心」的内部证据，OpenAI 至今没有公开。

把三层放在一起看：针对 DeepSeek 的蒸馏指控有异常 API 访问和系统性相似度两类公开依据，不算空穴来风；但一年半过去，公开证据仍停在「高度嫌疑」，没有一锤定音的实锤。至于 Kimi 这类此次真正处在风口上的开源模型，公开渠道连这种程度的证据都还没有。

这次 Bessent 加了一个新说法：许多中国模型上发现了美国大模型的「水印」。他没有说明是哪种水印，公开报道里也没有任何可查证的样本或技术细节——目前这只是一句断言。

还有两层含糊须点破。第一，蒸馏在法律上是什么性质并不清楚：用 API 输出训练竞品模型违反的是 OpenAI 的服务条款，属于违约；把它称作「盗窃」，在美国现行法下缺少明确依据——模型输出本身能否享有版权都还是悬而未决的问题。Linwei Ding 案能定罪，是因为被告偷的是 Google 内部的机密文件，证据链和法律定性都清楚；而蒸馏用的是模型公开卖的 API 输出，两者性质完全不同，前者的判例套不到后者头上。第二，指控别人偷数据的这一方，自己刚为训练数据付过大价钱：Anthropic 上周刚获批 15 亿美元和解，赔的正是盗版下载图书用于建库（[我此前的分析](/zh/anthropic-copyright-settlement-approved)）。「用别人的东西训练模型」这件事上，没有谁的手是干净的——区别只在偷的是书还是答案。

## 芯片管制为什么咬得住，权重为什么咬不住

对华芯片出口管制是这届和上届政府都用过的剧本，它之所以能产生实际约束，靠的是三个抓手：

**物理瓶颈。** 先进芯片的产能集中在极少数节点——最先进制程的代工、EUV 光刻机的供应，全球就那几家。卡住瓶颈，全链条都得停。

**可追踪。** 芯片是实物，有序列号、有报关单、有物流路径，卖了多少、发往哪里，账面可查。

**可拦截。** 货物要过海关。禁运的芯片被查到，可以扣下、罚没。

即便三个抓手都在，管制依然是漏的——H100 走私进中国的报道从未断过。而开源权重呢？**三个抓手一个都没有。** 复制的边际成本是零；一个几百 GB 的文件走网络传输，没有报关单。截至本文发稿，风口上的 Kimi K3 还只开放了 API 和聊天界面，权重尚未出现在 Moonshot 的 [Hugging Face 官方仓库](https://huggingface.co/moonshotai)；但它的前代 Kimi K2 系列和 DeepSeek 的权重，早已在 Hugging Face 和无数镜像、种子上扩散——已经落到全球开发者硬盘里的副本，任何行政令都收不回。更麻烦的是衍生物：有人下载权重、用自己的数据微调后再发布，这个新模型还算不算被制裁对象？再被别人二次蒸馏呢？制裁名单写得出公司名字，写不出一条能圈住衍生模型的边界。

## 制裁真正能咬到的地方

这不等于制裁毫无牙口——只是它咬到的不是下载这个动作。

财政部的工具是 OFAC（海外资产控制办公室）的 SDN 清单：一家公司上榜后，美国主体不得与其交易。落到开源模型上，实际后果是三层：Hugging Face 这样的美国平台大概率要下架其官方仓库；Together、Fireworks 等美国推理服务商必须停掉相应的托管 API；最重要的是，美国企业的法务部门会直接把「被制裁公司出品的模型」拉进黑名单——哪怕权重本身还躺在网上任人下载。

但制裁「代码本身」是有法律天花板的，先例就在财政部自己身上。2022 年 OFAC 制裁了混币器 Tornado Cash——不仅制裁运营者，还把一段部署在链上的开源智能合约直接列入清单。2024 年 11 月，第五巡回上诉法院裁定：不可变的开源代码不构成外国实体的「财产」，OFAC 无权制裁它（[判决书](https://www.ca5.uscourts.gov/opinions/pub/23/23-50669-CV0.pdf)）；2025 年 3 月，财政部把这些智能合约从清单上撤了下来（[OFAC 公告](https://ofac.treasury.gov/recent-actions/20250321)）。这是目前最接近的司法先例：**财政部可以制裁 Moonshot 这样的公司，但很难制裁一个已经开源的权重文件。** 文件一旦扩散，就不再是任何人的「财产」意义上的可制裁标的。

举证同样棘手。要制裁，先得证明蒸馏发生了。可如前所述，外部能拿到的只有相似度证据，而相似度是概率性的——高相似既可能来自刻意蒸馏，也可能只是因为公开网络语料里早已充斥 GPT-4 的输出，训练时无意「吃」了进去，研究者从外部无法区分这两种情形（[TechCrunch](https://techcrunch.com/2024/12/27/why-deepseeks-new-ai-model-thinks-its-chatgpt/)）。除非拿出 API 日志这类内部证据，「水印」式的输出指纹很难单独撑起一个制裁决定的举证责任。

## 制裁的真实产品：不是封锁，是合规寒蝉

把上面的机制串起来，可以给出一个相对确定的判断。

这类制裁管不住权重的流通——文件已经在全世界的硬盘里。它真正生产的东西是**合规不确定性**：美国企业的采购和法务流程厌恶模糊地带，只要「用中国开源模型」和「制裁风险」出现在同一句话里，大量美国公司就会主动回避，根本不需要禁令写得多严密。Axios 报道里官员们自己也说，走的是「更慢但更耐久」的路线：采购规则、安全要求、舆论施压，让美国企业用之前先掂量。制裁威胁是这套组合拳里声音最大的一记。

代价是市场分叉。而且要看清这个分叉的分量，得先看清一个现状：全球开源模型生态的重心已经在中国这边。新华社援引 Hugging Face 平台数据报道，阿里的 Qwen（千问）系列累计下载量在 2025 年 10 月就超过了 Meta 的 Llama，成为全球下载量最大的开放权重模型家族，2025 年 12 月单月下载量甚至超过其后八家（Meta、DeepSeek、OpenAI、Mistral 等）之和；据千问团队同期披露，社区基于千问微调的衍生模型已超过 18 万个（[新华社](https://english.news.cn/20260113/004b0522f987475cbf83ffc3a8d009aa/c.html)）。另据南华早报援引行业报告，到 2026 年 3 月，千问一家占了全球开源模型下载量的一半以上（[SCMP](https://www.scmp.com/tech/big-tech/article/3349552/alibabas-qwen-family-captures-over-50-global-open-source-downloads-report-finds)）。换句话说，今天一个团队要微调开源模型，起点多半已经是中国权重。在这个格局下，美国企业退回本土模型的同时，世界其他地区照样免费下载中国权重——对预算有限的全球开发者来说，被美国制裁点名甚至算一种广告。Sacks 反对限制时说得直白：领先的闭源实验室「想让政府替他们消灭开源竞争」（[Axios](https://www.axios.com/2026/07/17/sacks-kimi-open-source-weights-trump)）。这句话未必全对，但指出了同一个事实的另一面：制裁挡不住模型，只能改变谁用它。

所以这句威胁最合理的读法，不是一项即将落地的封锁政策，而是 9 月对话桌上的一枚筹码，外加一针给美国企业的预防性寒蝉剂。「偷 IP」的指控喊了一年半，动用的工具从设备禁令换到立法提案再换到制裁威胁，唯一不变的是：芯片管制好歹能让对手拿不到东西；对开源模型的制裁做不到这一点——它只能决定美国人用不用，而这恰恰是对美国 AI 生态自身影响最大的那个变量。

## 参考来源

- [US threatens sanctions against Chinese AI models over IP theft — TechCrunch](https://techcrunch.com/2026/07/21/us-threatens-sanctions-against-chinese-ai-models-over-ip-theft/) — Bessent 引语、Kimi K3/OpenAI/Anthropic 背景、访谈无执行细节
- [Bessent Says US to Scrutinize Chinese AI Models for IP Theft — Bloomberg](https://www.bloomberg.com/news/articles/2026-07-21/bessent-says-us-will-scrutinize-chinese-ai-models-for-ip-theft) — 原始报道：蒸馏与「水印」说法、9 月美中 AI 对话时点
- [Section 301 Report into China's Acts, Policies, and Practices — USTR (2018-03)](https://ustr.gov/about-us/policy-offices/press-office/press-releases/2018/march/section-301-report-chinas-acts) — 301 调查认定中国技术转让与知识产权做法不合理、具歧视性，为对华关税提供法律依据
- [Former Google engineer found guilty of economic espionage and theft of confidential AI technology — DOJ](https://www.justice.gov/usao-ndca/pr/former-google-engineer-found-guilty-economic-espionage-and-theft-confidential-ai) — Linwei Ding 案 2026 年 1 月定罪；司法部称系美国首例 AI 相关经济间谍定罪
- [What is distillation? — Fortune](https://www.fortune.com/2025/01/29/deepseek-openais-what-is-distillation-david-sacks) — Sacks 2025 年 1 月「大量证据表明 DeepSeek 蒸馏了 OpenAI 模型」表态
- [Commerce secretary nominee Howard Lutnick lashes out at China's suspected AI theft — Washington Times](https://www.washingtontimes.com/news/2025/jan/29/commerce-secretary-nominee-howard-lutnick-lashes-c/) — Lutnick 听证会「他们偷了东西」引语
- [Hawley Introduces Legislation to Decouple American AI Development from Communist China — 参议员 Hawley 官网](https://www.hawley.senate.gov/hawley-introduces-legislation-to-decouple-american-ai-development-from-communist-china/) — 2025 年初提出的美中 AI 脱钩法案（未获通过）
- [U.S. lawmakers move to ban China's DeepSeek from government devices — NBC News](https://www.nbcnews.com/business/business-news/us-lawmakers-move-ban-deepseek-government-devices-chinese-surveillance-rcna190965) — 政府设备禁令进展；海军、NASA 等机构先行禁用
- [The secret Trump administration battle to fight Chinese AI — Axios](https://www.axios.com/2026/07/20/ai-us-china-open-source-kimi) — 政府内部辩论、实体清单/采购规则/行政令的「更慢但更耐久」路线
- [David Sacks says Chinese open-weight AI models push China ahead — Axios](https://www.axios.com/2026/07/17/sacks-kimi-open-source-weights-trump) — Sacks 立场及「消灭开源竞争」引语
- [Moonshot AI 官方 Hugging Face 仓库](https://huggingface.co/moonshotai) — Kimi K2 系列权重已公开；截至发稿未见 K3 权重
- [Alibaba's Qwen leads global open-source AI community with 700 million downloads — Xinhua](https://english.news.cn/20260113/004b0522f987475cbf83ffc3a8d009aa/c.html) — 援引 Hugging Face 数据：Qwen 累计下载量 2025 年 10 月超过 Llama、2025 年 12 月单月下载超其后八家之和；千问团队披露衍生模型超 18 万个
- [Alibaba's Qwen family captures over 50% of global open-source downloads — SCMP](https://www.scmp.com/tech/big-tech/article/3349552/alibabas-qwen-family-captures-over-50-global-open-source-downloads-report-finds) — 援引行业报告：截至 2026 年 3 月 Qwen 占全球开源模型下载量一半以上
- [OpenAI investigating whether DeepSeek improperly obtained data — The Hill](https://thehill.com/policy/technology/5113470-openai-deepseek-data-theft/) — Microsoft 检测到 API 大规模抽取、OpenAI 调查
- [Why DeepSeek's new AI model thinks it's ChatGPT — TechCrunch](https://techcrunch.com/2024/12/27/why-deepseeks-new-ai-model-thinks-its-chatgpt/) — V3 自称 ChatGPT、数据污染与蒸馏难以区分
- [Quantification of Large Language Model Distillation — arXiv (ACL 2025)](https://arxiv.org/abs/2501.12619) — 身份认知与响应相似度两指标量化蒸馏程度；DeepSeek-V3、Qwen-Max、GLM-4-Plus 得分最高，豆包、Claude 最低
- [DeepSeek Unmasked — 美国众议院中共问题特别委员会调查报告](https://chinaselectcommittee.house.gov/media/reports/deepseek-unmasked-exposing-the-ccp-s-latest-tool-for-spying-stealing-and-subverting-us-export-control-restrictions) — OpenAI 对 DeepSeek 违反禁止蒸馏条款「有高度信心」及「推理结构与措辞模式」说法
- [Van Loon v. Department of the Treasury 第五巡回法院判决书](https://www.ca5.uscourts.gov/opinions/pub/23/23-50669-CV0.pdf) — 不可变开源代码不构成可制裁「财产」
- [OFAC Recent Actions 2025-03-21](https://ofac.treasury.gov/recent-actions/20250321) — Tornado Cash 智能合约从 SDN 清单移除
- [15 亿美元，买不来一个判例（本站）](/zh/anthropic-copyright-settlement-approved) — Anthropic 版权和解背景
