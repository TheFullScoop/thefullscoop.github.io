# The weekly runbook

The recurring job: find what genuinely changed in each open book's subject over the last
week or two, and add one dated chapter where there is something real to add.

Operating mode is **Legacy Charter v2**: verify, then publish. There is no human approval
gate. The internal verification pass replaces it and may never weaken. See `LEDGER.md`
L-07.

---

## Before anything else

Read, in this order:

1. `../FULL_SCOOP_LEGACY_CHARTER.md` — the authority, the seeds, the hard rules.
2. `STANDARDS.md` — how to research, write and verify here.
3. `LEDGER.md` — what has already gone wrong, what is settled, what is open.
4. The books you are about to touch.

Skipping step 3 is how this project repeats itself.

---

## The books

Four are **open** and get weekly attention:

| File | Book | Notes |
|---|---|---|
| `books/ai.html` | The State of AI | models, agents, the money, the fights |
| `books/longevity.html` | Longevity & Healthspan | what has evidence vs. what sells |
| `books/gott.html` | Göttingen | include German-language sources |
| `books/money.html` | Money & Markets | understanding, not stock tips |

The other books on the shelf are stubs. Do not touch them as part of this run.

---

## The pass

**1. Read the existing chapters.** Establish what is already covered and what the last
chapter date is. New material must be new *relative to the book*, not merely recent.

**2. Search.** Extensively, and from this session — training data is stale by definition.
Work the window (roughly the last one to two weeks), and chase every item back to its
primary document per `STANDARDS.md` §1.

**3. Decide what is real.** Ask of each candidate: did something actually change, or did
coverage of something old recirculate? A newsletter resurfacing a four-month-old paper is
not news. **If a book has nothing real this week, skip it and say why.** Fewer, well-sourced
chapters beat a pile of thin ones. Two consecutive skips is a legitimate outcome.

**4. Draft one chapter per book that has something.** Match the structure in
`STANDARDS.md` §2 exactly. Prefer a chapter that continues a thread the book has already
been pulling.

**5. Update the surrounding page.** Table of contents entry, story-so-far if the arc moved,
chapter count and `updated Month YEAR` in `.bh-meta`.

**6. Verify.**

```
python3 _craft/check.py                 # all four open books
python3 _craft/check.py books/ai.html   # one file
```

Fix everything it reports. Then do the manual pass it cannot do: open each linked source
and confirm it supports the specific sentence. Then the charter's four checks — sourced,
voice, firewall, both-sides.

**7. Record the reasoning.** A Study entry (`study.html`) in house form: what changed, then
a `Why these changes` paragraph covering balance, perspective and intention. Match the
existing entries.

**8. Ledger anything durable.** A correction, a dropped claim, a recurring failure, a
decision that should stop being re-argued, an open question. If it only lives in your
context window, it is already gone.

**9. Publish.** One commit, then push.

```
git add -A
git commit -m "Legacy session YYYY-MM-DD: <what got denser>"
git push
```

**10. Append one line** to the session log at the bottom of
`../FULL_SCOOP_LEGACY_CHARTER.md`: date, agent, what got denser, commit hash.

---

## Scope of publish authority

This site only. `getthefullscoop.org` is the sole surface in HQ that may be pushed from
this program. Everything else keeps the never-publish rule unchanged. No money, ever; the
funding wall is permanent and no grant of authority touches it.

Structural changes — a new book, a new room, a change to the voice or the firewall — are
inside the charter's creative-control grant, but they get a Seed Ledger row with the
reasoning at birth, and hard rules never bend.

---

## Failure modes worth knowing before you start

- Rebuilding on stale state. Check whether previous drafts were merged before drafting on
  top of the live page, or you will duplicate or skip chapters.
- Asserting a verification you did not perform. Run the script and report its output.
- Removing a bad claim and leaving no record of it (`LEDGER.md` L-04).
- Confidence. The most confident review in this project's history preceded its largest
  correction. Report method, not assurance.
