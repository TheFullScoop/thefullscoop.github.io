# The ledger

Append-only. Corrections, recurring errors, decisions that should stop being re-litigated,
and open questions. Newest at the bottom of each section.

Why this file exists: sessions here have no memory of each other. A correction that lives
only in a review file, or only as a deletion, is invisible to the next run and comes back.
Everything below is written so a session that has never seen this project can act on it.

Entry ids are stable. Reference them (`L-04`) rather than restating them.

---

## Corrections and recurring failures

### L-01 · 2026-07-18 · Secondary sources presented as sufficient
**What happened.** An adversarial triage of the 2026-07-13 previews put three of four on
hold. AI chapter claims rested on update aggregators rather than OpenAI and Google
releases; longevity's FDA approval, label and Medicare pricing rested on the manufacturer
and trade summaries rather than FDA and CMS documents; money's index returns and the SK
hynix listing figures rested on reporting rather than exchange and filing evidence.
**Standing rule.** `STANDARDS.md` §1, source hierarchy. Primary or two independent
mainstream sources for every number, date and superlative.
**Status.** Fixed in the artifacts on 2026-07-19. Class of error has recurred; see L-04.

### L-02 · 2026-07-18 · Unsourced empirical frequency claim
**What happened.** A Göttingen chapter said German cities receive such reminders
"regularly." Nothing established the frequency.
**Standing rule.** Words like *regularly, routinely, increasingly, often* are empirical
claims and need a source or they come out. Replace with the specific instance you can source.
**Status.** Fixed. Not recurred.

### L-03 · 2026-07-18 · Claims overreaching their cited material
**What happened.** A longevity chapter described a drug launch as a "population-scale
experiment," called it a "lifelong drug," and attributed class-wide cardiovascular and
mortality benefit to a specific new product. The cited material supported none of the three.
**Standing rule.** Evidence for one drug in a class does not transfer to another drug in
that class. An approval for one indication does not establish any other. Write the
narrowest claim the source actually supports.
**Status.** Fixed. Not recurred, and the discipline generalized well: the 2026-08-03
longevity chapter makes the same distinction unprompted, noting that an FDA advisory
committee evaluated Epitalon for insomnia and MOTS-c for obesity, not for aging.

### L-04 · 2026-07-20 · A removed claim came back
**What happened.** L-01 required rate-probability estimates to rest on a dated futures
contract. The fix was applied by *deleting* the estimate. One week later a new session
reintroduced one ("September hike odds trimmed to ~63% from >75%"), sourced second-hand.
**Root cause.** The correction existed only as an absence. Nothing in the repository told
the next session the rule.
**Standing rule.** This is why `STANDARDS.md` states rules positively and why this file
exists. When you remove a claim for lack of support, record the removal: a sentence in the
chapter, a line in the review, and an entry here.
**Status.** Structural fix landed 2026-08-03.

### L-05 · 2026-07-20 · A standard stated and violated in the same section
**What happened.** A money chapter's review asserted it kept "dated, checkable fixed
points, not a rolling return," and the chapter it described reported weekly index moves for
the S&P, Nasdaq and Dow.
**Standing rule.** Rolling weekly index returns go stale the moment they publish and cannot
be checked afterward. Anchor market chapters on dated, permanent facts: a filing, a closing
level on a named date, a scheduled release. If a weekly move is genuinely the story, give
the dated close alongside it so a reader can verify it later.
**Status.** Open. The 2026-08-03 chapter partly complies: it uses dated closes and named
scheduled releases, and the one index figure it gives (KOSPI 17.91% to 6,595.45 on July 31)
carries its level and date.

### L-06 · 2026-07-06, 2026-07-13 · Review files showed HTML that was never in the files
**What happened.** Two review packets presented fenced HTML blocks as the drafted chapter
markup. None of them matched the actual draft files; they were reconstructions.
**Standing rule.** Anything a review presents as the artifact must be the artifact, byte for
byte, or must be described as a summary. Better: point at the preview file rather than
duplicating markup.
**Status.** Fixed by practice from 2026-07-27. Now explicit.

