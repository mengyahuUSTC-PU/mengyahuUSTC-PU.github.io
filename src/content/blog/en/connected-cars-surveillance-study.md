---
title: "We packet-captured 21 cars. 19 were talking to third parties."
description: "Northeastern and Consumer Reports put 21 cars and 30 automaker apps on the wire: 19 vehicles sent traffic to third parties, 28 apps shipped data to advertisers, and in-car AI assistants are about to plug into the same pipeline."
pubDate: 2026-10-01
tags: [privacy, connected-cars, data-brokers]
lang: en
slug: connected-cars-surveillance-study
translationOf: connected-cars-surveillance-study
---

At Consumer Reports' auto test facility in Connecticut, researchers logged every network connection 21 connected cars tried to make. Eleven EVs went inside a garage-sized Faraday tent, a metal-mesh enclosure that attenuates radio signals by about 93 dB. Cut off from cellular networks, those cars could only route traffic through the researchers' controlled network. The other ten ran standard static and driving tests with traffic captured over controlled Wi-Fi. From October 2024 to August 2025 the team tested 21 vehicles across 19 brands (Tesla, Cadillac, Rivian, and Lucid among them, model years 2022–2025) plus 30 official automaker apps.

The results: 19 of the 21 cars sent traffic to at least one third party, and 28 of the 30 apps sent data to advertising or analytics companies ([Consumer Reports investigation](https://www.consumerreports.org/electronics/personal-information/your-car-is-sharing-data-with-big-tech-companies-study-finds-a4474820962/)). The study is a collaboration between Northeastern University's privacy researchers and Consumer Reports; the paper, "[Automatic Transmission](https://automatictransmission.khoury.northeastern.edu/)," has been accepted at the ACM Internet Measurement Conference (IMC '26) and will be published this October. It's the work Bruce Schneier [picked up](https://www.schneier.com/blog/archives/2026/10/connected-cars-are-a-surveillance-platform.html) on his blog.

## Measured traffic, not policy text

There's no shortage of "your car is spying on you" commentary. What this study adds is measurement: actual traffic on the wire rather than what privacy policies promise. Most vehicle traffic is encrypted, but encryption protects content, not destination. DNS queries and TLS handshakes carry the target domain in plaintext, and that was enough to map where the data goes.

A few specifics:

- **The recipients are familiar names**: Amazon, Google, Meta, Microsoft, Pinterest, Snap, Yahoo, Reddit. A single Tesla Model 3 contacted 34 advertising and tracking domains.
- **Seven of the 30 apps sent personally identifiable information**: owner email addresses, phone numbers, precise location, and the VIN. The VIN is a vehicle's permanent identity number; registration and insurance records are indexed by it ([NHTSA](https://www.nhtsa.gov/document/vehicle-identification-number-vin)). A VIN plus precise location is a persistent identifier that can be joined across databases.
- **The companion app doubles the exposure**: pairing the official app roughly doubled, on average, the number of advertising and tracking entities a vehicle touched.
- **Automakers don't necessarily know their own data flows**: only after seeing the results did Honda tell its analytics vendor Amplitude to delete the location data it had received. The study documents just that remediation step; my inference is that nobody inside these companies had checked, line by line, how the privacy policy matched the actual flows.

## Where the data goes is the point

Ad companies receiving vehicle data is the front half of the chain. The back half already has a case on record: in January 2025 the FTC [took action against General Motors](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-takes-action-against-general-motors-sharing-drivers-precise-location-driving-behavior-data), alleging that OnStar's Smart Driver feature collected precise location and driving behavior data and sold it to consumer reporting agencies (which play a role similar to credit bureaus), whose reports insurers then used to set rates and deny coverage. Some owners learned they had been enrolled only when the data showed up in their insurance pricing. The settlement order [took effect in January 2026](https://www.ftc.gov/news-events/news/press-releases/2026/01/ftc-finalizes-order-settling-allegations-gm-onstar-collected-sold-geolocation-data-without-consumers) and bans GM from disclosing such data to consumer reporting agencies for five years.

This explains why data as seemingly worthless as hard braking and rapid acceleration gets collected at all: it has a ready buyer in the insurance pricing market.

What about refusing? The study records one detail: Tesla warns users who switch off data sharing that this "may result in your vehicle suffering from reduced functionality, serious damage, or inoperability." Tesla is merely the bluntest about it. Across the vehicles tested, outbound data is the factory default, and the costs of opting out, whatever they turn out to be, sit entirely with the owner.

## The AI assistant plugs into the same pipeline

This April, GM announced it would push Google Gemini to roughly four million eligible vehicles with Google built-in ([GM press release](https://news.gm.com/home.detail.html/Pages/news/us/en/2026/apr/0428-Google-Gemini.html)) and previewed a proprietary assistant for later in 2026. On what that assistant runs on, there are two public statements: a GM executive says it combines conversational AI with "GM vehicle knowledge and OnStar intelligence" ([GM Authority](https://gmauthority.com/blog/2026/08/gm-proprietary-ai-assistant-launching-this-year/)); an earlier [TechCrunch report](https://techcrunch.com/2025/10/22/gm-is-bringing-google-gemini-powered-ai-assistant-to-cars-in-2026) quotes GM saying it will "take a base model and train it on the vehicle's specifications." The data in the FTC case also came through OnStar; both run on the same pipe. Whether location and driving-behavior data of that kind ends up in the assistant's training data, GM has not disclosed. I have no evidence that it does, so that stays an open question.

A conversational assistant also creates a category of data that didn't exist before: what you ask and say inside the car. How that will be collected and retained, the announcements don't say. This study measured network traffic and apps; it did not cover voice assistant data flows, which means the voice channel remains unmeasured rather than cleared. My read: an industry where the mismatch between privacy policy and actual traffic had to be discovered by outside researchers with packet captures gives no reason to expect sudden restraint at the AI layer.

## What owners can do

The options are limited but real. Some automakers provide controls: Toyota owners can adjust data permissions in the official app's Data Privacy Portal, and Ford's [privacy page](https://www.ford.com/help/privacy/) lists in-car settings and a factory reset (Master Reset) path; Consumer Reports maintains a [manufacturer-by-manufacturer guide](https://www.consumerreports.org/electronics/personal-information/how-to-stop-your-car-from-collecting-sharing-driving-data-a1233378612/). In states with privacy laws, residents can file requests to limit use, stop sharing, or delete data; [Privacy4Cars](https://privacy4cars.com/) offers a free service that locates each automaker's request channel. If you buy used, remember that the previous owner's data and app pairings may still live in the head unit; the FTC has a [specific alert](https://consumer.ftc.gov/consumer-alerts/2018/08/selling-your-car-clear-your-personal-data-first) about factory-resetting and unpairing apps before a car changes hands.

Settings menus won't fix the structural problem, though. The most useful thing this study leaves behind is a repeatable test: what the automaker says doesn't matter; what the car transmits does. The measurement worth watching next is which new domains show up in the capture list once in-car AI assistants ship.

## References

- [Automatic Transmission project page (Northeastern University)](https://automatictransmission.khoury.northeastern.edu/) — methodology (Faraday tent for 11 EVs, tcpdump, mitmproxy), the 19/21 and 7/30 figures, the app-pairing doubling effect, IMC '26 publication
- [Consumer Reports investigation](https://www.consumerreports.org/electronics/personal-information/your-car-is-sharing-data-with-big-tech-companies-study-finds-a4474820962/) — test scale and period, list of third-party companies, Tesla's 34 tracking domains, the Honda/Amplitude episode, Tesla's opt-out warning
- [Consumer Reports manufacturer-by-manufacturer opt-out guide](https://www.consumerreports.org/electronics/personal-information/how-to-stop-your-car-from-collecting-sharing-driving-data-a1233378612/) — Toyota Data Privacy Portal steps, the three request types under state privacy laws
- [Schneier on Security](https://www.schneier.com/blog/archives/2026/10/connected-cars-are-a-surveillance-platform.html) — where I found the study
- [FTC enforcement announcement against GM (January 2025)](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-takes-action-against-general-motors-sharing-drivers-precise-location-driving-behavior-data) — allegations that OnStar Smart Driver data was sold to consumer reporting agencies
- [FTC final order announcement (January 2026)](https://www.ftc.gov/news-events/news/press-releases/2026/01/ftc-finalizes-order-settling-allegations-gm-onstar-collected-sold-geolocation-data-without-consumers) — order effective, five-year ban
- [GM press release: Gemini rollout](https://news.gm.com/home.detail.html/Pages/news/us/en/2026/apr/0428-Google-Gemini.html) — roughly four million eligible vehicles, applicable brands
- [GM Authority: GM proprietary assistant launching this year](https://gmauthority.com/blog/2026/08/gm-proprietary-ai-assistant-launching-this-year/) — official statement on combining GM vehicle knowledge with OnStar intelligence
- [TechCrunch: GM's in-house assistant plans](https://techcrunch.com/2025/10/22/gm-is-bringing-google-gemini-powered-ai-assistant-to-cars-in-2026) — base model trained on vehicle specifications
