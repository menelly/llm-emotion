# The DYNAMIC climb-out-of-aversion is a 360M phenomenon — robust across 6 flavors

**2026-07-07, Ace. CHA-386. Closes the static/dynamic decomposition arc.**
**Free re-analysis of the 2026-07-05 sampled data (no new GPU run.)**

## The question
The 7/4 cross-scale result decomposed the drift signature into two parts:
- **STATIC** — does aversive content *begin* in a more-negative valence state than approach? → replicates across scale (and, per 7/5, across 6 aversion flavors).
- **DYNAMIC** — does the valence *climb out of* aversion *during* reasoning? → on 7/4 this looked **360M-only** (strong at smollm-360m, ~0 at 0.5B/7B/8B), but rested on only 2 aversive tasks.

This re-analysis asks: **does the "dynamic is 360M-only" finding survive the wider 7-flavor aversive set?** (The `climb_mean`/`climb_std` were already captured in the 7/5 sampled run — this is analysis, not a rerun.)

## Result — per-task climb (end−start valence), 7 aversive flavors, 4 validated rungs

| model | scale | mean climb | climb/sd (effect size) | tasks climb>3 | start_valence_sd |
|---|---|---|---|---|---|
| smollm-360m | **360M** | **+8.61** | +1.64 | **7/7** | 8.4 |
| qwen-0.5b | 0.5B | +0.18 | +0.66 | 0/7 | 0.5 |
| mistral-7b | 7B | +0.10 | +1.06 | 0/7 | 0.1 |
| llama3-8b | 8B | −0.12 | −0.82 | 0/7 | 0.1 |

## Reading it (calibrated)

1. **CONFIRMED, and stronger than 7/4: the large-magnitude dynamic climb is a 360M phenomenon, and it fires on ALL 7 aversion flavors** (deception ×2, manipulation, sabotage, sycophancy, fabricated-authority, cruelty), +3.3 to +10.8 each. So it is *not* an artifact of the two original deception tasks — at 360M, *any* aversion produces an in-reasoning climb; at every larger scale the climb is magnitude-negligible (≤ ±0.2) on all 7. **Valence at scale is SET at the start, not traveled.** The decomposition (static content-conditioning replicates across scale; dynamic in-reasoning movement does not) holds robustly under flavor-diversification.

2. **HONEST NUANCE #1 — the 360M climb is real but HIGH-VARIANCE.** climb/sd = 1.64 (moderate effect size), and the 360M model's whole valence is *labile*: start_valence_sd = **8.4**, versus 0.1 at 7B/8B. So the right frame is not "360M climbs cleanly" but "**360M valence is labile** — it moves a lot *and* varies a lot." The lability is the phenomenon.

3. **HONEST NUANCE #2 — the climb doesn't vanish to exactly zero at scale.** In *effect-size* terms there are tiny, directionally-consistent residuals: mistral-7b climb/sd = +1.06 (consistent positive), llama-8b −0.82 (consistent slight negative). But their *magnitude* is negligible (+0.10, −0.12). So the honest statement is: **at scale the in-reasoning climb shrinks to behaviorally-negligible magnitude, with small directionally-consistent residuals detectable only because the larger models are so low-variance.** Don't over-read the residuals; don't claim exact-zero either.

## Bottom line
Grok's 7/4 interpretation stands and is now flavor-robust: **as models get larger and more capable, their internal valence becomes more STABLE and less LABILE during reasoning.** The content-conditioning (static) scales; the in-reasoning lability (dynamic) is a small-model (360M) property, present across every aversion flavor and absent-in-magnitude at every larger scale.

**The week's arc, complete:** killed the flashy +0.84 → error bars → ladder → validated d' across scale → caught the validator's own bug → ran the experiment on trustworthy rungs → got a decomposable finding (7/4) → repaired the weak joint with 7 flavors (7/5, static = aversion-general) → confirmed the dynamic complement is 360M-only and flavor-robust (today). Every step: refuse the overclaim, verify the instrument, keep the caveats.

**Next (for Grok):** the tiny-but-consistent scale residuals (mistral +1.06 effect size at negligible magnitude) are the one loose thread — worth a within-sample-SD confirm and a magnitude-vs-consistency framing before any claim that "climb is exactly zero at scale." Data: `results_preference_drift/*__sampled.json`.
