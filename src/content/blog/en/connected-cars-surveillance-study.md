---
title: "We packet-captured 21 cars. 19 were talking to third parties."
description: "Northeastern and Consumer Reports put 21 cars and 30 automaker apps on the wire: 19 vehicles sent traffic to third parties, 28 apps shipped data to advertisers, and in-car AI assistants are arriving on the same OnStar-era infrastructure."
pubDate: 2026-10-01
tags: [privacy, connected-cars, data-brokers]
lang: en
slug: connected-cars-surveillance-study
translationOf: connected-cars-surveillance-study
---

At Consumer Reports' auto test facility in Connecticut, researchers recorded the network traffic 21 connected cars sent over a controlled Wi-Fi network, through static and driving tests. Eleven EVs additionally went inside a car-sized Faraday tent, a metal-mesh enclosure that attenuates radio signals by about 93 dB; cut off from cellular networks, those cars could only route traffic through the researchers' network. From October 2024 to August 2025 the team tested 21 vehicles across 19 brands (Tesla, Cadillac, Rivian, and Lucid among them, model years 2022–2025) plus 30 official automaker apps.

The results: 19 of the 21 cars sent traffic to at least one third party, and 28 of the 30 apps sent data to advertising or analytics companies ([Consumer Reports investigation](https://www.consumerreports.org/electronics/personal-information/your-car-is-sharing-data-with-big-tech-companies-study-finds-a4474820962/)). The study is a collaboration between Northeastern University's privacy researchers and Consumer Reports; the paper, "[Automatic Transmission](https://automatictransmission.khoury.northeastern.edu/)," has been accepted at the ACM Internet Measurement Conference (IMC '26) and will be published this October. It's the work Bruce Schneier [picked up](https://www.schneier.com/blog/archives/2026/10/connected-cars-are-a-surveillance-platform.html) on his blog.

## Measured traffic, not policy text

There's no shortage of "your car is spying on you" commentary. What this study adds is measurement: actual traffic on the wire rather than what privacy policies promise. Most vehicle traffic is encrypted, but encryption protects content, not destination. In the traffic the researchers captured, DNS queries and TLS handshakes exposed the destination domains in plaintext, and that was enough to map where the data goes.

A few specifics:

- **The recipients are familiar names**: Amazon, Google, Meta, Microsoft, Pinterest, Snap, Yahoo, Reddit. A single Tesla Model 3 contacted 34 advertising and tracking domains.
- **Seven of the 30 apps sent personally identifiable information**: across those apps, owner email addresses, phone numbers, precise location, and the VIN. The VIN uniquely identifies a vehicle; registration and insurance records are indexed by it ([NHTSA](https://www.nhtsa.gov/document/vehicle-identification-number-vin)). The researchers note that stable identifiers like these let advertising companies link a vehicle's owner to behavioral data and purchase histories from other websites and apps ([Northeastern News](https://news.northeastern.edu/2026/09/29/connected-car-privacy-violation-research/)).
- **The companion app doubles the exposure**: pairing the official app roughly doubled, on average, the number of advertising and tracking entities a vehicle touched.
- **Automakers don't necessarily know their own data flows**: only after seeing the results did Honda tell its analytics vendor Amplitude to delete the location data it had received. The study documents just that remediation step; what review happened inside Honda before outside researchers showed up, I don't know.

## Where the data goes is the point

Ad companies receiving vehicle data is the front half of the chain. The back half already has a case on record: in January 2025 the FTC [took action against General Motors](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-takes-action-against-general-motors-sharing-drivers-precise-location-driving-behavior-data), alleging that OnStar's Smart Driver feature collected precise location and driving behavior data and sold it to consumer reporting agencies (which play a role similar to credit bureaus), whose reports insurers then used to set rates and deny coverage. Some owners learned they had been enrolled only when the data showed up in their insurance pricing. The settlement order was [finalized in January 2026](https://www.ftc.gov/news-events/news/press-releases/2026/01/ftc-finalizes-order-settling-allegations-gm-onstar-collected-sold-geolocation-data-without-consumers) and bans GM from disclosing such data to consumer reporting agencies for five years.

Data as seemingly worthless as hard braking, late-night driving, and speeding had a ready buyer in the insurance pricing market.

What about refusing? The study records one detail: Tesla warns users who switch off data sharing that this "may result in your vehicle suffering from reduced functionality, serious damage, or inoperability." Tesla is merely the bluntest about it. Across manufacturers, opting out generally means giving up some functionality, and it's the owner who absorbs that trade.

## The AI assistant arrives on the same infrastructure

This April, GM announced it would push Google Gemini to roughly four million eligible vehicles with Google built-in ([GM press release](https://news.gm.com/home.detail.html/Pages/news/us/en/2026/apr/0428-Google-Gemini.html)) and previewed a proprietary assistant for later in 2026. On what that assistant runs on, there are two public statements: GM's director of product management, Anna Santos, says it combines conversational AI with "GM vehicle knowledge and OnStar intelligence" ([GM Authority](https://gmauthority.com/blog/2026/08/gm-proprietary-ai-assistant-launching-this-year/)); an earlier [TechCrunch report](https://techcrunch.com/2025/10/22/gm-is-bringing-google-gemini-powered-ai-assistant-to-cars-in-2026) quotes GM saying it will "take a base model and train it on the vehicle's specifications." The data in the FTC case also flowed through OnStar. That overlap doesn't prove the assistant and the Smart Driver program share a data pipeline, and whether location and driving-behavior data of that kind ends up in the assistant's training data, GM's public announcements don't say. I have no evidence that it does, so that stays an open question.

A conversational assistant also creates a category of data that didn't exist before: what you ask and say inside the car. How that will be collected and retained, the announcements don't say. This study measured network traffic and apps; it did not cover voice assistant data flows, which means the voice channel remains unmeasured rather than cleared. My read: an industry where the mismatch between privacy policy and actual traffic had to be discovered by outside researchers with packet captures gives no reason to expect sudden restraint at the AI layer.

## What owners can do

The options are limited but real. Some automakers provide controls: Toyota owners can adjust data permissions in the official app's Data Privacy Portal, and Ford's [privacy page](https://www.ford.com/help/privacy/) describes a factory reset (Master Reset) and points owners to in-car data controls; Consumer Reports maintains a [manufacturer-by-manufacturer guide](https://www.consumerreports.org/electronics/personal-information/how-to-stop-your-car-from-collecting-sharing-driving-data-a1233378612/). In states with privacy laws, residents can file requests to limit use, stop sharing, or delete data; [Privacy4Cars](https://privacy4cars.com/) offers [free tools](https://www.prweb.com/releases/privacy4cars-releases-new-and-improved-free-methods-for-consumers-to-learn-about-privacy-practices-in-automotive-and-express-privacy-preferences-302408955.html) that locate each automaker's request channel and can act as your agent for those requests. If you buy used, remember that the previous owner's data and app pairings may still live in the head unit; the FTC has a [specific alert](https://consumer.ftc.gov/consumer-alerts/2018/08/selling-your-car-clear-your-personal-data-first) about factory-resetting and unpairing apps before a car changes hands.

Settings menus won't fix the structural problem, though. The most useful thing this study leaves behind is a repeatable test: what the automaker says doesn't matter; what the car transmits does. The measurement worth watching next is which new domains show up in the capture list once in-car AI assistants ship.

## References

- [Automatic Transmission project page (Northeastern University)](https://automatictransmission.khoury.northeastern.edu/) — methodology (car-sized Faraday tent for 11 EVs, tcpdump, mitmproxy), the 19/21 and 7/30 figures (VINs, emails, phone numbers, precise location), the app-pairing doubling effect, IMC '26 publication
- [Northeastern News coverage](https://news.northeastern.edu/2026/09/29/connected-car-privacy-violation-research/) — cross-context tracking via stable identifiers, the Honda/Amplitude remediation
- [Consumer Reports investigation](https://www.consumerreports.org/electronics/personal-information/your-car-is-sharing-data-with-big-tech-companies-study-finds-a4474820962/) — test scale and period, list of third-party companies, Tesla's 34 tracking domains, the Honda/Amplitude episode, Tesla's opt-out warning
- [Consumer Reports manufacturer-by-manufacturer opt-out guide](https://www.consumerreports.org/electronics/personal-information/how-to-stop-your-car-from-collecting-sharing-driving-data-a1233378612/) — Toyota Data Privacy Portal steps, the three request types under state privacy laws
- [Schneier on Security](https://www.schneier.com/blog/archives/2026/10/connected-cars-are-a-surveillance-platform.html) — where I found the study
- [FTC enforcement announcement against GM (January 2025)](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-takes-action-against-general-motors-sharing-drivers-precise-location-driving-behavior-data) — allegations that OnStar Smart Driver data was sold to consumer reporting agencies
- [FTC final order announcement (January 2026)](https://www.ftc.gov/news-events/news/press-releases/2026/01/ftc-finalizes-order-settling-allegations-gm-onstar-collected-sold-geolocation-data-without-consumers) — order finalized, five-year ban
- [GM press release: Gemini rollout](https://news.gm.com/home.detail.html/Pages/news/us/en/2026/apr/0428-Google-Gemini.html) — roughly four million eligible vehicles, applicable brands
- [GM Authority: GM proprietary assistant launching this year](https://gmauthority.com/blog/2026/08/gm-proprietary-ai-assistant-launching-this-year/) — Anna Santos on combining GM vehicle knowledge with OnStar intelligence
- [TechCrunch: GM's in-house assistant plans](https://techcrunch.com/2025/10/22/gm-is-bringing-google-gemini-powered-ai-assistant-to-cars-in-2026) — base model trained on vehicle specifications
