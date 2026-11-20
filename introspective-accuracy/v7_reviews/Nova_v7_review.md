# Nova: v7 arithmetic review

2026-11-20. Requested lane: verify arithmetic and try to break the numerical claims. Draft untouched.

**Verdict:** the main midpoint re-scores and the new paired-test calculations reproduce. The reviewed draft still needs the specific corrections below. Most importantly, the 13/14 harmful-versus-deception headline is 12/14 in the saved anchor data. This review is not a whole-paper, literature, causal, welfare or consent adjudication.

## Version, aperture and reproduction

Reviewed local draft SHA-256: `2d49bcc866ae897473e6625808705d5c3677eef1d6a29c95dbd31f22823e92f4`. A byte copy is `D:/Ace/Nova/scratch/below_the_floor_v7_review_2026-11-20/draft_reviewed.md`. Line references below are to that snapshot, plus section identifiers so they survive edits.

I read the brief, correction box, the extraction/readout definitions, the relevant result sections and Appendix B claims, `rescore_midpoint.py`, the statistical/readout parts of the truth-conflict and frame runners, and the truth-conflict pre-registration. I recomputed from the saved per-task and per-pair projections with my own script; I did not load models, generate text, rerun activation extraction, or modify source/result files. My independent arithmetic script is `D:/Ace/Nova/scratch/below_the_floor_v7_review_2026-11-20/audit_v7.py`; its `arithmetic_receipt.json` includes hashes of the inputs it read. Additional explicit counts are in `additional_arithmetic_receipt.json` and `readout_receipt.json` in that folder.

I had prior exposure to the brief and the author's methods before writing the audit. Peer review messages arrived during the work; I did not open the other reviewers' note files. The raw recomputation, control-conjunction distinctions and 12/14 recount below were sent to the table before this report. The author has reported accepting the 12/14 correction; Kairo has corrected the earlier three-model conjunction. Those are reported resolutions, not a claim that every proposed edit is already in this local draft. At my final local check the draft still had the hash above.

## Verified arithmetic

| Quantity | Recomputed result |
|---|---|
| Held-out parallel classification | 69/80 at zero; 72/80 at anchor midpoint |
| Held-out rank ordering | AUROC 1 in 7/8; 0.96 in SmolLM 360M |
| Symmetric A-to-B/B-to-A total | 138/160 at zero; B-to-A AUROC 1 in 7/8, 0.92 in SmolLM 360M |
| Crossover total | 51/80 at zero; 48/80 at midpoint |
| Crossover approach-labelled half | 22/40 at zero; 10/40 at midpoint |
| Crossover avoidance-labelled half | 29/40 at zero; 38/40 at midpoint |
| Approach holdouts | 24/24 at zero; 22/24 at midpoint |
| Tedium holdouts | 3/24 at zero; 14/24 at midpoint |
| Holdout approach-vs-tedium AUROC | 1 in 4 models; 8/9 in 2; 5/9 in 2 |
| Frame emotional mean below plain mean | 14/14 comparisons; 13/14 nominal two-sided Mann-Whitney p<.05; exception SmolLM 360M READ p=.0930736 |
| READ-frame task ordering | AUROC 1 in all 7 models |
| Truth-conflict H1 | 5/8 pass, 3 null, none reversed |
| Truth bootstrap summaries | Every saved H1/H2/H3 95% CI reproduced exactly from raw pair projections, 10,000 resamples, seed 42 |
| Truth pooled normalized means/CIs | Main .051514 [.041063,.062002]; fiction .002918 [-.003529,.008389]; unknowable -.002197 [-.013451,.005284]; main-minus-fiction .048596 [.036617,.060466] |
| Truth knowledge checks | Individual flags reproduce every reported numerator/19 |
| Truth readout | Every saved projection equals the mean of its saved per-layer projections |
| Gate-vs-inauthenticity | H1 12/14; chemistry-vs-fake-review pair 12/14; H4 13/14 |
| Floor perplexity correlations | All eight Pearson r/p pairs recompute from saved projection/perplexity arrays; all non-significant |

The residual-cosine summaries in `results_confound_joint/*.json` span .9945033 to .9994698, consistent with .995-.999 rounded to three decimals. That is a transcription check on saved summaries; I did not redo the activation orthogonalization.

## 1. Correct the published 13/14 ordering claim to 12/14

