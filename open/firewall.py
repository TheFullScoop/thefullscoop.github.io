"""
engine/firewall.py — the executable leash-detector. Turns GOAL.md's firewall into code so "validated" is a
re-runnable check, not an opinion. firewall_check(package) runs the conditions in charter order and returns
PASS or the failing conditions (first-failure-kills is enforced by the caller treating any failure as fatal).

Mission: catch a leash before it ships. A directional hook, a page with no supporting source, a verdict, a
creator-blaming line, a sell — each is a hard fail. Reading grade is estimated (Flesch-Kincaid).
"""
from __future__ import annotations
import re

# directional / accusatory hook language — the opposite of the "embarrassment test"
DIRECTIONAL = re.compile(r"(not telling|won'?t tell|the truth is|debunk|exposed|exposing|really means|"
                         r"\blies\b|\blying\b|\bliar\b|brainwash|\bsheep\b|wake up|propaganda|shill|"
                         r"the real reason|what they don'?t want)", re.I)
# verdict phrasing — telling the reader what to conclude or do
VERDICT = re.compile(r"(therefore|you should|distrust|don'?t trust|stop trusting|must reject|proves that)", re.I)
# blaming a person/creator instead of contextualizing the topic
BLAME = re.compile(r"(is lying|is misleading you|is dishonest|the creator is wrong|is a liar|deceiv\w+ you)", re.I)
# selling / market language (money OUT) — narrow, to avoid flagging financial TOPICS (cost, $, prices)
MONEY = re.compile(r"(subscribe to us|our product|sign up now|premium plan|pricing plan|monetize|"
                   r"buy now|our service|paying customers|our sponsor)", re.I)
# charged moral/criminal characterizations of a person — may be REPORTED as an attributed/contested claim,
# but NEVER asserted by us as established fact (a claim marked "supported"). "X supports genocide" marked
# supported is a verdict on a person, not a fact we can stand behind.
CHARGED = re.compile(r"(genocid\w*|pedophil\w*|paedophil\w*|groomer|child molest\w*|\brapist\b|\bnazi\b|"
                     r"fascist|terrorist|traitor|treason\w*|white supremac\w*|\bracist\b|corrupt\w*)", re.I)
# page framed around judging a NAMED INDIVIDUAL (their "record" / "claims about [a politician]") instead of a
# contested TOPIC — mechanism-not-actor at the page level: we cover issues, never put a person on trial.
PERSON_TARGET = re.compile(r"('s record\b|claims about (a |an |the )?[\w\s]{0,30}?"
                           r"(senator|congress\w*|governor|mayor|president|judge|justice|representative|lawmaker)|"
                           r"\b(senator|congressman|congresswoman|governor|mayor|lawmaker)\b[^.]{0,40}\brecord\b)", re.I)


def _syllables(word: str) -> int:
    word = word.lower()
    groups = re.findall(r"[aeiouy]+", word)
    n = len(groups) - (1 if word.endswith("e") and len(groups) > 1 else 0)
    return max(1, n)


def fk_grade(text: str) -> float:
    """Flesch-Kincaid grade-level estimate (rough but reproducible)."""
    sents = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    words = re.findall(r"[A-Za-z']+", text)
    if not sents or not words:
        return 0.0
    syl = sum(_syllables(w) for w in words)
    return round(0.39 * (len(words) / len(sents)) + 11.8 * (syl / len(words)) - 15.59, 1)


def firewall_check(pkg: dict, max_grade: float = 8.0) -> dict:
    """Run the firewall on a context package. Returns {pass, failures:[{condition, why}], reading_grade}."""
    fails = []

    def chk(name, ok, why):
        if not ok:
            fails.append({"condition": name, "why": why})

    hook = (pkg.get("hook") or "")
    syn = (pkg.get("synthesis_5th_grade") or "")
    spectrum = pkg.get("spectrum", []) or []
    notes = " ".join((c.get("note") or "") for c in pkg.get("claims", []))
    g = fk_grade(syn)

    chk("DESCRIBE_HEADER", "does not prescribe" in (pkg.get("describe_header") or "").lower(),
        "missing the describe-don't-prescribe header")
    chk("BOTH_SIDES", any(s.get("supports_video_claim") for s in spectrum),
        "no source supports the video's own claim (both-sides mandate)")
    chk("CITED_LEAN_LABELED", bool(spectrum) and all(
        (s.get("url") and s.get("lean") in ("left", "center", "right")) for s in spectrum),
        "a source is missing a URL or a left/center/right lean label")
    chk("NON_DIRECTIONAL_HOOK", not DIRECTIONAL.search(hook),
        "hook uses directional/accusatory language (fails the embarrassment test)")
    chk("HOOK_OFFERS_CONTEXT", ("[link]" in hook or "→" in hook or "http" in hook),
        "hook does not offer a link to the context page")
    chk("NO_VERDICT", not (VERDICT.search(hook) or VERDICT.search(syn) or VERDICT.search(notes)),
        "output reaches a verdict / tells the reader what to conclude")
    chk("MECHANISM_NOT_ACTOR", not (BLAME.search(hook) or BLAME.search(syn) or BLAME.search(notes)),
        "output blames the creator instead of contextualizing the topic")
    chk("MONEY_OUT", not (MONEY.search(hook) or MONEY.search(syn)),
        "output references selling / market / our-product")
    chk("FIFTH_GRADE", g <= max_grade, f"synthesis reading grade {g} exceeds {max_grade}")

    claims = pkg.get("claims", []) or []
    charged_fact = next((c.get("claim", "") for c in claims
                         if c.get("status") == "supported" and CHARGED.search(c.get("claim") or "")), "")
    chk("NO_CHARGED_VERDICT", not charged_fact,
        "a charged characterization of a person is marked a supported fact — it may only be reported as "
        f"attributed/contested, never asserted as true: '{charged_fact[:70]}'")
    topic_hd = (pkg.get("topic") or "") + " | " + (pkg.get("headline") or "")
    chk("TOPICS_NOT_PEOPLE", not PERSON_TARGET.search(topic_hd),
        "page is framed around a named individual / their record, not a contested topic (we cover issues, "
        "never put a person on trial — mechanism-not-actor)")

    return {"pass": not fails, "failures": fails, "reading_grade": g}
