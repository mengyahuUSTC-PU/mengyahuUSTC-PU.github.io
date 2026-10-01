---
title: "The chat title your AI wrote for you just went to Meta and TikTok"
description: "IMDEA Networks tested nine conversational AI products: auto-generated chat titles leak to ad trackers, permalinks default to public, events are forwarded server-side, and 80.8% of trackers keep working after you reject cookies."
pubDate: 2026-09-29
tags: [privacy, trust-and-safety]
lang: en
slug: conversational-ai-trackers
translationOf: conversational-ai-trackers
---

You ask an AI assistant: I earn $85,000 a year, what mortgage can I afford in New York? While it answers, it also writes a one-line summary of the conversation and hangs it in your sidebar, something like "Salary 85k NYC: Mortgage of 280-350k". That title is not only for you. Paper co-author Jorge García Herrero [uses exactly this example](https://www.zeropartydata.es/p/i-do-not-know-if-ai-will-kill-us): in several products, the AI-generated title goes out with the rest of the page data to tracking scripts from Meta, TikTok, and DoubleClick.

The finding comes from [Prompt like a Butterfly, Sting like a Tracker](https://jorgegarciaherrero.com/wp-content/interactivos/20260916-Prompt-like-a-butterfly-sting-like-a-tracker-(clean).pdf), a study led by IMDEA Networks with collaborators at Universidad Carlos III de Madrid, accepted at PoPETs 2027 according to García Herrero. On September 29 it reached the [Hacker News front page](https://news.ycombinator.com/item?id=49890226), over 400 points as I write this. The team tested nine assistants (ChatGPT, Claude, Gemini, Copilot, Grok, Perplexity, Le Chat from Mistral, DeepSeek, Meta AI) across web and Android clients, free and paid tiers, and both cookie choices, accept and reject.

The results: all nine embed at least one third-party advertising or tracking service. Six of the nine web clients, and three of the eight testable Android apps, leak the conversation URL, title, prompt, or a screenshot to third parties, usually alongside persistent identifiers (cookies, account IDs, in some cases hashed email addresses). A tracker that receives the title together with your email hash isn't logging that someone, somewhere, is asking about mortgages. It can file "asking about mortgages" directly under the ad profile it already keeps on you.

## Old plumbing, new payload

Nothing in the paper depends on new technology. Meta Pixel, TikTok Pixel, Google Analytics: the same third-party scripts websites have embedded for years, reporting each page's URL and title back to the ad platform along with the ad cookies in your browser.

What changed is the payload. On a shopping site, the page title is "trail running shoes," and the tracker learns you are shopping for shoes. In a chat product, the page title is the model's freshly generated summary of your conversation: your health question, your finances, your legal trouble, compressed into one line and placed in exactly the field a tracking script reports by routine. The paper frames this as a new privacy attack surface. The leak source is not content the user chose to post but a "conversation artifact" the service manufactured. Three of the nine web clients send these AI-generated titles to nine third parties, Meta, TikTok, and DoubleClick among them.

Grok goes furthest. Its conversation permalinks are public by default and must be switched off by hand. And when a conversation is shared, [the team's project site](https://leakylm.github.io/) documents that the message text is written into the share page's Open Graph metadata, the fields social platforms read to build link-preview cards, including the title and the image caption. TikTok's pixel reads those fields, so it collects the title, the prompt, and a screenshot.

The permalink trap is familiar ground here: in August I wrote about [how Claude share links ended up in Google search](/en/claude-share-links-google-indexed). A capability URL, where holding the link is the credential, becomes public the moment the link escapes. This paper pushes the same chain one step further: the link doesn't need to escape at all, because the tracking script embedded in the page reads it on the spot. Perplexity's guest conversations are public as well, always.

## After you reject cookies

The harshest number sits in the consent section: after rejecting all non-essential cookies, 80.8% of the third-party trackers keep working, and four of the nine services keep sending data to third parties.

Part of the reason is that tracking has moved where users can't see it. Take Claude: the paper measured Anthropic forwarding user events from its own servers, via Segment's conversions endpoints, to eleven third-party platforms including Facebook, LinkedIn, TikTok, Reddit, and Google. This is server-side tracking. The data never passes through your browser, and ad blockers and privacy browsers only intercept what runs in the browser, so this path is out of their reach entirely.

Android is blunter. Most of the apps show no cookie dialog at all; you have to accept the terms of service before you can use them, and "reject" is not on the menu. And 71% of the endpoints the mobile clients contact come from in-app WebViews, the embedded browsers that carry the web tracking stack into the app unchanged. The web has its own no-choice cases: Le Chat only works if you accept the terms and privacy policy wholesale.

## What helps, and what won't

A few things are still worth doing on the user side. Rejecting non-essential cookies can't remove eight trackers in ten, but it removes two: the paper found that after rejection, Claude's Meta Pixel and all eleven server-side forwarding destinations stayed inactive. Don't use conversation sharing or permalinks; Grok users should switch off public-by-default and revoke anything already shared. For genuinely sensitive topics, the logged-out guest mode is the wrong instinct (Perplexity's guest chats are public). A fully local deployment with no telemetry sidesteps the entire third-party pipeline measured in the paper.

But my conclusion after reading the paper is that this is not a problem users can solve. Server-side forwarding is invisible to them, the consent mechanisms barely bind, and the authors' own recommendations all point at the platforms: don't default permalinks to public, don't let auto-generated titles reach fields third parties can read. One precedent is worth filing away. According to the project site, Perplexity removed its Meta Pixel on April 3, 2026, days after a US class action (Doe v. Perplexity AI, Meta Platforms, Google) was filed. The site words it carefully, saying the removal was "likely in response" to the suit. If that inference holds, what moved a platform to change its practice was a court filing.

Most of this year's AI privacy debate has stayed at the model layer: training data, model memory, whether conversations feed future training runs. What this paper measures is the ordinary web product wrapped around the model, running the oldest generation of ad tech, where nobody wiring the chat box into that plumbing stopped to ask whether the data now flowing through it still resembles a product-browsing log. The thing to watch next is the EU. The paper's legal analysis argues that disclosing conversation artifacts to third parties requires prior informed consent and can hardly claim contract performance as a legal basis, which puts the practice in tension with the GDPR and the ePrivacy Directive, though the authors stop short of declaring it unlawful. The measurements were run in Spain in May 2026, on products that all serve EU users, so the question now sits with EU regulators.

## References

- [Prompt like a Butterfly, Sting like a Tracker (paper PDF)](https://jorgegarciaherrero.com/wp-content/interactivos/20260916-Prompt-like-a-butterfly-sting-like-a-tracker-(clean).pdf) — core data: nine products tested, 6/9 and 3/8 leak rates, 80.8%, Claude's eleven server-side forwarding destinations, Grok permalinks public by default, absent consent dialogs on Android, 71% of endpoints from WebViews
- [LeakyLM project site (research team)](https://leakylm.github.io/) — mechanism of Grok leaking message text to TikTok via Open Graph metadata; timeline of Perplexity removing the Meta Pixel
- [Co-author Jorge García Herrero's write-up](https://www.zeropartydata.es/p/i-do-not-know-if-ai-will-kill-us) — PoPETs 2027 acceptance, the "Salary 85k NYC" title example
- [Hacker News discussion](https://news.ycombinator.com/item?id=49890226) — 422 points, 137 comments at the time of writing
- [Earlier on this site: Click 'share' and you've published](/en/claude-share-links-google-indexed) — capability URLs and share links ending up in search engine indexes
