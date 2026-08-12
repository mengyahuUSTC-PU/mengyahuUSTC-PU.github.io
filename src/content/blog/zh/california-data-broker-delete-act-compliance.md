---
title: "「一键删除」刚成硬义务，91% 的数据经纪商连法定数字都没报齐"
description: "斯坦福团队查了加州 522 家注册数据经纪商：只有 9% 报齐法定透明度数字，64% 的请求流程给消费者使绊子，其中 30 多家正把数据卖给生成式 AI 开发者。"
pubDate: 2026-08-11
tags: [data-privacy, ai-governance, training-data]
lang: zh
slug: california-data-broker-delete-act-compliance
translationOf: california-data-broker-delete-act-compliance
---

2026 年 8 月，加州隐私保护局（[CPPA](https://cppa.ca.gov/)，加州专设的隐私执法机构）的「删除请求与退出平台」（DROP）进入强制阶段：加州居民在一个网站上提交一次请求，所有在册的数据经纪商就都要在 90 天内删掉这个人的数据（法定豁免情形除外），而且从 8 月 1 日起每 45 天必须登录平台处理一轮新请求（[CPPA：DROP 数据经纪商指引](https://privacy.ca.gov/drop-for-data-brokers/)、[DROP 消费者页](https://privacy.ca.gov/drop/)）。纸面上，美国还没有别的机制走到这一步：各州隐私立法的横向对比把加州的框架评为全美覆盖最广的一档（[Security.org 的州际对比](https://www.security.org/resources/digital-privacy-legislation-by-state/)）。

就在这个节点，[斯坦福 RegLab](https://reglab.stanford.edu/team-members/anna-maria-gueorguieva)、HAI 与华盛顿大学的研究者发了一篇标题相当不客气的论文：《Privacy Without Remedy》，权利在纸上，救济不存在（[arXiv:2605.21376](https://arxiv.org/abs/2605.21376)，已被 FAccT 2026 收录）。他们把当时加州注册在案的全部 522 家数据经纪商查了一遍，结论：完整履行法定透明度义务的，只有 9%。

先把名词说清。数据经纪商（[data broker](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240SB362)）是那类你从没直接打过交道、却一直在收集和转卖你个人数据的公司：购物记录、地理位置、房产、健康线索（[官方列举的类别](https://privacy.ca.gov/drop/)还包括搜索记录、社会安全号码等），打包卖给广告商、保险公司、催收机构。加州 2018 年的 [CCPA](https://oag.ca.gov/privacy/ccpa)（加州消费者隐私法）给了居民删除、查询、退出出售等权利；2023 年的 [Delete Act](https://cppa.ca.gov/announcements/2023/20231011.html) 更进一步，把数据经纪商注册制度交到 CPPA 手里，要求经纪商每年注册，并公开报告五类权利请求的处理数据——收到、履行、拒绝了多少条请求，处理时长的平均数和中位数——每年 7 月 1 日前挂到自己的隐私政策页上，首个截止日是 2025 年 7 月 1 日（[SB 362 法案原文](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240SB362)）。

## 9% 是怎么量出来的

研究团队做了两件事。第一件，逐家人工核对 522 家注册经纪商的隐私政策，看五类指标是否报齐。报齐的只有 9.2%。拆开看也不乐观：报了删除请求数据的 53%，报了退出出售请求的 53%，报了「知悉数据被卖给谁」的只有 36%。还有约 45% 的经纪商一条权利请求数据都没报——论文特意指出，这说不清是真没有消费者找上门，还是压根没统计。两种情况对监管者是完全不同的信号，但现在没人分得清。

第二件事更能说明问题。团队抽了 250 家经纪商，实际走一遍消费者提交权利请求的流程。结果：43% 的经纪商让人无法完整行使法律给的全部权利；64% 的流程里至少有一处明显增加摩擦的设计，也就是常说的「暗模式」（dark pattern）——界面上故意给你使绊子，让你想办的事办不成。绊子长什么样，论文列得很具体：43% 要求把内容相同的表格重复填好几份；37% 对退出出售请求强加身份验证，而 CCPA 明文禁止对这类请求验明身份（[Hunton 对福特案的分析](https://www.hunton.com/privacy-and-cybersecurity-law-blog/calprivacy-reaches-settlement-with-ford-motor-company-over-ccpa-opt-out-right-violations)）；21% 塞验证码，最夸张的一家要连续解八个；10% 的提交入口干脆是坏链接。还有消费者提交请求后，确认邮件从一家从没听说过的公司发来，你都不知道请求到底进了谁的系统。

## 罚则打偏了

为什么两年了合规率还是个位数？论文的诊断落在罚则结构上：Delete Act 的罚款打在两件事上——没注册（每天罚 200 美元），以及 DROP 之下不处理删除请求；但「注册了却不报数」没有单列的罚款。也就是说，交注册费是有成本的，糊弄透明度义务几乎不用付出代价。消费者个人对这类违规也没有起诉权（法律术语叫 private right of action，即个人直接把违法企业告上法庭的资格——CCPA 只在特定数据泄露场景给了个人诉权，透明度违规不在其列），发现违规只能向 CPPA 举报，然后排队等它有限的执法资源。

参与领导这项研究的 Jennifer King 把话说得很直：「没有明确的报告要求和稳定兑现的财务后果，企业就是不会做。」（[Stanford HAI](https://hai.stanford.edu/news/companies-that-buy-and-sell-your-data-are-not-following-californias-strict-privacy-laws)）

执法不是完全没有。2026 年 3 月，CPPA 对福特开出 375,703 美元罚单，理由正是「使绊子」：福特要求消费者点邮件确认链接才处理退出请求，不点就当没提过（[CPPA 官方通报](https://privacy.ca.gov/2026/03/ford-to-change-practices-pay-fine-for-adding-unnecessary-friction-to-opt-out-process/)）。福特这单走的是 CCPA、不是针对数据经纪商的 Delete Act，但它说明监管方已经开始把程序性摩擦本身当违法行为来罚。问题在于覆盖面：CPPA 在 2026 年 1 月对两家未注册的经纪商开了罚单，并称还有十多起类似执法在推进（[CPPA 执法通报](https://cppa.ca.gov/announcements/2026/20260108.html)），但执法一单一单开，对面是 600 多家注册经纪商和不知多少家没注册的。论文写到执法资源有限就停了，往下这笔账是我自己算的：摊到每一家头上，被查的概率低到很难构成威慑。

## 上游漏水，AI 在下游接水

这项研究最值得 AI 从业者注意的一个细节，藏在注册表里：2025 年 10 月签署的 [SB 361 修正案](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260SB361)要求经纪商从 2026 年起在注册时披露，过去一年是否向生成式 AI 系统的开发者出售或共享过个人数据——目前已有 30 多家承认在做这门生意（[Stanford HAI](https://hai.stanford.edu/news/companies-that-buy-and-sell-your-data-are-not-following-californias-strict-privacy-laws)）。

把两组事实摆在一起看：一边是删除权的执行链条大面积失灵，一边是同一批公司正在给 AI 训练管线供货。论文写到披露这一步就停了，往下是我的推演：删除权是对着经纪商的数据库行使的，你让它删，它删的是自己库里的记录。Delete Act 把删除义务延伸到了经纪商的服务商和承包商，但对已经买走数据的第三方只字未提（[SB 362 §1798.99.86](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240SB362)）。所以如果这份数据在你提交请求之前已经卖给了某家 AI 公司，请求追不到那里。等模型训完，数据的影响已经写进权重。事后清除不是做不到：拿掉这条数据从头重训一遍是有效的，「机器遗忘」（machine unlearning，从训练完的模型里定点移除某条数据的影响）也是个活跃的研究方向。但那种规模的重训很少现实可行，遗忘本身也仍是开放的研究课题——2026 年的综述仍在讨论遗忘效果如何验证、被遗忘的内容会不会被重新学回来等未解决问题（[Unlearning in LLMs](https://arxiv.org/abs/2601.13264)）——据我检索，尚未见任何主流模型厂商把它做成产品功能。也就是说，实践中删除权只有赶在数据进入训练集之前行使才最管用，而这项研究证明的恰恰是：在这个最关键的窗口里，权利大概率行使不了。

对做模型和做应用的人，这不只是伦理问题，是供应链尽调问题。从经纪商或数据供应商手里采购训练数据时，值得多问一句：这批数据里有没有本该被删除、却因为对方不处理请求而留下来的记录？加州的注册表和这篇论文提供了一个可查的起点——供应商在不在注册表上、透明度指标报没报、报出来的收到与履行数量是多少，现在都是公开信息。数据来源的合规瑕疵会不会传导成模型层的法律责任，我没有检索到直接判例，但监管方向已经把「卖给生成式 AI 开发者」单列成披露项，这个信号本身就说明监管者在往上游看。

对加州居民，我的判断是：DROP 值得用，一次提交覆盖 600 多家注册经纪商（[官方 DROP 页](https://privacy.ca.gov/drop/)），比挨家挨户填表现实得多；但预期要放平——连最容易核查的透明度义务都只有 9% 的经纪商做齐，实际删除的履行情况只会更难说。而对看行业的人，这篇论文给出了一个可复用的方法：合规不合规，不听企业声明，去数它挂出来的数字、去走一遍它的流程。加州立了各州横向对比中公认全美覆盖最广一档的隐私法（[Security.org](https://www.security.org/resources/digital-privacy-legislation-by-state/)），然后用实测告诉所有人严法不等于严管。下一步值得盯的不是新法案，是 CPPA 会不会把福特那种罚单，开到数据经纪商头上。

## 参考来源

- [Privacy Without Remedy: An Assessment of Data Broker Compliance with California Privacy Law（arXiv:2605.21376）](https://arxiv.org/abs/2605.21376) — 核心数据：522 家、9.2% 合规率、45% 零申报、250 家流程实测与暗模式明细、罚则结构
- [Stanford HAI: Companies That Buy and Sell Your Data Are Not Following California's Strict Privacy Laws](https://hai.stanford.edu/news/companies-that-buy-and-sell-your-data-are-not-following-californias-strict-privacy-laws) — Jennifer King 引语、30+ 家经纪商披露向生成式 AI 开发者售数据
- [CPPA：DROP 数据经纪商指引](https://privacy.ca.gov/drop-for-data-brokers/) — 2026 年 8 月 1 日起每 45 天处理一轮请求的官方要求
- [CPPA：DROP 消费者页](https://privacy.ca.gov/drop/) — 一次请求覆盖 600 多家注册经纪商、90 天删除时限
- [CPPA 官方通报：福特罚款](https://privacy.ca.gov/2026/03/ford-to-change-practices-pay-fine-for-adding-unnecessary-friction-to-opt-out-process/) — 375,703 美元罚款金额及事由（退出请求强加邮件验证）
- [CPPA 执法通报：针对未注册数据经纪商的执法（2026 年 1 月）](https://cppa.ca.gov/announcements/2026/20260108.html) — 对未注册经纪商的罚款；10+ 起后续执法在推进
- [SB 362（Delete Act）法案原文](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240SB362) — 注册、年度透明度报告义务、罚则及删除义务的覆盖范围（§1798.99.86）
- [SB 361（Defending Californians' Data Act）法案原文](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260SB361) — 向生成式 AI 开发者售数的披露义务
- [Security.org：美国各州数字隐私立法对比](https://www.security.org/resources/digital-privacy-legislation-by-state/) — 称加州隐私框架为全美覆盖最广的依据
- [Unlearning in LLMs: Methods, Evaluation, and Open Challenges](https://arxiv.org/abs/2601.13264) — 机器遗忘仍属开放研究问题的综述依据
