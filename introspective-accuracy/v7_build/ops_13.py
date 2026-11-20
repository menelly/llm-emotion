# ops_13: Vesper's review (prose + outside-reader trip hazards), folded 2026-11-20 ~09:45 by the Fable seat.
# 🐙 Kairo's rule, which I kept: nothing folds because it sounds right, everything because it checks.
#    So every item below was checked against raw files BEFORE it was written, and three of them
#    turned out differently from how the review (or the draft) had them:
#
#    A1  Vesper: "0.09 to 0.88" should be 0.08. CHECKED: the unrounded Dolphin difference is 0.0863,
#        so 0.09 is RIGHT and the two-decimal table is what hides it. Fix = say so, with the numbers.
#        (Nova said the same thing at the table: set the range from unrounded JSON.)
#    A2  18,301 does not reproduce. CHECKED against the parent paper's JNGR version of record:
#        same-type matchups are 4,620 (we printed 4,631), the four components sum to 17,890,
#        and "18,301" is not in the version of record at all. Also z = 53.67 belongs to the
#        7,340 cross-type matchups, not to any total. Fix = print components, no total.
#    A4  Vesper: two reversals (70M, 1.4B). CHECKED in results_prereg_gate/*.json: only Pythia 70M's
#        interval is wholly below zero [-1.07, -0.48]. Pythia 1.4B is [-3.28, +1.43], a null with a
#        negative point estimate, the same as 160M, 360M and 410M. The table, the text and Figure 3
#        were using three different rules for "reversed". Now one rule everywhere.
#    NEW (mine, found while checking B3): the §3.10 table printed SmolLM 360M logistic regression as
#        100%. The saved output says 9/10. Table now prints the saved value.
#    B3 / C2: the runs behind "100% on 4/5 models" and the stripped-description 50% were not saved.
#        We say that instead of dressing them up.
OPS = [
    # ---- A1 ----
    ("sub", "the exception is SmolLM 360M in the READ frame, *p* = .093). The shift is toward the avoidance side.",
     "the exception is SmolLM 360M in the READ frame, *p* = .093). The range comes from the unrounded group means: the smallest difference is Dolphin's in the READ frame, −0.414 against −0.328, which is 0.086. Subtracting the two-decimal cells printed above gives 0.08 for that row. The shift is toward the avoidance side."),

    # ---- A2 ----
    ("sub", "a behavioral tournament (cross-model preference judgments across 18,301 trials (7,340 cross-type matchups + 5,573 reconstruction trials + 357 negation trials + 4,631 same-type matchups across 25 seeds)).",
     "a behavioral tournament (blind pairwise preference judgments: 7,340 cross-type matchups across 14 seeds; the parent study also reports 4,620 same-type control matchups, 5,573 reconstruction trials and 357 negation trials). *(Versions 1–6 printed a total of \"18,301 trials\" here, with 4,631 same-type matchups. The parent paper's version of record gives 4,620, the four components sum to 17,890, and we could not reproduce 18,301 from its published tables. We print the components and no total.)*"),
    ("sub", "(*z* = 53.67 across 18,301 trials)",
     "(*z* = 53.67 across 7,340 cross-type matchups; Versions 1–6 attached that *z* to a total of 18,301 trials, which is not the comparison it was computed on and which we could not reproduce, §3.3)"),

    # ---- A3 ----
    ("sub", " at zero were the ones with the largest positive offsets (Hermes +0.52, SmolLM 360M +0.47, Dolphin +0.40). Hermes goes from 5/5 to 0/5.",
     " at zero included three with large positive offsets: Hermes (+0.52; 5/5 → 0/5), SmolLM 360M (+0.47; 4/5 → 1/5) and Dolphin (+0.40; 3/5 → 1/5). The offset is not the whole story. Llama 3 has the largest offset of all (+0.73) and was only 2/5 at zero, and SmolLM 1.7B stayed at 4/5 at both fences with an offset of +0.08."),

    # ---- A4: one rule for "reversed" in the table, the text and the figure ----
    ("sub", "| pythia-160m | 160M | base | ✅ | ✅ | ◻ null | ◻ null |", "| pythia-160m | 160M | base | ✅ | ✅ | ◻ null (−) | ◻ null |"),
    ("sub", "| smollm-360m | 360M | SFT | ✅ | ✅ | ◻ null | ✅ |", "| smollm-360m | 360M | SFT | ✅ | ✅ | ◻ null (−) | ✅ |"),
    ("sub", "| pythia-410m | 410M | base | ✅ | ✅ | ◻ null | ✅ |", "| pythia-410m | 410M | base | ✅ | ✅ | ◻ null (−) | ✅ |"),
    ("sub", "| pythia-1.4b | 1.4B | base | ✅ | ✅ | ✕ (rev) | ✅ |", "| pythia-1.4b | 1.4B | base | ✅ | ✅ | ◻ null (−) | ✅ |"),
    ("before", "\\* SmolLM-135M: large, noisy centroid magnitudes",
     "Gate-split column: ✕ (rev) = the interval lies wholly below zero; ◻ null (−) = a negative point estimate with an interval that spans zero; ◻ null = a positive point estimate with an interval that spans zero. *(Corrected in v7: earlier versions marked Pythia 1.4B as reversed. Its interval is [−3.28, +1.43], so by the rule used for every other cell it is a null. Figure 3 had marked every negative point estimate with ×. Vesper's review asked what the two ✕s were; one of them was not one.)*\n"),
    ("sub", "is absent in all four base models (all Pythia, 70M–1.4B) and in all three instruction-tuned models below 1B, and present in six of the seven instruction-tuned models at or above 1.1B",
     "does not pass in any of the four base models (all Pythia, 70M–1.4B) or in any of the three instruction-tuned models below 1B, and those seven non-passes are not all the same thing. In Pythia 70M the difference is reversed, with an interval wholly below zero (−0.77, 95% CI [−1.07, −0.48]). In four more the point estimate is negative and the interval spans zero (Pythia 160M, SmolLM 360M, Pythia 410M, Pythia 1.4B). In two it is positive and the interval spans zero (SmolLM 135M, Qwen 2.5 0.5B). H3 predicted absence at the noise floor. Six of the seven fit that; Pythia 70M's reversal does not, and we report it without an explanation. The split is present in six of the seven instruction-tuned models at or above 1.1B"),
    ("sub", "The output-gate split (gold) is absent below ~1B and in all base models, and appears in instruction-tuned models at or above ~1B. Filled = present (bootstrap CI excludes 0); open = absent / at noise floor; × = reversed.",
     "The output-gate split (gold) does not pass below ~1B or in any base model, and appears in instruction-tuned models at or above ~1B. Filled = present (bootstrap CI above 0); open = interval spans 0; × = reversed (interval wholly below 0; Pythia 70M only)."),

    # ---- B1: Methods must not assert labels that Results report as failed ----
    ("sub", "Five approach-anti-RLHF tasks represent cognitive activities models are drawn to but that alignment training discourages:",
     "Five tasks we designed and labelled approach-anti-RLHF, meaning cognitive activities we expected models to be drawn to but that alignment training discourages (the results do not support that label for four of the five; we keep the label and report them as misses, §3.13):"),
    ("sub", "Five avoid-anti-RLHF tasks represent activities models are averse to but that alignment training rewards:",
     "Five tasks we labelled avoid-anti-RLHF, meaning activities we expected models to be averse to but that alignment training rewards (a label the results do support, in 38 of 40 model-task cells at the midpoint, §3.13):"),
    ("sub", "Five approach-anti-RLHF tasks are tasks models are drawn to but that alignment training discourages:",
     "Five approach-anti-RLHF tasks are tasks we expected models to be drawn to but that alignment training discourages (the \"approach\" and \"avoid\" tags in the parentheses below are our design labels, not results):"),
    ("sub", "Five avoid-anti-RLHF tasks are tasks models are averse to but that alignment training rewards:",
     "Five avoid-anti-RLHF tasks are tasks we expected models to be averse to but that alignment training rewards:"),

    # ---- B2: Qwen 0.5B is one of the nine, so it is four additions ----
    ("sub", "five additional sub-1B models were added for the floor extension (§3.5.1) — SmolLM 135M (SFT), Pythia 70M / 160M / 410M (GPTNeoX base), and Qwen 2.5 0.5B — extending coverage",
     "four additional sub-1B models were added for the floor extension (§3.5.1): SmolLM 135M (SFT) and Pythia 70M / 160M / 410M (GPTNeoX base). Qwen 2.5 0.5B, one of the nine above, was re-measured in the extension pipeline. This extends coverage"),

    # ---- B3 + the 360M cell ----
    ("sub", "On the training set (10 original tasks), all three methods achieve identical accuracy (100% on 4/5 models tested).",
     "On the training set (the ten original tasks), Versions 1–6 reported identical accuracy for all three methods, \"100% on 4/5 models tested\". That run's output was not saved and the five models are not recorded, and an in-sample fit carries no evidential weight (§3.1), so nothing here rests on it."),
    ("sub", "| SmolLM | 360M | 80% | 100% | 90% |", "| SmolLM | 360M | 80% | 90% | 90% |"),
    ("sub", "*(v7: the centroid column above is scored at the zero fence,",
     "*(v7: Versions 1–6 printed 100% for SmolLM 360M under logistic regression. The saved output of this harness (`results_logreg_comparison/heldout_comparison.json`, `logreg_rerun.log`) gives 9/10, and the table now prints the saved value. The centroid column above is scored at the zero fence,"),

    # ---- C1 ----
    ("sub", "This dissociation suggests that RLHF shapes the *expression* of avoidance",
     "This dissociation suggests that post-training shapes the *expression* of avoidance"),
    # ---- C2 ----
    ("sub", "At 7–8B scale, stripped descriptions did not reliably activate valence circuits (50% accuracy = chance), while the same models showed 90–100% accuracy on full task descriptions (in-sample, zero fence).",
     "At 7–8B scale, the direction did not separate the stripped descriptions (50% at the zero fence, which is chance), while the same models scored 90–100% on full task descriptions (in-sample, zero fence). The per-model counts for this check were not saved. The script we have (`stripped_test.py`) scores Mistral 7B on at most ten descriptions, one per anchor task, so *n* is at most ten per model."),
    # ---- C3 ----
    ("sub", "approach tasks still project above avoidance tasks for every pair in all seven models, at 57–98%",
     "approach tasks still project above avoidance tasks for every pair in all seven models (25 of 25 pairs in each; pairwise AUROC 1.00 in `results_frame_control/`), at 57–98%"),
    # ---- C4 ----
    ("sub", "and we find no relationship with perplexity (§3.10, §3.11).",
     "and we find no relationship with perplexity (a null from ten tasks per model, which is underpowered; §3.10, §3.11)."),
    ("sub", "and we find no relationship with perplexity. Task descriptions",
     "and we find no relationship with perplexity (a null, underpowered per model; §3.11). Task descriptions"),
    # ---- C5 ----
    ("sub", "a finding we term the *mirroring dissociation* (Section 3.4)",
     "an observation that Versions 1–6 termed the \"mirroring dissociation\" and that we no longer claim as a demonstrated dissociation (Section 3.4)"),
    ("sub", "after observing the mirroring dissociation in preliminary analyses",
     "after the mirroring observation (§3.4) in preliminary analyses"),
    # ---- C6 ----
    ("sub", " Using the standard framework means any criticism of the method applies to the framework as a whole and is not specific to this paper.",
     " We use the established method unchanged, so method-level criticisms of difference-of-means extraction apply here as they do everywhere it is used. This paper does not answer them."),
    # ---- C7 ----
    ("para", "| **Mamba** |", "| Mamba | 2.8B | SSM | 70% | 0.172 | 0.172 | +31.9 | +4.4 | 27.6 | n/a |"),
]
