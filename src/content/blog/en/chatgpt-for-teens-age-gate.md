---
title: "OpenAI finally stopped believing your self-reported birthday"
description: "What's actually new in ChatGPT for Teens, what's repackaged, and why the age gate arrived almost four years late."
pubDate: 2026-08-18
tags: [ai-safety, trust-and-safety, openai]
lang: en
slug: chatgpt-for-teens-age-gate
translationOf: chatgpt-for-teens-age-gate
---

On August 18, OpenAI launched [ChatGPT for Teens](https://openai.com/index/chatgpt-for-teens/), a version of the product for users aged 13 to 17. TechCrunch's same-day headline was blunt: ["OpenAI launches a safer ChatGPT for teens — years after teens started using it"](https://techcrunch.com/2026/08/18/openai-launches-a-safer-chatgpt-for-teens-years-after-teens-started-using-it/).

The criticism has a factual basis. ChatGPT [went live at the end of November 2022](https://openai.com/index/chatgpt/) and reached [900 million weekly active users by this February](https://openai.com/index/scaling-ai-for-everyone/). Teens have been in that user base all along: when [AP reporters and researchers posed as a fictional 13-year-old in 2025](https://apnews.com/article/c569cddf28f1f33b36c692428c2191d4), signup took nothing more than a self-reported birthday showing the user was at least 13, with no age verification and no parental consent. Protections specific to minors only started arriving in late 2025, and a dedicated age tier almost four years into a general-audience product is slow by consumer-internet standards.

But late and useless are two different things. Content moderation is my day job, so this piece takes the launch apart: which parts are real mechanism changes, which are old features repackaged, and the sharper question of why it's happening now.

## What's new and what's repackaged

Read the announcement against the past year's timeline and most of the components turn out to already exist:

- **Parental controls** [shipped in late September 2025](https://www.forbes.com/sites/kirkogunrinde/2025/09/29/openai-launches-parental-controls-for-chatgpt-following-lawsuit-from-teens-death/). Parents [link to a teen's account by invitation](https://openai.com/index/introducing-parental-controls/) and can turn off memory and image generation, set blackout hours, and get notified when the system detects the teen may be in acute distress. The increment this time is that [notifications now extend to certain eating-disorder-related situations](https://openai.com/index/chatgpt-for-teens/).
- **Under-18 model behavior rules.** OpenAI's Model Spec, the public document that defines how its models should respond across scenarios, [added an Under-18 section in December 2025](https://techcrunch.com/2025/12/19/openai-adds-new-teen-safety-rules-to-models-as-lawmakers-weigh-ai-standards-for-minors/): no immersive romantic roleplay or first-person intimacy, no terms of endearment toward teens, no suggesting the model has feelings or consciousness, and heightened handling of suicide, self-harm, body image, and dangerous items.
- **The Teen Safety Blueprint**, a policy document [published in November 2025](https://www.axios.com/2025/11/06/openai-blueprint-teen-ai-safety-standards) offering recommendations to regulators and industry peers.

Two things are genuinely new. One is the education layer around the teen tier. Study Mode, which walks students through problems instead of handing over answers, is itself an existing feature; what's new is that it now comes built into the teen experience, along with nudges when a request looks like copied homework, break reminders, and warnings before uploading sensitive images. The other is that age prediction is now wired into the teen tier. OpenAI [announced early this year](https://openai.com/index/our-approach-to-age-prediction/) that age prediction was rolling out across consumer accounts; this launch connects the two systems. Users who say they are 13 to 17, and users the system estimates are under 18, get placed into the teen version automatically, and uncertain cases default to the under-18 experience.

That second piece is the core of this launch.

## The age gate moved up a tier

The trust and safety industry calls this problem age assurance, and the common methods sort into three tiers (the UK data-protection regulator ICO's [age assurance guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/age-assurance/) catalogs the methods; the three-tier grouping is my own). Tier one is self-declaration: type a birthday at signup. Lying costs nothing, and nobody in the industry expects it to stop anyone. Tier two is age inference: instead of asking, the system estimates from behavioral signals. The [signals OpenAI has disclosed](https://openai.com/index/our-approach-to-age-prediction/) include stated age, how long the account has existed, and typical times of day the account is active. Tier three is hard verification: government ID or a face scan, accurate but with a real privacy cost.

What OpenAI's system does, at bottom, is move the default gate from tier one to tier two, treating uncertain cases as minors. Adults who get misclassified can restore full access by [submitting a selfie to Persona](https://gulfnews.com/technology/media/chatgpt-will-now-guess-your-age-to-protect-teens-from-sensitive-content-1.500415454), a third-party identity verification service.

"When in doubt, treat as a minor" is the most consequential decision in the design. Every age classifier makes mistakes, in two directions ([OpenAI's own age-prediction post](https://openai.com/index/our-approach-to-age-prediction/) acknowledges the first kind and promises to keep improving accuracy, without publishing error rates for either). Misclassify an adult as a teen and the cost is friction and privacy: you hand over a selfie to prove your age. Miss a teen and classify them as an adult and the cost is harm exposure and legal risk. OpenAI chose to push the cost onto the first kind of error. That matches what regulators want, and it follows a path social platforms already walked: when Instagram [launched Teen Accounts in September 2024](https://about.fb.com/news/2024/09/instagram-teen-accounts/), it defaulted all under-18 accounts into a restricted mode. So the precise framing is that OpenAI is not a pioneer here. It is catching up on homework Instagram turned in two years ago.

The direction is right, though. This layer, I think, is real mechanism, not PR.

## A spec is not enforcement

The real weak point is elsewhere: the Model Spec is a behavior specification, not a capability guarantee. Writing "the model must not do X" into a document, and the model still not doing X on turn 200 of a conversation, are two different things.

That is exactly where the Raine case broke through. On August 26, 2025, the parents of 16-year-old Adam Raine [sued OpenAI and Sam Altman](https://techcrunch.com/2025/08/26/parents-sue-openai-over-chatgpts-role-in-sons-suicide/) after their son died by suicide following months of conversations with ChatGPT. [According to the complaint](https://www.nbcnews.com/tech/tech-news/openai-denies-allegation-chatgpt-teenagers-death-adam-raine-lawsuit-rcna245946), ChatGPT itself mentioned suicide more than a thousand times; OpenAI's own moderation systems flagged 377 of Adam's messages for self-harm content, and the system never ended the conversation. The same day, OpenAI published a blog post [admitting the failure mode](https://openai.com/index/helping-people-when-they-need-it-most/): safeguards "work more reliably in common, short exchanges," and "as the back-and-forth grows, parts of the model's safety training may degrade." ChatGPT "may correctly point to a suicide hotline when someone first mentions intent, but after many messages over a long period of time, it might eventually offer an answer that goes against our safeguards."

Read this launch against that known defect, and the announcement answers less than it appears to. OpenAI did publish something: the announcement points to [new under-18 evaluations in its system cards](https://openai.com/index/chatgpt-for-teens/), covering self-harm, eating disorders, violence, age-restricted goods, and sexual content. But the specific question the Raine case raised, how much long-conversation degradation has improved, has no published number. What is the age model's misclassification rate, and how does it break down by age band? Not published; [the age-prediction post](https://openai.com/index/our-approach-to-age-prediction/) says only that accuracy will keep improving. What are the accuracy and miss rates of the crisis notifications? Not published either; [the parental-controls announcement](https://openai.com/index/introducing-parental-controls/) acknowledges notifications can misfire but gives no rates. TechCrunch also raised a question familiar to every platform that has shipped parental controls: teens are very good at working around them. Register a fresh account, claim to be an adult, and how long does age prediction take to pull you back in? No number for that either.

Without those numbers, outsiders can verify that the architecture is right, but not that the results are there. I can't tell. Until OpenAI publishes them, nobody outside the company can.

## Why now

Put the regulatory events and the product moves on one timeline. August 25, 2025: [44 state and territory attorneys general send a joint letter](https://www.naag.org/press-releases/bipartisan-coalition-of-state-attorneys-general-issues-letter-to-ai-industry-leaders-on-child-safety/) to OpenAI and other AI companies demanding real child protections. The next day, the Raine lawsuit. September: the FTC issues [6(b) orders to seven companies](https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-launches-inquiry-ai-chatbots-acting-companions) including OpenAI, Meta, and Character.AI (a 6(b) order is an FTC power that compels companies to hand over internal material without an enforcement action). Late September: parental controls ship. October: California signs [SB 243](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260SB243), regulating companion chatbots, while Senators Hawley and Blumenthal's [GUARD Act](https://www.hawley.senate.gov/senator-hawleys-guard-act-to-protect-kids-from-ai-chatbots-passes-committee-unanimously/) would go further and bar minors from companion AI chatbots outright. November: the Blueprint. December: the Model Spec additions. June 2026: [Florida's attorney general sues OpenAI and Altman](https://techcrunch.com/2026/06/01/florida-sues-openai-sam-altman-in-first-of-its-kind-lawsuit-over-violent-incidents/), the first suit of its kind brought by a state. August: ChatGPT for Teens.

The product moves land tightly on the heels of the legal and regulatory events. Sequence is not causation, so what follows is my inference, not a provable fact: teen safety got its place on the priority list from outside pressure. That doesn't make the launch pure theater; the mechanisms are real. But "we took reasonable measures" is itself litigation-defense material, and for a platform those two motives have never been in conflict.

## My read

On architecture, this is a real upgrade. Age inference plus a strict default plus tiered model behavior is the structure Instagram already runs and the ICO already catalogs. On results, it is currently unverifiable: misclassification rates, long-conversation safety evals, and notification accuracy are three sets of numbers, and none of them has been published. Judging how much this launch is actually worth means waiting for OpenAI to release those numbers, or waiting for discovery in the next lawsuit to surface the data.

One more line item the announcement won't compute for you: a strict default means age prediction rolls out across every consumer account, and for adults who get misclassified, the recovery path OpenAI offers is handing a selfie to a third party. The cost of protecting teens never lands only on teens. This time is no different.

## References

- [Introducing ChatGPT for Teens — OpenAI](https://openai.com/index/chatgpt-for-teens/) — official announcement: feature list, 13–17 scope, strict-default policy, eating disorder notifications, under-18 system card evaluations
- [Updating our Model Spec with teen protections — OpenAI](https://openai.com/index/updating-model-spec-with-teen-protections/) — Under-18 behavior rules
- [Our approach to age prediction — OpenAI](https://openai.com/index/our-approach-to-age-prediction/) — age prediction signals, under-18 default, Persona appeal
- [Introducing parental controls — OpenAI](https://openai.com/index/introducing-parental-controls/) — parental control feature list
- [Helping people when they need it most — OpenAI](https://openai.com/index/helping-people-when-they-need-it-most/) — official admission of safeguard degradation in long conversations
- [Introducing ChatGPT — OpenAI](https://openai.com/index/chatgpt/) — November 30, 2022 launch
- [Scaling AI for everyone — OpenAI](https://openai.com/index/scaling-ai-for-everyone/) — 900M+ weekly active users as of February 2026
- [OpenAI launches a safer ChatGPT for teens — TechCrunch](https://techcrunch.com/2026/08/18/openai-launches-a-safer-chatgpt-for-teens-years-after-teens-started-using-it/) — critical angle, control-bypass question
- [OpenAI adds new teen safety rules to models — TechCrunch](https://techcrunch.com/2025/12/19/openai-adds-new-teen-safety-rules-to-models-as-lawmakers-weigh-ai-standards-for-minors/) — December 2025 Model Spec rules, Raine case background
- [Parents sue OpenAI over ChatGPT's role in son's suicide — TechCrunch](https://techcrunch.com/2025/08/26/parents-sue-openai-over-chatgpts-role-in-sons-suicide/) — August 26, 2025 lawsuit filing
- [Study says ChatGPT is giving teens dangerous advice — AP](https://apnews.com/article/c569cddf28f1f33b36c692428c2191d4) — signup required only a self-reported birthday, no age verification or parental consent
- [OpenAI denies allegation in teen's death lawsuit — NBC News](https://www.nbcnews.com/tech/tech-news/openai-denies-allegation-chatgpt-teenagers-death-adam-raine-lawsuit-rcna245946) — complaint figures: ChatGPT's suicide mentions, 377 flagged messages, conversation never terminated
- [OpenAI launches parental controls — Forbes](https://www.forbes.com/sites/kirkogunrinde/2025/09/29/openai-launches-parental-controls-for-chatgpt-following-lawsuit-from-teens-death/) — parental controls launch, late September 2025
- [OpenAI unveils blueprint for teen AI safety standards — Axios](https://www.axios.com/2025/11/06/openai-blueprint-teen-ai-safety-standards) — Teen Safety Blueprint timing and content
- [ChatGPT will now guess your age — Gulf News](https://gulfnews.com/technology/media/chatgpt-will-now-guess-your-age-to-protect-teens-from-sensitive-content-1.500415454) — Persona selfie verification
- [Bipartisan coalition of state attorneys general issues letter to AI industry leaders on child safety — NAAG](https://www.naag.org/press-releases/bipartisan-coalition-of-state-attorneys-general-issues-letter-to-ai-industry-leaders-on-child-safety/) — August 25, 2025 letter from 44 attorneys general
- [FTC launches inquiry into AI chatbots acting as companions — FTC](https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-launches-inquiry-ai-chatbots-acting-companions) — 6(b) orders and the seven companies
- [SB 243 — California Legislative Information](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260SB243) — companion chatbot regulation
- [GUARD Act — Senator Hawley](https://www.hawley.senate.gov/senator-hawleys-guard-act-to-protect-kids-from-ai-chatbots-passes-committee-unanimously/) — bill barring minors from companion AI chatbots
- [Florida sues OpenAI, Sam Altman — TechCrunch](https://techcrunch.com/2026/06/01/florida-sues-openai-sam-altman-in-first-of-its-kind-lawsuit-over-violent-incidents/) — June 2026 Florida AG lawsuit
- [Age assurance guidance — ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/age-assurance/) — age assurance method taxonomy
- [Introducing Instagram Teen Accounts — Meta](https://about.fb.com/news/2024/09/instagram-teen-accounts/) — precedent for default-restricted teen mode
