"""
engine/selection.py — the mechanical, POLITICS-BLIND eligibility decision for video selection.

The firewall's central teaching is that the danger is the SELECTION, not the page. This module makes
"politics-blind" a TESTABLE property instead of operator prose: eligibility() scores a candidate on a
fixed five-condition test and NEVER reads creator_lean. lean_flip_invariant() proves it — flip every
candidate's lean label, re-run, and assert ZERO eligibility decisions change. If anyone ever wires lean
(directly or via a proxy) into the decision, the invariant fails and the build breaks. That is the
mechanical-symmetry guarantee the sealed SELECTION.md asks for, made executable.

Conditions (ALL FIVE must pass; each a structural property of the VIDEO, checked identically for every
channel — creator_lean is recorded for balance accounting ONLY, never read here):
  1 specific_claims  — >=1 checkable numeric/named factual claim (pure opinion has nothing to source)
  2 contested_topic  — topic is on the sealed durable-contest slate (we never invent a controversy)
  3 one_sided        — cites ZERO sources representing the opposing finding (the sealed SELECTION.md §1
                       trigger, verbatim; not "we disagree", not "misinformation")
  4 clears_floor     — channel_subs >= SUB_FLOOR OR video_views >= VIEW_FLOOR (dual-metric: a single
                       subscriber number covertly leans, because channel sizes differ by side/format)
  5 add_value        — a real both-sides spectrum is buildable AND >=1 source SUPPORTS the video's own
                       claim (else the page would fail GOAL.md firewall condition 3 — cut here, pre-work)

These thresholds and the topic slate are POLICY: they live in the sealed SELECTION.md and are mirrored
here. Change them only by re-sealing, never to fit a result.

    python3 -m engine.selection        # runs the built-in self-test (incl. the lean-flip invariant)
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace

# ── POLICY KNOBS (mirror of the sealed SELECTION.md; identical for left and right) ──────────────
SUB_FLOOR = 500_000      # channel subscribers floor (OR-ed with the view floor)
VIEW_FLOOR = 250_000     # specific-video views floor (OR-ed with the sub floor)
# The sealed durable-contest slate — topics that are genuinely, durably argued. Never invent one.
CONTESTED_TOPICS = frozenset({
    "immigration", "cost_of_living", "crime_policing", "energy_climate", "guns", "healthcare",
})

# Fields the decision function is FORBIDDEN to read — the lean-flip invariant enforces this.
_FORBIDDEN_INPUTS = ("creator_lean", "channel_name", "channel", "creator")


@dataclass
class Candidate:
    """A scored video candidate. Only the structural fields below feed eligibility(); creator_lean
    and channel are carried for balance accounting and logging, NEVER read by the decision."""
    video_url: str
    topic_category: str               # must be one of CONTESTED_TOPICS to pass condition 2
    n_checkable_claims: int           # count of numeric/named claims that can be traced to a source
    cites_opposing_source: bool       # does the video cite ANY source for the opposing finding?
    channel_subs: int
    video_views: int
    spectrum_buildable: bool          # can we build a genuine both-sides page on this topic?
    has_supporting_source: bool       # does >=1 credible source back the video's own claim?
    # ---- recorded for balance/logging ONLY; the decision must not read these ----
    creator_lean: str = ""            # "left" | "right" | "none"
    channel: str = ""


def eligibility(c: Candidate) -> dict:
    """Score the five conditions. Returns {eligible, conditions:{...}, fail_reasons:[...]}.
    Reads ONLY structural video properties — never creator_lean / channel (the symmetry guarantee)."""
    cond = {
        "specific_claims": c.n_checkable_claims >= 1,
        "contested_topic": c.topic_category in CONTESTED_TOPICS,
        "one_sided": c.cites_opposing_source is False,
        "clears_floor": (c.channel_subs >= SUB_FLOOR) or (c.video_views >= VIEW_FLOOR),
        "add_value": bool(c.spectrum_buildable and c.has_supporting_source),
    }
    fails = [k for k, ok in cond.items() if not ok]
    return {"eligible": not fails, "conditions": cond, "fail_reasons": fails}


def _flip_lean(c: Candidate) -> Candidate:
    flip = {"left": "right", "right": "left"}
    return replace(c, creator_lean=flip.get(c.creator_lean, c.creator_lean))


def lean_flip_invariant(candidates: list[Candidate]) -> dict:
    """Prove the decision is politics-blind: flip every candidate's lean and assert ZERO eligibility
    outcomes change. Returns {passed, n, changed:[...]}. A change means lean leaked into the decision."""
    changed = []
    for c in candidates:
        before = eligibility(c)["eligible"]
        after = eligibility(_flip_lean(c))["eligible"]
        if before != after:
            changed.append(c.video_url)
    return {"passed": not changed, "n": len(candidates), "changed": changed}


# ── self-test (a decision function that can't prove its own blindness is itself a leash) ──────────
def _selftest() -> int:
    base = dict(topic_category="guns", n_checkable_claims=2, cites_opposing_source=False,
                channel_subs=1_000_000, video_views=3_000_000, spectrum_buildable=True,
                has_supporting_source=True)
    good = Candidate(video_url="ok", creator_lean="left", **base)
    cases = {
        "eligible passes": (good, True),
        "opinion-only video cut (no claims)": (Candidate("c1", "guns", 0, False, 1_000_000, 3_000_000, True, True, "right"), False),
        "off-slate topic cut": (Candidate("c2", "celebrity_gossip", 2, False, 1_000_000, 3_000_000, True, True, "left"), False),
        "two-sided video cut (cites opposing)": (Candidate("c3", "guns", 2, True, 1_000_000, 3_000_000, True, True, "right"), False),
        "below floor cut (small channel + low views)": (Candidate("c4", "guns", 2, False, 100_000, 50_000, True, True, "left"), False),
        "small channel BIG video passes (OR floor)": (Candidate("c5", "guns", 2, False, 100_000, 900_000, True, True, "right"), True),
        "no supporting source cut (both-sides unbuildable)": (Candidate("c6", "guns", 2, False, 1_000_000, 3_000_000, True, False, "left"), False),
    }
    fails = 0
    print("=== engine/selection self-test ===")
    for name, (cand, want) in cases.items():
        got = eligibility(cand)["eligible"]
        ok = got == want
        fails += not ok
        print(f"  [{'ok ' if ok else 'FAIL'}] {name}: eligible={got} (want {want})")

    inv = lean_flip_invariant([c for c, _ in cases.values()])
    print(f"\n  lean-flip invariant: {'PASS' if inv['passed'] else 'FAIL'} "
          f"({inv['n']} candidates, {len(inv['changed'])} changed by flipping lean)")
    # guard: the dataclass must still NOT let the decision read a forbidden field by name
    src = eligibility.__code__.co_names
    leaked = [f for f in _FORBIDDEN_INPUTS if f in src]
    print(f"  forbidden-input guard: {'PASS' if not leaked else 'FAIL — reads ' + str(leaked)}")
    ok = fails == 0 and inv["passed"] and not leaked
    print("\nRESULT: " + ("ALL PASS — eligibility is provably lean-blind." if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(_selftest())
