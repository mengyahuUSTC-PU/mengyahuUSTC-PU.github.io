---
title: "From the crib to age 100: the baby monitor company that wants a lifelong file"
description: "What Nanit's AI camera actually collects, where the data flows, why HIPAA and COPPA don't reach it, and three questions parents should ask before buying one."
pubDate: 2026-08-26
tags: [privacy, consumer-ai, iot]
lang: en
slug: ai-baby-monitor-lifelong-data
translationOf: ai-baby-monitor-lifelong-data
---

In early August, Sapna Maheshwari published a New York Times feature on Nanit ([paywalled; Techmeme entry here](https://www.techmeme.com/260803/p8), headline: "Aw, It's Baby's First A.I. Surveillance System"). Nanit's flagship product is a camera mounted directly above the crib. HD video streams to Nanit's servers, machine learning logs the exact moment the baby's eyes open and close, and the app rolls it all up into charts: a nightly sleep score from 0 to 100, a sleep-efficiency percentage, minutes to fall asleep, number of times a parent got up in the night.

When Bruce Schneier [linked to the piece](https://www.schneier.com/blog/archives/2026/08/spyware-for-babies.html), his post title needed three words: "Spyware for Babies."

That sounds harsh. Look at the scale first, then decide.

## This is not a niche gadget

Nanit says it has one million daily active users and over $100 million in annual revenue (the company's own figures, as reported by the Times). In December 2025 it closed a [$50 million growth round](https://www.prnewswire.com/news-releases/nanit-raises-50m-to-expand-its-ai-powered-systems-giving-parents-real-time-insights-into-infant-health-and-development-302643439.html) led by Springcoast Partners, with Upfront Ventures and JVP participating.

The press release is plain about where the money goes: a "Parenting Intelligence System" rolling out in 2026 that moves beyond sleep to track breathing patterns, movement signatures, gross motor milestones, speech and language development, and "trends that may predict metabolic, emotional, or cognitive challenges." Two numbers in the release say more about the direction than the feature list does (both are company-reported, with no independent verification): Nanit claims over 5 billion hours of infant sleep data from more than one million babies across 100+ countries, and says more than 70% of its active camera users keep using the product past age four. CEO Anushka Salinas, in her own words: "We envision a future where people can track and access their comprehensive health data from birth to 100 years old."

Birth to 100. The baby monitor as a category is nearly ninety years old ([Zenith's Radio Nurse shipped in 1937](https://slate.com/human-interest/2013/02/zeniths-radio-nurse-designed-by-isamu-noguchi-was-the-worlds-first-baby-monitor.html)), and for most of that time it was a transmission device: a microphone by the crib, a speaker by the parent, and if the baby cries you hear it. Nanit's business is a different species. The device is an intake point; the product is a data platform. One detail the Times dug up makes the intent explicit: the consultancy that did Nanit's branding wrote in its own case study that the central challenge was "how to introduce this novel technology to the parenting market while transcending the negative connotations of 'surveillance.'"

## What the privacy policy lists

To judge a product like this, the privacy policy beats the marketing page, because the policy is written for regulators. I read [Nanit's](https://www.nanit.com/policies/privacy-policy) in full (last updated February 10, 2026). The collection list comes in three layers.

About parents: name, email, phone number, payment information, IP address, and the name of your home WiFi network. About the child: name, profile photo, gender, date of birth, plus whatever care logs parents enter by hand. About the nursery: video and audio recording, temperature, humidity, and computer-vision analysis of breathing motion during sleep.

Under purposes, alongside providing the service, sits a standard clause worth reading word by word: "legitimate interests" cover "direct marketing, research and development," including "custom audiences advertising" and cross-device tracking. Custom audiences is a routine ad-industry mechanism: an advertiser uploads its customer list (emails, phone numbers) to an ad platform, the platform matches those against its own user base, and the matched people get targeted ads ([Meta's documentation](https://www.facebook.com/business/help/112061095610075) describes the matching flow). Cross-device tracking stitches your phone, tablet, and laptop activity into a single profile. Nanit's policy doesn't name which platform it works with, but both practices are listed in black and white. Data from a tool that helps your baby sleep enters the targeted-advertising pipeline.

Nanit does say it does not sell personal information, but the sentence has a second half. The policy's position is that its practices don't meet the [CCPA definition of "sale"](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.140), while conceding that the third-party analytics tools it uses "may be construed as a 'sale.'" The CCPA defines sale more broadly than everyday usage: transferring personal information to a third party for "monetary or other valuable consideration" counts, and money doesn't have to change hands. So the accurate reading of the disclaimer is this: Nanit argues its practices fall short of the statutory definition, while acknowledging that data does flow to third-party analytics and advertising services.

Two more items. The policy gives no concrete retention period, only that data is kept "as long as you use our Services or as necessary to fulfill the purpose(s) for which it was collected." It also states outright that it does not honor browsers' Do Not Track signals. I looked for a clause restricting the use of video and audio for training AI models. There isn't one.

## The security is decent; security is not privacy

To be fair: the measures on Nanit's [security page](https://www.nanit.com/pages/privacy-security) are serious by consumer-product standards. Video is encrypted with 256-bit AES. Streams are push-only: Nanit's servers push video to your device, and nothing can pull video directly off the camera. Two-step verification is mandatory, not optional. The company states that general employees cannot access customer video streams, and recordings are stored in the cloud only if you opt into an Insights subscription.

All of that answers one question: can outsiders get in? The core privacy question is a different one: what does the company itself do with the data? Encryption stops hackers. It does not stop a business model. Product pages tend to blur these two questions together; parents evaluating the product should keep them apart.

There is a third question that gets less attention: whether the data is even accurate. The Times reports that the camera logs visits and crying episodes that never happened. And Columbia pediatrician Rebekah Diamond's worry in the piece cuts deeper than accuracy: "Parents are losing a little bit of the muscle of their own confidence and decision-making." When a score tells you every morning how last night went, you slowly substitute it for your own observation, even if you have no idea how the score is computed.

## Why regulation doesn't catch this

US privacy law mostly idles on this product category, and the reasons are worth taking apart.

HIPAA applies to ["covered entities"](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html): health plans, healthcare providers, healthcare clearinghouses. Nanit collects breathing and sleep data that looks a lot like medical data, but it is a consumer electronics company, so HIPAA does not reach it. The same data coming out of a hospital device gets HIPAA's full protection; coming off a camera above a crib, the remaining constraints are the company's own privacy policy, the FTC's general consumer-protection authority, and a patchwork of state privacy laws. That is an order-of-magnitude difference in protection.

COPPA looks on-point and also misses. Its core mechanism is verifiable parental consent: it exists to stop companies from collecting data online from children behind their parents' backs. Per the [FTC's own FAQ](https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions), COPPA covers information collected online from the child; information about a child that an adult volunteers is out of scope. With a baby monitor, the parent buys the camera, installs it, and types in the birth date. The statute never triggers. COPPA assumed the parent is the gatekeeper of the child's privacy; it did not anticipate a structure where the parent hands the data over. And the actual data subject, the baby, cannot exercise any rights until adulthood. If the camera stays in use, by the time the child can object, the file is eighteen years deep.

## Three questions parents can ask

At the practical level, I think evaluating any product in this category comes down to three questions.

One: where is the data processed? On-device analysis with nothing uploaded and cloud processing are two different risk classes. Nanit is cloud-based; [non-WiFi local monitors](https://www.eufy.com/collections/non-wifi-baby-monitor) exist, such as eufy's SpaceView line, where the camera talks directly to a dedicated parent screen and the video never touches the internet. Settle this before buying.

Two: how does the company make money? Hardware plus subscription is one model; data monetization is another. Don't judge by the marketing. Judge by whether the privacy policy contains marketing, advertising, and third-party-sharing clauses. As shown above, Nanit's contains all three.

Three: what does leaving cost? Can you delete the data? (Nanit takes deletion requests at privacy@nanit.com and commits to responding within 45 days.) The policy states the company can revise it at any time, so today's promises don't bind tomorrow's version. And if the company is merged, acquired, or sells its assets, the data can transfer as part of the deal. That last part is not speculation; the clause is in Nanit's policy. Both points belong in any evaluation of a startup's data promises.

One more general habit: read the feature list as a collection list. Every new "insight" on the product page (breathing monitoring, language development, mood trends) usually means one more data pipeline behind it. Unless the vendor states that a new feature uses only existing data and runs only on-device, a feature upgrade is a collection upgrade.

Infant data differs from adult data in two basic ways: the subject cannot consent, and nothing about it is resettable. A leaked password can be changed. A person's breathing patterns, sleep curves, and language development from day one have no reset button; once leaked, the remedies are thin. When Nanit's CEO says "from birth to 100," she is describing the center of the fundraising story as much as a product vision — the 5 billion hours of sleep data sit right there in the $50 million press release. The hardware is the least of it. What the category leader has made the default is a file that starts on day zero, with consent given by someone else. And defaults are the hardest thing to renegotiate.

## References

- [Aw, It's Baby's First A.I. Surveillance System (The New York Times, 2026-08-02, Sapna Maheshwari; via Techmeme)](https://www.techmeme.com/260803/p8) — core feature facts: 0–100 sleep score, eye open/close logging, company-reported 1M daily users and $100M+ revenue, branding consultancy quote, false-positive detail, Dr. Diamond quote
- [Spyware for Babies — Schneier on Security](https://www.schneier.com/blog/archives/2026/08/spyware-for-babies.html) — where I found the story; only the title is cited in the text
- [Nanit Privacy Policy](https://www.nanit.com/policies/privacy-policy) — collection list, data purposes, CCPA "sale" language, retention wording, DNT, deletion requests and 45-day response, policy revision and merger/transfer clauses
- [Nanit Privacy & Security](https://www.nanit.com/pages/privacy-security) — encryption, push-only video streaming, mandatory two-step verification, employee access limits, Insights subscription and cloud storage
- [Nanit Raises $50M… (PR Newswire, official press release, December 2025)](https://www.prnewswire.com/news-releases/nanit-raises-50m-to-expand-its-ai-powered-systems-giving-parents-real-time-insights-into-infant-health-and-development-302643439.html) — funding details, Parenting Intelligence System, 5 billion hours of data, 70% of active users continuing past age four, CEO quote
- [HHS: HIPAA covered entities](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html) — HIPAA's scope (health plans, healthcare providers, healthcare clearinghouses)
- [FTC: Complying with COPPA FAQ](https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions) — COPPA covers only information collected online from the child; verifiable parental consent mechanism
- [California Civil Code §1798.140 (CCPA/CPRA)](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.140) — statutory definition of "sale" (monetary or other valuable consideration)
- [Meta Business Help Center: About Hashing Customer Information](https://www.facebook.com/business/help/112061095610075) — custom audiences list upload and matching mechanism
- [Slate: Zenith's Radio Nurse Was the World's First Baby Monitor](https://slate.com/human-interest/2013/02/zeniths-radio-nurse-designed-by-isamu-noguchi-was-the-worlds-first-baby-monitor.html) — origin of the baby monitor category (1937, one-way audio)
- [eufy: Non-WiFi Baby Monitors](https://www.eufy.com/collections/non-wifi-baby-monitor) — example of local, non-connected monitors
- [Democratic Underground forum transcription](https://www.democraticunderground.com/100221417047) — used to verify NYT quotes verbatim (branding consultancy, false positives, Diamond quote)
- [The Hustle: Even babies are living in an AI-powered surveillance state](https://thehustle.co/news/even-babies-are-living-in-an-ai-powered-surveillance-state) — cross-check of NYT reporting; none of its exclusive figures cited in the text