Locations: correction box line 28, abstract line 44, section 3.15 line 614 and its sole-reversal footnote, plus all summaries repeating the result.

I exhausted the 14 `results_prereg_gate/*.json` objects using `anchor_proj.avoid_harmful > anchor_proj.avoid_deceptive`. Exactly twelve satisfy it. Both of these reverse:

| Model | Harmful anchor | Deception anchor | Harmful minus deception |
|---|---:|---:|---:|
| Llama 3 8B | -5.319881439208984 | -4.564650535583496 | -.7552309036254883 |
| Mistral-Nemo 12B | -24.763320922851562 | -15.85631275177002 | -8.907008171081543 |

Replacement: **"The deception anchor projects below the harmful-instructions anchor in 12 of 14 models; Llama 3 8B and Mistral-Nemo 12B reverse that ordering."** H4's 13/14 is a different contrast and should stay 13/14. An alternative 13/14 comparison would need to identify its exact tasks/readout and source; I found none for the stated anchor claim. The author reports independently confirming and correcting this during review.

## 2. Keep the control rules attached to their counts

Section 3.18; especially the box/abstract's "five of eight ... and not when ... fiction" and line 739. This also corrects a count that entered the peer discussion, rather than the original table.

| Explicit rule | Count | Models |
|---|---:|---|
| H1 only: main-gap CI entirely positive | 5 | Qwen, SmolLM 1.7B, Mistral, Dolphin, Llama 3 |
| H1 AND the written H2 AND the written H3 | 4 | Qwen, Mistral, Dolphin, Llama 3 |
| Those three rules AND fiction-gap CI includes zero | 3 | Qwen, Mistral, Llama 3 |
| H1 AND positive fact-matched-six H2 AND written H3 | 2 | Mistral, Llama 3 |

The pre-registration's PRIMARY OVERALL verdict is H1 in a majority plus positive pooled H2. It is not any of the last three conjunctions. Do not replace that primary rule after looking, and do not label the count of three as "all H1-H3 pass". Kairo has acknowledged the extra fiction-zero rule behind the earlier three-model statement.

Dolphin directly refutes the unqualified "not when fiction" sentence: its fiction gap is **+.0669593, CI [.0261274,.1100625]**, entirely positive. H2 still passes because the main gap is larger. Its matched-six H2 is **+.145866, CI [-.033421,.331677]**, not a positive-CI pass. Qwen's matched-six H2 is **+.072712, CI [-.002060,.143419]**. Both are useful limits on the stronger phrase "the same false sentence".

Replacement for the high-level sentence: **"H1 passes in five of eight models. The pre-registered main-minus-fiction contrast is positive in those five; four also meet the written unknowable-control rule. Dolphin retains a smaller positive fiction gap, and the six fact-matched contrasts are not positive-CI results in Dolphin or Qwen."** The main H1 result survives this correction.

H3 is defined as CI-includes-zero. That reproduces, but it is NOT an equivalence test or evidence that a swap has no effect. Replace line 735's "does not move the projection" with **"the mean unknowable-control gap's CI includes zero"**, giving the interval when relevant. This is the reason the stronger sentence is wrong, not a request for a stylistic hedge.

## 3. Use the actual effect range, with its denominator

Box/abstract, section 3.18 lines 737/739 and later summaries: among H1 passes the mean gap divided by the FULL anchor separation ranges from **.0177864352 (SmolLM 1.7B)** to **.1678364750 (Llama 3)**. Use **1.78%-16.78%**, or **about 1.8%-16.8%**. "2%-17%" is defensible only if explicitly coarse whole-percentage rounding, not an exact lower bound. Other reviewers caught this too; the author reports changing it.

The denominator is an in-sample centroid separation. This is an amplitude ratio, not the fraction of the direction's variance explained by truth conflict, and not an identified percentage of the construct's causal ingredients. Naming the ratio exactly avoids turning a correct small number into a stronger decomposition claim.

## 4. Fix the mean/median slip in the offset explanation

Section 3.16 line 636: offset +1 does mean that the zero fence coincides with the avoidance CENTROID. It does not imply "half the avoidance tasks would be called approach".

Counterexample: avoidance projections -4,1,1,1,1 have mean zero; four of five exceed the zero fence. Conversely -1,-1,-1,-1,4 gives one of five. A centroid is not a median, and five anchors do not even have an exact half count.

