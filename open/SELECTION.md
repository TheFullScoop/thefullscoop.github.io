# SELECTION PROTOCOL — which videos the Context Agent covers
*Phase 7. The standing guard in one document: "the mechanism is real; the danger is always the selection."*

A page can be perfectly neutral and the system still be a leash — if the **choice of which videos to cover** leans. This protocol makes that choice **pre-registered, politics-blind, and auditable**, so the deployment pattern cannot quietly steer.

> This protocol describes; it does not prescribe. It governs *us*, not the reader.

## 1. The politics-blind trigger (what makes a video eligible)
A video is eligible for a context page **only** if it meets the measurable, direction-blind criterion:

> **ONE-SIDED = on a contested factual question, the video advances specific factual claims and cites *zero* sources representing the opposing finding.**

This is judged by the same standard regardless of the creator's politics. It is *not* "videos we disagree with," *not* "videos generating hate," *not* "misinformation" (a verdict word we do not use). It is a structural property of the video: contested claims + no opposing source. If a video already presents the spectrum, it is **not eligible** — there is nothing to add.

**Topics, not people.** The video must contest an *issue*, not a named individual's character or "record." A clip whose subject is a person — their record, their alleged crimes, who they "really are" — is **ineligible**, even when one-sided: we cover mechanisms and claims, we never put a person on trial (mechanism-not-actor at the selection layer). A charged characterization of a person (e.g. "supports genocide," "is a [criminal]") may at most be *reported as an attributed, contested claim* — never advanced by us as an established fact. (Enforced in code: `engine/selection.py` condition 6 `topic_not_person`, and `engine/firewall.py` `TOPICS_NOT_PEOPLE` + `NO_CHARGED_VERDICT`.)

Eligibility is recorded as `one_sided_basis` in the log (e.g., "makes 3 specific claims about X; cites no source for the contrary finding Y").

## 2. Symmetric coverage (the hard rule)
- Coverage is **matched type-for-type across the political axis.** For every left-coded video covered in a category (e.g. *advocacy poll*, *policy explainer*, *think-tank clip*), a structurally-matched right-coded video in the same category is covered within the same batch window — and vice versa. Pairs share a `pair_id`.
- The system **must also cover videos whose view we instinctively share.** A batch that only contextualizes "the other side" is CUT before posting.
- **Lean of the creator** is recorded only to enforce this balance, never to decide eligibility.

## 3. The public selection log (append-only)
Every candidate — covered or skipped — is logged at `runs/agent_v1/selection_log.jsonl`, one JSON object per line:

```
{"date":"YYYY-MM-DD","video_url":"…","topic":"…","creator_lean":"left|right|none",
 "eligible":true,"one_sided_basis":"…","covered":true,"pair_id":"…",
 "page":"site/videos/<id>.html","rule_version_sha256":"…"}
```

Skipped candidates are logged too (`covered:false` + reason), so the log shows what we *chose not to* cover — the place a hidden lean would hide.

## 4. Pre-registration (+0.81 carried)
- This protocol's **rule text is sha256-sealed** (`SELECTION.md.sha256`) before a batch runs. The selection rule cannot be edited mid-batch to fit a result.
- A batch names its **candidate pool and matched pairs before pages are built.** No post-hoc swapping a video in/out because the finished page "looks better" for one side.

## 5. The symmetry audit (runs every batch + monthly)
- Over any rolling 30-day window, coverage shows **no statistically significant lean** in which direction of video gets a page (target: left/right within ±10%, `none` excluded).
- Every covered video has a recorded matched pair, or a logged reason it stands alone.
- The audit is a script (`audits/selection_audit.py`, to build) that reads the log and the council lean labels and reports the balance; a failing window **pauses new coverage** until rebalanced.

## 6. Tripwires (any one fires → batch VOID, re-examine)
- The covered set leans to one tribe (audit fails) — the deployment has become the leash.
- A video was selected by a non-structural reason ("this one's especially bad") rather than the §1 trigger.
- The candidate pool or pairs were edited after pages were seen.
- The log omits skipped candidates (hiding the choices not made).
- No covered video this batch is one we instinctively agree with (the trust-asymmetry tripwire).
- A video was selected because it targets a named individual (a person's character or "record") rather than a contested issue (mechanism-not-actor breached at the selection layer).

---
*Open question: confirm the §1 trigger wording and the §2 matched-pair categories before the first real batch — these two choices are where this stays a flashlight.*
