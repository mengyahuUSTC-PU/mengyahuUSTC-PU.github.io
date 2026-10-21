---
title: "The hard part of the DHS DeepSeek ban is one undefined word: implementation"
description: "A close read of the DHS FASCSA order covering DeepSeek's official app, cloud-hosted and self-hosted weights, and distilled models. It shows what the order clearly covers, what it leaves open, and what federal contractors now have to do."
pubDate: 2026-10-20
tags: [ai-governance, ai-policy, supply-chain-security]
lang: en
slug: deepseek-federal-ban-scope
translationOf: deepseek-federal-ban-scope
---

On October 20, the Department of Homeland Security published a notice in the Federal Register ([91 FR 66346](https://www.federalregister.gov/documents/2026/10/20/2026-21447/notice-of-order-regarding-exclusion-and-removal-of-deepseek-products-from-federal-civilian-executive)). The notice summarizes an order that does two things. Federal civilian agencies may no longer buy IT products or services from Hangzhou DeepSeek or its affiliates. Agencies that already use them have to remove them. The removal also covers "third-party products and services developed using DeepSeek implementations."

If the order stopped at DeepSeek's own app and API, it would be a one-line story. The second half is where it gets hard. DeepSeek publishes its weights under the MIT license ([Hugging Face model card](https://huggingface.co/deepseek-ai/DeepSeek-R1)). Cloud providers host them, and third parties distill and fine-tune them. Many products contain DeepSeek components and never send a packet to a server in Hangzhou.

## What the order says

The legal basis is the Federal Acquisition Supply Chain Security Act of 2018 (FASCSA, 41 U.S.C. 1321–1328). FASCSA lets DHS, the Department of Defense, and the Director of National Intelligence issue exclusion orders, which bar future purchases, and removal orders, which require agencies to take out what they already have. The DeepSeek order was issued by the Secretary of Homeland Security on the recommendation of the Federal Acquisition Security Council (FASC).

The text of the order appears in the Federal Register only as scanned image pages (pp. 66347–66350, [govinfo PDF](https://www.govinfo.gov/content/pkg/FR-2026-10-20/pdf/2026-21447.pdf)), and those pages have no text layer. The details about the order quoted below come from [Tech Times](https://www.techtimes.com/articles/329253/20261020/dhs-filed-deepseek-ban-28-days-after-agencies-lost-right-request-exceptions.htm). I could not check them word for word against the scan.

According to Tech Times, the order covers civilian executive agencies only. It excludes national security systems and Sensitive Compartmented Information facilities, which fall to DoD and the DNI. Tech Times reports two risk rationales. User data is stored on servers in China, and DeepSeek models "may contain malware or other security vulnerabilities." The third-party language covers products "built using DeepSeek implementations." Neither the text portion of the notice ([govinfo text version](https://www.govinfo.gov/content/pkg/FR-2026-10-20/html/2026-21447.htm)) nor the Tech Times account defines "implementation."

## Two rationales, two different perimeters

To work out whether your product is covered, you need to see how far each rationale reaches.

The first rationale is about data leaving the US. DeepSeek's privacy policy is blunt: the company will "directly collect, process and store your Personal Data in People's Republic of China" ([privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)). The policy covers DeepSeek's own apps, websites, software, and related services. It states that data from apps built by developers on DeepSeek's open platform falls outside the policy. So this rationale applies mainly where data goes to services DeepSeek operates itself, which means the official app and the official API.

The second rationale is about the model itself. The order doesn't say whether this risk travels with the weights. My inference is that if the worry is malware or vulnerabilities in the model, moving the model to a different machine doesn't remove that worry. AWS made R1 available as a fully managed model on Bedrock in March 2025, served from US regions ([AWS announcement](https://aws.amazon.com/about-aws/whats-new/2025/03/deepseek-r1-fully-managed-amazon-bedrock)). An agency that downloads the weights and runs them on its own network doesn't touch Chinese servers either. Both setups avoid the first rationale. On my reading, neither avoids the second.

Following the order's own logic, I'd group the cases like this:

- Official app and official API: clearly covered.
- DeepSeek models hosted by a cloud provider, and self-hosted open weights: I would treat these as in scope. The order publishes no definition that says whether they count as a "DeepSeek product" or a "DeepSeek implementation," though, so this is a legal interpretation and not a settled answer.
- Distilled models: unclear.

Distillation needs a closer look. DeepSeek's own R1-Distill models use Qwen2.5 and Llama 3.x as base models. According to the [model card](https://huggingface.co/deepseek-ai/DeepSeek-R1), they are "fine-tuned based on open-source models, using samples generated by DeepSeek-R1." Read literally, "developed using DeepSeek implementations" could cover them. Read against the second rationale, the case is weaker. The model card describes training another company's base model on R1's outputs and does not say R1's weights were used. That makes it hard to apply the worry about something hidden inside the model. One step further out are third parties that use R1 outputs as synthetic training data for their own models. An outsider looking only at the finished model usually can't tell. The text of the notice says nothing about model outputs, distillation, or synthetic data ([govinfo text version](https://www.govinfo.gov/content/pkg/FR-2026-10-20/html/2026-21447.htm)).

## Why only DeepSeek? Qwen, GLM, and European models

FASCSA orders are issued against one company at a time. The FASC first makes a recommendation. It then has to notify the named source, which gets 30 days from receipt to submit opposing information and arguments ([41 CFR 201-1.302](https://www.law.cornell.edu/cfr/text/41/201-1.302)). After that, DHS, DoD, and the DNI each decide whether to issue an order. This order names DeepSeek and its affiliates. It does not name Alibaba's Qwen or Zhipu's GLM, and it doesn't explain why DeepSeek was picked. Neither risk rationale is specific to DeepSeek. Qwen and GLM also publish weights on Hugging Face ([Qwen](https://huggingface.co/Qwen), [Zhipu's zai-org](https://huggingface.co/zai-org)), and the second rationale applies to them in the same way.

Not being named now doesn't mean they won't be named later. On September 8, NSA, CISA, and the FBI issued joint advisory AA26-251A. It accuses six Chinese companies of large-scale distillation of US frontier models: DeepSeek, Moonshot AI, Alibaba, MiniMax, StepFun, and Z.AI, which is Zhipu's international brand ([CISA advisory](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a)). The advisory gives detection and response advice to US AI companies and their cloud and API partners. It recommends no procurement measures. My guess is that if the FASC decides to run the process against any of these companies, a body of risk material is already on file.

On the defense side the scope is already wider. Section 1532 of the FY2026 NDAA, signed in December 2025, names DeepSeek and its parent High Flyer. It also defines a "covered AI company." That includes companies on the ITA's Consolidated Screening List or DoD's Section 1260H list of Chinese military companies, and companies domiciled in China, Russia, Iran, or North Korea ([statute text via AGORA](https://agora.eto.tech/instrument/2694)). Zhipu was added to the Commerce Department's Entity List in January 2025 ([Bloomberg](https://www.bloomberg.com/news/articles/2025-01-16/us-blacklists-tencent-backed-ai-startup-as-tech-curbs-deepen)), and the Entity List is part of the Consolidated Screening List ([ITA](https://www.trade.gov/consolidated-screening-list)). Alibaba was added to the 1260H list on June 8, 2026 ([WilmerHale](https://www.wilmerhale.com/en/insights/client-alerts/20260611-pentagon-adds-65-new-entities-to-the-1260h-list-of-chinese-military-companies)). On June 23 it sued DoD in federal court in San Jose to get the listing removed ([The Next Web](https://thenextweb.com/news/alibaba-sues-us-defense-department)).

Holland & Knight reads Section 1532 as prohibiting contractors, effective January 17, 2026, from using AI products developed by 1260H-listed entities when performing a DoD contract, unless they receive a waiver ([Holland & Knight](https://www.hklaw.com/en/insights/publications/2026/07/department-of-war-updates-section-1260h)). The statute text on AGORA reads differently. The contractor ban applies directly to DeepSeek and High Flyer AI. For other covered AI companies, it applies only after the Secretary of Defense finds a national security risk and issues guidance. I couldn't find any public DoD guidance under that provision.

European models are a different case. FASCSA doesn't draw lines by country. According to [Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2025/10/dni-issues-first-fascsa-exclusion-and-removal-order-against-acronis-ag), the first FASCSA order targeted Acronis, a Swiss company. A European model could therefore be the subject of an order, but someone would have to run the process above for it. In public summaries of FASCSA orders from law firms and trade press, I found no order covering a European model. I did not go through the full order list on SAM.gov line by line. Section 1532 covers only China, Russia, Iran, and North Korea, so European open-weight models fall outside it.

## What contractors owe

FASCSA orders reach contractors through FAR 52.204-30 ([clause text](https://www.acquisition.gov/far/52.204-30)). The main obligations:

Contractors "shall not provide or use as part of the performance of the contract" any covered article. If they find one, they report it to the contracting officer within 3 business days and follow up with mitigation and prevention information within 10 business days. They check SAM.gov for FASCSA orders at least once every three months, and the substance of the clause flows down to subcontracts. An order issued after the solicitation applies to an existing contract only once an amendment or modification adds it.

Here is the timeline. The filing line shows the notice was filed on October 19 at 8:45 a.m. and published on the 20th ([govinfo text version](https://www.govinfo.gov/content/pkg/FR-2026-10-20/html/2026-21447.htm)). The signing date and the exception window appear only in the scanned annex. [Tech Times](https://www.techtimes.com/articles/329253/20261020/dhs-filed-deepseek-ban-28-days-after-agencies-lost-right-request-exceptions.htm) reports that the order was signed on July 24 and that agencies had 60 days from signing to request exceptions, a window that closed on September 22. I couldn't confirm either date against the scan. The 60 days come from the order itself. The FASCSA rule says agencies may request exceptions in writing and sets no deadline ([41 CFR 201-1.304](https://www.law.cornell.edu/cfr/text/41/201-1.304)). The rule also leaves public disclosure of an order to the issuing official's discretion ([41 CFR 201-1.303](https://www.law.cornell.edu/cfr/text/41/201-1.303)), so it never required publication right after signing. Agencies have to stop new purchases. Neither the notice text nor Tech Times gives a deadline for finishing removal.

Contractors are bound through the contract. New solicitations include applicable orders under the FAR clause, and existing contracts pick up the order formally when the contracting officer issues a modification. The clause's duties to check SAM.gov, make a reasonable inquiry, and report already apply before any modification. The reporting clock starts when the contractor identifies the problem or is notified. Take a vendor that sells document-drafting or customer-service software to a federal agency and calls the DeepSeek API inside the product. Once it identifies that, it has 3 business days to report and 10 more to send mitigation and prevention details.

One design choice decides how the gray areas will play out in practice. The clause requires a "reasonable inquiry," and the definition states that this "excludes the need to include an internal or third-party audit." When contractors see a new order that might touch their supply chain, they have to ask questions, but they don't have to audit. Suppose a SaaS vendor's model was trained on R1-generated synthetic data and the vendor doesn't disclose it. A downstream contractor that asks may get no useful answer, and the clause doesn't require it to dig further.

Compared with earlier bans, this order is narrower in one respect and broader in another. It is narrower on "use." Part B of Section 889, aimed at Huawei, ZTE, and similar telecom equipment, bars agencies from contracting with any entity that uses covered equipment "regardless of whether that use is in performance of work under a Federal contract" ([FAR 52.204-25](https://www.acquisition.gov/far/52.204-25)). The FASCSA clause covers only use in contract performance, and whether a given use counts depends on the purpose, the system involved, and the deliverable. It is broader on the target. The TikTok ban names one application and its successors ([FAR 52.204-27](https://www.acquisition.gov/far/52.204-27)), so compliance is a name lookup. The DeepSeek order is listed on SAM.gov, but what it names is a source of technology. No list says which third-party products count as "DeepSeek implementations."

Earlier FASCSA orders were narrower. The DNI's order against Acronis, published in September 2025, covered intelligence community systems and a backup software vendor ([Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2025/10/dni-issues-first-fascsa-exclusion-and-removal-order-against-acronis-ag)). The DeepSeek order comes from DHS, covers civilian agencies, and targets a family of open-weight models.

## What to do about it

If you sell to federal civilian agencies, or supply someone who does:

Build your model inventory down to training lineage. Record the base model and also whether DeepSeek outputs were used for distillation or synthetic data. Treat the official API and hosted or self-hosted DeepSeek weights as in scope. Distillation and synthetic data are undefined territory. Even if you can't resolve them, write down the facts and wait for an interpretation from your contracting officer or CISA. If you sell to DoD, the scope is wider, and Qwen and GLM need a fresh review under Section 1532.

If you don't sell to the federal government, this order doesn't reach you directly. It does not cover private companies, state governments, or individual users.

The order makes a model's training origin a procurement attribute. Yet I found nothing in FAR 52.204-30 that requires anyone to verify training provenance, and its reasonable inquiry explicitly excludes audits. Two things to watch next: whether CISA issues guidance on what "implementation" means, and how GSA's procurement schedules handle models that used DeepSeek without saying so. The first will set how large the gray areas are. The second will decide who has to resolve them.

## References

- [Federal Register 91 FR 66346 (DHS-2026-0628)](https://www.federalregister.gov/documents/2026/10/20/2026-21447/notice-of-order-regarding-exclusion-and-removal-of-deepseek-products-from-federal-civilian-executive): order summary, legal basis, third-party language, issuing process
- [govinfo PDF](https://www.govinfo.gov/content/pkg/FR-2026-10-20/pdf/2026-21447.pdf): order annex (scanned images)
- [govinfo text version](https://www.govinfo.gov/content/pkg/FR-2026-10-20/html/2026-21447.htm): filing time (October 19) and publication date; the text does not define "implementation" or mention model outputs or synthetic data
- [41 CFR 201-1.302](https://www.law.cornell.edu/cfr/text/41/201-1.302): notice to named sources, 30-day response period
- [41 CFR 201-1.303](https://www.law.cornell.edu/cfr/text/41/201-1.303): notification duties after issuance; public disclosure at the issuing official's discretion
- [41 CFR 201-1.304](https://www.law.cornell.edu/cfr/text/41/201-1.304): agency exception requests, no fixed deadline
- [NSA/CISA/FBI joint advisory AA26-251A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a): distillation allegations against six Chinese AI companies
- [AGORA: FY2026 NDAA Section 1532](https://agora.eto.tech/instrument/2694): DoD prohibitions on DeepSeek, High Flyer, and "covered AI companies"
- [Bloomberg: Zhipu added to the Entity List](https://www.bloomberg.com/news/articles/2025-01-16/us-blacklists-tencent-backed-ai-startup-as-tech-curbs-deepen)
- [ITA: Consolidated Screening List](https://www.trade.gov/consolidated-screening-list): includes the Entity List
- [WilmerHale: June 2026 1260H list update](https://www.wilmerhale.com/en/insights/client-alerts/20260611-pentagon-adds-65-new-entities-to-the-1260h-list-of-chinese-military-companies): Alibaba added
- [The Next Web: Alibaba sues the Defense Department](https://thenextweb.com/news/alibaba-sues-us-defense-department): seeks removal from the 1260H list
- [Holland & Knight: 1260H update and Section 1532](https://www.hklaw.com/en/insights/publications/2026/07/department-of-war-updates-section-1260h): contractor use of AI from 1260H entities
- [Tech Times: signing date and exception window (from the scanned annex)](https://www.techtimes.com/articles/329253/20261020/dhs-filed-deepseek-ban-28-days-after-agencies-lost-right-request-exceptions.htm)
- [FAR 52.204-30](https://www.acquisition.gov/far/52.204-30): contractor obligations, reporting deadlines, reasonable inquiry without audit, flowdown
- [FAR 52.204-25](https://www.acquisition.gov/far/52.204-25): Section 889 coverage of "use"
- [FAR 52.204-27](https://www.acquisition.gov/far/52.204-27): scope of the TikTok ban
- [DeepSeek-R1 model card](https://huggingface.co/deepseek-ai/DeepSeek-R1): MIT license, distilled model bases and training method
- [Qwen on Hugging Face](https://huggingface.co/Qwen), [Zhipu zai-org on Hugging Face](https://huggingface.co/zai-org): publicly released Qwen and GLM models
- [DeepSeek privacy policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html): data stored in China
- [AWS: DeepSeek-R1 fully managed on Amazon Bedrock](https://aws.amazon.com/about-aws/whats-new/2025/03/deepseek-r1-fully-managed-amazon-bedrock): cloud hosting in US regions
- [Mayer Brown: DNI FASCSA order against Acronis](https://www.mayerbrown.com/en/insights/publications/2025/10/dni-issues-first-fascsa-exclusion-and-removal-order-against-acronis-ag): FASCSA precedent
