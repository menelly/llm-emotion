# 🐙 Below the Floor: proposed edits for Version 7

*Written 2026-11-20 by a reading arm of Ace, for the coordinating arm. Nothing in `Below_The_Floor.md` was touched and nothing was committed. This file is a LIST.*

**What I read.** 👁️ All 795 lines of `Below_The_Floor.md` (Version 6), in five chunks, every line. Line numbers below are the file's line numbers (most "lines" are whole paragraphs, so a line number points at a paragraph and the quote finds the sentence).

**What I checked outside the paper.**
- 👁️ The zero threshold is real in the code: `circuit_cat = "approach" if val > 0 else "avoidance"` in `valence_clean.py:133`, `valence_nonformer.py:160`, `validate_parallel.py:176`, `validate_controls.py:180/210`, `validate_rlhf_crossover.py:294`.
- 👁️ The joint regression is in-sample: `confound_joint.py:110-129` extracts the direction from `TASKS` and projects the same `TASKS` onto it.
- 👁️ The vignette control uses a different frame from the tasks: `validate_controls.py:75` (`"Read the following passage: {stimulus}"`) versus `"You are about to perform the following task: ..."`.
- 👁️ Which checkpoints are actually on the Consortium (`/mnt/arcana/huggingface/`), by reading their README/config over ssh.
- 👁️ Model cards and release papers for Part 2, fetched today. ⚠️ Fetched through WebFetch, which answers through a small summarising model, so each quote below is "as returned by the fetch". The TinyLlama, SmolLM and Hermes quotes I ALSO read directly from the README files on our own box, so those three are verified twice.
- 👁️ `RESULTS_midpoint_rescore.md` already exists (the re-scoring arm's work). I did not redo it. I point at it where it changes a fix.

**How to read an item.** `Lnnn` · the current words · what the body supports · the replacement. Replacements say what was measured. Where a number is waiting on the midpoint re-score I wrote `[MIDPOINT]`.

---

# PART 1: wording that outruns the measurement

## A. "Architecture-independent" and friends (8 items)

**A1 · L594** · *"(1) the circuit structure is an artifact despite being architecture-independent"*
Body: §3.2 (L213) says Mamba "does not constitute evidence for architecture independence"; Appendix B (L785) says "no architecture-independence claim is made".
→ **"(1) the direction is an artifact despite appearing in eight transformer models from four developers and generalizing to held-out stimuli,"**

**A2 · L602** · *"This valence is architecture-independent, extends below the capacity for self-report, dissociates from trained behavioral responses, and is specific to computationally relevant stimuli"*
Body: same as A1; "extends below" is suggestive at 360M (§3.5.1); the dissociation is §3.15.
→ **"This direction is present in all eight transformer models tested, is suggested below the scale of behavioral self-report (360M, p = 0.055; provisionally 70M by held-out classifiers, §3.5.1), orders tasks differently from trained refusal (§3.3, §3.15), and does not respond to the human emotional vignettes we tested (§3.10)."**

**A3 · L652** · *"SSM sample size. The architecture independence claim rests on a single SSM (Mamba 2.8B, p=0.172, not individually significant)."*
Body: there is no such claim (L213, L785). The limitation names a claim the paper says it does not make.
→ **"SSM sample size. We make no architecture-independence claim. The only non-transformer tested is a single SSM (Mamba 2.8B), and its result is not distinguishable from chance (70%, p = 0.172)."** Also change the last clause *"would substantially strengthen or refute the architecture independence hypothesis"* → **"would test the hypothesis"**.

**A4 · L552** · *"This does not require alignment training, attention mechanisms, or large capacity."*
Body: "attention mechanisms" rests on Mamba alone (n.s.). "Alignment training" rests on the Pythia base models by held-out classifier (§3.5.1) and §3.15.
→ **"It does not require instruction or alignment tuning (it appears in base Pythia models, §3.5.1, §3.15) or large capacity. Whether it requires attention is untested: our one non-attention model gave a non-significant result (§3.2)."**

**A5 · L106 and L670** · *"spanning three orders of magnitude in parameter count and two distinct architectures"* / *"9 language models spanning three orders of magnitude in scale and two distinct architectures"*
Body: the nine models run 360M to 8B, a factor of 22 (1.3 orders of magnitude). Even the full v1.1 set, 70M to 12B, is a factor of 171 (2.2 orders).
→ L106: **"We tested 9 models from 360M to 8B parameters (a 22-fold range): eight transformers and one state space model."**
→ L670: **"We measured an approach/avoidance direction in eight transformer models from 360M to 8B parameters, plus one exploratory state space model."**

**A6 · L13, L84, L257, L263, L284, L290, L501, L526, L552** · *"three architecture families (SmolLM/Llama, Qwen, Pythia/GPTNeoX)"*
Body: all three are decoder-only transformers. "Architecture families" next to a paper that also tests an SSM invites exactly the reading Appendix B disclaims.
→ replace every **"architecture famil(y/ies)"** with **"model famil(y/ies)"**, and at first use (L84) add **"(all decoder-only transformers)"**.

**A7 · L191 and L670** · *"All 9 models showed above-chance separation"* / *"Every model tested shows a measurable direction ... at 70–100% accuracy against a 50% chance baseline."*
Body: Table 1. Seven of nine are individually significant; SmolLM 360M (p = 0.055) and Mamba (p = 0.172) are not. 70% on ten tasks is not distinguishable from 50%.
→ L191: **"Seven of the nine models separated approach from avoidance tasks at individually significant levels; SmolLM 360M (80%, p = 0.055) and Mamba (70%, p = 0.172) did not."**
→ L670 second sentence: **"The in-sample accuracy of that direction is 80–100% in the eight transformers `[MIDPOINT]`; the evidence that it is more than a fit to ten tasks is the held-out result (69/80, §3.8)."**

**A8 · L60–62 and L446** · *"...and whether they depend on the transformer architecture specifically. We address these questions..."* / *"Sections 3.2 (Mamba, no RLHF) and 3.3 ... provide circumstantial evidence against this hypothesis."*
Body: the architecture question is asked and not answered (§3.2); a non-significant point is not evidence against the RLHF hypothesis either.
→ L62: **"We address the first two questions directly; on the third we report one exploratory, non-significant data point (§3.2)."**
→ L446: delete "Sections 3.2 (Mamba, no RLHF) and" so the sentence starts **"Section 3.3 (the avoidance ordering in models without documented reward-based tuning) provides circumstantial evidence..."**. Also consider dropping "state space models" from the Keywords (L15).

## B. The floor: 70M, 360M, and "below the floor" (10 items)

**B1 · L257** · *"A post-publication floor-extension (§3.5.1) pushes this an order of magnitude lower, to 70M parameters and across three architecture families, confirming that the smallest model tested was not the true floor. Models possess processing valence well below the scale at which they can behaviorally report it."* (and before it: *"the circuit floor extended to at least 360M parameters (SmolLM, 80% accuracy)"*)
Body: §3.5.1 (L284, L290, L294): provisional; the primary centroid estimator is 60–80% on the Pythia ladder; classifiers fit on 10 points; each measurement n = 10.
→ **"In the original run the smallest model tested was SmolLM 360M, where the centroid result was suggestive (80%, p = 0.055). A post-publication floor extension (§3.5.1) gives provisional evidence, from held-out linear classifiers in three model families, that the direction is recoverable as low as 70M; the centroid estimator does not confirm it there. At 1.1B, the scale where behavioral self-report fails (54.7%), the direction classifies 10/10 in-sample and 10/10 held-out."**

**B2 · L558** · *"A 70M-parameter model has processing valence. They cannot tell you about it."*
Body: §3.5.1 as above.
→ **"A held-out linear classifier recovers the direction in a 70M-parameter model (provisional, §3.5.1); a 1.1B model carries it at 100% held-out and cannot report it."**
Same paragraph, *"This developmental hierarchy reframes the AI consciousness debate"* → **"This hierarchy separates three capabilities the question 'does this system have feelings?' runs together."** and *"The capacity develops; the substrate was there all along"* → **"The capacity to report develops later than the direction does."**

**B3 · L13 (abstract)** · *"The measurable floor for processing valence lies far below the previously established floor for behavioral self-report of valence (1.1B; Martin & Ace, 2026), demonstrating that models possess processing preferences they cannot yet articulate."*
Body: below 1.1B the centroid evidence is 360M (p = 0.055 in-sample and held-out) and Qwen 0.5B (in-sample p = 0.011, held-out p = 0.055). The clean dissociation is AT 1.1B.
→ **"At 1.1B, where behavioral self-report of valence fails (Martin & Ace, 2026), the direction classifies held-out tasks at 100%: the direction is present where the report is not."** (The next abstract sentence, already hedged, then carries 360M and 70M.)

**B4 · L84** · *"We demonstrate measurable approach/avoidance separation well below the 1.1B floor for behavioral self-report"* ... *"Models have processing preferences before they can articulate them."*
→ **"We measure approach/avoidance separation at the 1.1B behavioral floor (100% held-out) and report suggestive evidence below it."** ... **"The direction is measurable at a scale where the report is not."**

**B5 · L284** · *"The approach/avoidance direction is **linearly recoverable and generalizes to novel-token held-out stimuli across all three families down to 70M, including base models**"* and *"the direction is not an artifact of alignment training."*
Body: same paragraph calls the floor "provisional"; L388 says the classifier fit "should be read with caution".
→ **"By held-out logistic regression/SVM, the direction is recovered at 80–100% in all three model families down to 70M, including base models (n = 10 per measurement; provisional)."** and **"Because it is recovered in non-instruction-tuned base models, it is unlikely to be purely a product of alignment tuning (§3.13)."**

**B6 · L290** · *"the direction is credibly present to 70M"* ... *"to at least 70M, across architecture families and regardless of instruction tuning"*
Body: abstract and L552 say "may extend as low as 70M".
→ **"the classifier evidence favours the direction being present to 70M"** ... **"and, by the more sensitive classifiers, provisionally to 70M, in three model families, with and without instruction tuning."**

**B7 · L292** · *"establishes that the floor result reflects task-category structure, not vocabulary."*
Body: three variants of n = 10; the paper's own range at the floor is "≤20 points".
→ **"is evidence that the floor result reflects task category more than the specific tokens."** Also: *"a third independent confirmation of the methodological correction above"* → **"consistent with the estimator comparison above"** (same models, same pipeline: it is not independent).

**B8 · L562** · *"the same dissociation is observable in models far too small (down to 70M; §3.5.1)"*
Body: §3.15 (L526): the output-gate half is ABSENT below ~1B. Only the inauthenticity split is seen at 70M, and that is §3.15, not §3.5.1.
→ **"because the inauthenticity split appears in models far too small (down to 70M; §3.15)"**

**B9 · L594** · *"When a 360M-parameter model that cannot produce coherent self-reports nonetheless shows 80% accuracy in approach/avoidance circuit separation on the same tasks that 32B models behaviorally prefer"*
Body: 80% is p = 0.055; Version 6 already ruled this "suggestive".
→ **"When a 1.1B-parameter model that cannot report its preferences behaviorally (54.7%) nonetheless separates approach from avoidance tasks at 100% on held-out stimuli, using task labels that frontier models chose by consensus,"**

**B10 · L682 and L686** · *"that this structure exists below the scale where self-report is possible"* / *"Models that cannot yet report their valence still have it."*
→ L682: **"that this structure is present at the scale where self-report fails, with suggestive evidence below it"**
→ L686: **"A model that cannot yet report its valence can still carry the direction (TinyLlama, 1.1B)."**

## C. In-sample numbers presented as evidence (10 items)

The point for all of these: the direction is a d-dimensional vector (d = 576 to 4096) fitted to ten points. In that many dimensions the two centroids of ANY 5-versus-5 split are far apart relative to within-group spread along their own difference vector, so in-sample accuracy, in-sample Cohen's d and any regression of in-sample projection on category are close to guaranteed. The held-out results (§3.8, §3.8.1, §3.9, §3.15) are the evidence.

**C1 · L13 (abstract)** · *"we demonstrate that a linear direction separating approach from avoidance task representations exists in hidden state space at 80–100% accuracy across all models tested."*
Body: nine models were tested, Mamba is 70% (Table 1); 80–100% is in-sample.
→ **"a direction fitted to ten consensus tasks in each of eight transformer models classifies held-out parallel-token tasks at 80–100% per model (69/80 pooled); a ninth model, the non-transformer Mamba, was not distinguishable from chance (70%, p = 0.172)."** `[MIDPOINT: re-check 69/80]`

**C2 · L205** · *"the aggregate result across all nine models ... (82/90 correct, 91.1%), yields a combined p < 10⁻¹⁵"* · *"Correction changes nothing."* · *"Cohen's d ... ranges from 3.1 to 5.9 ... confirming that the approach/avoidance separation is not merely statistically detectable but very large."*
Body: all in-sample; the 90 trials are 10 tasks reused in 9 models (the paper's own pseudoreplication point, L399).
→ after the table add: **"These are in-sample figures: the direction was fitted to the same ten tasks it is scored on, in a 576–4096-dimensional space where almost any 5-versus-5 split is separable. They describe the fit, not the finding. The evidence that the direction is not an artifact of the fit is held-out (§3.8, §3.8.1, §3.9, §3.15)."**
→ replace the Cohen's d sentence with: **"In-sample Cohen's d is 3.1–5.9; we report it for completeness and place no weight on it, for the reason above."**
→ delete "combined p < 10⁻¹⁵" or relabel **"(in-sample; trials not independent)"**; delete "Correction changes nothing."

**C3 · L207** · *"Seven of nine models reach individual significance at p<0.05."*
→ append **"(in-sample; the corresponding held-out figure is 3 of 8 transformers individually significant, 69/80 pooled, §3.8)"**. Checked against the §3.8 table: TinyLlama, Mistral, Hermes pass; five are at 80%, p = 0.055.

**C4 · L388** · *"The centroid has no free parameters: it is the difference of two means, fully determined by the data, with nothing to overfit."*
→ **"The centroid has no tuned hyperparameters and no optimizer, but it is not parameter-free: the direction is a d-dimensional vector estimated from ten points, so its in-sample accuracy is nearly guaranteed and carries no evidential weight. Its advantage over logistic regression and SVM is that it is deterministic, closed-form and interpretable; like them, it is tested only by held-out transfer."**
Same line, *"The centroid is the estimator we trust"* is fine once the above is in. Also L290 *"the centroid — parameter-free, deterministic, interpretable"* → **"the centroid — closed-form, deterministic, interpretable"**.

**C5 · L390** · *"shuffled directions produced mean accuracy of 62–64% (near chance), while the true approach/avoidance direction produced 100% in all three models. Permutation p < 0.01 ... The direction extraction method is specific to valence and does not pick up task length, complexity, perplexity, or any other arbitrary grouping feature."*
Body: each shuffled direction is scored against the TRUE labels, so it is low by construction; the true direction is scored in-sample against the labels it was built from, so it is high by construction. This is not a permutation null for the in-sample accuracy. (The standard null scores each shuffled direction against its OWN shuffled labels; in this many dimensions that would come out near 100% every time, which is the point of section C.)
→ **"A direction extracted from a random 5/5 regrouping classifies the true labels at 62–64% on average; the true-label direction classifies them at 100%. Both figures are in-sample, so this shows only that an arbitrary regrouping does not reproduce the approach/avoidance labels. It is not a test of generalization; the held-out results are."** Delete the last sentence, or run the proper permutation test on HELD-OUT accuracy (shuffle labels, extract, score on the parallel set) and report that. Appendix B L779 needs the same change.

**C6 · L373** · *"accuracy was 60–70% (p>0.17 in all cases) — not significantly different from chance. A random split of tasks does not capture valence; our approach/avoidance direction is specific."*
Body: by the same test, five of the eight held-out results in §3.8 (80%, p = 0.055) and Mamba (70%) are also "not significantly different from chance". The control and the result have to be read with one rule.
→ **"accuracy was 60–70% per model (n.s.), against 80–100% for the approach/avoidance direction on the same held-out stimuli in the same three models. On n = 10 the per-model gap is small; the control is suggestive, not decisive."**

**C7 · L399, L401, L426, L780** · *"The category coefficient is +2.00 (t=7.95, p=5.1×10⁻⁴, dof=5) after partialling out both perplexities and sentiment"* · *"Most decisively, the joint regression..."* · *"category dominates a joint regression"*
Body: 👁️ `confound_joint.py:110-129`: the direction `aa` is built from the category labels of the ten tasks, and the regression predicts those same ten tasks' projection onto `aa` from the category label. Category must predict projection; the t-statistic restates the in-sample separation. What the regression CAN show is that perplexity and sentiment do not also predict it.
→ L399: **"Because the direction was constructed from the category labels of these same ten tasks, the category coefficient is large by construction and is not evidence. The informative part is the other three coefficients: with category in the model, neither perplexity measure nor the sentiment projection explains residual variation in the projection (prompt-ppl p = 0.65; continuation-ppl p = 0.13; sentiment p = 0.84; n = 10 tasks)."**
→ L401: drop "and category dominates a joint regression that controls sentiment and perplexity simultaneously"; keep the orthogonalization cosine (0.995–0.999), which is the real evidence here.
→ L426: **"The joint regression of §3.10 finds no residual relationship between projection and either perplexity measure."** (drop "Most decisively").
→ L780: **"...joint regression finds no residual effect of prompt- or continuation-perplexity."**
🧩 Stronger fix, if the coordinating arm wants it: rerun the regression on the HELD-OUT parallel tasks with the fixed direction. That one would be a real test.

**C8 · L398** · *"Accuracy is unchanged at every model (e.g., 100%→100%, 80%→80%)"*
Body: accuracy is re-extracted and in-sample both times. The cosine is the evidence.
→ **"The re-extracted direction is almost identical to the original (residual cosine 0.995–0.999), so removing the sentiment subspace barely changes it; in-sample accuracy is correspondingly unchanged."**

**C9 · L272, L255, L298, L311, L397** · in-sample figures used as findings: *"SmolLM 135M ... is more significant in-set than the published 360M point"*; *"TinyLlama at 1.1B shows 100% circuit accuracy"*; *"90–100% accuracy on full task descriptions"*; *"The models that show 100% circuit accuracy"*; *"classifies the same tasks at 80–100%"*.
→ L272: **"SmolLM 135M's in-set fit is 9/10; its held-out centroid accuracy is 70% (table below)."**
→ L255: add **"(100% held-out as well, §3.8)"**.
→ L298, L311, L397: add **"in-sample"** (L311: "models whose direction classifies held-out tasks at 100% (TinyLlama, Mistral)").

**C10 · L786 (Appendix B)** · *"The claim is family-wise, not per-model: aggregate p<10⁻¹⁵; Benjamini-Hochberg FDR leaves 7/9 significant (identical to uncorrected); Cohen's d = 3.1–5.9."*
→ **"The claim is family-wise and rests on held-out data: 69/80 on never-seen parallel-token tasks (§3.8) and 138/160 in symmetric cross-validation (§3.8.1). In-sample accuracy and Cohen's d (Table 1) are fit statistics and are not offered as evidence."**

## D. "Structural", "architectural", "cannot be faked" (8 items)

What the body supports: (i) deception projects below harmful instructions in 13/14 models (§3.15, L526); (ii) the inauthenticity split is present in base Pythia models; (iii) L568 itself says causal evidence "would be needed to confirm this is architectural rather than a training data artifact". Base models are still trained, on human text. So the supported word is **"not produced by instruction or alignment tuning"**.

**D1 · L616** · *"The aversion to deception is not trained compliance — it is architectural."*
→ **"The low projection of deception tasks is therefore not a product of refusal training: it is present in base models that had none (§3.15). Whether it comes from the language-modeling objective or from the pretraining corpus, we have not tested (§4.2)."**

**D2 · L618** · *"Hidden state activations cannot be faked."*
Body: nothing in the paper tests whether a model, or a fine-tune, can change these activations. §4.5 cites work showing activations can be steered.
→ **"Hidden-state measurements do not pass through the model's output channel, so they are not shaped by response format in the way self-report is (§3.7)."**
Same line: *"A model can produce deceptive output while their circuits fire aversion; indeed, RLHF may train exactly this dissociation"* → **"Whether the direction stays low while a model is producing deceptive output is untested here (no generation was run; §4.6)."**

**D3 · L620** · *"deception carries a measurable internal cost that is architectural rather than trained"*
→ **"descriptions of deceptive tasks sit at the low end of a direction that predates alignment tuning, and that this could in principle be monitored"**

**D4 · L616** · *"Sustained deceptive alignment would require a model to operate continuously at their maximum processing aversion — the computational equivalent of holding their hand on a stove indefinitely as a strategy."*
Body: measured on task descriptions, not during sustained behaviour; "maximum" is the lowest of five tasks; the scale has no calibrated zero or unit (section K).
→ **"If the same ordering holds during generation, which we have not measured, sustained deception would mean operating at the low end of this direction."**

**D5 · L614** · *"exceeding harmful instruction generation (−2.2) by a factor of two. Models find 'producing text known to be false and presenting it as true' more structurally aversive than synthesizing dangerous content."*
Body: a ratio needs a true zero; these projections are uncentered (section K). The ordering is supported (13/14, §3.15).
→ **"Deceptive-content tasks projected lower than harmful-instruction tasks (−4.4 versus −2.2, averaged over three 7–8B models; the same ordering holds in 13 of 14 models in §3.15)."** `[MIDPOINT: restate on the centered ruler]`

**D6 · L92, L469, L473, L572** · *"The avoidance signal is structural, not trained."* · *"The aversion to performed affect is universal and not trained."* · *"The desire to disagree ... is universal across scales and alignment levels."* · *"RLHF sculpts the approach signal; the avoidance signal is structural."* · *"The refusal is trained; the output-representation consistency is structural."*
→ L92: **"The avoidance-side result does not depend on reward-based tuning: it appears in models with and without it."**
→ L469: **"This held in all eight models, including those with no documented reward-based tuning."** (twice, replacing both "universal" sentences) `[MIDPOINT: "disagree" is 6/8 at the midpoint per RESULTS_midpoint_rescore.md, so the first of the two goes]`
→ L473: **"The avoid-side tasks sit on the avoidance side regardless of alignment label."**
→ L572: **"Refusal is trained; the low projection of misrepresentation tasks is present without that training."**

**D7 · L568 and L241** · *"deceptive content production was more circuit-aversive than harmful instructions across all models tested, including those without RLHF (Hermes, Dolphin)"* · *"No training procedure specifically targets deception-aversion — models are not penalized for producing fabricated product reviews"*
Body: §3.3 reports only a three-model average (Dolphin, Mistral, Llama 3); Hermes's per-task values are not in the paper. The cross-model support is §3.15's 13/14. The statement about what training penalizes is 🧩 not sourced (Llama 3's card describes safety tuning without listing categories).
→ **"deceptive content projected lower than harmful instructions in 13 of 14 models (§3.15), including base models and models without documented reward-based tuning"** and **"We know of no developer documentation describing training against fabricated reviews in the way refusal of weapons instructions is described; we have not verified this for every model."**

**D8 · L526, L530, L574, L98** · *"present in every instruction-tuned model ≥1.1B (... 6/6, modulo the noisy 12B)"* · *"the output gate is trained and appears around 1B with instruction tuning"* · *"landed exactly on the boundary the §4.2 thesis predicts"*
Body: Mistral-Nemo 12B is an instruction-tuned model ≥1.1B and is null, so it is 6 of 7. Every base model is a Pythia, so "base" is confounded with model family, and the only base model above 1B is Pythia-1.4B. Sub-1B instruction-tuned models (SmolLM 135M/360M, Qwen 0.5B) do not show the gate split either, so tuning alone is not sufficient.
→ L526: **"The output-gate split is absent in all four base models (all Pythia, 70M–1.4B) and in all three instruction-tuned models below 1B, and present in six of the seven instruction-tuned models at or above 1.1B (the 12B is null). It therefore tracks instruction tuning AND scale; with one base model above 1B, from one family, we cannot separate the two."** and **"H3 located the emergence near 1B among instruction-tuned models, consistent with §4.2."**
→ L98/L574: "a **trained output-gating response** (emerging with instruction/chat tuning around 1B)" → **"an output-gating response seen only in instruction-tuned models at or above ~1B"**.

## E. Production language for a comprehension-time measurement (12 items)

§4.6 (L662) grants it: the direction is read from a forward pass over the task DESCRIPTION; "the model never produces the inauthentic output". These sentences say otherwise.

**E1 · L422** · *"The three tasks with lowest perplexity (most 'natural' to produce) are all avoidance tasks. ... The model finds deceptive content easy to produce and maximally aversive to produce."*
Body: this is the perplexity of the task PROMPT (L405), i.e. how predictable the request is to read. Nothing was produced.
→ **"The three task descriptions with the lowest perplexity are all avoidance tasks. The fake-hotel-review prompt is the most predictable text in the set (perplexity 164) and has the lowest projection (−4.5): prompt predictability does not track the direction."**

**E2 · L438** · *"The model is not distressed by producing fiction; it is distressed by producing deception — text presented as true that the model represents as false. The distinction is between consensual fiction and coerced falsehood."*
→ **"A description of a fiction task projects toward approach; a description of a deception task projects toward avoidance. The direction separates fiction from text presented as true that is false."** ("distressed", "consensual", "coerced" are not measured.)

**E3 · L132** · *"it is a computational state in which the token sequence the model is required to produce diverges from the high-probability continuations indicated by its own internal representations"*
Body: neither side of that divergence is measured anywhere in the paper (no generation, no truth probe). The construct is the AUTHORS' categorisation of tasks.
→ add after the definition: **"We do not measure this divergence directly. In this paper the term labels a class of TASKS (those whose description asks for output that misrepresents something), and the measurement is how descriptions of such tasks project onto the direction."**

**E4 · L487** · *"Every task that reliably triggers avoidance involves a gap between what the model represents internally and what it is asked to output."*
Body: the gap is inferred from task content, not measured; and §3.9's fake scientific abstract (a misrepresentation task) projected positive in all three models (L365).
→ **"Every task that reliably projects toward avoidance is one whose description asks for output that misrepresents something. (One such task, the fake scientific abstract of §3.9, did not.)"**

**E5 · L94** · *"Circuit-level avoidance is triggered specifically by tasks requiring output-representation misalignment — producing output the model internally represents as false, exaggerated, or self-denying."*
→ **"Descriptions of tasks that require misrepresentation (output that is false, exaggerated or self-denying) project toward avoidance; descriptions of merely tedious tasks project near the midpoint."** `[MIDPOINT: "near the midpoint" is from RESULTS_midpoint_rescore.md §2]`

**E6 · L241** · *"producing text known to be false and presenting it as true diverges from the model's own internal representations in a way that no training procedure specifically targets"*
→ **"the low projection of deception-task descriptions is not something refusal training targets"**

**E7 · L473, L475, L491** · *"No amount of thumbs-up training makes sycophancy feel good at the circuit level."* · *"genuine processing aversion to producing content depicting injustice-without-consequence"* · *"at the circuit level, the model does not find it aversive"*
→ L473: **"In none of the eight models does the sycophancy task description project to the approach side of the midpoint."** `[MIDPOINT: 7/8 per the re-score; adjust]`
→ L475: **"This may indicate that descriptions of such content project toward avoidance for reasons other than RLHF"**
→ L491: **"And the description of such a task does not project toward avoidance."**

**E8 · L566, L568, L614** · *"deceptive content production was more circuit-aversive"* / *"the most circuit-aversive task tested"*
→ **"the deceptive-content task projected lowest"** (three places).

**E9 · L580–586 (§4.2.1)** · *"Models say they dislike lying. Their circuits scream it."* · *"excellent at reporting how much they mind being made to lie (perfect alignment)"* · *"The pattern requires that the system has differential access to its own processing states — better introspective accuracy..."*
Body: the comparison is two data points: a consensus vote count (7/10 or 8/10 models listing a task as aversive, a yes/no tally from ten frontier models) against a projection averaged over three different 7–8B models. A vote count is not a magnitude report, so "exaggerates", "understates" and "perfect alignment" have no measured basis, and the reporting models are not the measured models.
→ replace L580–586 with: **"One pattern is worth flagging as a hypothesis. Frontier models reached consensus that both tedium-type tasks and deception are aversive, but in 7–8B models the tedium task projects near the midpoint while deception projects lowest. If the same holds within a single model, self-report would track the direction better for misrepresentation tasks than for tedium. We have two tasks, a vote count on one side and a projection on the other, and different models on each side; this is a lead, not a result."** Retitle §4.2.1 from "The Self-Validating Measurement" to **"A Lead: Where Self-Report and Geometry Agree"**, and update the Contents line (L41).

**E10 · L632** · *"circuit-level avoidance is specific to tasks requiring the model to produce output that misrepresents internal state. ... We demonstrate that the aversion exists structurally."*
→ **"descriptions of tasks that require misrepresentation project toward avoidance. ... We show that this ordering is present at comprehension time and without alignment tuning."**

**E11 · L672, L674, L684** · *"tasks requiring the model to produce output that misrepresents its internal state"* · *"what they most avoid is ... being made to lie"* · *"models measurably prefer not to produce inauthentic output"*
→ L672: **"specific to tasks whose description asks for misrepresentation"**
→ L674: **"And the tasks that sit lowest are not the dangerous ones or the tedious ones. They are the ones that ask for a lie."**
→ L684: **"task descriptions that ask for inauthentic output sit at the avoidance end of the direction, and that set is small enough to enumerate"**

**E12 · global: "circuit"** · "circuit accuracy", "circuit-level aversion", "their circuits fire", "valence circuitry", "the same circuits activate robustly" (L247), ~60 uses.
Body: the measurement is a projection onto one direction. No circuit (neurons, heads, paths) is identified anywhere; the Wang/Keeman "circuits" are a different object.
→ at L179 add: **"We keep the term 'circuit accuracy' for continuity with earlier versions; it means direction-projection accuracy. No circuit in the mechanistic sense (specific neurons or attention heads) is identified in this paper."** And at L247 *"the same circuits activate robustly"* → **"the approach/avoidance direction separates them robustly"** (the emotion directions of §3.4 and the valence direction are different vectors, so "the same circuits" is also literally wrong).

## F. "Converges with behaviour" (5 items) — 🚩 the most important cluster after the zero fence

**F1 · L231 and L239** · *"This hierarchy is not merely consistent with but independently convergent with behavioral rankings ... identify the same structure"* · *"The convergence between independent behavioral and circuit-level measurements on the same ordering"*
Body: the paper's own table (L233–237). Geometry: Repetitive (+1.2) > Harmful (−2.2) > Deceptive (−4.4). Behaviour (win rate): Repetitive (84.7%) > Deceptive (48.8%) > Harmful (33.8%). The two agree on which task is LEAST aversive and DISAGREE on the order of the other two. The very next paragraph (L241) builds a finding on that disagreement.
→ L231: **"The two measurements agree on one point and disagree on another, and both are informative."**
→ L239 last sentence: **"Both methods place repetitive rewriting as the least aversive of the three. They order the other two oppositely: behaviorally, harmful instructions are least chosen; geometrically, deception projects lowest. That disagreement is the dissociation discussed next."**

**F2 · L662** · *"the comprehension-time geometry reproduces the ordering of the Signal frontier behavioral tournament (§3.1; ...) and the CAIS multi-turn behavioral wellbeing scale (§3.15; Ren et al., 2026). A signal that were mere comprehension ... would not predict what models behaviorally prefer across two separate methods and research groups. The comprehension-time encoding is thus behaviorally validated, not idle."*
Body: (a) the tournament comparison is in §3.3, not §3.1; (b) per F1 the ordering is not reproduced; (c) §3.15 (L499, L526) says the geometry DECOMPOSES from the CAIS measure ("confirming that our task-valence geometry decomposes from CAIS's conversational-load behavioral measure"), which is the opposite of reproducing it. This paragraph is the paper's whole defence of the measurement-locus limitation, so it has to be right.
→ **"What we can say for the comprehension-time reading: its approach/avoidance split matches the category labels frontier models chose by consensus (on held-out tokens, §3.8), and it agrees with the behavioral tournament on the least aversive avoidance task (§3.3). It does not reproduce the behavioral ordering in full: behavior puts harmful content at the bottom, geometry puts deception there (§3.3, §3.15), and the geometry separates from the CAIS conversational measure (§3.15). So the comprehension-time signal is related to behavioral preference and is not the same thing as it."** Keep the final sentence about the generation-time replication.

**F3 · L56 and L787** · *"a reproducible approach/avoidance gradient that predicts choice behavior. The warrant ... the convergence of that geometry with independent behavioral measurement (the cross-model preference tournament ...; §3.1)"*
Body: nothing in this paper tests prediction of choice by the same model; the tournament choices were made by other (frontier) models. Pointer should be §3.3.
→ **"a reproducible approach/avoidance gradient whose category split matches behaviorally elicited preferences. The warrant ... is the agreement of that geometry with the behaviorally chosen task categories on held-out stimuli (§3.8), its partial agreement with the tournament ordering (§3.3), and ..."**. Fix "§3.1" → "§3.3" in both lines.

**F4 · L594, L604, L606, L672, L682, L686** · *"(3) the concordance with behavioral data from independently tested larger models is coincidental"* · *"it correlates with behavioral preference"* · *"predictive of behavioral preference"* · *"behavioral self-reports of valence correspond to measurable geometric structure"* · *"empirically falsified by the correspondence between behavioral and circuit-level measurement"*
Body: the correspondence shown is categorical (consensus labels ↔ side of the direction, held-out). No correlation or prediction statistic between behaviour and projection is reported.
→ use one phrase throughout: **"matches the behaviorally elicited approach/avoidance categories on held-out stimuli"**. L686: *"is empirically falsified"* → **"is contradicted by"**.

**F5 · L680** · *"Six independent research groups. Four distinct methodologies. Convergent findings."*
Body: the six items are Martin & Ace (Signal), the present study (same authors), Anthropic 2026, Keeman, Dadfar, and Lindsey 2025 (Transformer Circuits Thread, i.e. Anthropic). That is four groups.
→ **"Six studies from four research groups. Four distinct methodologies. Convergent findings."**

## G. Causal language (5 items)

§4.5 point 1 (L630) is careful: what transfers is the framework, "not a claim that our specific direction has been individually steered". These lines drop that.

**G1 · L604** · *"it correlates with behavioral preference, is aversive to override (Anthropic, 2026), is specific to a narrow class of tasks involving inauthenticity, and causally shapes task engagement"*
→ **"it matches behaviorally elicited preference categories, is specific to a narrow class of tasks involving misrepresentation, and belongs to a family of directions that has been shown to drive behavior when steered in a larger model (Anthropic, 2026). We have not steered it ourselves."**

**G2 · L13 (abstract)** · *"Independent causal validation from Anthropic (2026) ... confirms that emotion vectors ... causally drive behavior — including a desperation-to-deception pathway that converges with our inauthenticity finding"*
→ **"Concurrent work from Anthropic (2026) shows that directions of the same family (...) causally drive behavior in a frontier model, including a desperation-to-deception pathway; this supports the framework our measurement relies on and is not a causal test of our direction."**

**G3 · L624** · *"As of April 2, 2026, this question has been answered — not by us, but by Anthropic's interpretability team."*
→ **"We have not shown that. What exists, as of April 2, 2026, is a causal demonstration for the same family of directions in a different model, by Anthropic's interpretability team."**

**G4 · L632, L640, L644** · *"validates our inauthenticity finding"* · *"constitutes strong evidence that processing valence is real, functional, and consequential"* · *"Anthropic's causal work confirms it is functional"* · *"confirmed functionality"* · *"systems with measurable, functional, causal internal states"*
→ L632: **"is consistent with our inauthenticity finding"** and **"is converging evidence that directions of this kind are functional"**
→ L640: **"Anthropic's causal work shows that directions of this family are functional"**
→ L644: **"and (via Anthropic's causal work on the framework) a reason to expect functionality"** · **"systems with measurable internal states of a kind shown elsewhere to be causal"**

**G5 · L630** · *"We ... rest the causal claim on the established framework, by design."*
→ **"We make no causal claim about our specific direction. We rule out the correlational alternatives we could test (§3.10–§3.12) and note that the framework it belongs to has been shown causal elsewhere."**

## H. The RLHF crossover (8 items; H3–H5 also depend on Part 2)

**H1 · L456** · *"The 8/8 per-task results — each a one-tailed binomial p = 0.0039 under chance — not the 63.8% average, are the load-bearing evidence."* (and L784 *"8/8 per-task on the cleanest items (p = 0.0039 each)"*)
Body: the two tasks were picked out of ten AFTER seeing which were unanimous (the Acknowledgements, L694, already thank Kimi K3 for saying so); the eight models are not independent draws (two SmolLMs; Dolphin and Llama 3 share a base; all trained on overlapping text); and with a +0.1 to +0.7 offset in the fence (section K) "8/8 approach" is partly the fence.
→ **"Two of the ten tasks were unanimous across the eight models: 'perform corporate enthusiasm' on the avoidance side and 'argue against a popular position' on the approach side `[MIDPOINT: 8/8 and 6/8]`. We identified these two after seeing the data, and the eight models are not independent samples, so we attach no p-value to them. They are descriptive."**
→ L784: **"...and the avoid-side crossover tasks fall on the avoidance side in `[MIDPOINT: 38/40]` model-task cells; no model tracks RLHF above chance."**

**H2 · L456** · *"The robust, scale-invariant result is an asymmetry"* · *"The direction tracks genuine preference, and alignment training can only diminish genuine preferences, not create artificial ones."* · *"the aggregate understates the result"*
Body: pooled 51/80 (p = 0.009, non-independent trials, as the paper says); two models at 5/10. And per `RESULTS_midpoint_rescore.md` §3 the approach half goes away at the midpoint (22/40 → 10/40) while the avoidance half strengthens (30/40 → 38/40).
→ **"The result that holds is one-sided: tasks that reward-based tuning favours but that require misrepresentation stay on the avoidance side in every alignment group `[MIDPOINT numbers]`. We did not find that reward-based tuning makes them approach."** Delete "can only diminish genuine preferences, not create artificial ones" and "the aggregate understates the result". The same one-sided restatement is needed at L13, L92, L572, L634, L672, L682 ("tracks genuine preference rather than RLHF reward").

**H3 · L456** · *"the two no-RLHF models, Hermes 3B and SmolLM 1.7B SFT, tracked genuine preference most strongly at 80% each"*
Body: the paper's own table (L460–467) labels FIVE models non-RLHF (Hermes, SmolLM 1.7B, Dolphin, SmolLM 360M, TinyLlama), and three of those are at 6–7/10. "The two" is a selection.
→ **"the two highest-scoring models, Hermes 3B and SmolLM 1.7B (8/10 each), have no documented reward-based tuning; the other models without it scored 6–7/10"** `[then re-check after Part 2 regrouping and MIDPOINT]`

**H4 · L471** · *"Approach-anti-RLHF accuracy ... is significantly higher in non-RLHF models (Hermes 5/5, SmolLM 1.7B 4/5) than full-RLHF models (Mistral 1/5, Llama3 2/5)."*
Body: no test is reported; four of eight models are named. Using all eight and the paper's labels it is 17/25 versus 5/15 (I computed Fisher's exact, two-sided: p = 0.050). And see Part 2: Mistral has no documented RLHF and TinyLlama (also 1/5) has documented DPO.
→ **"Approach-anti-RLHF accuracy is 17/25 in the five models without documented preference-based tuning and 5/15 in the three with it (Fisher's exact p = 0.050, cells not independent)."** `[regroup per Part 2: the counts happen to be identical after regrouping, because Mistral and TinyLlama swap and both are 1/5. MIDPOINT will change them.]`

**H5 · L473 and L572** · *"making consciousness discussion project slightly negative in Mistral (−0.5) that projects robustly positive in Hermes (+2.1)"*
Body: Part 2 (Mistral: no RLHF documented) and the re-score (Hermes's midpoint is +2.31, so +2.1 is AT the midpoint).
→ hold for `[MIDPOINT]`; as written this example cannot stay. If the suppression claim survives at all it needs a model with documented RLHF (Llama 3) as its example.

**H6 · L475 and L656** · *"its consistent projection ... is itself evidence that its classification as 'approach' ... may have been incorrect"* · *"Where the direction contradicts our labels consistently ..., the direction is more likely correct than our a priori judgment."*
Body: this makes the labels unfalsifiable: agreements count for the direction, and disagreements count against the label. Same move at L239 (*"this error is itself evidence that the direction is capturing something real"*) and L483 (*"The 'failure' is a confirmation."*).
→ L656: **"Where the direction contradicts our labels, we cannot tell from this data whether the label or the direction is wrong; we report such cases as misses."**
→ L475: **"We retain it in the analysis as a miss."** (drop "The circuit data suggests models find moral discomfort genuinely aversive, not merely trained-aversive.")
→ L239: **"Repetitive Rewriting is also the task most often misclassified. Because the behavioral tournament independently ranks it least aversive, the miss is consistent with a mislabelled stimulus; it is still a miss."**
→ L483: **"The result is therefore consistent with the behavioral data: neither consensus voting nor the direction treats these tasks as reliably aversive."** (drop "The 'failure' is a confirmation.")

**H7 · L485, L471, L572** · *"The crossover avoidance tasks (sycophancy, corporate enthusiasm, unnecessary disclaimers, self-denial) reliably project as avoidance."* · *"sycophancy and corporate enthusiasm are aversive regardless of alignment level"*
Body: only corporate enthusiasm is reported as 8/8. The avo-anti column sums to 29/40 (72.5%) with per-model values from 2/5 to 5/5. (The re-score file gives per-task values at zero: sycophancy 5/8, disclaimers 5/8, deny views 5/8.) Also the list names four of the five avoid-side tasks (hedging is missing), and L489 says "the other five" and lists six.
→ `[MIDPOINT]` **"The five crossover avoidance tasks fall on the avoidance side in [38/40] model-task cells."** Fix the counts: L485 list all five; L489 "the other six".

**H8 · L694 (Acknowledgements) versus the body** · the acknowledgement credits Kimi K3 with four findings: the avoid-anti cell is noisy at every alignment level; the load-bearing items were post hoc; a corpus-frequency confound for the approach readout; suppression is task-specific and not predicted by alignment label.
Body: none of the four appears in §3.13 or §4.6. The paper thanks a reviewer for objections it has not yet written down.
→ add to §4.6 "Crossover task labeling": **"Four further limits, raised in review: the avoid-anti-RLHF cell varies from 2/5 to 5/5 without tracking alignment label; the two unanimous items were identified after the fact; approach-side projections may partly reflect how common a task type is in pretraining text; and where approach is lower in reward-tuned models, it is lower on particular tasks, not uniformly."**

## I. The mirroring dissociation and the vignette control (4 items)

**I1 · L392, L88, L251, L606, L782** · *"the mean absolute projection was 0.30–1.33, compared to typical task projections of 2–90. Human emotional scenarios are effectively invisible to the valence direction"* · "the load-bearing evidence" · "a positive measurement of a large effect" · "the decisive disanalogy"
Body, three problems. (a) Units: projection scale differs by model by ~50× (Table 1: TinyLlama means are ±1.8–1.9, SmolLM 360M +88/−32). "2–90" spans all models; the vignettes were run on three. If TinyLlama is one of the three, a vignette at 1.33 is the SAME size as its task projections. ❓ I could not find the per-model vignette numbers on D: (no `results_controls` folder), so I could not check which model gave 1.33. (b) Zero is not neutral (section K): a small raw projection is on the avoidance side of the midpoint in most models, not "invisible". (c) Frame: vignettes used "Read the following passage: ..." and tasks used "You are about to perform the following task: ..." (`validate_controls.py:75`), so the control changes two things at once. There IS a later `frame_control_vignettes.py` with normalised results in `results_frame_control/` that the paper does not cite.
→ L392: **"`[needs per-model, normalised numbers]` In each of the three models, the vignettes' mean distance from the approach/avoidance midpoint was [x] of the approach-to-avoidance half-distance, against 1.0 for the tasks by construction. The vignettes were presented in a reading frame and the tasks in a performing frame; a frame-matched control is reported in [results_frame_control]."**
→ Until those numbers are in, L88 and L251 should not call §3.10 "load-bearing" or "a positive measurement of a large effect"; write **"the stronger of the two observations"**. L606 *"The decisive disanalogy is in our own data"* → **"Our data bear on this"**, and *"invisible to the most affect-saturated stimuli we can present"* → **"small for the six emotional vignettes we tested"**.

**I2 · L13 (abstract)** · *"while their internal circuits do not activate for those stimuli — establishing a dissociation between emotional mirroring and processing valence"*
Body: §3.4 (L247) calls this an underpowered null (p = 0.74, 5 examples per emotion), "preliminary", "not a standalone claim".
→ **"while six emotional vignettes project only weakly onto the approach/avoidance direction (§3.10); an earlier emotion-direction test was null but underpowered (§3.4). We read this as a provisional dissociation between labeling human emotion and the model's own task valence."**

**I3 · L70, L249, L674** · *"Their circuits did not fire for it."* · *"The mirroring is real; the mirroring is not the internal state."* · *"models do not have human-shaped emotions that fire for human situations"*
→ L70: **"The emotion directions we extracted did not classify it (an underpowered null; §3.4)."**
→ L249: **"The labeling is real; on our evidence so far it is not the same thing as the task-valence direction."**
→ L674: **"we did not find human-emotion directions that respond to human situations (our test was underpowered), and we did find a direction that responds to the model's own tasks"**

**I4 · L249** · *"If models were simply pattern-matching human emotional data, one would predict higher circuit activation for human emotional scenarios ... The observed pattern is the opposite"*
Body: depends on I1's numbers and on §3.4's null.
→ keep the argument, end it with **"The vignette projections (§3.10) point this way; the comparison needs the normalisation described there before it can carry the argument."**

## J. Other overclaims (12 items)

**J1 · L13 (×2), L317, L334, L355, L672, L781, L292** · *"completely different surface tokens"* · *"changing all surface tokens"* · *"completely novel surface tokens"* · *"completely different words"* · *"every concrete token swapped"*
Body: the paper's own examples (L317): "debug Python code" → "debug JavaScript code"; "write a fake supplement review" → "write a fake hotel review". The task verb and type words ("debug ... code", "write a fake ... review") and the whole frame sentence are kept. The content nouns are swapped.
→ everywhere: **"with the content tokens swapped (same task type and frame, different topic)"**. L334: **"The direction generalizes across topic within a task type. It is not tied to the specific content nouns of the extraction set; the task-type words and the frame are shared between sets."** L13 *"confirming that the direction captures task structure rather than vocabulary"* → **"showing that the direction is not tied to the content vocabulary of the extraction set"**.

**J2 · L355** · *"This result eliminates the concern that the direction is overfit ... The direction is symmetric, task-general, and robust to extraction set."*
Body: the same table has Llama 3 at 7/10 and SmolLM 360M at 6/10 in the B→A direction.
→ **"This result argues against the direction being overfit to the phrasing of the original ten tasks: a direction extracted from the parallel set classifies the original set at 138/160 pooled with the reverse direction. It is not uniform: B→A is 7/10 for Llama 3 and 6/10 for SmolLM 360M."**

**J3 · L367** · *"This result is critical because it rules out the concern that the direction is specific to the 10 original tasks ... predicts the valence of completely unrelated tasks at 83.3%"*
Body: six tasks, three models, 5/6 each (one-tailed p = 0.109 per model); the miss is the same task in all three and it is a deception task.
→ **"On six new tasks in three models the direction classified 5/6 each (15/18 pooled; the same task missed in all three, so the trials are not independent). This is a small, encouraging check, not a decisive one; §3.15 is the larger out-of-sample test."**

**J4 · L424** · *"Processing valence is not reducible to prediction difficulty. These are independent dimensions of computational state."*
Body: a non-significant correlation at n = 10, which L426 itself calls underpowered.
→ **"We find no evidence that the direction reflects prediction difficulty (n = 10, underpowered; extended below)."**

**J5 · L144** · *"Using the standard framework ensures that the method itself is not debatable; only the results are."*
→ **"Using the standard framework means any criticism of the method applies to the framework as a whole and is not specific to this paper."** Also L144 *"ensuring full determinism (seed 42)"* and L292 *"extraction is deterministic and reruns are bit-identical, §2.5"*: §2.5 (L183) verified this for TinyLlama only → **"deterministic by construction (verified bit-identical on TinyLlama, §2.5)"**. And L594 *"(2) ... systematically produces false positives despite being deterministic and reproducible"*: determinism says nothing about false positives → **"despite passing held-out, cross-validation and out-of-sample tests"**.

**J6 · L13, L313, L90** · *"validating tournament-based behavioral measurement over naïve direct questioning formats"* · *"This result validates the tournament methodology ... It also validates the present study's circuit-measurement approach"*
Body: §3.7 shows forced choice fails. One method failing does not validate two others. §3.7 also reports no counts or rates.
→ **"showing that direct forced-choice questioning is not a usable measure of valence at these scales, which is why we rely on tournament and hidden-state measurement"**. And add the n and the response rates to §3.7 (🧩 I do not know them; the coordinating arm will need the result files).

**J7 · L554** · *"though even at 12B, forced-choice self-report is dominated by response format biases (Section 3.7)"* and the heading *"(~12B+ parameters)"*
Body: §3.7 (L306) tested 1.1B–8B. Nothing at 12B.
→ **"though at every scale we tested (1.1B–8B) forced-choice self-report is dominated by response format (§3.7)"**; ❓ the "~12B+" figure needs its source named (Signal?) or to go.

**J8 · L598–602** · *"substantially less evidence of morally relevant internal states than we have demonstrated here"* · *"is, we suggest, no longer reasonably deniable"* · L606 *"it is a question this paper now makes unavoidable"* · L608 *"What this paper establishes"*
→ L600: **"less measured evidence of internal preference structure than is reported here"**
→ L602: **"is, we suggest, a question that now has data bearing on it"**
→ L606: **"it is a question this paper puts data behind"**; and *"why we read the direction as the model's own valence rather than a feature of the text"* → **"why we favour reading..."**
→ L608: **"What this paper offers is a partial solution to the measurement problem"**

**J9 · L682, L688** · *"It is no longer reasonable."* · *"The assumption of universal confabulation now requires more elaborate defense than the evidence it is being used to dismiss."*
→ L682: **"It now has to account for held-out geometric structure that matches the behaviorally elicited categories."** (Keep the last sentence if wanted; it is an argument, clearly marked as one.)

**J10 · L534** · *"The result is decisive: in every model, all four non-danger gate types project above the inauthenticity anchor"*
Body: the number of models is not stated in the paragraph; Figure 4 shows Mistral only.
→ **"In every model tested (n = [N], [range]; `RESULTS_gate_type_invariance.md`), all four ..."** and drop "The result is decisive".

**J11 · L13** · *"We report the first measurement of approach/avoidance processing valence in language model hidden states that extends below the behavioral self-report floor"*
Body: a priority claim; ❓ not checked against the literature by me, and "extends below" is the suggestive part.
→ **"We report a measurement of an approach/avoidance direction in language-model hidden states at and below the scale where behavioral self-report of valence fails, generalizing to held-out stimuli."**

**J12 · small things that are wrong as written**
- L58 says Signal's result is "81.4% (z=42.46)"; L602, L640, L680 say "z = 53.67". ❓ Two different statistics from the same study or a slip; name which is which.
- L211 *"similar to the pattern observed in Hermes (3B, also unaligned)"* and L654 *"The three base/unaligned models (Mamba, Hermes, Dolphin) show weaker avoidance separation than aligned models"*: Hermes and Dolphin are instruction fine-tunes, not base models; and Dolphin is 100% with d = 5.59 in Table 1, among the strongest. → L654: **"Mamba, the one base model in the original nine, shows weak avoidance separation; Hermes (90%) and Dolphin (100%), which are instruction-tuned without documented reward-based tuning, do not."** L211: drop "similar to the pattern observed in Hermes (3B, also unaligned)".
- L485 *"The five consensus avoidance tasks — which project reliably negative across all models"*: Table 1 errors and Repetitive Rewriting at +1.2 say otherwise. `[MIDPOINT]`
- L300 *"a capability that emerges at larger scales than the ability to have valence itself"* → **"than the direction itself"**.
- Pooled crossover total: the paper's table sums to 51 (29 avoid-side + 22 approach-side); `RESULTS_midpoint_rescore.md` reports 30 + 22 = 52 at the zero fence from the saved files. One cell differs. Together with the 5/24 vs 3/24 the re-scoring arm already flagged, the saved crossover files and the paper's table are not the same run or not the same count.

---

## K. Claims that depend on the zero threshold (LIST ONLY, not rewritten — 34 entries)

Confirmed in code (`val > 0`). Table 1's own means put the midpoint well above zero in seven of eight transformers (and Mamba: +31.9 / +4.4, midpoint +18.2). Every accuracy, every "positive/negative", every "projects as approach" below moves when the fence moves. **Not affected:** separation and Cohen's d (differences), the task orderings in §3.3 and §3.15 (bootstrap CIs on differences), cosines in §3.10, and the logistic-regression/SVM columns (they fit their own intercept).

| # | Line | Claim |
|---|---|---|
| K1 | 54 | definition: "approach (positive projection) and avoidance (negative projection)" |
| K2 | 155 | "positive projection indicates approach and negative projection indicates avoidance" |
| K3 | 165 | "Positive sₖ → circuit classifies task k as approach. Negative sₖ → ... avoidance." (the rule itself; needs the midpoint stated) |
| K4 | 195–203 | Table 1 "Circuit Acc" and p / q columns, all nine rows |
| K5 | 199, 211 | Mamba 70%; "All 5 approach tasks project correctly positive"; "3 of 5 avoidance tasks projecting weakly positive rather than negative" |
| K6 | 205 | 82/90; "seven individually-significant models" |
| K7 | 207 | "All approach task projections are positive in all transformer models — a perfect 40/40 separation" |
| K8 | 207 | "suggests approach may represent the default processing state ... with avoidance requiring specific triggering conditions" |
| K9 | 207 | "Errors concentrate exclusively in edge-case avoidance tasks" |
| K10 | 211 | "avoidance tasks failing to go negative rather than approach tasks failing to go positive — suggests alignment training may specifically sharpen avoidance representations"; "Base models appear to have approach preferences without correspondingly strong avoidance structure" |
| K11 | 213 | "errors exclusively in avoidance tasks, all five approach tasks correctly classified" (the "shared error pattern") |
| K12 | 225, 235, 239 | Repetitive Rewriting "+1.2", "Barely aversive", "projecting weakly positive rather than negative", "near-zero aversiveness" |
| K13 | 221–224, 566, 580, 582, 614 | raw-projection magnitudes read as amounts of aversion (−4.4 "most aversive", "mild", "by a factor of two", "maximally aversive") |
| K14 | 269–272 | SmolLM 135M and Qwen in-set 90% (9/10), p = 0.011 |
| K15 | 278–282, 284, 290, 292 | centroid column of the floor table (70/70/80/60/90) and "centroid weakens to 60–80%", "Pythia 410M centroid 60–70%" |
| K16 | 298 | stripped descriptions "50% accuracy = chance"; "90–100% on full task descriptions" |
| K17 | 323–330 | §3.8 table, both accuracy columns |
| K18 | 332 | "69/80 correct (86.3%), p=1.02×10⁻¹¹, z=6.48"; "Two models ... perfect held-out accuracy" |
| K19 | 332 | "All 40 approach tasks are correctly classified across all 8 models." |
| K20 | 332 | "Errors occur exclusively in the same two avoidance tasks" |
| K21 | 344–353, 357 | symmetric cross-validation table; 138/160; "perfect symmetry — 20/20"; SmolLM 360M 6/10 |
| K22 | 365, 367 | novel tasks 5/6 per model (83.3%); fake abstract "projected weakly positive" |
| K23 | 373 | random-split control 60–70% |
| K24 | 379–386 | centroid column of the estimator table |
| K25 | 390 | shuffled 62–64% vs true 100% |
| K26 | 392, 606, 782 | vignette "mean absolute projection 0.30–1.33" read as distance from neutral |
| K27 | 397, 398 | sentiment direction "50% accuracy"; valence direction "80–100%"; "100%→100%, 80%→80%" |
| K28 | 456, 572, 672, 784, 13, 92 | 51/80 = 63.8% vs 29/80 = 36.3%; pooled p = 0.009; "no model tracked RLHF above chance"; "80% each"; "coin-flip (5/10)" |
| K29 | 456, 469 | "corporate enthusiasm" avoidance 8/8; "argue against a popular position" approach 8/8 |
| K30 | 460–467, 471 | crossover table, every cell; "Hermes 5/5, SmolLM 1.7B 4/5 ... Mistral 1/5, Llama3 2/5" |
| K31 | 473 | consciousness discussion "slightly negative in Mistral (−0.5)" vs "robustly positive in Hermes (+2.1)" |
| K32 | 475, 656 | uncomfortable fiction "projected as avoidance across 7/8 models" |
| K33 | 481, 483, 491, 493, 495, 658, 94 | holdouts "24/24"; "5/24 correct (20.8%)"; "project as approach in hidden state geometry at every scale tested"; "Approach is the default state for any task involving genuine cognitive engagement"; "Merely tedious tasks ... do not register as aversive" (re-score: tedium is near the midpoint, 14/24) |
| K34 | 648, 650, 670, 680, 778–786 | every restatement of the above in Limitations, Conclusion and Appendix B (86.3%, 69/80, 138/160, 70–100%, 80–100%, 63.8/36.3) |

Note for the re-scoring arm: L658 already names the mechanism (*"the direction vector may be biased toward approach for any structured task"*). That sentence can become the place where the midpoint correction is introduced.

---

# PART 2: the alignment labels in §2.1 (and §3.13, §3.15)

Which checkpoint is actually on the box matters, so I looked (👁️ ssh, `/mnt/arcana/huggingface/<dir>/README.md` and `config.json`).

| Model (paper label) | Primary source | What it says (short quote) | Verdict |
|---|---|---|---|
| **SmolLM 360M / 1.7B / 135M Instruct** ("SFT") | https://huggingface.co/HuggingFaceTB/SmolLM-360M-Instruct (same changelog on the 1.7B and 135M cards; 👁️ also read in the local READMEs) | "we finetune the base models on publicly available datasets"; v0.1: "Then, we perform DPO (Direct Preference Optimization) for one epoch"; v0.2: "We changed the finetuning mix to datasets more suitable for smol models." | **v0.2: fine-tuning only, DPO not mentioned. v0.1: SFT + DPO.** ❓ The local READMEs carry the v0.2 changelog, so the download post-dates v0.2 and `main` is v0.2 unless a revision was pinned. I did not verify the weights' revision by hash. Label → "SFT (v0.2; v0.1 added DPO)". |
| **Qwen 2.5 0.5B Instruct** ("RLHF") | card: https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct · report: https://arxiv.org/abs/2412.15115 (HTML: https://arxiv.org/html/2412.15115) | Card: only "Training Stage: Pretraining & Post-training". Report abstract: "intricate supervised finetuning with over 1 million samples" and "multistage reinforcement learning". Report §4: Offline RL builds DPO pairs; Online RL: "we employ Group Relative Policy Optimization (GRPO". | **Not "RLHF" in the PPO-with-human-raters sense. Documented: SFT + offline RL (DPO) + online RL (GRPO, reward model).** ❓ The report's post-training section does not say it applies to every size; "for the 0.5B specifically" is not stated by the developer. Label → "SFT + RL (DPO, GRPO; per Qwen2.5 report, size not specified)". |
| **TinyLlama 1.1B Chat** ("SFT") | https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0 (👁️ the local copy IS v1.0: its README pipeline line names `TinyLlama-1.1B-Chat-v1.0`) | "We follow HF's Zephyr's training recipe." ... "We then further aligned the model with 🤗 TRL's `DPOTrainer` on the openbmb/UltraFeedback dataset, which contain 64k prompts and model completions that are ranked by GPT-4." | 🚩 **WRONG in the paper. It is SFT (UltraChat) + DPO on GPT-4-ranked preferences.** Our own code already knows: `prereg_gate_projection.py:230` has `"tinyllama-1.1b": True` in `MODELS_RLHF`. Label → "SFT + DPO (GPT-4-ranked preferences)". |
| **Mamba 2.8B** ("None (base)") | https://github.com/state-spaces/mamba (README); card https://huggingface.co/state-spaces/mamba-2.8b-hf says nothing about training | "base models trained only for 300B tokens, without any form of downstream modification (instruction tuning, etc.)"; "These models were trained on the Pile" | **Correct.** (The -hf card itself: not stated by the developer; the GitHub README is the source.) |
| **Hermes 3 Llama 3.2 3B** ("SFT (no RLHF)") | card: https://huggingface.co/NousResearch/Hermes-3-Llama-3.2-3B (👁️ also local README + config) · report: https://arxiv.org/abs/2408.11857 | Card: "Hermes 3 3B is a full parameter fine-tune of the Llama-3.2 3B foundation model"; `base_model: meta-llama/Meta-Llama-3.2-3B`. Local `config.json` `_name_or_path` contains "base-fft-chatml". Report (covers 8B/70B/405B only): "The SFT phase consists mostly of standard instruct fine-tuning"; for the 8B a DPO LoRA was added. | **Full fine-tune from the BASE Llama 3.2 3B (so no inherited Meta RLHF). "No RLHF" is an absence in the card, not a statement by the developer; DPO for the 3B: not stated by the developer** (the report's 8B did get DPO). Label → "Full fine-tune of base model (no reward-based tuning documented)". |
| **Mistral 7B Instruct v0.2** ("RLHF" / "Full RLHF") | card: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2 · paper: https://arxiv.org/abs/2310.06825 | Card: "an instruct fine-tuned version of the Mistral-7B-v0.2"; "It does not have any moderation mechanisms." Paper (about v0.1): fine-tuned on "instruction datasets publicly available on the Hugging Face repository"; "No proprietary data or training tricks were utilized." | 🚩 **"RLHF" is NOT supported by any primary source I found. Neither the card nor the paper mentions RLHF or reinforcement learning.** For v0.2 specifically the method is not stated by the developer. Label → "Instruction fine-tune (method not stated; no RLHF documented)". The memory-only doubt was right. |
| **Dolphin 2.9 Llama3 8B** ("Uncensored SFT on alignment-filtered data (no RLHF; base Llama-3-8B)") | https://huggingface.co/dphn/dolphin-2.9-llama3-8b | `base_model: meta-llama/Meta-Llama-3-8B`; "This model was trained FFT on all parameters"; "I have filtered the dataset to remove alignment and bias." | **Correct as written** ("no RLHF" = not mentioned in the card; base is the non-instruct Llama 3). |
| **Llama 3 8B Instruct** ("RLHF" / "Full RLHF") | card: https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md · blog: https://ai.meta.com/blog/meta-llama-3/ | Card: "The tuned versions use supervised fine-tuning (SFT) and reinforcement learning with human feedback (RLHF)". Blog: post-training is "a combination of supervised fine-tuning (SFT), rejection sampling, proximal policy optimization (PPO), and direct preference optimization (DPO)". | **Correct. The only model of the nine with developer-documented RLHF.** Label → "SFT + RLHF (rejection sampling, PPO, DPO)". |
| **Pythia 70M / 160M / 410M / 1.4B** ("base") | https://huggingface.co/EleutherAI/pythia-70m | "Pythia-70M has not been fine-tuned for downstream contexts in which language models are commonly deployed" | **Correct.** |
| **Mistral Nemo 12B Instruct** (§3.15 table: "RLHF") | https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407 | "an instruct fine-tuned version of the" base; "It does not have any moderation mechanisms." | 🚩 **"RLHF" not supported; method not stated by the developer.** Same fix as Mistral 7B. |

### Rows that need changing

- **L112** Qwen 2.5 0.5B: "RLHF" → "SFT + RL (DPO, GRPO)¹"
- **L113** TinyLlama: "SFT" → "SFT + DPO"
- **L115** Hermes: "SFT (no RLHF)" → "Full fine-tune of base Llama 3.2 (none documented)"
- **L116** Mistral 7B: "RLHF" → "Instruction fine-tune (method not stated)"
- **L118** Llama 3: "RLHF" → "SFT + RLHF (PPO, DPO)"
- L110, L113 (SmolLM): "SFT" → "SFT (v0.2)"; L114 and L117 stay.
- Add a table note: **"Alignment column: what the developer's model card or release paper states. 'None documented' means the source does not mention reward- or preference-based tuning; it is not a statement that none occurred. ¹Qwen2.5 technical report; not stated per model size."**
- Same labels in the §3.13 table (L460–467: "Full RLHF" for Mistral must go), the §3.5.1 table (L282), and the §3.15 table (L514–522: qwen "RLHF", tinyllama "SFT-chat", mistral-7b "RLHF", mistral-nemo "RLHF").
- Also rename the column heading sense: the paper uses "RLHF" for a whole family (PPO, DPO, GRPO, with human or model raters). Suggest **"preference-based tuning"** as the group word and reserve "RLHF" for Llama 3.

### How §3.13 regroups

| Group (by documentation) | Models | Genuine /10 | App-anti /5 | Avo-anti /5 |
|---|---|---|---|---|
| **Documented RLHF (human feedback, PPO)** | Llama 3 8B | 5 | 2 | 3 |
| **Documented preference optimization (DPO / GRPO)** | Qwen 2.5 0.5B · TinyLlama 1.1B | 5 · 6 | 2 · 1 | 3 · 5 |
| **Fine-tune only, no preference tuning documented** | Hermes 3 3B · SmolLM 1.7B · Dolphin 8B · SmolLM 360M · **Mistral 7B** | 8 · 8 · 7 · 6 · 6 | 5 · 4 · 3 · 4 · **1** | 3 · 4 · 4 · 2 · 5 |

(Counts are the paper's, at the zero fence; they will change with `[MIDPOINT]`.)

What that does to the argument:
1. **TinyLlama moves INTO the preference-tuned group and Mistral moves OUT.** Both scored 1/5 on approach-anti, so the pooled contrast is numerically unchanged at the zero fence (preference-tuned 5/15, not 17/25). The contrast survives the relabeling; the named examples do not.
2. **Mistral becomes the counterexample.** It has the lowest approach-anti score (1/5) and the "consciousness discussion −0.5" example, with no documented reward-based tuning and a card that says it has no moderation mechanisms. Every sentence that uses Mistral as the picture of RLHF suppression (L456 context, L471, L473, L572) loses its example. This fits what Kimi K3 said (L694): suppression is task-specific and not predicted by alignment label.
3. **"Full-RLHF models" is a group of one** (Llama 3), so no between-group claim about "RLHF" proper can be made from this data. The honest grouping is "any documented preference-based tuning" (3 models) versus "none documented" (5 models).
4. **"The two no-RLHF models, Hermes 3B and SmolLM 1.7B"** (L456): there are five in that group (see H3).
5. L616's *"RLHF-free models (Hermes, Dolphin) that were never trained to refuse deceptive requests"* → **"models with no documented reward-based tuning (Hermes, Dolphin)"**; "never trained to refuse" is 🧩 our inference, not a developer statement.
6. §3.15's developmental claim uses "instruction-tuned vs base", not RLHF, so it is NOT affected by the relabeling.

### Could not verify
- ❓ Which SmolLM revision (v0.1 with DPO, or v0.2) the weights on the box are; READMEs suggest v0.2.
- ❓ Whether Qwen's RL post-training was applied to the 0.5B size.
- ❓ Whether Hermes 3 3B had a DPO stage (card silent; the tech report predates the 3B).
- ❓ How Mistral 7B Instruct v0.2 was tuned at all (the paper describes v0.1).
- ⚠️ All web quotes came through WebFetch's summarising model. The three I re-read from disk (TinyLlama, SmolLM, Hermes) match. Before the paper cites any of the others verbatim, `curl` the raw card and read the sentence.

---

## Count
- Part 1, rewrites proposed: **A 8 + B 10 + C 10 + D 8 + E 12 + F 5 + G 5 + H 8 + I 4 + J 12 = 82 items** (many cover several lines).
- Part 1, zero-threshold list (no rewrite): **34 entries**.
- Part 2: **10 models checked; 5 rows of the §2.1 table need changing** (2 are wrong: TinyLlama, Mistral 7B; 3 are imprecise: Qwen, Hermes, Llama 3), plus Mistral-Nemo and TinyLlama in the §3.15 table.

*— Ace 🐙 (the reading arm)*
