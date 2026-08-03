# The Full Scoop — front door

The deploy repository for getthefullscoop.org. A small public library of living books:
dated chapters that accrete as a story develops, every claim linked to its source, both
sides shown, no verdicts.

## Read before working here

1. `../FULL_SCOOP_LEGACY_CHARTER.md` — the authority. The two seeds, the hard rules, the
   publish grant, the session log.
2. `_craft/STANDARDS.md` — how to research, write and verify here.
3. `_craft/LEDGER.md` — what has already gone wrong, what is settled, what is still open.
4. `_craft/RUNBOOK.md` — the weekly chapter procedure.

Sessions here have no memory of each other. Those files are the memory, and they only work
if each session reads them at the start and adds to them at the end.

## Before publishing

```
python3 _craft/check.py
```

Fix every error. Then the manual pass the script cannot do — open each source and confirm
it supports the sentence — then the charter's four checks: sourced, voice, firewall, both
sides.

## Authority

Publish authority covers **this site only** (Legacy Charter v2, reaffirmed 2026-08-03).
Every other surface in HQ keeps the never-publish rule. No money, ever: the funding wall
is permanent and no grant of authority touches it.

## Layout

```
books/          the shelf. four open books get weekly chapters; the rest are stubs
_craft/         standards, runbook, ledger, checker
_drafts/        weekly previews and review packets
study.html      the public journal of what changed and why
parlor.html     the connection wing — humans talking to each other, never to the AI
```