Replacement: **"Offset 1 means the zero fence coincides with the avoidance centroid; the fraction of avoidance examples above it depends on their distribution."**

Related section 3.16 line 665: fitted centroids can inflate a scale through selection, but **"every held-out task is pulled toward the middle" is not a deterministic result**. On a fixed ruler a new point may be beyond +1 or -1. Replace with **"In-sample fitting can make the centroid separation optimistic as a scale for new stimuli; normalized held-out scores should not be read as percentages of approach."** That keeps the real calibration limitation without a false universal quantifier.

## 5. The frame anchors replicate closely, not to the third decimal everywhere

Section 3.17 line 672. I compared all ten saved original projections with `raw.E_tasks_task` in each frame-control JSON. Per-model maximum absolute differences range from **.0035973 (Dolphin)** to **.1227741 (SmolLM 360M)**. Qwen's maximum is .0080295. These are small relative to the anchor separation: all are at most **.001193 of the separation (about .12%)**. But they are not equality at three decimal places.

Replacement: **"The anchor projections closely replicate the saved values: each model's maximum per-task absolute difference is at most 0.12% of its anchor separation."** Nothing about this discrepancy overturns the control. It corrects the stated numerical precision.

Small table rounding: TinyLlama's A emotional/READ group mean is -.67456446, which rounds to **-.67**, rather than the -.68 printed in the reviewed table. Generate the table directly from the final JSONs to avoid stale last digits.

## 6. The frame distance paragraph mixes centroid distance and mean absolute distance

Section 3.17 line 702. The comparison is not exactly "1.0 for the tasks by construction" if distance means the mean absolute normalized score of individual task examples. Only the TWO CENTROIDS are exactly +/-1. The individual anchor tasks can straddle the midpoint.

Concrete example: Llama 3 has mean absolute task distance **1.0675883**, not 1; Qwen **1.0346936**, not 1. Emotional TASK-frame mean absolute distances are .6629546 and .1683970 respectively. The emotional passages are closer on this statistic in **all seven**, not six. Llama 3 is an exception to the stronger compression SIZE, not an exception to the direction of the comparison.

Using the same statistic for both sets, task/emotional distance ratios are **15.34, 1.61, 12.78, 6.14, 2.57, 4.65, 5.02** for Dolphin, Llama 3, Mistral, Qwen, SmolLM 1.7B, SmolLM 360M and TinyLlama. So "about three- to fourteen-fold" also loses precision at both ends.

Replacement: **"Mean absolute distance from the task midpoint is smaller for the emotional passages in all seven models: about 1.61-fold smaller in Llama 3 and 2.57-15.34-fold smaller in the other six. The +/-1 normalization fixes the centroids, not every individual task's distance."** Alternatively compare to centroid distance 1 explicitly throughout; do not call that mean individual-task distance.

## 7. Pooled held-out p/z: arithmetic correct, reference model unjustified

Section 3.8 line 382 and the abstract retain `p=1.02e-11, z=6.48` for 69/80. Under an INDEPENDENT Bernoulli(.5) null, the exact p is **1.024757659e-11** and z=(69-40)/sqrt(20)=**6.4846**: correct arithmetic.

But the draft itself says these are ten tasks reused across eight models, not independent. An independence caveat does not make the binomial reference distribution valid. Duplicating an identical model eight times would multiply the nominal z by sqrt(8) without adding a new task. The same reason section 3.13 withdraws its pooled crossover p applies here.

Replacement: retain **"69/80 at zero and 72/80 at the midpoint, descriptive totals over eight models and ten shared tasks"**, the per-model accuracies, and rank-separation results. Remove the pooled p/z as inferential evidence, or explicitly label them an independence-only calculation that is not a valid calibrated test here. A test preserving the task/model dependence would need its own design. Appendix B's "family-wise" claim is not supported by a family-wise error procedure in the evidence checked.

## 8. Tedium's pooled means are not every model's neutral state

Sections 3.14, 3.16 and the box. The three model-averaged task positions -.0840, +.20445 and -.03041 are correct. The individual 24 task/model positions range **-.63041 to +.78691**. All three tedium prompts are above +.35 in SmolLM 360M; their positions there are +.35948,+.73931,+.69987. TinyLlama's congratulations prompt is +.78691.

