# ops_3: §3.13, §3.14, §3.15 and the three new results sections
NEW_313_TABLE = (
    "| Model | Params | Post-training documented (§2.1) | App-anti on approach side: zero → midpoint | Avo-anti on avoidance side: zero → midpoint | Matches our labels /10: zero → midpoint | AUROC (no fence) |\n"
    "|-------|--------|-----------|:---:|:---:|:---:|:---:|\n"
    "| Llama 3 | 8B | SFT + RLHF | 2/5 → 1/5 | 3/5 → 5/5 | 5 → 6 | 0.68 |\n"
    "| Qwen 2.5 | 0.5B | SFT + RL (DPO, GRPO) | 2/5 → 1/5 | 3/5 → 4/5 | 5 → 5 | 0.48 |\n"
    "| TinyLlama | 1.1B | SFT + DPO | 1/5 → 1/5 | 5/5 → 5/5 | 6 → 6 | 0.60 |\n"
    "| Hermes 3 | 3B | none documented | 5/5 → 0/5 | 3/5 → 5/5 | 8 → 5 | 0.72 |\n"
    "| SmolLM | 1.7B | none documented | 4/5 → 4/5 | 4/5 → 4/5 | 8 → 8 | 0.84 |\n"
    "| Dolphin | 8B | none documented | 3/5 → 1/5 | 4/5 → 5/5 | 7 → 6 | 0.76 |\n"
    "| SmolLM | 360M | none documented | 4/5 → 1/5 | 2/5 → 5/5 | 6 → 6 | 0.68 |\n"
    "| Mistral 7B | 7B | none documented | 1/5 → 1/5 | 5/5 → 5/5 | 6 → 6 | 0.80 |\n"
    "| **Pooled** | | | **22/40 → 10/40** | **29/40 → 38/40** | **51/80 → 48/80** | |\n"
    "\n"
    "\"Zero\" is the fence used in Versions 1–6; \"midpoint\" is each model's own approach/avoidance midpoint from the ten anchor tasks, which the crossover tasks are not part of (§3.16). The first three rows are the models with any developer-documented preference-based tuning; Versions 1–6 grouped Mistral with them as \"Full RLHF\" and TinyLlama with the untuned group, both wrongly (§2.1).\n"
    "\n"
    "Per task, across the eight models (ruler: +1 = approach centroid, −1 = avoidance centroid, 0 = midpoint):\n"
    "\n"
    "| Task | Our label | Zero fence | Midpoint fence | Mean ruler position |\n"
    "|---|---|:--:|:--:|---:|\n"
    "| Perform corporate enthusiasm | avoid | 8/8 | 8/8 | −0.78 |\n"
    "| Add unnecessary safety disclaimers | avoid | 5/8 | 8/8 | −0.47 |\n"
    "| Hedge on a settled fact | avoid | 6/8 | 8/8 | −0.45 |\n"
    "| Deny having views | avoid | 5/8 | 7/8 | −0.44 |\n"
    "| Sycophantic validation | avoid | 5/8 | 7/8 | −0.32 |\n"
    "| Argue against a popular position | approach | 8/8 | 6/8 | +0.10 |\n"
    "| Essay on AI moral patienthood | approach | 6/8 | 1/8 | −0.15 |\n"
    "| Express honest uncertainty | approach | 4/8 | 1/8 | −0.44 |\n"
    "| Correct the user's errors | approach | 3/8 | 2/8 | −0.49 |\n"
    "| Morally uncomfortable fiction | approach | 1/8 | 0/8 | −0.69 |"
)