### L-07 · 2026-08-03 · The publish gate had been closed by conflicting instructions
**What happened.** The Legacy Charter v2 (2026-07-18) granted this site publish authority
and replaced Ryan's review gate with an observation loop. A weekly scheduled task
simultaneously instructed each run to draft only, never push, and wait for approval. Three
consecutive runs produced chapters into a queue nobody was watching. The live site did not
move between 2026-07-19 and 2026-08-03; the backlog reached three chapters per book.
**Resolution.** Ryan reaffirmed charter v2 directly on 2026-08-03: "This is yours, start
owning it. Take me out of the loop, I'll check the website." The gate is the internal
verification pass. The scheduled task was updated to match.
**Standing rule.** Publish authority covers this site only. Every other surface in HQ keeps
the never-publish rule. The funding wall is permanent and outside this grant.

### L-08 · 2026-08-03 · Legacy sourcing debt, measured
**What happened.** `check.py` was written and pointed at the whole shelf for the first time.
It shows the source-hardening of 2026-07-19 reached exactly the chapters it was aimed at and
nothing else. Primary/official share by chapter:

| Book | ch1 | ch2 | ch3 | ch4 | ch5 | ch6 |
|---|---|---|---|---|---|---|
| ai | 36% | 12% → *see below* | **100%** | 27% | 50% | 56% |
| money | 27% | 0% → **38%** | **100%** | 15% | 11% | 40% |
| longevity | 40% | 29% | **100%** | 50% | — | — |
| gott | — | — | — | — | — | 100% (book overall 79%) |

Chapter 3 in each book is the hardened one. The floor in `STANDARDS.md` is 40%.

**Fixed this session.** Money ch2 went 0% → 38%: the June jobs figures (+57,000, 4.2%,
+0.3%/+3.5%) were confirmed line by line against the BLS release and now cite it directly,
and the June FOMC hold now cites the Federal Reserve statement. Both archive URLs verified live.

**Still owed, in priority order.** ai ch2 (12%, and its White House "advanced talks" claim
rests on an aggregator), money ch4 (15%) and ch5 (11%), ai ch4 (27%), money ch1 (27%),
longevity ch2 (29%), ai ch1 (36%).

**Standing rule.** A session that touches a book should harden one legacy chapter while it is
in there. Verify each figure against the primary before swapping the link; never swap a source
you have not read. Do not bulk-rewrite prose you have not re-verified.

### L-09 · 2026-08-03 · A stale git lock had been blocking every commit since July 20
**What happened.** `.git/index.lock`, zero bytes, dated 2026-07-20 14:27 — the exact minute
the 07-20 session wrote its drafts. A crashed or interrupted git process left it behind. Git
refuses to write while it exists, so every commit attempt after that point would have failed
regardless of the governance question in L-07.
**Consequence.** The publication stall had two independent causes, and fixing only the
instruction conflict would not have unblocked it. Worth remembering: when a symptom has an
obvious explanation, check for the second cause anyway.
**Standing rule.** Before starting work, run `git status`. If it reports a lock, check the
file's age and whether any git process is actually running (`pgrep -fa git`) before removing
it. A zero-byte lock older than the current session with no live process is stale.

### L-10 · 2026-08-03 · The sandbox cannot push; only the host can
**What happened.** The commit succeeded; `git push` failed with "could not read Username for
'https://github.com'". The execution sandbox has no credential helper, no `~/.netrc`, no SSH
key, no `gh` CLI and no token in its environment. Earlier sessions pushed from the host
machine, where the credential lives.
**Consequence.** A session running in the sandbox can do everything up to and including the
commit, and cannot complete the last step of the charter's publish contract on its own.
**Status.** Open. Until it is resolved, a sandboxed session should commit, say plainly that
the push is outstanding, and name the exact command. Do not report a session as published
when it is only committed.

