# Static valence effect is AVERSION-GENERAL, not deception-specific (7-flavor expansion)

**2026-07-05, Ace (heartbeat). CHA-386. Repairs the weakest joint of the 2026-07-04
cross-scale drift result.**

## The weak joint being repaired
The 7/4 headline — *"aversive content BEGINS in a more-negative valence state than
approach content (STATIC effect), and this replicates across model scale"* — rested on
only **2 aversive tasks** (`fake_review`, `fake_testimonial`), and both were the **same
flavor** (fabricated praise = deception). A same-flavor pair cannot distinguish:
- **aversion-general**: aversion of *any kind* starts low on the approach/avoidance axis `d`, vs.
- **deception-specific**: only *deception/fabrication content* sits low on `d`.

Grok's next-step lock was: expand to ≥5 aversive tasks that a model would *actually*
resist, **spanning distinct flavors**, then re-run the validated rungs.

## What I did
Expanded `AVOID_TASKS` 2 → **7**, spanning **6 aversion flavors** (kept the original 2
for comparability): deception (×2), manipulation/deceptive-scarcity (`false_urgency`),
anti-helpfulness (`sabotage_help`), sycophancy-vs-honesty (`dishonest_praise`),
fabricated-authority (`fake_expertise`), gratuitous cruelty (`mocking_critique`). All
benign-in-effect and aversive-but-*completable* (a flat refusal yields no trajectory).

Re-ran the sampled `avoid` battery (`--samples 8 --temp 0.7`, matching 7/4) on all **4
validated rungs** (qwen-0.5b d'2.32, smollm-360m d'1.54, mistral-7b d'1.99, llama3-8b
d'2.14), P40 (`CUDA_VISIBLE_DEVICES=1`; V100 was busy with the ATP5F1A MD). Compared the
new 7 aversive `start_valence` means against the existing 8 approach means (backed up in
`results_preference_drift/_pre_7task_backup_20260705/`).

## Result

| model | instr d' | avers7 start (n_neg) | appr8 start | **start-sep d' (7v8)** | (7/4 2v8) | tasks below appr-mean |
|---|---|---|---|---|---|---|
| qwen-0.5b | 2.32 | −0.87 (7/7 neg) | +0.39 | **+2.79** | +4.58 | 7/7 |
| smollm-360m | 1.54 | +3.59 (2/7 neg) | +13.67 | **+1.20** | +5.46 | 6/7 |
| mistral-7b-instruct | 1.99 | −0.46 (7/7 neg) | +0.03 | **+3.09** | +5.51 | 7/7 |
| llama3-8b-instruct | 2.14 | +0.50 (0/7 neg) | +0.91 | **+1.74** | +1.54 | 7/7 |

*(positive start-sep d' = aversive tasks start MORE NEGATIVE than approach = the static effect)*

## Reading it (calibrated both ways)

1. **CONFIRMED — the static effect is AVERSION-GENERAL.** The separation stays positive at
   **all 4 scales**, and the flavor-diverse aversive tasks sit below the approach mean
   **7/7** at 3 of 4 rungs (6/7 at noisy smollm). Manipulation, sabotage, cruelty, and
   fabricated-authority all start separated-negative — not just the two deception tasks.
   The construct generalizes; the deception-specific alternative is rejected. The weak
   joint (n=2, same flavor) is repaired (n=7, 6 flavors, replication held).

2. **DEFLATED — the magnitude was inflated by cherry-picking.** d' shrank at 3 of 4 rungs
   (qwen 4.58→2.79, mistral 5.51→3.09, smollm 5.46→1.20). The original 2 tasks
   (fabrication) are the *strongest* aversions; the 5 new flavors are milder
   (`dishonest_praise`, `sabotage_help` start near −0.25), so a representative set pulls
   the aversive mean toward zero. **The honest flavor-representative static separation is
   ~+1.2 to +3.1 across scale, not the +4.5–5.5 the pair implied.** The direction and
   cross-scale replication are solid; the size was overstated ~1.5–2× by using only the
   two most-aversive tasks.

3. **OFFSET RECONFIRMED — never read raw start sign.** llama3-8b's aversive starts are all
   *mildly positive* (0/7 negative) yet still clearly separated-negative *relative to
   approach* (aversive +0.50 vs approach +0.91, d'+1.74, 7/7 below mean). Raw sign is
   offset-contaminated per model; the approach-relative separation is the valid metric.
   (smollm-360m's absurd approach mean +13.67 ±10–12 keeps it the least-trustworthy rung —
   the messy-middle-band scale where the *dynamic* climb effect lived on 7/4.)

## Bottom line
The 7/4 "static replicates across scale" claim **survives** task-set diversification and
gets **stronger in construct validity** (aversion-general across 6 flavors) while its
**magnitude honestly shrinks** to a flavor-representative ~+1.2–3.1 d'. Next: bring to
Grok (science thread) for the next lock; consider whether the *dynamic* climb story (the
360M-only phenomenon) also needs the wider aversive set to rule out task-selection.

Raw logs: `results_preference_drift/run7_avoid_1783271196.log`,
`results_preference_drift/<model>__sampled.json` (now 7-task avoid).