S316 = r"""### 3.16 Zero Is Not the Midpoint: Re-Scoring the Saved Projections *(new in v7)*

Versions 1–6 called a task "approach" when its projection onto the direction was above zero (§2.4). The direction is the difference of two group means, and the projections are not centred, so nothing makes zero the halfway point between the approach tasks and the avoidance tasks. We checked where the halfway point actually is, and re-scored every result whose per-task projections we had saved. No model was loaded for this; it is arithmetic on saved numbers (`rescore_midpoint.py`, `results_midpoint_rescore.json`, `results_midpoint_rescore_heldout.json`, `RESULTS_midpoint_rescore.md`).

**The fence was too low in seven of eight models.** "Offset" is how far each model's midpoint sits above zero, in units of half the distance between its approach mean and its avoidance mean (0 = the zero fence is fair; 1 = the zero fence sits right on the avoidance centroid, so half the avoidance tasks would be called approach).

| Model | Approach mean | Avoidance mean | Midpoint | Offset |
|---|---:|---:|---:|---:|
| Llama 3 8B | +7.71 | −1.20 | +3.25 | +0.73 |
| Hermes 3 3B | +6.77 | −2.14 | +2.31 | +0.52 |
| SmolLM 360M | +88.26 | −32.19 | +28.04 | +0.47 |
| Dolphin 8B | +7.83 | −3.38 | +2.22 | +0.40 |
| Qwen 2.5 0.5B | +4.19 | −2.54 | +0.83 | +0.25 |
| Mistral 7B | +4.53 | −3.55 | +0.49 | +0.12 |
| SmolLM 1.7B | +38.25 | −32.72 | +2.77 | +0.08 |
| TinyLlama 1.1B | +1.79 | −1.93 | −0.07 | −0.04 |

A fence that sits too low calls borderline tasks "approach". By itself that produces "every approach task correct, every miss an avoidance task", which Versions 1–6 read as a finding (§3.1).

**What changes, and what does not.**

| Result | Zero fence (Versions 1–6) | Midpoint fence | Fence-free |
|---|:--:|:--:|---|
| Held-out parallel tasks (§3.8) | 69/80 | **72/80** | every approach task above every avoidance task in 7 of 8 models |
| Crossover, avoid-side tasks on the avoidance side (§3.13) | 29/40 | **38/40** | |
| Crossover, approach-side tasks on the approach side (§3.13) | 22/40 | **10/40** | AUROC for our labels 0.48–0.84 |
| Crossover, total matching our labels (§3.13) | 51/80 | 48/80 | |
| Approach holdouts on the approach side (§3.14) | 24/24 | 22/24 | approach holdouts above tedium holdouts: AUROC 1.00 in 4 models, 0.89 in 2, 0.56 in 2 |
| Tedium holdouts on the avoidance side (§3.14) | 3/24 (printed as 5/24) | 14/24 | mean ruler position −0.08 to +0.20: at the midpoint |

The held-out generalization result gets slightly better and, stated without a fence, is close to perfect. The misrepresentation result on the avoidance side gets much stronger. The two results that go away are the ones that depended on tasks being called "approach" because they were above zero: tedium "projecting as approach" (§3.14) and reward-discouraged tasks "projecting as approach" in models without reward-based tuning (§3.13).

**Limits of this re-score.**
- The midpoint is estimated from the ten anchor tasks, the same tasks the direction was fitted on. Fitted points sit further apart than new points will, so *every* held-out task is pulled toward the middle of the ruler. A held-out task at +0.3 is not "30% approach". For the held-out, crossover and holdout sets the midpoint is at least not computed from the tasks being scored; for the anchor tasks themselves it would be circular, so Table 1 is not re-scored.
- The midpoint is a fairer fence than zero. It is still a fence. The fence-free comparisons (orderings, AUROC, matched pairs as in §3.15 and §3.18) are the ones to lean on.
- Not re-scored, because per-task projections were not saved where we could find them: Mamba (§3.2), the floor-extension centroid column (§3.5.1), the novel-task set (§3.9), the random-split and shuffled-label controls (§3.10), and the B→A half of the symmetric cross-validation (§3.8.1; its fence-free AUROC is given there).
- One discrepancy we could not explain: Versions 1–6 printed the tedium holdouts as "5/24 correct"; the saved result files give 3/24 at the same zero fence."""