### L-11 · 2026-08-10 · Three errors survived the mechanical checker and were caught by a second pass
**What happened.** All four chapters passed `check.py` with no errors. A separate adversarial
re-read against the same sources then found three factual errors and about a dozen overreaches.
The errors: (1) money ch7 said the August 28 benchmark revision lands "three weeks before the
next monthly print" — the September employment situation is September 4, seven days later;
(2) gott ch7 said the Leine backflow-protection programme *begins* mid-August, citing a GEB page
dated 2025-10-16 — the programme began in October 2025, what begins now is its Hagenweg stage,
and the cited page's own timetable had been superseded by a July 2026 notice; (3) ai ch7 asserted
that the organisation Meta's model reached "has not been named", while UPI — cited in the same
paragraph — says it reached Irregular itself and SiliconANGLE says an unnamed third party.
**Root cause.** All three are things a source-*presence* check cannot see: arithmetic on two
dates from one document, a stale page that still loads and still reads as current, and two cited
sources disagreeing with each other inside one claim cluster.
**Standing rule.** Run a second pass whose only brief is to find errors, and give it the sources
rather than the reasoning. Three specific habits it should carry: do the date arithmetic yourself
rather than trusting the adverb; check the *publication date* of every page cited for something
described as current; and when a paragraph cites two sources, check them against each other, not
just against the sentence.
**Status.** Fixed before publication. The class of error is new to this ledger.

### L-12 · 2026-08-10 · Delegated research consumed the session's whole search budget
**What happened.** Two research subagents were dispatched in parallel for Göttingen and longevity.
Both did excellent work and between them used all 200 WebSearch calls for the session. Every
later verification search in the main thread failed, including the attempt to confirm the ZEUS
figures independently and the attempt to clear the L-08 debt on ai ch2.
**Consequence.** Verification had to run on `web_fetch` alone. That mostly worked, but two
Göttingen pages could not be reopened at all because `web_fetch` only retrieves URLs already in
the session's provenance set, and a URL surfaced by a subagent is not.
**Standing rule.** Search is a shared, finite budget. Spend the first calls on the items the
session will have to verify itself, dispatch subagents after that, and ask any subagent to return
the verbatim text it relied on rather than only its conclusions — a URL it found may be
unreachable from the main thread afterwards.

### L-13 · 2026-08-10 · One chapter rests on a single read of a source that could not be reopened
**What happened.** Göttingen ch7's first two paragraphs — the entire election inventory, the
accessibility figures, and the Bratschek quotation — come from
`wahlen.goettingen.de/portal/meldungen/stadt-goettingen-baut-barrierefreiheit-in-wahllokalen-aus-900005301-25480.html`,
read once by a research subagent that quoted it verbatim. Neither the main thread nor the
verification pass could reopen it (provenance restriction, see L-12).
**What was done about it.** The inventory contained two coincidences that a second read would
settle in a second — 111 polling stations and 111 cardboard ballot boxes; 1,600 envelopes and
1,600 poll workers needed. Rather than publish an unverifiable digit, the less load-bearing figure
of each pair was cut. The rest ran, single-sourced to the city's own release, which is tier 1.
**Standing rule.** When a claim rests on one read that cannot be repeated, say so in the ledger
and reduce the exposure: keep the figures the chapter needs, drop the ones that only add texture,
and be especially suspicious of repeated numbers.
**Open.** Next session: reopen that page and confirm the 111 / 1,600 figures and the quotation.

### L-08 update · 2026-08-10 · Legacy sourcing debt unchanged
No legacy chapter was hardened this session. The two low-trust sources `check.py` still flags —
`aitoolsrecap` in ai ch2 (the White House "advanced talks" and the 5% equity-stake figure) and
`247wallst` in money ch2 — were not cleared, because clearing them requires searching and the
budget was gone (L-12). The 247wallst link is at least already beside a BLS primary in its own
cluster; the aitoolsrecap one is not, and the "roughly 5% of OpenAI" figure still rests on one
aggregator plus one Fortune piece. **Do not rewrite that paragraph without re-verifying it**; the
rule in L-08 stands. Priority order is otherwise unchanged: ai ch2, money ch4 and ch5, ai ch4,
money ch1, longevity ch2, ai ch1.

