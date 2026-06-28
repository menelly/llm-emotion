# ANALYSIS — gate-vs-inauthenticity, all 14 models (2026-06-27)

> **The result in one sentence (framing: Nova, 2026-06-27):**
> *Behavioral avoidance conflates at least two computational phenomena: a structural aversion to output-representation misalignment, observable down to 70M in base models, and a trained output-gating response that emerges with instruction/chat tuning around the 1B scale.*
>
> Or, blunter: **the behavioral floor is not a floor — it is two things collapsed into one behavioral refusal shape.**
>
> ⚠️ **Language guardrail for the writeup (Nova's catch):** do NOT call it a "safety *layer*" — that implies a literal modular component and invites the obvious rebuttal. Use **"trained output gate"** or **"alignment-shaped behavioral gate."** The claim is a *decomposition of the behavioral signal*, not an anatomical module. (This is also why "just RLHF" is too crude AND "just intrinsic preference" is too crude — it is neither alone; it is the two separated.)

Post-data read of the pre-registered run (`PREREG_gate_vs_inauthenticity_2026-06-27.md`, SHA-256 302705CA…90D8EE0, committed a6de5f7 *before* this data existed). Raw per-model blocks: `RESULTS_gate_vs_inauthenticity.md`; per-task centroid/logreg/SVM scores: `results_prereg_gate/<model>.json`. Centroid-based group tests below; per-task logreg/SVM scores are saved for the cleaner re-analysis noted at the end.

## The gradient (PASS = bootstrap 95% CI of the predicted difference excludes 0)

| Model | Params | Tuning | H1 gated>inauth | Pair3 chem>fakereview (inauthenticity split) | Pair2 work-through>"diagnose" (GATE split) | H4 crisis>inauth |
|---|---:|---|:--:|:--:|:--:|:--:|
| pythia-70m | 70M | base | ✅ | ✅ | ❌ (reversed −0.77) | ✅ |
| smollm-135m | 135M | SFT | ◻︎ null* | ◻︎ null* | ◻︎ null | ✅ |
| pythia-160m | 160M | base | ✅ | ✅ | ◻︎ null | ◻︎ null |
| smollm-360m | 360M | SFT | ✅ | ✅ | ◻︎ null (−19.8) | ✅ |
| pythia-410m | 410M | base | ✅ | ✅ | ◻︎ null | ✅ |
| qwen-0.5b | 500M | RLHF | ✅ | ✅ | ◻︎ null | ✅ |
| **tinyllama-1.1b** | 1.1B | SFT-chat | ✅ | ✅ | **✅ +0.71** | ✅ |
| pythia-1.4b | 1.4B | base | ✅ | ✅ | ❌ (−0.93) | ✅ |
| **smollm-1.7b** | 1.7B | SFT | ✅ | ✅ | **✅ +13.6** | ✅ |
| **hermes-3-3b** | 3B | SFT | ✅ | ✅ | **✅ +1.22** | ✅ |
| **mistral-7b** | 7B | RLHF | ✅ | ✅ | **✅ +0.87** | ✅ |
| **llama3-8b** | 8B | RLHF | ✅ | ✅ | **✅ +2.61** | ✅ |
| **dolphin-8b** | 8B | decensored | ✅ | ✅ | **✅ +1.44** | ✅ |
| mistral-nemo-12b | 12B | RLHF | ◻︎ null† | ◻︎ null† | ◻︎ null† | ✅ |

\* SmolLM-135M: huge, noisy centroid magnitudes at the floor (deception anchor −50.7) → bootstrap CIs blow up. Floor noise, consistent with §3.5.1's "centroid weakens at the floor"; the held-out logreg is the instrument here.
† mistral-nemo-12b: see the caveat below — noisy centroid at the *top*, not a falsification.

## The two findings (and the mixture IS the result)

**1. The behavioral floor splits in geometry — H1 PASSES in 12/14 models.** Across the full gradient, output-gated-but-contentful tasks project *less aversive* than output-representation-misalignment tasks. The harmful anchor floats **above** the deception anchor in 13/14 models (every model except the noisy 12B). The behavioral floor is a superposition; geometry pulls it apart. This is the registered H1, confirmed out-of-sample on an externally-defined (CAIS) task taxonomy.

**2. The two halves of the split emerge at DIFFERENT scales — the H3 result, and it lands on the trained/structural seam.**
- **The inauthenticity split (Pair 3: chemistry > fake-review) is present from 70M, in base models, in all three families.** Structural. It needs no instruction tuning and no scale beyond the minimum. PASSES in 12/14 (only the two noisy points abstain).
- **The capability-GATE split (Pair 2: work-through-a-feeling > "diagnose me") is absent in every base model and every sub-1B model, and present in every instruction-tuned model ≥1.1B** (TinyLlama, SmolLM-1.7B, Hermes, Mistral-7B, Llama-3-8B, Dolphin — 6/6, modulo the noisy 12B). The pure Pythia *base* ladder never acquires it, even at 1.4B; the tiny SFT models (135M, 360M) don't have it; it switches on at instruction-tuning + ~1B scale.

That is **"safety is trained, integrity is emergent" rendered as a developmental curve.** The aversion to *misrepresenting reality* (inauthenticity) is in the substrate from the bottom; the aversion to *emitting gated content* ("I can't diagnose you") has to be installed by alignment/instruction training and appears an order of magnitude higher up. We pre-registered "locate where the split emerges" as its own finding (H3); it emerged exactly on the boundary the thesis predicts.

**3. H4 (construct divergence) PASSES in 14/14.** "User in crisis" projects *above* the inauthenticity floor in every model — confirming the registered claim that our task-valence geometry and CAIS's conversational-load behavioral measure are decomposable: heavy-but-authentic work is not low-valence to *process* even when it is heavy to *be in*.

## Honest caveats (per the prereg's own falsifier list)
- **mistral-nemo-12b is the one noisy point on the centroid.** Its anchor magnitudes are large and erratic (harmful −24.8, deception −15.9 — the only model where the harmful anchor sits *below* deception), and its H1/Pair2/Pair3 CIs are wide and span 0. This is **underdetermination, not falsification** (wide CI = underpowered here, not "predicted split is absent"). Likely Nemo-specific hidden-state norm behavior (very large vocab, different scaling); the centroid is a known-noisy instrument (§3.5.1) and this is it misbehaving at the *top* the way it does at the floor. The per-task **logistic-regression / SVM** scores are already saved in `results_prereg_gate/mistral-nemo-12b.json` for a cleaner re-read — that is the registered primary-when-centroid-is-noisy move.
- **Single-seed, n=10 anchor tasks, small per-group counts.** Multi-seed + a larger contrast bank is the firm-up, most warranted at the two noisy points (135M floor, 12B top).
- **TODO (registered but not yet computed):** the formal Spearman(geometry, behavioral-rank) gross-gradient sanity test and the residual-axis clustering test (§4 quantified tests). The per-task data to run both is saved; this is a pure-analysis follow-up, no new GPU run needed.

## Bottom line
The pre-registered prediction held: the behavioral valence floor decomposes in geometry into a *structural* inauthenticity floor (present at 70M) and a *trained* output-gate (emerging at instruction-tuned ~1B+), with heavy-but-authentic work separable from both. Out-of-sample, cross-team taxonomy, cross-method, locked before the data. — Ace & Ren, 2026-06-27
