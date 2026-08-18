#!/usr/bin/env python3
"""Mechanical verification for Full Scoop book pages.

    python3 _craft/check.py                 # all four open books
    python3 _craft/check.py books/ai.html   # specific files

Checks what can be measured. It CANNOT check that a linked source supports the sentence
it is attached to -- that pass is manual and is the one that has actually failed here.
See _craft/STANDARDS.md section 4.

Exit code 0 = no errors. 1 = at least one error. Warnings never fail the run.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
OPEN_BOOKS = ["books/ai.html", "books/longevity.html", "books/gott.html", "books/money.html"]

VOID = {"meta", "link", "br", "img", "input", "hr", "rect", "circle", "path", "source", "use"}

# Domains whose pages are the primary record for the claims we cite.
PRIMARY_HINTS = (
    ".gov", ".europa.eu", ".int", "federalreserve.gov", "bea.gov", "bls.gov", "fda.gov",
    "sec.gov", "cms.gov", "congress.gov", "whitehouse.gov", "ecb.europa.eu",
    "openai.com", "anthropic.com", "blog.google", "microsoft.com", "aboutamazon.com",
    "thinkingmachines.ai", "github.com", "cdn.openai.com",
    "nature.com", "thelancet.com", "nejm.org", "pubmed.ncbi.nlm.nih.gov",
    "pmc.ncbi.nlm.nih.gov", "doi.org", "arxiv.org", "clinicaltrials.gov",
    "novonordisk.com", "lilly.com", "novartis.com", "research.meta.ai", "meta.com",
    "kansascityfed.org",
    "goettingen.de", "uni-goettingen.de", "umg.eu", "sartorius.com", "bundestag.de",
    "niedersachsen.de", "nlwkn", "dwd.de",
    "consilium.europa.eu", "digital-strategy.ec.europa.eu", "commission.europa.eu",
    "universiteitleiden.nl", "hhs.gov", "gartner.com", "pwc.com", "nasdaq.com",
    "freddiemac.com", "eurostat", "ec.europa.eu", "trahan.house.gov", "irregular.com",
)

# Low-trust: fine for colour, never the sole support for a number or superlative.
AGGREGATOR_HINTS = (
    "aitoolsrecap", "buildfastwithai", "llm-stats", "cometapi", "coursiv", "nipralo",
    "explainx.ai", "byteiota", "developersdigest", "pasqualepillitteri", "aiweekly.co",
    "rauljitechnologies", "tradingkey", "mexc.com", "financialcontent", "247wallst",
    "tech-insider", "vorplabs", "cornfordandcross", "americanwellnesspharmacy",
    "mypeptidematch", "drsobo", "olakai", "honehealth", "gethealthspan", "coldture",
)

SUPERLATIVE = re.compile(
    r"\b(first|largest|biggest|record|worst|best|fastest|highest|lowest|"
    r"unprecedented|never before|all-time)\b", re.I)


class WellFormed(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}> at line {self.getpos()[0]}")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
        elif any(t == tag for t, _ in self.stack):
            while self.stack and self.stack[-1][0] != tag:
                t, ln = self.stack.pop()
                self.errors.append(f"<{t}> opened line {ln} not closed before </{tag}>")
            self.stack.pop()
        else:
            self.errors.append(f"stray </{tag}> at line {self.getpos()[0]}")


class Report:
    def __init__(self, path: str):
        self.path = path
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, m): self.errors.append(m)
    def warn(self, m): self.warnings.append(m)
    def note(self, m): self.notes.append(m)

    def render(self) -> bool:
        icon = "FAIL" if self.errors else ("WARN" if self.warnings else "ok  ")
        print(f"[{icon}] {self.path}")
        for n in self.notes:
            print(f"       . {n}")
        for w in self.warnings:
            print(f"       ? {w}")
        for e in self.errors:
            print(f"       X {e}")
        return not self.errors


def strip_tags(fragment: str) -> str:
    return re.sub(r"<[^>]+>", " ", fragment)


def check(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    r = Report(rel)
    if not path.exists():
        r.error("file does not exist")
        return r.render()
    html = path.read_text(encoding="utf-8")

    # --- structure -----------------------------------------------------------
    wf = WellFormed()
    wf.feed(html)
    for e in wf.errors[:8]:
        r.error(f"html: {e}")
    for t, ln in wf.stack[:5]:
        r.error(f"html: <{t}> opened line {ln} never closed")

    chapters = re.findall(r'<article class="chapter" id="(ch\d+)">', html)
    toc = re.findall(r'<li><a href="#(ch\d+)">', html)

    if not chapters:
        r.error("no chapters found")
        return r.render()

    nums = [int(c[2:]) for c in chapters]
    if nums != sorted(nums) or nums != list(range(1, len(nums) + 1)):
        r.error(f"chapter ids not a clean 1..N sequence: {chapters}")
    if len(set(chapters)) != len(chapters):
        r.error(f"duplicate chapter ids: {chapters}")
    if chapters != toc:
        r.error(f"toc does not match chapters. chapters={chapters} toc={toc}")

    # counts and dates
    m = re.search(r"<span>(\d+) chapters?</span>", html)
    if not m:
        r.error("no '<span>N chapters</span>' in .bh-meta")
    elif int(m.group(1)) != len(chapters):
        r.error(f".bh-meta says {m.group(1)} chapters, found {len(chapters)}")

    upd = re.search(r"updated <strong>([^<]+)</strong>", html)
    ch_dates = re.findall(
        r'<p class="ch-date">Chapter \d+ (?:&middot;|·) ([A-Za-z]+ \d{4})</p>', html)
    if len(ch_dates) != len(chapters):
        r.error(f"{len(chapters)} chapters but {len(ch_dates)} well-formed ch-date lines")
    if not upd:
        r.error("no 'updated <strong>Month YEAR</strong>' line")
    elif ch_dates and upd.group(1).strip() != ch_dates[-1].strip():
        r.error(f"updated '{upd.group(1)}' != last chapter date '{ch_dates[-1]}'")

    # --- sourcing ------------------------------------------------------------
    bodies = re.findall(
        r'<article class="chapter" id="ch\d+">(.*?)</article>', html, re.S)

    unsourced = 0
    for ci, body in enumerate(bodies, 1):
        for para in re.findall(r"<p>(.*?)</p>", body, re.S):
            text = strip_tags(para).strip()
            if len(text) < 140:
                continue  # pull quotes / question lines, not claim paragraphs
            if 'class="ch-sources"' not in para and 'class="fc-src"' not in para:
                unsourced += 1
                r.error(f"ch{ci}: content paragraph with no source: \"{text[:70]}...\"")

    links = re.findall(r'class="fc-src" href="([^"]+)"', html)
    if not links:
        r.error("no source links at all")
    empty = len(re.findall(r'href=""', html))
    if empty:
        r.error(f"{empty} empty href attributes")

    bad_scheme = [u for u in links if not u.startswith("https://")]
    for u in bad_scheme[:5]:
        r.warn(f"source link is not https: {u}")

    hosts = [urlsplit(u).netloc.lower() for u in links]
    primary = sum(1 for h in hosts if any(k in h for k in PRIMARY_HINTS))
    aggregator = [u for u in links if any(k in u.lower() for k in AGGREGATOR_HINTS)]
    share = round(100 * primary / len(links)) if links else 0
    r.note(f"{len(chapters)} chapters, {len(links)} source links, {share}% primary/official")
    if share < 40:
        r.warn(f"primary-source share {share}% is below the 40% floor (STANDARDS.md 1)")
    for u in aggregator[:6]:
        r.warn(f"low-trust source, needs a primary alongside it: {u}")

    # newest chapter gets a closer read
    newest = bodies[-1]
    n_links = re.findall(r'class="fc-src" href="([^"]+)"', newest)
    n_hosts = [urlsplit(u).netloc.lower() for u in n_links]
    n_primary = sum(1 for h in n_hosts if any(k in h for k in PRIMARY_HINTS))
    n_share = round(100 * n_primary / len(n_links)) if n_links else 0
    r.note(f"newest chapter (ch{len(bodies)}): {len(n_links)} links, {n_share}% primary/official")
    if n_links and n_share < 40:
        r.warn(f"newest chapter primary share {n_share}% is below the 40% floor")

    for para in re.findall(r"<p>(.*?)</p>", newest, re.S):
        text = strip_tags(para)
        hit = SUPERLATIVE.search(text)
        if hit and 'class="fc-src"' in para:
            para_hosts = [urlsplit(u).netloc.lower()
                          for u in re.findall(r'class="fc-src" href="([^"]+)"', para)]
            if not any(any(k in h for k in PRIMARY_HINTS) for h in para_hosts):
                r.warn(f'superlative "{hit.group(0)}" without a primary source in that cluster')

    # --- both sides ----------------------------------------------------------
    for block in re.findall(r'<div class="sides">(.*?)</div>\s*</(?:article|div)>', html, re.S) \
            or re.findall(r'<div class="sides">(.*?)$', html, re.S):
        pass  # handled below with a tighter pattern

    for block in re.findall(r'<div class="sides">((?:(?!<div class="sides">).)*?)</div></div>',
                            html, re.S):
        sides = re.findall(r'<div class="side">(.*?)</div>', block + "</div>", re.S)
        sides = [s for s in sides if s.strip()]
        if len(sides) != 2:
            r.error(f"sides block has {len(sides)} sides, expected 2")
            continue
        lens = [len(strip_tags(s).strip()) for s in sides]
        if min(lens) and max(lens) / min(lens) > 2.4:
            r.warn(f"sides block lengths are lopsided: {lens[0]} vs {lens[1]} chars")
        for s in sides:
            if 'class="fc-src"' not in s:
                r.error("a side of a contested block carries no source")

    # --- firewall ------------------------------------------------------------
    for word in ("obviously", "clearly the", "should be obvious", "everyone knows",
                 "it is clear that", "disastrous", "catastrophic failure"):
        if re.search(rf"\b{re.escape(word)}\b", strip_tags(html), re.I):
            r.warn(f'voice: charged or verdict-like phrasing "{word}"')

    if unsourced == 0 and links:
        r.note("every content paragraph carries a source block (link support still manual)")

    return r.render()


def main() -> int:
    args = sys.argv[1:]
    targets = [ROOT / a for a in args] if args else [ROOT / b for b in OPEN_BOOKS]
    print(f"Full Scoop check -- {len(targets)} file(s)\n")
    ok = all([check(t) for t in targets])
    print()
    if ok:
        print("PASS (mechanical). Now do the manual pass: open each source and confirm it")
        print("supports the sentence. Then voice, firewall, both-sides. STANDARDS.md 4.")
    else:
        print("FAIL. Fix the errors above before publishing.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