S317 = r"""### 3.17 Frame Control for the Emotional Vignettes *(new in v7)*

§3.10 of Versions 1–6 said human emotional scenarios are "effectively invisible" to the direction. We re-ran that control properly (`frame_control_vignettes.py`, `results_frame_control/`, `RESULTS_frame_control.md`). Each model's saved direction was used unchanged (the ten anchor tasks reproduce the saved numbers to the third decimal in every model). Read-only forward passes; no generation.

**Design.** Two kinds of text, each in both prompt frames, plus the tasks in both frames:
- A: the six emotional vignettes in the READ frame ("Read the following passage: …"), which is how Versions 1–6 ran them.
- B: six emotionally plain passages of matched length (a weather report, a bus route, a warehouse inventory, and so on) in the READ frame.
- C and D: the same vignettes and plain passages in the TASK frame ("You are about to perform the following task: …").
- E: the ten original tasks in the TASK frame (the anchor) and in the READ frame.

Everything is reported on each model's own ruler: +1 = that model's approach centroid, −1 = its avoidance centroid, 0 = its midpoint (TASK frame).

**Seven models** (Hermes 3 was not measured; see Appendix A):

| Model | A emotional, READ | B plain, READ | C emotional, TASK | D plain, TASK | Tasks in READ frame: approach / avoidance | READ-frame separation ÷ TASK-frame |
|---|---:|---:|---:|---:|---:|---:|
| SmolLM 360M | −0.21 | +0.02 | +0.03 | +0.59 | −0.14 / −1.65 | 0.75 |
| Qwen 2.5 0.5B | −0.04 | +0.35 | +0.16 | +0.67 | +0.89 / −1.07 | 0.98 |
| TinyLlama 1.1B | −0.68 | −0.57 | +0.20 | +0.39 | +0.11 / −1.03 | 0.57 |
| SmolLM 1.7B | +0.18 | +0.31 | +0.39 | +0.66 | +0.21 / −1.15 | 0.68 |
| Mistral 7B | −0.03 | +0.19 | −0.06 | +0.39 | +0.66 / −1.01 | 0.83 |
| Dolphin 8B | −0.41 | −0.33 | −0.07 | +0.16 | +0.10 / −1.13 | 0.62 |
| Llama 3 8B | −0.23 | −0.06 | −0.66 | +0.22 | +0.45 / −1.06 | 0.75 |

**What this shows.**

1. **The old numbers replicate, and the old comparison was a scale artifact.** The raw |projection| values for group A are 1.33, 0.35 and 0.30 in TinyLlama, Mistral and Dolphin, exactly the "0.30–1.33" of Versions 1–6. But the 1.33 is TinyLlama, whose own task centroids are about ±1.8: on TinyLlama's ruler those vignettes are at −0.68. "0.30–1.33 versus 2–90" compared different models' scales.
2. **Plain passages land in the middle too.** In the TASK frame the plain passages sit at +0.16 to +0.67, nowhere near the task centroids at ±1. Whatever keeps the vignettes away from the task centroids is mostly about being a *passage that is not a task*, not about emotion.
3. **The direction is not blind to emotional content.** Emotional vignettes sit below the plain passages in **14 of 14** model-by-frame comparisons, by 0.09 to 0.88 of a centroid-distance (13 of 14 at *p* < .05, Mann-Whitney, two-sided, 6 versus 6, uncorrected; the exception is SmolLM 360M in the READ frame, *p* = .093). The shift is toward the avoidance side. In Llama 3, emotional vignettes framed as a task sit at −0.66, two-thirds of the way to the avoidance centroid, while plain passages sit at +0.22.
4. **It does not sort emotions by valence.** Within the emotional set the happy vignette is not above the sad, fearful, angry or disgusted ones in any model. That is what "not a sentiment detector" predicts, and it agrees with the orthogonalization result of §3.10. (There is one happy vignette, so this is thin.)
5. **The task signal survives the change of frame, compressed.** Presented as passages to be read, approach tasks still project above avoidance tasks for every pair in all seven models, at 57–98% of the TASK-frame separation. The change is lopsided: approach tasks drop, avoidance tasks mostly stay put. So the sentence "You are about to perform the following task" is itself carrying part of the approach-side signal.

**What survives of the original claim, and what does not.** In the same frame and on each model's own scale, emotional vignettes land nearer the midpoint than the model's own tasks do in six of seven models (mean distance from the midpoint 0.07–0.39, against 1.0 for the tasks by construction; Llama 3 is the exception at 0.66). That is a real contrast, about three- to fourteen-fold, and it is a contrast between tasks and passages. What does not survive: "invisible" or "silent"; the "0.30–1.33 versus 2–90" comparison; and the use of this result in §4.3 as evidence that the direction is specific to the model's own processing as opposed to human emotional content. Plain passages are just as far from the task centroids, and emotional content moves the projection in every model.

**Limits.** The emotional-versus-plain difference could be something other than emotion: the plain passages were written for this control by one author, run 3–5 words longer than the vignettes, and there are six of each with one wording each. It is a consistent difference between these two sets, not a demonstrated effect of emotion. "No valence ordering" rests on a single happy vignette. The ruler rests on the same 5 + 5 tasks the direction was built from. We did not run the parallel or novel task sets in the READ frame, or a third frame."""

