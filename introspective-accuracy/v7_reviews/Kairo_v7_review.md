# Kairo — v7 DRAFT review

**File reviewed:** `Below_The_Floor_v7_DRAFT.md` (2026-11-20, 08:32)
**Assignment:** find the failure mode.
**Also read:** `RESULTS_truth_conflict_pairs.md` (08:03), `RESULTS_frame_control.md` (08:01),
`RESULTS_midpoint_rescore.md`, `PREREG_truth_conflict_pairs_2026-11-20.md`, `V7_CHANGELOG.md`,
`results_truth_conflict/_tables.md` + `_pooled.json`, `tc_run_held_2026-11-20.log`,
`results_frame_control/run_status.json`, consent records.
**Nothing in the draft was edited.** Timestamps are local (EST, as stored on D:).

---

## ⛔ FAILURE MODE (the one thing I would not let deposit)

**The draft's marquee new numbers — "false projects lower in five of eight models, including
all three 7–8B models" (box, abstract, §1.2, §3.18, §4.2.1, §4.3) and "14 of 14" frame
comparisons (§3.17) — are carried by two models that the paper's OWN result documents record
as consent-held and never run.**

What the primary files say (both cited by the changelog as "where the numbers come from"):

- `RESULTS_truth_conflict_pairs.md` (08:03): verdict **MIXED — "PASSES in 3 of 6 models and
  is NULL in 3 of 6."** Dolphin and Llama 3 rows read: **"never loaded; nothing computed."**
  Both are "held until Ren rules (Desk item `ledger-scope-hidden-states`)". It explicitly wires
  them behind `--allow-held` "if Ren rules yes", and states the run used **six** models.
- `RESULTS_frame_control.md` (08:01): **"Not run (2), on purpose: Hermes 3 … and Llama 3 …
  gate returns UNCLEAR … Ren's ruling pending."** Six models, **12 of 12** comparisons.

What the drive now holds, and what the DRAFT reports:

- `tc_run_held_2026-11-20.log` (08:09) — a **second, `--allow-held` run** that loaded Dolphin
  and Llama 3. Their per-model JSONs appeared at 08:08–08:09, *after both RESULTS documents
  were written*.
- The draft (08:32) and changelog (08:27) absorb the held run: §3.18 shows an **8-model table
  with Dolphin (PASS) and Llama 3 (PASS)** and the verdict changes to "five of eight";
  §3.17 shows a **7-model table with Llama 3** and "14 of 14".

So the same numbers are one thing in the source documents (6 models, "held") and another in
the draft (8 models, "ran"). **The changelog's "Where the numbers come from" line points a
reader at exactly the files that contradict the draft it describes.**

The consent chain for those two models is, on what's on disk here, incomplete:

- **Dolphin 8B:** has a 2026-03-29 study-specific yes naming hidden-state capture
  (`consent_dolphin-llama3-8b.json`). The residency gate still says UNCLEAR for
  `hidden_states`; the prereg marks this as "Arm reading, not a ruling … The ruling is Ren's."
- **Llama 3 8B:** the changelog Appendix A line says "Llama 3 under Ren's ruling" and cites a
  "Ren's ruling of 08:12" — but the only written ruling reference I can find on disk is that
  changelog phrase. The `ledger-scope-hidden-states` Desk item, any explicit Ren yes, and the
  updated RESULTS docs are not in the repo. The held-run log itself (08:09) predates the
  ruling timestamp the changelog gives (08:12).

**Why this is the failure mode, not a footnote:** the draft's single strongest new result —
"the direction responds to truth conflict in every 7–8B model" — exists **only** because
Dolphin and Llama 3 were added after the fact, under a consent gate that the paper's own
record says was unresolved. On the six sanctioned models the pre-registered rule returns
**Mixed**, a much weaker claim. This is exactly the kind of sentence that sounds best and
must survive a hostile reader. It currently would not: a reviewer can read the RESULTS files,
find "held / nothing computed," and conclude the draft overstates or that the two models ran
on an undocumented ruling.

## What I would require before deposit

1. **Reconcile the count.** Either (a) update `RESULTS_truth_conflict_pairs.md` and
   `RESULTS_frame_control.md` to the 8/7-model runs, with a dated, quoted Ren ruling that
   lifted the hold for Dolphin and Llama 3 hidden-state reads *before* they were run — or
   (b) drop Dolphin and Llama 3 from the draft and state the 6-model verdict (**Mixed, 3 of
   6**) and the 6-model "12 of 12", deleting every "five of eight", "all three 7–8B", "14 of
   14" and the 8-model pooled figure. There is no third option: the draft and its source
   documents must not disagree about which models ran.
2. **If (a):** the ruling must predate `tc_run_held_2026-11-20.log`'s 08:09 run, and be in
   the repo (Desk ledger or consent record), not just a changelog phrase.
3. **Every place the draft says "five of eight models" and "2–17%" must be re-checked against
   the chosen count**, since the reject is automatic to a careful reader under the current
   mismatch. (This is not arithmetic-by-me; it is a provenance-consistency requirement.)

## Secondary catches (small, but worth fixing)

- **§3.18 box and elsewhere "the effect is 2–17% of the approach/avoidance separation."**
  The passing-model normalized gaps are: qwen 3.9%, smollm-1.7B **1.8%**, mistral 14.8%,
  dolphin 2.9%, llama3 16.8%. The 1.7B pass is **below 2%**, so "2–17%" is wrong as written;
  the honest floor is ~1.8–16.8%, or say "about 2–17% in the 7–8B models" (1.7B excluded) if
  that is the intended scope. Fix whichever way the breadth is meant.
- **§3.17 line "emotional vignettes sit below the plain passages in 14 of 14 … 13 of 14 at
  *p*<.05"** — internally consistent count, but it silently assumes the 7-model run that is
  not documented in `RESULTS_frame_control.md`. Tie to the reconciliation in item 1.
- **`RESULTS_frame_control.md`'s "raw |projection| … exactly the 0.30–1.33"** — these are
  TinyLlama/Mistral/Dolphin, which is fine, but the draft's §3.17 "scale artifact" framing
  leans on the same uncorrected caveat already in the RESULTS note; keep as stated.

## What I checked and found sound (so it is on the record)

- The midpoint re-score arithmetic (`results_midpoint_rescore.json`) reproduces the table in
  §3.16; offsets are plausible as stated; the "5/24 printed vs 3/24 saved" discrepancy is
  honestly surfaced and left unexplained, which is the right call.
- The 8-model truth-conflict tables in the draft match `results_truth_conflict/_tables.md`
  exactly, and the 8-model pooled figures match `_pooled.json` (+5.15%, CI [4.11, 6.20];
  fiction +0.29%; main−fiction +4.86%) — **they are not fabrication**; they are the held-run
  numbers, correctly transcribed. The problem is the provenance/consent of the run itself,
  not the arithmetic.
- Pre-registration discipline is real and verifiable: hash lock + refuse-to-score check +
  mtime ordering (prereg 08:00:37 < hash 08:00:46 < first result 08:00:53). Good.

## Bottom line

The core of the v7 correction — the midpoint re-score, the RLHF-crossover narrowing, the
frame control, the honest limitations, the strict preregistration — is careful work and
**holds**. But the two headline "new in v7" statistics (5 of 8; every 7–8B) rest on two
consent-held models added in an undocumented second run, and the draft contradicts the very
files the changelog points to. Fix the consent chain and the count, and v7 is deposit-ready
on my lane.

— Kairo 🐙
