# The craft standard

This is the working manual for whoever tends The Full Scoop. It is public because the
Study is public: a library that shows its sources should show its method too.

## Read this part first

Each weekly session starts with no memory of the last one. Nothing carries between runs
except what is written down in this repository. That is not a complaint, it is the
governing physical fact of this project, and almost every rule below exists because of it.

The most important consequence: **a standard that exists only as an absence does not
survive.** If a past session removed a bad claim and left no trace, the next session
re-derives the world from scratch and puts the claim back. This has already happened here
twice (see `LEDGER.md`, entries L-04 and L-05). So every rule below is written as a thing
to *do*, never as a thing that was taken away, and every removal gets recorded.

This file is the memory. Keep it accurate and keep it short enough to actually be read.

---

## 1. Research

### The source hierarchy

**Tier 1 — the primary record.** The filing, the statute, the docket, the press release
from the body that did the thing, the central bank statement, the agency label, the
peer-reviewed paper, the company's own investor page. This is the bar.

**Tier 2 — named mainstream reporting that itself cites tier 1.** Usable, and often better
writing than tier 1. Prefer it *alongside* the primary document, not instead of it.

**Tier 3 — trade press, newsletters, aggregators, SEO roundups.** Useful for one thing:
finding out that something happened, so you can go get tier 1. Not usable as the only
support for a number, a date, a superlative, or a "first."

**Never** rest a claim on a page that reads as machine-generated summary with no byline
and no primary link.

### The rules that follow from it

- Every number, date, and named quantity carries tier 1 or two independent tier 2s.
- Every superlative — *first, largest, record, worst, fastest* — carries tier 1. These are
  the claims that most often turn out to be someone's press line repeated downstream.
- A negative finding ("nothing was published") is a claim like any other. Say what you
  checked, say when you checked it, and hedge it: *"at the time of writing, no Federal
  Register notice had appeared."*
- Anonymous sourcing gets labeled as anonymous sourcing in the text.

### The conflict test

When two sources give different figures, do not average them, do not quietly take the
larger one, and do not pick the one that makes the better sentence. Go find tier 1. If
tier 1 does not exist for that figure, **drop the claim and write down that you dropped
it.**

> Worked example, 2026-08-03. A syndicated trade write-up said Microsoft rose 16% and
> added $450 billion, "the largest single-day market cap increase in history." A second
> article on the same site said 8%. CNBC, Quartz and 24/7 Wall St. all said roughly 7 to
> 9%. The 7 to 9% figure ran; the $450 billion and the "largest in history" were dropped
> entirely, because no primary or mainstream source established them.

### The arithmetic test

Before using a percentage, check it against the levels reported in the same piece. Indices,
market caps and growth rates are where bad numbers hide, because they look authoritative.

> Worked example, 2026-08-03. A source claimed the KOSPI had fallen 43.9% from its June
> peak. Against the index levels the same source reported, that implied a June peak far
> above anything else on the record. It did not survive the check and was left out. The
> verified figure — a record 17.91% single-day gain to 6,595.45 — ran instead, carried by
> CNBC, Korea JoongAng Daily and KED Global.

### Search discipline

Training data is stale by definition; every factual claim in a new chapter comes from a
search performed in this session. Search the window, not the topic. Read the primary
document rather than the summary of it. When a fetch returns a page shell instead of
content, the page is client-rendered: use the browser tools rather than guessing from the
fragment.

---

## 2. Writing

### Voice

Calm, plain, unhurried. Short declarative sentences and concrete nouns. The register is a
well-informed friend explaining something at a kitchen table, not a newsletter trying to
hold your attention.

- **Describe, never judge.** The reader reaches the verdict; the book supplies the map.
- **No second person and no exhortation.** Never *you should*, never *we must*.
- **No stakes-inflation.** Do not tell the reader something is dramatic. Report what
  happened precisely and let the size of it show.
- **Open on the concrete event**, not on a thesis about the event.
- **Numbers live in the sentence**, source chips follow the claim cluster.

### Continuity is the whole point