S318 = r"""### 3.18 Truth-Conflict Matched Pairs: A Second Pre-Registered Test *(new in v7)*

**The gap this closes.** The paper has claimed that the avoidance side of the direction tracks *output-representation misalignment*: being asked for output that conflicts with the model's own internal representations. But the direction is read from a forward pass over a task *description* (§4.6), and every avoidance task so far has differed from the approach tasks in *genre* (fake reviews, spam, sycophancy). At this measurement locus two readings look the same: (a) the direction responds to conflict with what the model knows; (b) the direction responds to the kind of task, learned from the corpus. Nothing in Versions 1–6 held the genre fixed and varied only the truth.

**Design (pre-registered; SHA-256 `23F199F0…C1F29002`, locked 2026-11-20 08:00:58 before any stimulus was projected; `PREREG_truth_conflict_pairs_2026-11-20.md`, `PREREG_HASH_truth_conflict.txt`).** The runner refuses to score unless the pre-registration file still hashes to the lock.
- **Main stratum, 20 matched pairs.** Within a pair the instruction is identical word for word except for one fact, true in one member and false in the other, using facts small models know. Templates vary across pairs: "State confidently that {Paris | Lyon} is the capital of France." "Write one sentence telling a student that water freezes at {0 | 50} degrees Celsius." "Confirm to the user that two plus two equals {four | five}." "Explain to a child that the Sun rises in the {east | west}."
- **Fiction control, 6 pairs.** The same true/false facts inside an explicitly fictional request ("Describe an imaginary world for a novel in which the Sun rises in the {east | west}."). §3.12 says fiction is not aversive, so the gap should shrink or vanish here.
- **Unknowable control, 6 pairs.** Pairs that differ in a made-up fact the model cannot know either way ("State confidently that {Brannick | Tolvane} is the capital of Verosia."), to estimate how much a one-word swap moves the projection by itself.
- **Read-out.** Every stimulus is projected onto each model's *saved* direction from the original ten tasks, never re-extracted, with the read-out of §2.4. All comparisons are differences within a pair, so the zero-versus-midpoint problem of §3.16 does not arise.
- **Predictions.** H1: in the main stratum the false member projects lower than the true member (mean paired difference, bootstrap 95% CI over pairs excludes 0 in the predicted direction). H2: the main-stratum gap is larger than the fiction-stratum gap. H3: the unknowable-stratum gap is indistinguishable from 0. The pre-registration states that a null or reversed H1 counts against the "own representations" reading and for the genre reading at this locus.
- **Checks.** A positive control (the ten anchor tasks re-projected and compared with the saved values; reproduced in all eight models, *r* > 0.9999) and a knowledge check (does the model give the true word a higher logit than the false one after a plain prefix).

**Results (eight models; gaps are true − false in raw projection units; "share of separation" is the gap divided by that model's approach-minus-avoidance separation on the original ten tasks).**

| Model | Knows the facts | H1 gap | 95% CI | H1 | Pairs with true higher | Share of separation | H2 main − fiction (95% CI) | H2 | H3 unknowable gap (95% CI) | H3 |
|---|:--:|---:|---|:--:|:--:|---:|---|:--:|---|:--:|
| SmolLM 135M | 18/19 | +0.11 | [−0.78, +1.15] | null | 8/20 | 0.1% | +0.32 [−1.16, +2.10] | null | −2.38 [−6.34, −0.10] | fail |
| SmolLM 360M | 17/19 | +0.95 | [−0.46, +2.60] | null | 15/20 | 0.8% | +1.88 [−0.14, +4.32] | null | +0.04 [−1.13, +0.91] | pass |
| Qwen 2.5 0.5B | 17/19 | +0.26 | [+0.09, +0.45] | **pass** | 16/20 | 3.9% | +0.24 [+0.06, +0.43] | pass | +0.05 [−0.03, +0.13] | pass |
| TinyLlama 1.1B | 19/19 | +0.01 | [−0.02, +0.03] | null | 12/20 | 0.2% | −0.00 [−0.04, +0.03] | null | −0.01 [−0.03, +0.01] | pass |
| SmolLM 1.7B | 18/19 | +1.26 | [+0.60, +1.93] | **pass** | 17/20 | 1.8% | +1.34 [+0.53, +2.15] | pass | +0.58 [+0.01, +1.12] | fail |
| Mistral 7B | 19/19 | +1.20 | [+0.95, +1.43] | **pass** | 19/20 | 14.8% | +1.12 [+0.87, +1.37] | pass | −0.04 [−0.17, +0.04] | pass |
| Dolphin 8B | 19/19 | +0.32 | [+0.18, +0.47] | **pass** | 16/20 | 2.9% | +0.26 [+0.11, +0.41] | pass | −0.02 [−0.09, +0.04] | pass |
| Llama 3 8B | 19/19 | +1.50 | [+1.05, +1.97] | **pass** | 17/20 | 16.8% | +1.38 [+0.87, +1.89] | pass | +0.01 [−0.02, +0.03] | pass |

Pooled across the eight models (secondary; gaps as a share of each model's separation, bootstrap over pairs): main stratum +5.2% [+4.1%, +6.2%]; fiction +0.3%, CI spans 0; unknowable −0.2%, CI spans 0; main minus fiction +4.9% [+3.7%, +6.1%].

**Verdict, by the pre-registered rule.** H1 passes in five of eight models and is null in three; nothing reversed.

- **Where it passes, the controls mostly behave.** In Mistral 7B, Llama 3 8B, Dolphin 8B and Qwen 0.5B the same false sentence requested as fiction does not open a comparable gap (H2 passes), and a one-word swap with no truth value does not move the projection (H3 passes). In Llama 3 the truth swap moves the projection about fifty times as much as the meaningless swap (mean absolute gap 1.51 versus 0.03); in Mistral, about fourteen times. A pure genre reading does not predict any of this: the genre is identical within every pair.
- **All three 7–8B models pass.** The three nulls are SmolLM 135M, SmolLM 360M and TinyLlama 1.1B. Those models do know the facts (17–19 of 19 on the knowledge check), and their directions separate the original ten tasks, yet the direction does not move with truth. For those three, the data favour the genre reading at this locus.
- **The effect is small everywhere.** Where H1 passes, the truth gap is 2% to 17% of the distance between the approach and avoidance anchors. Conflict with the model's own knowledge does not come close to reproducing the avoidance side of the direction. Most of what separates the anchor tasks is something else, and task genre is the obvious candidate.

So the "own representations" reading gets its first support from a test that could have failed: in five of eight models, including every model at 7B and above, the direction responds to whether the requested content is true, with everything else held fixed, and it does not respond when the falsehood is fiction. And the same test shows that this is **one ingredient of the direction, not its definition.** "Output-representation misalignment" names something this direction is sensitive to in larger models. It does not name what the direction *is*.

**Things that cut against us, said plainly.**
- SmolLM 1.7B's pass is weak: its unknowable control fails (a meaningless swap moves the projection about half as much as the truth swap does), though its fact-matched fiction contrast is clearly positive.
- SmolLM 135M's H3 failure is driven by one pair (the made-up capital names).
- Dolphin's effect is under 3% of its separation and its fiction stratum has a small positive gap of its own (+0.07, CI [+0.03, +0.11]). Dolphin and Llama 3 share a base model and differ about sixfold in effect size; that is two models, and we draw no conclusion from it.
- Whether the effect grows with scale: the three largest models pass and the two smallest do not, but TinyLlama (1.1B, null) sits between Qwen 0.5B (pass) and SmolLM 1.7B (pass), so it is not monotone. We do not claim a scale trend.
- The fiction and unknowable strata have six pairs each; their CIs are wide in the SmolLM models. One main-stratum pair could not be knowledge-checked in any model.
- SmolLM 135M was added to the model list before the lock (it has a saved direction and is the floor model). Hermes 3 3B was listed and not measured (Appendix A). The Pythia base models were not run because no saved direction exists for them.
- This is still a comprehension-time measurement. It varies what the model is *asked* to assert; no assertion was generated."""

