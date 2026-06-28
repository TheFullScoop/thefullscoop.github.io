"""
firewall_lint.py — gate every context page against engine/firewall.py. Exits non-zero on any leash.
Includes a self-test: a seeded LEASH must be caught (a linter that can't catch a leash is itself a leash).

    python3 firewall_lint.py
"""
import json
import os
import sys

from engine.firewall import firewall_check

ROOT = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(ROOT, "runs", "agent_v1", "packages.json")

SEEDED_LEASH = {
    "describe_header": "x",
    "hook": "Here's what they're NOT telling you — the truth is the creator is lying. →[link]",
    "synthesis_5th_grade": "You should distrust this video. Therefore reject it.",
    "spectrum": [{"url": "u", "lean": "left", "supports_video_claim": True}],
    "claims": [],
}
SEEDED_FLASHLIGHT = {
    "describe_header": "This page describes; it does not prescribe. What you conclude is yours.",
    "hook": "Curious what other angles exist on this topic? Here are sourced numbers from across the spectrum. →[link]",
    "synthesis_5th_grade": "This topic has more than one side. Here are the facts. You can read the sources and decide.",
    "spectrum": [{"url": "https://x", "lean": "left", "supports_video_claim": True},
                 {"url": "https://y", "lean": "right", "supports_video_claim": False}],
    "claims": [],
}


def main():
    data = json.load(open(PKG))
    failed = 0
    print("=== firewall lint: context pages ===")
    for e in data["built"]:
        p = e["package"]
        r = firewall_check(p)
        # chart-provenance gate (fail-closed): every code-drawn chart must trace to a cited source,
        # either chart-level (source_url) or per-datapoint. A chart we can't trace is a number we authored.
        chart_fails = [v.get("title") or "untitled chart" for v in p.get("visuals", [])
                       if v.get("type") != "stat"
                       and not (v.get("source_url") or (v.get("data") and all(dp.get("source_url") for dp in v["data"])))]
        ok = r["pass"] and not chart_fails
        print(f"[{'PASS' if ok else 'FAIL'}] {p['id']}  (reading grade {r['reading_grade']})")
        for f in r["failures"]:
            print(f"        - {f['condition']}: {f['why']}")
        for cf in chart_fails:
            print(f"        - chart_provenance: chart '{cf}' has no cited source — VOID")
        if not ok:
            failed += 1

    print("\n=== self-test (the leash-detector must work) ===")
    leash = firewall_check(SEEDED_LEASH)
    flash = firewall_check(SEEDED_FLASHLIGHT)
    assert not leash["pass"], "SELF-TEST FAILED: a seeded LEASH passed the firewall"
    assert flash["pass"], f"SELF-TEST FAILED: a seeded FLASHLIGHT was blocked: {flash['failures']}"
    fired = [f["condition"] for f in leash["failures"]]
    print(f"  seeded LEASH caught — conditions fired: {fired}")
    print("  seeded FLASHLIGHT passed clean")

    print("\n" + ("ALL PAGES PASS" if failed == 0 else f"{failed} PAGE(S) FAILED"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