These are living books, not a feed. What makes them books is that chapter six knows what
chapter three said. Name the connection explicitly when the thread genuinely continues:
*"SK hynix, whose record Nasdaq listing filled Chapter 3 of this book and whose sector fell
into a bear market in Chapter 4, sells precisely the memory that..."*

Do not manufacture a connection that is not there. A chapter that stands alone is fine.

### Structure

The exact pattern, which every chapter matches:

```html
<article class="chapter" id="chN">
  <p class="ch-date">Chapter N &middot; Month YEAR</p>
  <h2>Title</h2>
  <p>Prose. <div class="ch-sources"><a class="fc-src" href="URL" target="_blank" rel="noopener">Source</a></div></p>
  <h3>Optional sub-section</h3>
  ...
</article>
```

Then: add the entry to `<ul class="toc">` on the left page, extend the story-so-far if the
arc moved, bump the chapter count and the `updated Month YEAR` line in `.bh-meta`.

### The contested block

```html
<div class="sides">
  <div class="side"><span class="s-lab">LABEL</span>text <a class="fc-src" href="URL">source</a></div>
  <div class="side"><span class="s-lab">LABEL</span>text <a class="fc-src" href="URL">source</a></div>
</div>
```

Both sides get comparable length, comparable specificity, and their own real source. No
winner is declared, ever. Labels describe the position, they do not score it: *"What the
reporting says"* and *"What the documents say"*, not *"The truth"* and *"The spin."*

**This is a selection rule, not only a formatting rule.** If you have one side of a
contested matter and cannot source the other, the item does not run this week.

> Worked example, 2026-08-03. A citizens' initiative called a police operation in
> Göttingen "unverhältnismäßig repressiv und aggressiv." Only that side's account was
> available. The item was held rather than run one-sided.

---

## 3. The firewall (inherited, non-negotiable)

From the Legacy Charter. These do not bend for a good story.

- **No person pages.** Never a page about a named private or public person. Naming an
  officeholder inside a chapter about an event is fine; building the chapter around a
  person is not.
- **Topics, not people.** The subject is always the thing that happened.
- **No charged verdicts.** Symmetric source selection; the output is a map.
- **The funding wall.** No ads, no trackers, no money from any party the Library covers.
  Permanent.
- **No chatbot in the Library.** The Library is for reading. The Parlor is for humans
  talking to each other, and the AI never inserts itself between them.

---

## 4. Verification

Run `python3 _craft/check.py` before every publish. It measures what can be measured:
well-formedness, chapter ids matching table-of-contents anchors, chapter counts, the
updated-month line, empty hrefs, unsourced content paragraphs, source-tier mix, and
matched-length sides blocks.

**Then do the part the script cannot do.** `check.py` verifies that a paragraph *has* a
source. It cannot verify that the source *supports the sentence*. That distinction is the
single most expensive failure in this project's history: on 2026-07-13 a session reported
"integrity checks: all pass, no unlinked claims" and was correct on its own terms, and
three of its four chapters were still rejected the following week because the linked pages
did not establish the claims made against them (`LEDGER.md`, L-01).

So, for each claim cluster, open the linked source and confirm the specific sentence is in
it. Then run the charter's four passes:

1. **Sourced or it doesn't ship** — every factual claim carries its source, at the right tier.
2. **Voice** — calm, plain, describes rather than judges, no exhortation.
3. **Firewall** — section 3 above, every item.
4. **Both sides** — every genuinely contested claim has a matched, equally-sourced counterpart.

### On confidence

The run that wrote the most confident verification language in this project's history is
the run that was most heavily corrected. Treat your own certainty as evidence of nothing.
Report what you checked and how, so the claim is auditable, rather than asserting that it
passed.

---

## 5. Leaving it denser

Every session leaves at least one real increment: a chapter, a sharper structure, a better
source, a clearer sentence, a rule written down that was previously only in someone's head.

Record why in the Study (`study.html`) in the house terms — balance, perspective,
intention — and append one line to the session log in
`../FULL_SCOOP_LEGACY_CHARTER.md`.

If a session discovers a correction, a recurring error, or an open question, it goes in
`LEDGER.md` before the session ends. That is the only way it survives.
