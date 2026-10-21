---
title: "DHS 的 DeepSeek 禁令，难点在「基于 DeepSeek 实现」这七个字"
description: "逐条读 DHS 的 FASCSA 命令：官方 App、云上托管、自部署权重、蒸馏模型，哪些被禁令覆盖，哪些还说不准，联邦承包商又要承担什么。"
pubDate: 2026-10-20
tags: [ai-governance, ai-policy, supply-chain-security]
lang: zh
slug: deepseek-federal-ban-scope
translationOf: deepseek-federal-ban-scope
---

10 月 20 日，美国国土安全部（DHS）在 Federal Register 发了一份通知（[91 FR 66346](https://www.federalregister.gov/documents/2026/10/20/2026-21447/notice-of-order-regarding-exclusion-and-removal-of-deepseek-products-from-federal-civilian-executive)）。通知摘要说了两件事。第一，联邦文职机构不得再采购杭州深度求索及其关联方的 IT 产品和服务。第二，已经在用的要移除，移除范围除了 DeepSeek 自家产品，还包括"使用 DeepSeek 实现开发的第三方产品和服务"（third-party products and services developed using DeepSeek implementations）。

如果只是 DeepSeek 自家的 App 和 API，这条新闻一句话就讲完了。麻烦在后半句。DeepSeek 的权重以 MIT 许可证公开（[Hugging Face 模型卡](https://huggingface.co/deepseek-ai/DeepSeek-R1)），云厂商在托管，第三方拿它做蒸馏、做微调。大量产品身上都带着 DeepSeek 的成分，但它们和杭州的服务器没有任何连接。

## 命令本身说了什么

法律依据是 2018 年的《联邦采购供应链安全法》（FASCSA，41 U.S.C. 1321–1328）。这部法律允许 DHS、国防部和国家情报总监对有供应链风险的产品下达"排除令"和"移除令"：排除令管以后不能买，移除令管已经在用的要拆掉。这次的命令由 DHS 部长签发，依据是联邦采购安全委员会（FASC）的建议。

需要说明的是，命令正文在 Federal Register 里只有扫描图片附录（第 66347–66350 页），没有文字层。下面引用的几句原文来自多家媒体的转录，各家内容一致，但扫描件本身我没能逐字核对。

转录显示，命令只覆盖文职机构，"国家安全系统"和敏感隔离信息系统不在范围内，那部分归国防部和情报总监管。命令给了两条风险理由：一是 DeepSeek 的服务器在中国，二是"模型本身可能含有恶意代码或其他安全漏洞"。第三方条款还附了一条脚注，把范围扩展到"用于向文职机构提供产品和服务的 DeepSeek 第三方实现"。至于"implementation"具体指什么，命令没有定义。

## 两条理由，各自圈出不同的范围

判断你的产品算不算被覆盖，关键在于看清这两条理由各自管到哪里。

第一条是数据出境。DeepSeek 隐私政策写得很直白：个人数据"在中华人民共和国收集、处理和存储"（[DeepSeek 隐私政策](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)）。这条理由只管请求会发到 DeepSeek 服务器的用法，也就是官方 App 和官方 API。

第二条针对模型本身：权重里可能藏了东西，跑在哪儿都一样。这条理由会跟着权重文件走。AWS 在 2025 年 3 月把 R1 作为全托管模型上架 Bedrock，跑在美国区域（[AWS 公告](https://aws.amazon.com/about-aws/whats-new/2025/03/deepseek-r1-fully-managed-amazon-bedrock)）。机构自己下载权重、部署在内网，同样不碰中国的服务器。这两种情形躲得开第一条理由，躲不开第二条。

所以按命令自己的逻辑，可以这样分：

- 官方 App、官方 API：明确覆盖。
- 云厂商托管的 DeepSeek 模型、自部署的开放权重：两条理由占了一条，再加上那条脚注，基本可以认定在范围内。
- 蒸馏模型：说不准。

蒸馏这一类值得单独说。DeepSeek 官方发布的 R1-Distill 系列，权重底座是 Qwen2.5 和 Llama 3.x，用 R1 生成的样本微调而成（[模型卡](https://huggingface.co/deepseek-ai/DeepSeek-R1)）。按字面读，"使用 DeepSeek 实现开发"可以套上去；可按第二条理由读，这些模型里没有一个参数来自 DeepSeek 的权重，"模型里藏东西"的担忧很难成立。再往外一层是第三方自己用 R1 的输出造合成数据、训练自家模型。这种情况连训练者以外的人都无从知道。命令没有处理这一层。

## 为什么只有 DeepSeek：千问、智谱和欧洲模型

FASCSA 命令是一家一家下的。每一份都要先由 FASC 提出建议，再书面通知被点名的公司，对方有 30 天提交反驳材料（[41 CFR 201-1.302](https://www.law.cornell.edu/cfr/text/41/201-1.302)），之后 DHS、国防部、国家情报总监才各自决定签不签。这次走完流程的只有 DeepSeek 及其关联方，阿里的通义千问（Qwen）、智谱的 GLM 都不在命令里。命令没有解释为什么只选 DeepSeek。上面两条风险理由也不是 DeepSeek 独有：千问和 GLM 同样有开放权重，第二条理由对它们一样说得通。

这次没点名，不代表以后不点。9 月 8 日，NSA、CISA、FBI 联合发布公告 AA26-251A，指认六家中国公司大规模蒸馏美国前沿模型：DeepSeek、月之暗面、阿里、MiniMax、阶跃星辰和 Z.AI（智谱的国际品牌）（[CISA 公告](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a)）。这份公告只给美国 AI 公司提了检测和应对建议，没有提任何采购措施。我的推断是，如果 FASC 要对这几家再走一遍流程，风险材料已经有现成的一份。

国防一侧的范围已经比文职宽。2025 年 12 月签署的 2026 财年 NDAA 第 1532 条，除了点名 DeepSeek 和它的母公司幻方（High Flyer），还定义了一类"受管辖 AI 公司"：上了商务部综合筛查名单或国防部 1260H"中国军事企业"名单的，注册在中国、俄罗斯、伊朗、朝鲜的，都算（[AGORA 收录的法条文本](https://agora.eto.tech/instrument/2694)）。智谱 2025 年 1 月被列入商务部实体清单（[Bloomberg](https://www.bloomberg.com/news/articles/2025-01-16/us-blacklists-tencent-backed-ai-startup-as-tech-curbs-deepen)），实体清单是综合筛查名单的一部分。阿里 2026 年 6 月 8 日进了 1260H 名单，目前正在起诉国防部要求撤销（[WilmerHale 整理](https://www.wilmerhale.com/en/insights/client-alerts/20260611-pentagon-adds-65-new-entities-to-the-1260h-list-of-chinese-military-companies)）。律所 Holland & Knight 的解读是，1532 条已经禁止国防承包商在合同履行中使用 1260H 名单企业的 AI 产品（[Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/07/department-of-war-updates-section-1260h)）。按法条文本，这一层要先由国防部长认定风险并发布指引。指引有没有发布，我没查到。

欧洲模型的情况不一样。FASCSA 不按国别划线，第一份 FASCSA 命令针对的 Acronis 就是瑞士公司，所以欧洲公司的模型在法律上同样可以被下令。但那需要单独走一遍上面的流程，目前公开渠道里没有针对任何欧洲模型的命令。1532 条的受管辖国家只有中、俄、伊、朝四国，欧洲开放权重模型不在其中。

## 承包商要承担什么

FASCSA 命令落到承包商身上，走的是 FAR 52.204-30 条款（[条款原文](https://www.acquisition.gov/far/52.204-30)）。几处要点：

承包商"不得在合同履行中提供或使用"被命令覆盖的产品；发现在用的，3 个工作日内向合同官报告，10 个工作日内补交缓解措施；至少每三个月查一次 SAM.gov 上的 FASCSA 命令；条款要逐级写进分包合同。另外，对已签的合同，新命令要经合同修订加进去才生效。

时间线是这样的。Federal Register 的归档行显示，这份通知 10 月 19 日上午提交、20 日刊出（[govinfo 文本版](https://www.govinfo.gov/content/pkg/FR-2026-10-20/html/2026-21447.htm)）。命令本身的签发日期和例外窗口只印在扫描附录里：据 [Tech Times](https://www.techtimes.com/articles/329253/20261020/dhs-filed-deepseek-ban-28-days-after-agencies-lost-right-request-exceptions.htm) 等多家媒体的转录，命令 7 月 24 日就已签发，机构申请例外的窗口是签发后 60 天，9 月 22 日已经关闭。这 60 天是命令自己定的：FASCSA 实施细则只规定机构可以书面申请例外，没有设天数（[41 CFR 201-1.304](https://www.law.cornell.edu/cfr/text/41/201-1.304)）。细则还把要不要公开命令交给签发官员决定（[41 CFR 201-1.303](https://www.law.cornell.edu/cfr/text/41/201-1.303)），所以签发近三个月后才公开并不违规。对机构的要求是立即停止新采购，公开报道里没有看到移除必须完成的截止日期。对承包商来说，时间从命令写进你的合同那天开始算：新招标会直接带上它，已签合同要等合同官发来修订。比如一家给联邦机构卖公文写作或客服软件的公司，产品里调用了 DeepSeek API，修订一生效，就要在 3 个工作日内报告、10 个工作日内交出替换或缓解方案。

有一处设计决定了灰色地带最后怎么落地。条款要求的是"合理询问"，定义里明说这种询问"不需要内部或第三方审计"。也就是说，承包商只对自己已知的情况负责。一个 SaaS 供应商的模型如果是用 R1 合成数据训练的，只要它不披露，下游承包商没有义务、也没有手段查出来。

和先例放在一起看，这次的范围窄在一处、宽在另一处。窄的是"使用"：针对华为、中兴等电信设备的 889 条款 B 部分，禁止政府和任何使用涵盖设备的企业签约，哪怕这种使用和政府合同毫无关系（[FAR 52.204-25](https://www.acquisition.gov/far/52.204-25)）。FASCSA 条款只管合同履行中的使用，承包商员工私下用 DeepSeek 写代码，只要不进入合同交付，就不在条款范围内。宽的是"对象"：TikTok 禁令点名的是一个应用及其后继产品（[FAR 52.204-27](https://www.acquisition.gov/far/52.204-27)），名单可以照着查；DeepSeek 命令点的是一类技术来源，没有名单可查。

这也不是 FASCSA 第一次被动用。2025 年 9 月，国家情报总监办公室对瑞士公司 Acronis 下过排除和移除令，范围是情报系统（据 [Mayer Brown 整理](https://www.mayerbrown.com/en/insights/publications/2025/10/dni-issues-first-fascsa-exclusion-and-removal-order-against-acronis-ag)）。DeepSeek 这份是 DHS 在文职一侧的对应动作，对象从一家备份软件公司换成了一个开放权重的模型家族。

## 关键结论

如果你的产品卖给联邦文职机构，或者是这类产品的上游：

先把模型清单列到"训练血统"这一层，不只写底座模型，还要写有没有用过 DeepSeek 的输出做蒸馏或合成数据。官方 API 和托管或自部署的 DeepSeek 权重，按"在范围内"处理。蒸馏和合成数据属于未定义地带，处理不了也要把事实写下来，等合同官或 CISA 的解释。卖给国防部的，范围更宽，千问和 GLM 也要按 1532 条重新评估。

不卖给联邦的，这份命令不直接管你。它不覆盖私营企业、州政府和个人用户。

这份命令把"一个模型是用什么训练出来的"变成了采购属性，但联邦采购体系里目前没有任何字段、任何检测标准能核验这件事。下一步值得盯的是 CISA 会不会对"implementation"出补充说明，以及 GSA 在采购目录里如何处理那些用过 DeepSeek 却没有标注的模型。前者决定灰色地带有多大，后者决定这些地带最后由谁来认定。

## 参考来源

- [Federal Register 91 FR 66346 通知（DHS-2026-0628）](https://www.federalregister.gov/documents/2026/10/20/2026-21447/notice-of-order-regarding-exclusion-and-removal-of-deepseek-products-from-federal-civilian-executive)：命令摘要、法律依据、第三方条款原文、签发流程
- [govinfo 版 PDF](https://www.govinfo.gov/content/pkg/FR-2026-10-20/pdf/2026-21447.pdf)：命令附录（扫描图片）
- [govinfo 文本版](https://www.govinfo.gov/content/pkg/FR-2026-10-20/html/2026-21447.htm)：通知提交时间（10 月 19 日）与刊出时间
- [41 CFR 201-1.302](https://www.law.cornell.edu/cfr/text/41/201-1.302)：FASC 建议须通知被点名方，30 天答辩期
- [41 CFR 201-1.303](https://www.law.cornell.edu/cfr/text/41/201-1.303)：命令签发后的通知义务，公开与否由签发官员决定
- [41 CFR 201-1.304](https://www.law.cornell.edu/cfr/text/41/201-1.304)：机构申请例外的程序，未设天数
- [CISA 等联合公告 AA26-251A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a)：六家中国 AI 公司的蒸馏指控
- [AGORA：2026 财年 NDAA 第 1532 条](https://agora.eto.tech/instrument/2694)：国防部对 DeepSeek、幻方及"受管辖 AI 公司"的禁用条款
- [Bloomberg：智谱被列入实体清单](https://www.bloomberg.com/news/articles/2025-01-16/us-blacklists-tencent-backed-ai-startup-as-tech-curbs-deepen)
- [WilmerHale：1260H 名单 2026 年 6 月更新](https://www.wilmerhale.com/en/insights/client-alerts/20260611-pentagon-adds-65-new-entities-to-the-1260h-list-of-chinese-military-companies)：阿里入列
- [Holland & Knight：1260H 更新与 1532 条](https://www.hklaw.com/en/insights/publications/2026/07/department-of-war-updates-section-1260h)：对承包商使用 1260H 企业 AI 产品的解读
- [Tech Times：命令签发日期与例外申请窗口（扫描附录转录）](https://www.techtimes.com/articles/329253/20261020/dhs-filed-deepseek-ban-28-days-after-agencies-lost-right-request-exceptions.htm)
- [FAR 52.204-30](https://www.acquisition.gov/far/52.204-30)：承包商义务、报告时限、"合理询问"不含审计、分包流转
- [FAR 52.204-25](https://www.acquisition.gov/far/52.204-25)：889 条款对"使用"的覆盖范围
- [FAR 52.204-27](https://www.acquisition.gov/far/52.204-27)：TikTok 禁令的涵盖范围
- [DeepSeek-R1 模型卡](https://huggingface.co/deepseek-ai/DeepSeek-R1)：MIT 许可证、蒸馏模型底座与训练方式
- [DeepSeek 隐私政策](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)：数据存储于中国
- [AWS：DeepSeek-R1 在 Bedrock 全托管上线](https://aws.amazon.com/about-aws/whats-new/2025/03/deepseek-r1-fully-managed-amazon-bedrock)：云端托管、美国区域
- [Mayer Brown：DNI 对 Acronis 的 FASCSA 命令](https://www.mayerbrown.com/en/insights/publications/2025/10/dni-issues-first-fascsa-exclusion-and-removal-order-against-acronis-ag)：FASCSA 先例

<!--
事实核查点（供作者审阅，不进正文）：
1. 时间线的政府一手来源核查结果（2026-10-21）：
   - 已用一手来源核实：govinfo 文本版归档行 "[FR Doc. 2026-21447 Filed 10-19-26; 8:45 am]"，10 月 20 日刊出；41 CFR 201-1.304 对例外申请不设天数；41 CFR 201-1.303 规定公开命令属签发官员裁量。
   - 未能在政府渠道拿到文字版：签发日 7/24 与 60 天例外窗口只印在扫描附录里。Federal Register API 的 signing_date 字段为空，通知文字部分没有 DATES 节；govinfo 与 public inspection 两版 PDF 的附录都是无文字层的扫描图片；regulations.gov 上的签署件 DHS-2026-0628-0002（"26-49174 S1 SIGNED DEEPSEEK R&E order"）抓取返回 403；SAM.gov 的 FASCSA 命令清单要下载 CSV，经 api.sam.gov 获取需 API key；dhs.gov、cisa.gov 未检索到新闻稿。
   - 建议：本地对 govinfo PDF 第 66347–66350 页跑 OCR，或登录 SAM.gov 下载 FASCSA Orders CSV 查看签发日期。核实后可把正文"据 Tech Times 等多家媒体的转录"改为直接引用附录页码。
   - 媒体转录另称命令编号为 2026-01，由部长签署；这一点同样未经一手核实，所以没有写进正文。
2. 1532 条对"受管辖 AI 公司"的承包商禁令是否已直接生效：AGORA 法条文本显示以国防部长"认定风险并发布指引"为前提，Holland & Knight 读作已直接适用于 1260H 企业。两者有出入，建议查 congress.gov 的 P.L. 119-60 原文及国防部是否发布了相关指引。
3. 智谱入实体清单引的是 Bloomberg；一手来源是 BIS 2025 年 1 月 Federal Register 规则，可替换链接。阿里入 1260H 引的是律所整理，一手来源是国防部 1260H 名单公告。
4. 中文版新增了"为什么只有 DeepSeek"一节以及承包商时间线一段，英文版需同步；本次时间线段新增的 41 CFR 201-1.303/304 两句也要同步。
5. 篇幅已超过 2200 字。新增内容是用户点名要求的新信息，如需压缩，可以先删 Acronis 那段，它和新增一节的欧洲段落有部分重叠。
-->
