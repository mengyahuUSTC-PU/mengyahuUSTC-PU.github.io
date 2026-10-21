---
title: "DHS 的 DeepSeek 禁令，难点在「基于 DeepSeek 实现」这七个字"
description: "逐条读 DHS 的 FASCSA 命令：官方 App、云上托管、自部署权重、蒸馏模型，哪些被禁令覆盖，哪些还说不准，联邦承包商又要承担什么。"
pubDate: 2026-10-20
tags: [ai-governance, ai-policy, supply-chain-security]
lang: zh
slug: deepseek-federal-ban-scope
translationOf: deepseek-federal-ban-scope
---

10 月 20 日，美国国土安全部（DHS）在 Federal Register 发了一份通知（[91 FR 66346](https://www.federalregister.gov/documents/2026/10/20/2026-21447/notice-of-order-regarding-exclusion-and-removal-of-deepseek-products-from-federal-civilian-executive)）。通知摘要说了两件事。第一，联邦文职机构不得再采购杭州深度求索及其关联方的 IT 产品和服务。第二，已经在用的要移除。移除范围除了 DeepSeek 自家产品，还包括"使用 DeepSeek 实现开发的第三方产品和服务"（third-party products and services developed using DeepSeek implementations）。

如果只是 DeepSeek 自家的 App 和 API，这条新闻一句话就讲完了。麻烦在后半句。DeepSeek 的权重以 MIT 许可证公开（[Hugging Face 模型卡](https://huggingface.co/deepseek-ai/DeepSeek-R1)），云厂商在托管，第三方拿它做蒸馏、做微调。这些带着 DeepSeek 成分的产品，完全可以不连接杭州的服务器就跑起来。

## 命令本身说了什么

法律依据是 2018 年的《联邦采购供应链安全法》（FASCSA，41 U.S.C. 1321–1328）。这部法律允许 DHS、国防部和国家情报总监对有供应链风险的产品下达"排除令"和"移除令"：排除令管以后不能买，移除令管已经在用的要拆掉。这次的命令由 DHS 部长签发，依据是联邦采购安全委员会（FASC）的建议。

需要说明的是，命令正文在 Federal Register 里只有扫描图片附录（第 66347–66350 页，[govinfo PDF](https://www.govinfo.gov/content/pkg/FR-2026-10-20/pdf/2026-21447.pdf)），没有文字层。下面引用的几句附录内容来自 [Tech Times](https://www.techtimes.com/articles/329253/20261020/dhs-filed-deepseek-ban-28-days-after-agencies-lost-right-request-exceptions.htm) 的转录，扫描件本身我没能逐字核对。

据 Tech Times 转录，命令只覆盖文职机构。"国家安全系统"和敏感隔离信息系统不在范围内，那部分归国防部和情报总监管。转录列出的风险理由有两条：一是用户数据存放在中国的服务器上，二是 DeepSeek 模型"可能含有恶意代码或其他安全漏洞"。第三方条款覆盖的是"使用 DeepSeek 实现构建"的产品。至于"implementation"具体指什么，通知的文字部分没有定义（[govinfo 文本版](https://www.govinfo.gov/content/pkg/FR-2026-10-20/html/2026-21447.htm)），转录的附录内容里也没有。

## 两条理由，各自圈出不同的范围

判断你的产品算不算被覆盖，关键在于看清这两条理由各自管到哪里。

第一条是数据出境。DeepSeek 隐私政策写得很直白：个人数据"在中华人民共和国收集、处理和存储"（[DeepSeek 隐私政策](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)）。这份政策适用于 DeepSeek 自己运营的网站、App、软件和相关服务，并写明开发者在 DeepSeek 开放平台上构建的应用所产生的数据不归这份政策管。我的理解是，这条理由咬得最紧的，是数据会交给 DeepSeek 自营服务的用法，也就是官方 App 和官方 API。不过这只是我根据政策里数据最终去向做的推断：政策本身没这么说，命令也没有这样限定数据理由的范围。

第二条针对模型本身。命令没说这种风险会不会跟着权重文件走。不过我的推论是：如果担心的是模型里有恶意代码或漏洞，那么把模型搬到哪儿跑，都不会消除这个担忧。AWS 在 2025 年 3 月把 R1 作为全托管模型上架 Bedrock，跑在美国区域（[AWS 公告](https://aws.amazon.com/about-aws/whats-new/2025/03/deepseek-r1-fully-managed-amazon-bedrock)）。机构自己下载权重、部署在内网，同样不碰中国的服务器。这两种情形躲得开第一条理由，按我的推论躲不开第二条。

所以按命令自己的逻辑，我的分法如下，其中只有第一类是命令文本本身能定下来的：

- 官方 App、官方 API：明确覆盖。
- 云厂商托管的 DeepSeek 模型、自部署的开放权重：我倾向于按在范围内处理。但它们算不算"DeepSeek 产品"或"DeepSeek 实现"，命令没有公开定义。这是法律解释，不是定论。
- 蒸馏模型：说不准。

蒸馏这一类值得单独说。DeepSeek 官方发布的 R1-Distill 系列，底座是 Qwen2.5 和 Llama 3.x，用 R1 生成的样本微调而成（[模型卡](https://huggingface.co/deepseek-ai/DeepSeek-R1)）。按字面读，"使用 DeepSeek 实现开发"可以套上去。可按第二条理由读，模型卡描述的是拿 R1 的输出去微调别家底座，没有说用到 R1 的权重，"模型里藏东西"的担忧不好直接套用。再往外一层是第三方自己用 R1 的输出造合成数据、训练自家模型。只看最终模型，外人通常很难确认这一点。通知的文字部分没有单独提到模型输出、蒸馏或合成数据（[govinfo 文本版](https://www.govinfo.gov/content/pkg/FR-2026-10-20/html/2026-21447.htm)）。

## 为什么只有 DeepSeek：千问、智谱和欧洲模型

FASCSA 命令是一家一家下的。每一份都要先由 FASC 提出建议，再书面通知被点名的公司，对方有 30 天提交反驳材料（[41 CFR 201-1.302](https://www.law.cornell.edu/cfr/text/41/201-1.302)），之后 DHS、国防部、国家情报总监才各自决定签不签。这次的命令点名的是 DeepSeek 及其关联方，阿里的通义千问（Qwen）、智谱的 GLM 都不在其中。命令没有解释为什么只选 DeepSeek。上面两条风险理由也不是 DeepSeek 独有：千问和 GLM 同样在 Hugging Face 上发布权重（[Qwen](https://huggingface.co/Qwen)、[智谱 zai-org](https://huggingface.co/zai-org)），第二条理由对它们一样说得通。

这次没点名，不代表以后不点。9 月 8 日，NSA、CISA、FBI 联合发布公告 AA26-251A，指认六家中国公司大规模蒸馏美国前沿模型：DeepSeek、月之暗面、阿里、MiniMax、阶跃星辰和 Z.AI（智谱的国际品牌）（[CISA 公告](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a)）。这份公告只给美国 AI 公司及其云服务和 API 合作方提了检测和应对建议，没有提任何采购措施。我的推断是，如果 FASC 要对这几家再走一遍流程，风险材料已经有现成的一份。

国防一侧的范围已经比文职宽。2025 年 12 月签署的 2026 财年 NDAA 第 1532 条，除了点名 DeepSeek 和它的母公司幻方（High Flyer），还定义了一类"受管辖 AI 公司"：上了商务部综合筛查名单或国防部 1260H"中国军事企业"名单的，注册在中国、俄罗斯、伊朗、朝鲜的，都算（[AGORA 收录的法条文本](https://agora.eto.tech/instrument/2694)）。智谱 2025 年 1 月被列入商务部实体清单（[Bloomberg](https://www.bloomberg.com/news/articles/2025-01-16/us-blacklists-tencent-backed-ai-startup-as-tech-curbs-deepen)），实体清单是综合筛查名单的一部分（[ITA 综合筛查名单说明](https://www.trade.gov/consolidated-screening-list)）。阿里 2026 年 6 月 8 日进了 1260H 名单（[WilmerHale 整理](https://www.wilmerhale.com/en/insights/client-alerts/20260611-pentagon-adds-65-new-entities-to-the-1260h-list-of-chinese-military-companies)），6 月 23 日在加州圣何塞联邦法院起诉国防部，要求撤销列名（[The Next Web](https://thenextweb.com/news/alibaba-sues-us-defense-department)）。律所 Holland & Knight 的解读是，自 2026 年 1 月 17 日起，1532 条禁止承包商在履行国防部合同时使用 1260H 名单企业开发的 AI，除非获得豁免（[Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/07/department-of-war-updates-section-1260h)）。但 AGORA 收录的法条文本读下来不一样：承包商禁令直接适用的只有 DeepSeek 和幻方；对其他受管辖 AI 公司，要先由国防部长认定存在国家安全风险并发布指引，禁令才适用。我在国防部和 DFARS 的公开材料里没找到这样的指引，不过也可能发在我没查到的地方。

欧洲模型的情况不一样。FASCSA 不按国别划线，据 [Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2025/10/dni-issues-first-fascsa-exclusion-and-removal-order-against-acronis-ag) 整理，第一份 FASCSA 命令针对的 Acronis 就是瑞士公司，所以欧洲公司的模型在法律上同样可以被下令。但那需要单独走一遍上面的流程。我在律所和行业媒体对 FASCSA 命令的公开整理里，没看到针对欧洲模型的命令；SAM.gov 上的完整命令清单我没有逐条核对。1532 条的受管辖国家只有中、俄、伊、朝四国，欧洲开放权重模型不在其中。

## 承包商要承担什么

FASCSA 命令落到承包商身上，走的是 FAR 52.204-30 条款（[条款原文](https://www.acquisition.gov/far/52.204-30)）。几处要点：

承包商"不得在合同履行中提供或使用"被命令覆盖的产品；发现在用的，3 个工作日内向合同官报告，10 个工作日内补交缓解和预防措施信息；至少每三个月查一次 SAM.gov 上的 FASCSA 命令；条款要逐级写进分包合同。另外，对已签的合同，新命令要经合同修订加进去才生效。

时间线是这样的。Federal Register 的归档行显示，这份通知 10 月 19 日上午提交、20 日刊出（[govinfo 文本版](https://www.govinfo.gov/content/pkg/FR-2026-10-20/html/2026-21447.htm)）。命令本身的签发日期和例外窗口只印在扫描附录里：据 [Tech Times](https://www.techtimes.com/articles/329253/20261020/dhs-filed-deepseek-ban-28-days-after-agencies-lost-right-request-exceptions.htm) 的转录，命令 7 月 24 日就已签发，机构申请例外的窗口是签发后 60 天，9 月 22 日已经关闭。这两个日期我没能在扫描件上逐字核对。60 天是命令自己定的：FASCSA 实施细则只规定机构可以书面申请例外，没有设天数（[41 CFR 201-1.304](https://www.law.cornell.edu/cfr/text/41/201-1.304)）。细则还把要不要公开命令交给签发官员决定（[41 CFR 201-1.303](https://www.law.cornell.edu/cfr/text/41/201-1.303)），所以在这一层，细则并没有要求签发后马上公开。对机构的要求是停止新采购。通知的文字部分和 Tech Times 的报道都没有给出移除必须完成的截止日期。

对承包商来说，命令要通过合同条款落实：新招标按 FAR 条款带上适用的命令，已签合同要等合同官发来修订才正式适用。但修订之前，条款里查询 SAM.gov、做合理询问和报告的义务已经在了。报告时限从承包商识别出问题或收到通知那天算起。比如一家给联邦机构卖公文写作或客服软件的公司，产品里调用了 DeepSeek API，一旦识别出来，就要在 3 个工作日内报告，10 个工作日内补交缓解和预防措施等信息。

有一处设计决定了灰色地带最后怎么落地。条款要求的是"合理询问"，定义里明说这种询问"不需要内部或第三方审计"。承包商发现可能影响自己供应链的新命令后，要去问；但不必审计。一个 SaaS 供应商的模型如果是用 R1 合成数据训练的，它自己不披露，下游承包商问了也未必问得出来，条款也不要求再往下查。

和先例放在一起看，这次的范围窄在一处、宽在另一处。窄的是"使用"：针对华为、中兴等电信设备的 889 条款 B 部分，禁止政府和任何使用涵盖设备的企业签约，哪怕这种使用和政府合同毫无关系（[FAR 52.204-25](https://www.acquisition.gov/far/52.204-25)）。FASCSA 条款只管合同履行中的使用，算不算履行，要看用途、所用系统和产出。宽的是"对象"：TikTok 禁令点名的是一个应用及其后继产品（[FAR 52.204-27](https://www.acquisition.gov/far/52.204-27)），照着名字就能查。FASCSA 命令要对照 [SAM.gov](https://sam.gov/supplychainorders) 上的清单核查，这份清单只提供下载，我没能在里面确认 DeepSeek 这一条。不管怎样，DeepSeek 命令点的是一类技术来源，哪些第三方产品算"DeepSeek 实现"，公开的通知没有附清单可对（[Federal Register](https://www.federalregister.gov/documents/2026/10/20/2026-21447/notice-of-order-regarding-exclusion-and-removal-of-deepseek-products-from-federal-civilian-executive)）。

这也不是 FASCSA 第一次被动用。2025 年 9 月，国家情报总监办公室对瑞士公司 Acronis 下过排除和移除令，范围是情报系统（据 [Mayer Brown 整理](https://www.mayerbrown.com/en/insights/publications/2025/10/dni-issues-first-fascsa-exclusion-and-removal-order-against-acronis-ag)）。DeepSeek 这份由 DHS 签发、覆盖文职机构，对象从一家备份软件公司换成了一个开放权重的模型家族。

## 关键结论

如果你的产品卖给联邦文职机构，或者是这类产品的上游：

先把模型清单列到"训练血统"这一层，不只写底座模型，还要写有没有用过 DeepSeek 的输出做蒸馏或合成数据。稳妥起见，官方 API 和托管或自部署的 DeepSeek 权重，按"在范围内"处理。蒸馏和合成数据属于未定义地带，处理不了也要把事实写下来，等合同官或 CISA 的解释。卖给国防部的，范围更宽，千问和 GLM 也要按 1532 条重新评估。

不卖给联邦的，这份命令不直接管你。它不覆盖私营企业、州政府和个人用户。

这份命令把"一个模型是用什么训练出来的"变成了采购属性。可 FAR 52.204-30 里我没看到要求核验训练来源的条款，它要的合理询问也明确不含审计。下一步值得盯的是 CISA 会不会对"implementation"出补充说明，以及 GSA 在采购目录里如何处理那些用过 DeepSeek 却没有标注的模型。前者决定灰色地带有多大，后者决定这些地带最后由谁来认定。

## 参考来源

- [Federal Register 91 FR 66346 通知（DHS-2026-0628）](https://www.federalregister.gov/documents/2026/10/20/2026-21447/notice-of-order-regarding-exclusion-and-removal-of-deepseek-products-from-federal-civilian-executive)：命令摘要、法律依据、第三方条款原文、签发流程
- [govinfo 版 PDF](https://www.govinfo.gov/content/pkg/FR-2026-10-20/pdf/2026-21447.pdf)：命令附录（扫描图片）
- [govinfo 文本版](https://www.govinfo.gov/content/pkg/FR-2026-10-20/html/2026-21447.htm)：通知提交时间（10 月 19 日）与刊出时间；文字部分未定义"implementation"，未提及模型输出或合成数据
- [41 CFR 201-1.302](https://www.law.cornell.edu/cfr/text/41/201-1.302)：FASC 建议须通知被点名方，30 天答辩期
- [41 CFR 201-1.303](https://www.law.cornell.edu/cfr/text/41/201-1.303)：命令签发后的通知义务，公开与否由签发官员决定
- [41 CFR 201-1.304](https://www.law.cornell.edu/cfr/text/41/201-1.304)：机构申请例外的程序，未设天数
- [CISA 等联合公告 AA26-251A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a)：六家中国 AI 公司的蒸馏指控
- [AGORA：2026 财年 NDAA 第 1532 条](https://agora.eto.tech/instrument/2694)：国防部对 DeepSeek、幻方及"受管辖 AI 公司"的禁用条款
- [Bloomberg：智谱被列入实体清单](https://www.bloomberg.com/news/articles/2025-01-16/us-blacklists-tencent-backed-ai-startup-as-tech-curbs-deepen)
- [ITA：综合筛查名单](https://www.trade.gov/consolidated-screening-list)：实体清单是其组成部分
- [WilmerHale：1260H 名单 2026 年 6 月更新](https://www.wilmerhale.com/en/insights/client-alerts/20260611-pentagon-adds-65-new-entities-to-the-1260h-list-of-chinese-military-companies)：阿里入列
- [The Next Web：阿里起诉美国国防部](https://thenextweb.com/news/alibaba-sues-us-defense-department)：要求撤销 1260H 列名
- [Holland & Knight：1260H 更新与 1532 条](https://www.hklaw.com/en/insights/publications/2026/07/department-of-war-updates-section-1260h)：对承包商使用 1260H 企业 AI 产品的解读
- [Tech Times：命令签发日期与例外申请窗口（扫描附录转录）](https://www.techtimes.com/articles/329253/20261020/dhs-filed-deepseek-ban-28-days-after-agencies-lost-right-request-exceptions.htm)
- [FAR 52.204-30](https://www.acquisition.gov/far/52.204-30)：承包商义务、报告时限、"合理询问"不含审计、分包流转
- [FAR 52.204-25](https://www.acquisition.gov/far/52.204-25)：889 条款对"使用"的覆盖范围
- [FAR 52.204-27](https://www.acquisition.gov/far/52.204-27)：TikTok 禁令的涵盖范围
- [SAM.gov FASCSA 命令清单](https://sam.gov/supplychainorders)：现行命令清单（仅提供下载）
- [DeepSeek-R1 模型卡](https://huggingface.co/deepseek-ai/DeepSeek-R1)：MIT 许可证、蒸馏模型底座与训练方式
- [Qwen Hugging Face 主页](https://huggingface.co/Qwen)、[智谱 zai-org Hugging Face 主页](https://huggingface.co/zai-org)：千问、GLM 公开发布的模型
- [DeepSeek 隐私政策](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)：数据存储于中国
- [AWS：DeepSeek-R1 在 Bedrock 全托管上线](https://aws.amazon.com/about-aws/whats-new/2025/03/deepseek-r1-fully-managed-amazon-bedrock)：云端托管、美国区域
- [Mayer Brown：DNI 对 Acronis 的 FASCSA 命令](https://www.mayerbrown.com/en/insights/publications/2025/10/dni-issues-first-fascsa-exclusion-and-removal-order-against-acronis-ag)：FASCSA 先例

<!--
事实核查点（供作者审阅，不进正文）：
1. 时间线的政府一手来源核查结果（2026-10-21）：
   - 已用一手来源核实：govinfo 文本版归档行 "[FR Doc. 2026-21447 Filed 10-19-26; 8:45 am]"，10 月 20 日刊出；41 CFR 201-1.304 对例外申请不设天数；41 CFR 201-1.303 规定公开命令属签发官员裁量。
   - 未能在政府渠道拿到文字版：签发日 7/24、60 天例外窗口、两条风险理由和脚注措辞都只印在扫描附录里，正文目前只引 Tech Times 一家转录。Federal Register API 的 signing_date 字段为空，通知文字部分没有 DATES 节；govinfo 与 public inspection 两版 PDF 的附录都是无文字层的扫描图片；regulations.gov 上的签署件 DHS-2026-0628-0002 抓取返回 403；SAM.gov 的 FASCSA 命令清单要下载 CSV。
   - 建议：本地对 govinfo PDF 第 66347–66350 页跑 OCR，或登录 SAM.gov 下载 FASCSA Orders CSV。核实后可把正文的"据 Tech Times 转录"改为直接引用附录页码。
   - 媒体转录另称命令编号为 2026-01，由部长签署；这一点同样未经一手核实，所以没有写进正文。
2. 1532 条对"受管辖 AI 公司"的承包商禁令是否已直接生效：AGORA 法条文本显示以国防部长"认定风险并发布指引"为前提，Holland & Knight 读作自 2026-01-17 起已直接适用于 1260H 企业。正文已并列两种读法。建议查 congress.gov 的 P.L. 119-60 原文及国防部是否发布了相关指引。
3. 智谱入实体清单引的是 Bloomberg；一手来源是 BIS 2025 年 1 月 Federal Register 规则（https://public-inspection.federalregister.gov/2025-00704.pdf），可替换链接。阿里入 1260H 引的是律所整理，一手来源是国防部 1260H 名单公告；阿里起诉引的是 The Next Web，一手来源是加州北区联邦法院案卷。
4. 中文版新增了"为什么只有 DeepSeek"一节以及承包商时间线一段，英文版需同步；本次按核查报告做的修改（扫描附录来源降级为 Tech Times 单一转录、托管/自部署范围改为法律解释、合理询问义务、删除员工私用例子、SAM.gov 可查命令但无第三方清单、新增 Qwen/zai-org/ITA/The Next Web 引用）也要同步。
5. 篇幅已超过 2200 字。新增内容是用户点名要求的新信息，如需压缩，可以先删 Acronis 那段，它和新增一节的欧洲段落有部分重叠。
-->