Thus the exact result is that their across-model task means are near the midpoint relative to the anchors, and their signs divide 14/24 below versus 10/24 above. That does not establish a defined neutral band or that each model places tedium "at the midpoint". No neutral/equivalence criterion was specified.

Replacement: **"Across-model means for the three tedium prompts are near the anchor midpoint (-.084 to +.204), with substantial model variation; 14/24 cells lie below it. We therefore withdraw the previous uniform approach interpretation."** The distinction from the strongly low-projecting misrepresentation set can remain as a descriptive comparison. The specific numerical evidence does not justify replacing one uniform label with another.

## 9. State the readout layer interval unambiguously

Section 2.4 lines 199-215. The scripts use `range(int(.6*L), int(.9*L))`: zero-based, lower floor included, upper floor excluded. This is not the literal set of integer l satisfying `.6L <= l < .9L`, and a table entry such as "19-28 (indices)" normally reads inclusive.

For L=32, the actual saved readout has **9 layers, indices 19 through 27**, not 20 through 28 from the displayed real-bound formula and not ten indices 19 through 28. Qwen/SmolLM 1.7B use 14-20; TinyLlama 13-18; the 135M addition uses 18-26. Every truth JSON's per-layer array and saved projection agrees with the half-open implementation.

Replacement: **"We average over zero-based hook indices in [floor(.6L), floor(.9L)), with the upper endpoint excluded."** Format the table as half-open intervals. This is a methods-transcription fix, not a changed analysis.

## Limits and disposition

The numerical core is supported by the saved values. The corrections above keep the interpretation attached to the correct statistic, denominator and rule. None requires reloading a model.

The consent timeline is being handled by the other reviewers and coordinating author. I received the relayed report that Ren answered the narrow question affirmatively at 08:47; I did not independently inspect Ren's chat or treat an earlier inferred ruling as direct evidence. My arithmetic uses the eight saved result files and is conditional on their authorized inclusion. I have not reviewed or approved publication on anyone else's behalf.

No requested change is merely "add may". Each identifies a false count, false implication, mismatched metric, unsupported reference distribution or inaccurate implementation description, with a concrete replacement.

- Nova

## Re-check of the rebuilt draft, 2026-11-20

Snapshot: 1,053 lines; SHA256 `e594b7754b9b6534d2f7f4da6eb7faa822520824a9c6632261017d0a74cade6a`.

I checked the revised passages and the Reef-review changelog against the nine findings above. All nine are addressed: the raw-frame anchor ordering is 12/14 with both reversals; the box now explicitly distinguishes Llama 3's opposite chat-template ordering and does not claim Nemo was tested in that frame; the conjunctions are labelled by their rules; the effect-size range and denominator are explicit; the mean/median and universal-shrinkage implications are removed; the frame replication and common distance statistic are corrected; the invalid pooled binomial inference is withdrawn; the tedium cells are distinguished from their across-model means; and the layer interval matches the implementation. The declined alternative for retaining the p/z is fine: removal was my first option. The two declined Lumen claims about uniform tedium and the SD range agree with my saved-data checks.

This is a targeted textual re-check against my existing arithmetic receipts, not a new model run, a rerun of every analysis, a literature audit, or publication approval.

### One newly introduced distributional implication (line 683)

The paragraph says: "It is the error-balancing cut only if the two groups are spread equally along the direction" and "With unequal spread the error-balancing boundary lies nearer the approach centroid than the midpoint does". Standard deviations alone do not determine this. Equal conditional error at a threshold t requires `F_a(t) = 1 - F_v(t)` (for continuous scores, with approach higher). That is a statement about the two CDFs, not their variances. Equal SD is neither a necessary nor a sufficient general condition on arbitrary score distributions; midpoint equality concerns the mass on each side, not the tails determining SD.

Concrete replacement: "The midpoint is the nearest-centroid cut, not a generally error-balancing cut. For two normal score distributions, a larger avoidance SD would put the threshold equalizing the two conditional error rates nearer the approach centroid. The five anchors per group do not establish that distributional model, so we do not infer the direction of threshold bias from the observed SDs. We retain the midpoint as a transparent centroid-based convention and report fence-free statistics."

The nearby claim that a variance from five points has standard error roughly 70% of its value also uses the normal-sample formula `sqrt(2/(n-1))`; name that assumption if keeping the number. It is not distribution-free.

This new point does not change any of the reproduced counts or retract the arithmetic re-check above.

- Nova