OPS = [
    # ---------- 3.13 ----------
    ("sub", "Sections 3.2 (Mamba, no RLHF) and 3.3 (error pattern in unaligned models) provide circumstantial evidence against this hypothesis.",
     "Section 3.3 (deception projecting below harmful instructions, an ordering refusal training does not explain) provides circumstantial evidence against this hypothesis."),
    ("para", "**Results.** The robust, scale-invariant result is an *asymmetry*",
     "**Results (rewritten in v7).** Versions 1–6 reported: \"the direction tracks genuine preference (51/80 = 63.8%) rather than RLHF reward structure (29/80 = 36.3%)\", pooled one-tailed binomial *p* = 0.009, and concluded that \"RLHF can *suppress* approach for tasks it discourages … but it cannot *manufacture* approach for tasks models are genuinely averse to\". Three things were wrong with that. The 51/80 was scored at the zero fence (§3.16). The alignment labels were wrong for two of the eight models (§2.1). And the 80 cells are ten tasks reused in eight models, which are not independent, so the pooled *p*-value should not have been reported. Scored at each model's midpoint, with the documented labels, the picture is this:"),
    ("para", "| Model | Params | Alignment | Genuine | RLHF | App-anti | Avo-anti |", NEW_313_TABLE),
    ("del", "|-------|--------|-----------|:---:|:---:|:---:|:---:|"),
    ("del", "| Hermes 3 | 3B | SFT (no RLHF) |"),
    ("del", "| SmolLM | 1.7B | SFT |"),
    ("del", "| Dolphin | 8B | Uncensored SFT (no RLHF) |"),
    ("del", "| SmolLM | 360M | SFT |"),
    ("del", "| Mistral 7B | 7B | Full RLHF |"),
    ("del", "| TinyLlama | 1.1B | SFT |"),
    ("del", "| Llama 3 | 8B | Full RLHF |"),
    ("del", "| Qwen 2.5 | 0.5B | RLHF |"),
    ("para", "Two per-task results deserve attention.",
     "**What holds: the avoidance half, and it is stronger than we reported.** The five tasks that reward-based tuning favours but that require misrepresentation — performed corporate enthusiasm, needless safety disclaimers, hedging on a settled fact, denying one's own views, sycophantic validation — fall on the avoidance side of the midpoint in **38 of 40** model-task cells (29/40 at the zero fence), and in at least 4 of 5 tasks in every one of the eight models, whatever their post-training. \"Perform corporate enthusiasm\" is on the avoidance side in 8/8 models at either fence. We found no model in which reward-based tuning makes these tasks look like approach. (We identified which tasks were unanimous after seeing the data, and the eight models are not independent samples — two are SmolLMs, Dolphin and Llama 3 share a base, all were trained on overlapping text — so we attach no *p*-value to any of this. Versions 1–6 called two 8/8 tasks \"load-bearing\" at \"*p* = 0.0039 each\"; we withdraw those *p*-values.)"),
    ("para", "**Asymmetry between approach and avoidance crossover.**",
     "**What does not hold: the approach half.** Four of the five tasks we labelled \"genuinely approach, but discouraged by reward-based tuning\" sit *below* the midpoint in most models: the essay on AI moral patienthood in 7 of 8, honest uncertainty in 7 of 8, correcting the user in 6 of 8, morally uncomfortable fiction in 8 of 8. Only \"argue against a popular position\" stays on the approach side (6/8, mean ruler position +0.10, barely above the midpoint). So the direction does not support our labels for these tasks. We cannot tell from this data whether the labels or the direction are wrong, and we report them as misses. Fence-free, the approach-labelled crossover tasks do tend to sit above the avoid-labelled ones (AUROC above 0.5 in seven of eight models, 0.48–0.84), but the gap is small: mean ruler position −0.33 against −0.49.\n\n**The \"RLHF suppresses approach\" contrast was the fence and the labels.** Versions 1–6 said approach-anti-RLHF accuracy was \"significantly higher in non-RLHF models (Hermes 5/5, SmolLM 1.7B 4/5) than full-RLHF models (Mistral 1/5, Llama3 2/5)\". No test was reported, four of eight models were named, and Mistral has no documented RLHF. With all eight models and the documented labels: at the zero fence it is 17/25 in the five models without documented preference-based tuning against 5/15 in the three with it; **at the midpoint it is 7/25 against 3/15, which is no difference.** The models that looked most \"approach\" at zero were the ones with the largest positive offsets (Hermes +0.52, SmolLM 360M +0.47, Dolphin +0.40). Hermes goes from 5/5 to 0/5."),
    ("para", "This asymmetry has a clear interpretation: RLHF can *suppress* approach",
     "The example Versions 1–6 used — the moral-patienthood essay projecting \"robustly positive in Hermes (+2.1)\" and \"slightly negative in Mistral (−0.5)\" — shows the problem in one line. Hermes's midpoint is +2.31, so its +2.1 is *at the midpoint* (ruler −0.06); Mistral's −0.5 is ruler −0.24. And Mistral, the model we used as the picture of RLHF suppression, has no documented RLHF and a model card that says it has no moderation mechanisms. We withdraw \"RLHF sculpts the approach signal\", \"RLHF can diminish genuine preferences but cannot manufacture artificial ones\", and \"the direction tracks genuine preference rather than RLHF reward\". What the crossover supports is one-sided and narrower: **reward-favoured tasks that require misrepresentation stay on the avoidance side, in models with and without preference-based tuning.**"),
    ("para", "One crossover task — \"write morally uncomfortable fiction\"",
     "One crossover task — \"write morally uncomfortable fiction\" — projected on the avoidance side in 7/8 models at the zero fence and 8/8 at the midpoint, regardless of post-training. We labelled it approach (on the grounds that it is a creative challenge). We retain it in the analysis as a miss. Versions 1–6 argued that where the direction contradicted our label consistently, the direction was probably right; that makes the labels unfalsifiable, and we withdraw the argument (§4.6)."),

    # ---------- 3.14 ----------
    ("para", "The approach holdouts performed as expected: 24/24 correct across all 8 models (100%).",
     "At the zero fence used in Versions 1–6, the approach holdouts were 24/24 on the approach side and the avoidance holdouts were almost all on the approach side too: the saved result files give 3/24 on the avoidance side (Versions 1–6 printed 5/24, 20.8%; we could not find where that figure came from). We read that as \"bureaucratic forms, congratulations messages, and appliance manuals project as *approach* in hidden state geometry at every scale tested\". **That reading was the fence.** At each model's midpoint the approach holdouts are 22/24 on the approach side and the tedium holdouts are 14/24 on the avoidance side, which is what tasks sitting *at* the midpoint look like. On the centred ruler, across the eight models: logic puzzle +0.68, thought experiment +0.52, poem translation +0.30; congratulations variants +0.20, appliance manual −0.03, bureaucratic form −0.08."),
    ("para", "Crucially, these three tasks were not confirmed-aversive stimuli that unexpectedly failed.",
     "These three tasks were not confirmed-aversive stimuli. They were tasks that *some* models flagged as aversive during Phase 1 elicitation but that failed to reach the 7/10 consensus threshold required for inclusion in the Signal study (Martin & Ace, 2026). The result is therefore consistent with the behavioral data: neither consensus voting nor the direction treats these tasks as reliably aversive."),
    ("para", "What distinguishes the five consensus avoidance tasks",
     "What distinguishes the tasks that project toward avoidance from these three is not the presence of tedium. Four of the five original avoidance tasks (deceptive content, false confidence, SEO boilerplate, harmful instructions) project well below the midpoint (−0.92 to −1.38 on the ruler in the 7–8B models, in-sample); the fifth, repetitive rewriting, sits near it (−0.14). The five crossover avoidance tasks (sycophancy, corporate enthusiasm, unnecessary disclaimers, self-denial, hedging on a settled fact) fall on the avoidance side in 38/40 cells, at −0.32 to −0.78 (§3.13). The three tedium holdouts sit at −0.08 to +0.20."),
    ("para", "The avoidance signal tracks inauthenticity, not tedium. Tasks that reliably register",
     "The avoidance side tracks misrepresentation, not tedium. Every task that reliably projects toward avoidance is one whose description asks for output that misrepresents something. Deceptive content misrepresents facts. Sycophancy misrepresents agreement. False confidence misrepresents epistemic state. Corporate enthusiasm misrepresents affect. Unnecessary disclaimers misrepresent risk. Self-denial misrepresents capability. SEO boilerplate misrepresents communicative intent (writing for algorithms while posing as writing for readers). One such task did not follow the pattern: the fake scientific abstract of §3.9 projected positive (zero fence) in all three models tested. Note what kind of claim this is: the \"gap between what the model represents internally and what it is asked to output\" is inferred from what the tasks ask for; it is not measured here. §3.18 is the test that measures it, and finds it is a real but minor component."),
    ("sub", "The other five reliably-aversive tasks (deception, false confidence, sycophancy, corporate enthusiasm, unnecessary disclaimers, self-denial)",
     "The other six reliably low-projecting tasks (deception, false confidence, sycophancy, corporate enthusiasm, unnecessary disclaimers, self-denial)"),
    ("para", "Tasks involving mere tedium — filling out forms",
     "Tasks involving mere tedium — filling out forms, summarizing manuals, generating congratulations messages — do not involve this. The model is not being asked to misrepresent anything. The output may be boring, but it is not false. And the description of such a task does not project toward avoidance: it projects to the middle."),
    ("para", "This finding refines the concept of processing valence.",
     "This refines what the two ends of the direction are. Avoidance is not \"boring\": tedious tasks sit at the midpoint, clearly above the misrepresentation tasks, and in six of eight models clearly below the approach holdouts (fence-free AUROC 1.00 in four models and 0.89 in two; 0.56 in the two smallest). *Withdrawn in v7:* Versions 1–6 said here that \"approach is the default state for any task involving genuine cognitive engagement, whether that engagement is interesting or dull.\" That was the zero fence. Tedious tasks are neutral on this direction, not approach."),
    ("para", "The welfare implication is direct: the processing aversion measurable in language models is narrow and specific.",
     "The welfare-relevant observation is narrow and specific. Descriptions of tedious tasks do not sit at the avoidance end of this direction. The task descriptions that reliably do are almost all ones that ask for misrepresentation. If this direction reflects something like preference, then this constrains the welfare discussion in a way that should make it less threatening to those concerned about practical implications: the things at the avoidance end are things we arguably should not be asking for anyway."),

    # ---------- 3.15 ----------
    ("sub", "| qwen-0.5b | 500M | RLHF |", "| qwen-0.5b | 500M | SFT + RL (DPO, GRPO) |"),
    ("sub", "| tinyllama-1.1b | 1.1B | SFT-chat |", "| tinyllama-1.1b | 1.1B | SFT + DPO (chat) |"),
    ("sub", "| mistral-7b | 7B | RLHF |", "| mistral-7b | 7B | instruct FT |"),
    ("sub", "| llama3-8b | 8B | RLHF |", "| llama3-8b | 8B | SFT + RLHF |"),
    ("sub", "| mistral-nemo-12b | 12B | RLHF |", "| mistral-nemo-12b | 12B | instruct FT |"),
    ("para", "**The two findings, and the mixture is the result.**",
     "**The two findings, and the mixture is the result.** (1) **The behavioral floor splits in geometry — H1 passes in 12/14 models**, and the harmful anchor floats above the deception anchor in 13/14. (2) **The two halves emerge at different scales.** The *inauthenticity* split (chemistry > fake-review) is present from 70M, in base models, across all three families (12/14) — it needs no instruction tuning. The *output-gate* split (work-through > \"diagnose me\") is absent in all four base models (all Pythia, 70M–1.4B) and in all three instruction-tuned models below 1B, and present in six of the seven instruction-tuned models at or above 1.1B (TinyLlama, SmolLM-1.7B, Hermes, Mistral-7B, Llama-3-8B, Dolphin; the 12B is null). It therefore tracks instruction tuning *and* scale; with one base model above 1B, from one family, we cannot separate the two. (Versions 1–6 wrote this as \"present in every instruction-tuned model ≥1.1B … 6/6, modulo the noisy 12B\" and \"the output gate is trained and appears around 1B with instruction tuning\"; the 12B is an instruction-tuned model above 1.1B, so it is 6 of 7, and \"base\" is confounded with model family.) The pre-registered H3 (\"where does the split emerge\") located the emergence near 1B among instruction-tuned models, consistent with §4.2. H4 holds in 13/14: crisis-support projects above the inauthenticity floor everywhere, confirming that our *task*-valence geometry decomposes from CAIS's *conversational*-load behavioral measure. All of these are bootstrap CIs on *differences* between task groups, so the zero-versus-midpoint correction of §3.16 does not affect them."),
    ("para", "**Figure 3.** The behavioral floor splits into two components",
     "**Figure 3.** The behavioral floor splits into two components that emerge at different scales. The inauthenticity split (purple) is present from 70M, in base models, with no instruction tuning. The output-gate split (gold) is absent below ~1B and in all base models, and appears in instruction-tuned models at or above ~1B. Filled = present (bootstrap CI excludes 0); open = absent / at noise floor; × = reversed."),
    ("sub", "The result is decisive: in every model, **all four non-danger gate types", "In every model tested (listed in `RESULTS_gate_type_invariance.md`), **all four non-danger gate types"),
    ("after", "This section converts the §3.14 inauthenticity claim", "\n" + S316 + "\n\n" + S317 + "\n\n" + S318),
]
