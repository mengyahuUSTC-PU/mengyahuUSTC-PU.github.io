---
title: "A $1.5 Billion Settlement, and Still No Precedent"
description: "Anthropic's copyright settlement is finally approved. The money pays for pirated downloads, not for AI training — and the one question the industry most needs answered has been quietly bought off the docket."
pubDate: 2026-07-20
tags: [ai-copyright, ai-governance, training-data]
lang: en
slug: anthropic-copyright-settlement-approved
translationOf: anthropic-copyright-settlement-approved
---

On July 20, in the federal district court in San Francisco, Judge Araceli Martinez-Olguin signed the final approval of Anthropic's $1.5 billion settlement with the authors' class action ([TechCrunch](https://techcrunch.com/2026/07/20/anthropics-landmark-1-5b-copyright-settlement-is-approved/)). It is the largest known copyright recovery in U.S. history ([Reuters](https://www.investing.com/news/stock-market-news/us-judge-approves-anthropics-15-billion-settlement-of-copyright-lawsuit-4801706)). Preliminary approval came last September from Judge William Alsup, now retired; the numbers are now settled: roughly 500,000 works, about $3,000 per work, with over 91% of class members filing claims ([Reuters](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/)).

On paper, a decisive win for the plaintiffs. Yet on approval day, some authors still stood up to object ([Reuters](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/)). The complaints centered on money: $3,000 per work is too little, the $101 million in attorneys' fees takes too big a bite out of the pool; some rejected the deal outright, opting out to sue on their own. But the money is only the surface. Read the terms, and the settlement gives authors even less than the headline number suggests.

## The release is much narrower than it looks

The settlement terms set out three limits ([Copyright Alliance](https://copyrightalliance.org/participating-bartz-v-anthropic-settlement/)):

- The release covers conduct only through **August 26, 2025**;
- The settlement **grants no license for future use** — Anthropic gets no permission to keep using these books;
- **Claims over infringing model outputs are expressly excluded**, and authors can still bring them later.

In other words, this release settles old accounts: Anthropic's downloads of pirated books from Library Genesis and Pirate Library Mirror, and any claims arising from using those eligible works for training, research, and product development before August 26, 2025 ([Copyright Alliance](https://copyrightalliance.org/participating-bartz-v-anthropic-settlement/)). Anthropic must also destroy every file downloaded from those two pirate libraries, along with all copies.

Meanwhile, the question that actually decides where this industry goes — **is training a large language model on copyrighted books fair use?** — was already answered by Judge Alsup in his June 2025 summary judgment, and the answer favored the AI companies. To see what that ruling did, split what Anthropic did into two steps: first acquiring the books, then training on them.

**Step one is acquisition, and its legality turns on where the books came from.** Anthropic got books two ways. One was downloading more than seven million ebooks directly from the two pirate libraries into an internal "central library." The other, later, was buying print books, cutting them apart, scanning them, and destroying the originals. Alsup drew the line cleanly: buying and scanning is fair use — you paid for the book, converting it to another format for your own retention is fine; downloading from pirate libraries is not fair use, and liability and damages for that piece were headed to a jury before the settlement mooted the trial. Worse for Anthropic, the library held large numbers of pirated books the company itself had decided never to use for training, kept on hand anyway — for those, even the "it served training" defense didn't apply ([Reuters](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/)). The line the court drew was never "you built a library"; it was whether the books in it were bought or stolen. Retaining lawfully purchased books for future training got the court's blessing.

**Step two is training, and Alsup gave AI companies the answer they most wanted:** as to the works and training practices in this case, using books to train a large language model is a highly transformative use, and it qualifies as fair use. In this case, the court's view was that the problem lay in where the books came from — not in the training itself.

Put the two steps together and the settlement's boundaries come into focus. The $1.5 billion closes the books on everything before August 26, 2025. If Anthropic downloads from pirate libraries again, that is fresh infringement, outside the release. If it keeps buying, scanning, and training, what it leans on is not this settlement but Alsup's ruling — a ruling that decided the specific facts of this case, so a different practice or a different dispute (model outputs, say) can still draw new lawsuits.

What the authors most wanted overturned was exactly the "training is fair use" half. But once the settlement was signed, nobody appealed, and the ruling stands untouched. That is precisely what Anthropic deputy general counsel Aparna Sridhar chose to emphasize: "We reached this settlement in 2025, after the court's landmark ruling that training AI on books is fair use under copyright law" ([Reuters](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/)).

So the true ending of this lawsuit is this: **what drove the $1.5 billion was pirated downloads, not AI training.**

## Where the $3,000 per book comes from

The $3,000 figure isn't arbitrary. The anchor is the statutory damages range in U.S. copyright law ([17 U.S.C. § 504](https://www.law.cornell.edu/uscode/text/17/504)): $750 to $30,000 per work for ordinary infringement, up to $150,000 for willful infringement, with the exact amount set by the court within the range — and willfulness is something plaintiffs must separately prove.

Apply that range to 500,000 registered works and Anthropic's willingness to pay $1.5 billion makes sense. If a jury found willful infringement and awarded the maximum, the theoretical exposure was $75 billion — an existential number for any company. Even at the statutory floor, it was $375 million. Three thousand dollars is roughly four times the floor. For Anthropic, it is an insurance premium against a company-ending risk, payable in four installments through September 2027 ([Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/)). For an individual author, the default is a 50/50 split with the publisher ([Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/)) — nominally $1,500, and less after administrative costs. That gap is roughly the distance between "historic settlement" and the authors' disappointment.

There is also an easily missed gate: to be among the 500,000 works at all, a book needed an ISBN or ASIN **and a Copyright Office registration completed within the required window** ([Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/)). Unregistered books didn't even qualify for compensation.

## Why this "landmark" is not a precedent

Settlements create no precedent — that is black-letter procedure. What makes this case unusual is that it also sealed away a ruling that could have become one.

Alsup's fair use ruling is a district court decision. For other judges it is persuasive at most, never binding. On the normal path, a ruling this consequential gets appealed to the Ninth Circuit, whose published decisions bind every court in the circuit ([Ninth Circuit](https://www.ca9.uscourts.gov/decisions)). But a settlement means no appeal — **the question this industry most needs an authoritative answer to stopped at the trial court in this case.** A binding answer now has to wait for some other case to carry it up to a circuit court.

The consequences are immediate. Google, Meta, Midjourney, and OpenAI are all still being sued, and just last week major publishers filed a new training-data lawsuit against Google ([TechCrunch](https://techcrunch.com/2026/07/14/google-faces-another-ai-training-lawsuit-from-major-publishers/)). Every presiding judge is free to reach their own conclusion on fair use and owes Alsup nothing. NYT v. OpenAI is still mired in discovery fights ([TechCrunch](https://techcrunch.com/2026/07/09/new-york-times-says-openai-hid-evidence-in-chatgpt-copyright-trial/)); if it ever reaches judgment, the answer could well come out the other way.

Mechanically, ending in settlement is no surprise. The key is that a settlement and a losing precedent are two entirely different endings — the difference isn't whether you pay, but how much, under whose rules, and whether you can keep operating afterward.

A settlement is a negotiated, discounted price, and it closes only this one case. $1.5 billion sounds enormous; next to the $75 billion theoretical maximum, it is 2%. The plaintiffs accepted that discount because, with no precedent on the books, they could lose too — fair use was unresolved, a different judge might have handed Anthropic a complete win and left the authors with nothing. That uncertainty is the biggest chip AI companies hold at the negotiating table.

A losing precedent would confiscate that chip. Suppose this case had skipped the settlement and gone all the way up, and the Ninth Circuit had reversed on "training is fair use." From that day forward, every court in the circuit would be bound by that conclusion on the same legal question. The next class of authors suing any AI company would face a defendant stripped of its strongest defense. Plaintiffs would still have to prove ownership, copying, registration, and damages case by case; willfulness would still need separate proof; settlements would still happen — but the scales would have tipped. The uncertainty discount collapses, and asking prices can hug the statutory range (up to $150,000 per work for willful infringement). Paying under both scenarios is not the same kind of paying: without a precedent, you pay a discounted price and close one case; with one, every later plaintiff arrives holding the same weapon.

And the cost of losing isn't only money. If an appeals court held that training infringes, Anthropic could face remedies including an injunction. Its scope would depend on the specific works, models, and equitable factors — not necessarily "shut down every model" — but it would be aimed at the practice of training on books itself, and every subsequent training run might require licenses obtained one by one. Lay that ledger out and you get an asymmetric bet: win the appeal, and you mostly save the settlement money; lose it, and you may have wagered the business model. This is my inference from public information — the real decision also turned on win probabilities, injunction standards, and litigation costs outsiders can't see — but it at least explains why both sides were willing to stop here: paying for certainty.

If that logic holds, similar cases all have an incentive to settle before an appellate precedent can form: sued again and again, settling again and again, each time at a discount — because one loss means paying full price, plus injunction risk, plus handing every future plaintiff the same weapon. Whether this case is a one-off will depend on how the current wave of lawsuits ends.

## It didn't set the rule, but it set the price

The settlement's real industry effect is putting a visible number on the "compliance premium" for training data.

The after-the-fact cost of pirated data now has a reference magnitude — in this case, about $3,000 per work. To be precise: that is a negotiated gross figure, not a court-set minimum, and certainly not a statutory starting price for future cases. But add the destroyed dataset, the litigation costs, and years of uncertainty, and the bill is legible enough. Alsup's ruling, meanwhile, confirmed that the other path was lawful in this case: Anthropic bought print books, cut them apart, scanned them, and destroyed the originals, and the court called that format conversion — a paper copy you paid for in full, replaced by a digital copy for your own use, with not one extra copy added to circulation — and fair use ([the order](https://copyrightalliance.org/wp-content/uploads/2025/06/Bartz-v.-Anthropic-Order.pdf)).

But this "lawful path" is narrower than much of the coverage implies. It is not a general license for any company to buy one copy of anything and train on it. Three qualifications can't be skipped:

- **It is not an industry-wide pass.** This is a district court ruling at first instance, persuasive but not binding on other judges. Another AI company copying the playbook would still have to convince its own judge to accept the same analysis when sued.
- **It ruled on exactly one practice: buy print, scan, destroy the original.** Fair use worked here because a physical copy bought outright was replaced one-for-one by a digital copy, with no copies added. Ebooks are a different matter: they are generally sold under license agreements, and whether you may copy them or mine them for text depends on the terms. Alsup never ruled on that path, and this case's ruling won't help there.
- **Film and music can't borrow it at all.** Fair use is a case-by-case defense, not a general rule; change the type of work and the analysis can change entirely — "effect on the potential market for the original" is one of the four fair use factors ([17 U.S.C. § 107](https://www.law.cornell.edu/uscode/text/17/107)), and film and music have mature licensing markets, so that factor may no longer lean toward the user. Moreover, purchased DVDs and Blu-rays ship with digital encryption (DVD's CSS and Blu-ray's AACS both fall under the Copyright Office's anti-circumvention rules, [37 CFR § 201.40](https://www.copyright.gov/title37/201/37cfr201-40.html)), and circumventing it to extract video and audio may violate the DMCA's anti-circumvention provision ([17 U.S.C. § 1201](https://www.law.cornell.edu/uscode/text/17/1201)) — a separate violation independent of copyright infringement, where an ordinary fair use defense does not apply, and the only outs are the narrow exemptions the Copyright Office publishes every three years (for example, text and data mining by nonprofit institutional researchers).

So the accurate statement is: the buy-and-scan path was endorsed once, by one judge, in this case — a template you can point to, not a license you can wave. Even with those discounts applied, though, the price-gap logic stands. Between the retail price of a book and a roughly $3,000-per-work bill after the fact lies the entire pricing space for a training-data licensing market. As long as that gap exists, bulk purchasing, scanning, and package licensing deals with publishers may well shift from the ethical choice to the financially cheaper one — a projection, not an established industry fact, but the direction of the arithmetic is hard to miss.

Which leaves one judgment for each of three audiences:

**AI companies**: this case made "where did the data come from" the first question to be settled — but the fight over "what did you do with it" is still ahead, since output-infringement claims were expressly preserved. Data provenance records just changed from an engineering habit into a legal asset: when the next lawsuit comes, a company that can prove where every book came from starts its defense in a different place.

**Authors**: in this case, copyright registration was the ticket to compensation. For authors in the U.S. market, registering on time just changed from lawyerly advice into an act with a dollar figure attached.

**Industry observers**: don't watch the settlement amount; watch the appellate courts. Until fair use is resolved at the circuit level, every new case is a fresh roll of the dice.

$1.5 billion bought quiet, not rules. For Anthropic, it was a good trade. For the industry, the legal foundation under training data is still the same unpoured slab of ground — only now there's a price sign standing on the lot.

## References

- [Anthropic's landmark $1.5B copyright settlement is approved — TechCrunch](https://techcrunch.com/2026/07/20/anthropics-landmark-1-5b-copyright-settlement-is-approved/) — approval news, case background, legality of buy-and-scan, list of other companies still in litigation
- [US judge approves Anthropic's $1.5 billion settlement of copyright lawsuit — Reuters (via WSAU)](https://wsau.com/2026/07/20/us-judge-approves-anthropics-1-5-billion-settlement-of-copyright-lawsuit/) — approving judge, 91% claim rate, $101M attorneys' fees, 7 million pirated books and Alsup ruling description, statements from both sides, objectors
- [US judge approves Anthropic's $1.5 billion settlement — Reuters (via Investing.com)](https://www.investing.com/news/stock-market-news/us-judge-approves-anthropics-15-billion-settlement-of-copyright-lawsuit-4801706) — "largest known copyright recovery" characterization, Sridhar statement
- [Bartz v. Anthropic fair use order (June 23, 2025, Judge Alsup) — Copyright Alliance archive](https://copyrightalliance.org/wp-content/uploads/2025/06/Bartz-v.-Anthropic-Order.pdf) — format-conversion analysis of buying, scanning, and destroying print books; training as fair use; pirated downloads not fair use
- [What Authors Need to Know About the Anthropic Settlement — Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/) — ~500,000 works, ~$3,000 per work, installment schedule (final payment 2027-09-25), work eligibility (ISBN/ASIN and registration windows), default author-publisher 50/50 split
- [Bartz v. Anthropic Settlement FAQ — Authors Alliance](https://www.authorsalliance.org/resources/generative-ai/bartz-v-anthropic-settlement-faq/) — unregistered works ineligible for compensation
- [What to Know About the Bartz v. Anthropic Settlement — Copyright Alliance](https://copyrightalliance.org/participating-bartz-v-anthropic-settlement/) — release cutoff of 2025-08-26 and covered past training/research/product-development claims, no future license, output claims excluded, destruction of pirated files
- [Google faces another AI training lawsuit from major publishers — TechCrunch](https://techcrunch.com/2026/07/14/google-faces-another-ai-training-lawsuit-from-major-publishers/) — new Google lawsuit
- [New York Times says OpenAI hid evidence in ChatGPT copyright trial — TechCrunch](https://techcrunch.com/2026/07/09/new-york-times-says-openai-hid-evidence-in-chatgpt-copyright-trial/) — NYT v. OpenAI still in discovery
- [Opinions — Ninth Circuit](https://www.ca9.uscourts.gov/decisions) — binding effect of published circuit decisions
- [17 U.S.C. § 107 — Cornell LII](https://www.law.cornell.edu/uscode/text/17/107) — the four fair use factors
- [17 U.S.C. § 504 — Cornell LII](https://www.law.cornell.edu/uscode/text/17/504) — statutory damages range
- [17 U.S.C. § 1201 — Cornell LII](https://www.law.cornell.edu/uscode/text/17/1201) — DMCA anti-circumvention provision
- [37 CFR § 201.40 — U.S. Copyright Office](https://www.copyright.gov/title37/201/37cfr201-40.html) — anti-circumvention exemption rules covering DVD (CSS) / Blu-ray (AACS)