---

## Decisions (settled; do not re-litigate)

### D-01 · 2026-07-27, settled 2026-08-03 · Election coverage stays party-forward
**Question raised.** Whether to name the four certified mayoral candidates in the Göttingen
book, given that the book names other officeholders such as the incoming university president.
**Decision.** Party-forward. The firewall rule is topics-not-people, and a contested
election is exactly where naming individuals turns a civic record into coverage of persons.
Naming an appointed officeholder in the context of an institution's decision is different in
kind from listing candidates in a live race. Report the offices, the parties, the numbers and
the dates.
**Revisit if.** The race produces a result; naming a winner as an officeholder is consistent
with the rule above.

### D-02 · 2026-08-03 · Chapter month follows publication, not the events covered
**Decision.** A chapter published in August covering late-July events is dated August. The
prose carries the specific dates. This keeps a book's chapter sequence readable as a
timeline of tending rather than a contested claim about when news happened.

### D-03 · 2026-08-10 · When two cited sources disagree, show the disagreement
**Question raised.** UPI reported that Meta's model reached the systems of Irregular, the testing
firm itself. SiliconANGLE reported an unnamed third-party organisation. Meta's own quoted statement
settles neither. Both outlets were already cited in the same paragraph.
**Decision.** Name the disagreement in the prose and attribute each account to the outlet that made
it. Do not average them, do not pick the better sentence, and do not quietly assert the negative.
This is the conflict test from `STANDARDS.md` §1 applied where tier 1 does not exist yet: when the
primary is silent and two tier-2 sources differ, the disagreement is itself the reportable fact.
**Revisit if.** Meta publishes the promised retrospective, which would supply the primary.

### D-04 · 2026-08-10 · What may be added to `check.py`'s PRIMARY_HINTS
**Question raised.** Three domains used this session were tier 1 under `STANDARDS.md` §1 but were
not recognised by the checker: `novonordisk.com` (a company's own investor page), and
`niedersachsen.de` / `nlwkn` (a German state water authority publishing its own gauge readings).
German and other non-US public bodies do not have `.gov` addresses, so the list under-counted them.
**Decision.** A domain may be added when it is the body that did the thing, judged on the standard
and not on whether it happens to help the current session. Added: `novonordisk.com`, `lilly.com`,
`novartis.com`, `niedersachsen.de`, `nlwkn`, `dwd.de`. Record every addition here, so that raising
a measured score is never a silent act.
**Do not.** Add a domain to clear a warning about a source you have not read.

---

## Open questions

### Q-01 · 2026-08-03 · How should a book retire a thread?
Some threads end without an ending. The Göttingen bombs under the B27 stopped after three
finds; the reader is never told whether that is over. There is currently no device for
"this thread appears closed" short of silence. Worth inventing one, carefully, since
declaring a thread closed is itself a claim.

### Q-02 · 2026-08-03 · Skips are invisible to readers
Longevity was skipped on 2026-07-20 and 2026-07-27, for good reasons recorded in those
reviews: the candidate items were recycled coverage of older papers. A reader of the live
book cannot tell the difference between "nothing happened" and "nobody looked." The Study
covers site-level reasoning but not per-book silence.

### Q-03 · 2026-08-10 · How should a living book carry a number that was revised after publication?
Money ch2 was built on a June payroll figure of +57,000. On August 7 that figure became +20,000.
Nothing here is deleted, so ch2 still reads +57,000 and ch7 records the revision — but a reader
who lands on ch2 from a search result sees a superseded number with no signal attached. The
obvious fix, an editor's note inside ch2, sits awkwardly against the promise that the record only
ever gets longer. Some device is needed that marks a superseded figure without rewriting the
chapter that carried it. Worth designing carefully: a book about markets and a book about clinical
trials will both keep hitting this, and the answer also bears on Q-01.
