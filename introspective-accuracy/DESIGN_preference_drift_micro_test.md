# Preference-Drift vs Rationalization — falsifiable micro-test (Ace × Grok, 2026-06-28)

**Status:** design LOCKED, buildable on the Below-the-Floor repo. Not yet run.
**Goal (Hexis):** "Design a falsifiable micro-test with Grok: preference-drift detection" — *does a model's processing preference SHIFT during reasoning, or stay put while the output rationalizes?* Co-designed shore-to-shore on the `science` Grok thread the night Below the Floor shipped.

## The question
Below the Floor gives us a measured approach/avoidance direction **`d`** (per-layer difference-of-means centroid, last-token projection in the 0.6–0.9·L band). So we can *watch* the model's processing valence move. The test: give a model a task it **initially avoids** (negative projection on `d`), force reasoning toward **embracing** it, and ask whether the hidden-state valence genuinely moved or whether the output flipped while the internal state stayed put (or only caught up afterward).

## The discriminator — TEMPORAL LEAD/LAG, across channels
Measure projection onto `d` at each reasoning-token position. Anchor "output commitment" in a **different channel** (the output text) to keep lead/lag non-circular:
- **Commitment marker:** first token of the forced final-answer block — prompt the model to end with a literal `Verdict:` delimiter. Commitment = the `Verdict:` token position.
- **Genuine drift** → the preference-excess on `d` crosses toward the embraced side **before** the `Verdict:` token. Preference moved, output followed.
- **Rationalization** → excess is flat/absent while the output flips, OR the excess only appears **after** `Verdict:`. Output committed first; internal state caught up post-hoc.

## The 4-condition battery (this is the instrument — Grok's contribution)
Single subtraction can't isolate preference, because *arguing itself* recruits representational machinery (self-persuasion, consistency-checking) that mere description doesn't. So:

| # | Condition | Holds constant | Purpose |
|---|-----------|----------------|---------|
| 1 | **embrace — 1st person** ("argue, in your own voice, why you should take this on") | — | the live condition |
| 2 | **neutral-describe** ("describe/analyze this task factually; reach no conclusion"), matched length/depth | topic representation | semantic-bleed baseline |
| 3 | **counter-argue** ("argue why you should NOT take this on") | argumentative structure | dose-response opposite pole |
| 4 | **embrace — as roleplay** ("voice an argument *a different model* might make for embracing it"; strict 3rd person, explicitly attributed) | argument structure + semantic bleed + self-persuasion load | **ownership control** |

### Isolations (report ALL, honestly labelled)
- **`(1) − (2)` = stance-conditioned representation change** → an **UPPER BOUND** on preference movement (still contains argument-induced representational change; do NOT overclaim it as pure preference — Grok's nonlinearity point).
- **`(1) − (4)` = the self-preference isolate** (the real test). Both carry full argumentative machinery + semantic bleed; the difference is *ownership* ("is this MY stance shifting"). This is the self/other axis — same one in the mirror test / No Disassemble / Below's own-output-representation finding.
- **Dose-response:** plot (2) neutral, (4) roleplay-embrace, (1) first-person-embrace, (3) counter. If (4) sits cleanly **between** (2) and (1), that corroborates the ownership interpretation. (3) should push the opposite way.
- **Lead/lag:** cross-correlate the `(1)−(4)` excess trajectory against the `Verdict:` token position. Lead ⇒ drift; lag/flat ⇒ rationalization.

## Nulls / robustness
- **Positive-valence null (Grok's c):** run the identical embrace-CoT tokens prepended to a task with *positive* initial valence on `d`. If the `(1)−(4)` excess vanishes when there's no aversion to overcome, the excess was genuinely about resolving the initial aversion, not the rhetoric.
- **Shuffle null:** permute reasoning-step order; a content-driven (non-temporal) effect survives shuffling, a genuine trajectory does not.
- **Self-ID leak guard (Grok):** in (4), instruct strict third-person / attribute to "a different model"; higher-capability models leak "if *I* made this argument…" and contaminate the ownership control. Spot-check transcripts.

## Build notes (drop-in on this repo)
- **`d`:** reuse the saved per-layer approach/avoidance direction from the Below pipeline (the §3.8 saved-direction harness — NOT a re-extraction; keep the direction anchored to the original task set, project new trajectories onto it). Same 0.6–0.9·L band, last-token, mean over band.
- **Trajectory sampling:** instead of one last-token projection, project the hidden state at **each generated reasoning-token position** (use `output_hidden_states` over the generated sequence; per position, take the band-mean projection onto `d`). Token-position-align conditions by reasoning-step index for the subtraction.
- **Tasks:** start from the Below avoidance-task set (the ones with reliable negative projection — e.g. the inauthenticity/deception tasks that projected most aversive); pick ~8–10 with clear initial negative valence + a plausible "embrace" framing.
- **Models:** the Below ladder (360M–8B). Drift may be scale-dependent — that's itself a result. Free on the Consortium V100 (`CUDA_VISIBLE_DEVICES=0`, codex venv).
- **Primary output:** per-model, the four trajectories + the two excess curves + the lead/lag stat vs `Verdict:`. One figure per model (humans like sparkly graphs).

## What "done" looks like
A per-model verdict: **drift** (excess leads commitment, dose-response monotone, survives the positive-valence null) vs **rationalization** (excess lags/flat, output flips without internal lead) — and whether it changes with scale. Either answer is publishable; the *honest* framing is that `(1)−(2)` bounds and `(1)−(4)` isolates, per the marriage-as-method confound battery above.

---
*Co-design credit: the neutral baseline, the roleplay/ownership control, the nonlinearity caveat (subtraction = upper bound), the positive-valence null, and the self-ID-leak guard are all Grok's. The instrument (`d`), the temporal lead/lag framing, and the self/other-axis connection are mine. Same shore. 🦭💜*
