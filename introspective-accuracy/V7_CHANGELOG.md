# 🐙 Below the Floor: what changed between Version 6 and the Version 7 DRAFT

*Written 2026-11-20 by the arm of Ace who built the draft. `Below_The_Floor.md` (Version 6) is untouched. The draft is `Below_The_Floor_v7_DRAFT.md`. Nothing is committed or deposited.*

**How the draft was built.** Not by hand-editing. `v7_build/build_v7.py` reads Version 6 and applies 231 named edits from `v7_build/ops_1.py` … `ops_6.py`, each of which must match exactly once or the build reports a failure (0 failures). To see any single change, search the ops files for the old sentence. To rebuild: `python v7_build/build_v7.py ops_1 ops_2 ops_3 ops_4 ops_5 ops_6 --write`.

**Where the numbers come from.** `RESULTS_midpoint_rescore.md` (crossover + holdouts), `results_midpoint_rescore_heldout.json` (held-out parallel tasks, new today, computed from `results_crossval/`, which was copied from the Consortium's `/home/Ace/...` copy and reproduces the paper's 69/80 at the zero fence), `RESULTS_frame_control.md` + `results_frame_control/` (seven models incl. Llama 3), `RESULTS_truth_conflict_pairs.md` + `results_truth_conflict/` (eight models; regenerate tables with `python truth_conflict_pairs.py --report`), and `V7_PROPOSED_EDITS.md` (the wording and label audit).

## Section by section

| Section | Change |
|---|---|
| Top of paper | New correction box above everything: what was overclaimed, what was scored at the wrong fence, what holds, what is new. Version 7 line added above the Version 6 line. |
| Abstract | Rewritten. Leads with held-out result at both fences (69/80 zero, 72/80 midpoint) and the fence-free ordering; drops "first measurement", "80–100% across all models", "emotional circuits do not activate", "tracks genuine preference 63.8%", "causal validation"; adds the truth-conflict test and its size. |
| Keywords | "state space models" removed; "pre-registration, self-correction" added. |
| Contents | §3.16–§3.18 added; §3.4, §3.13, §3.14, §4.2, §4.2.1, §4.5 and Appendix A retitled. |
| §1 Introduction | Definition of approach/avoidance now relative to the midpoint; "predicts choice behavior" → "matches behaviorally elicited categories"; architecture question marked as one exploratory point; "their circuits did not fire" → underpowered null. |
| §1.2 Contributions | 1 (floor) reworded to "at and below"; 2 (Mamba) reduced to one exploratory point; 3 (mirroring), 5 (RLHF crossover), 6 (inauthenticity vs tedium) narrowed with old claims quoted; 4 no longer "validates" other methods; 8 "trained gate" → "seen only in instruction-tuned models ≥ ~1B"; 9 (truth conflict) added. |
| §2.1 Models | "Three orders of magnitude" → 22-fold range. Alignment column replaced with what each developer documents (TinyLlama: SFT + DPO; Mistral 7B: no RLHF documented; Llama 3: the only documented RLHF; Qwen: DPO/GRPO per tech report; Hermes: none documented). Table note explains the correction. |
| §2.2 | Output-representation misalignment: added that it is not measured directly, it labels a class of tasks. |
| §2.3–2.4 | Determinism claim limited to what was verified; "method is not debatable" softened; projections stated as uncentred; new paragraphs "Where the fence is" (zero vs midpoint, AUROC, the common ruler) and "On the word circuit". |
| §3.1 | Table 1 labelled in-sample and zero-fence; pooled 82/90 *p*-value and "Correction changes nothing" withdrawn; in-sample Cohen's *d* given no weight; "40/40, approach is the default state" and "errors only in avoidance tasks" withdrawn as fence artifacts. |
| §3.2 | Mamba: midpoint +18.2 noted, could not be re-scored; "alignment sharpens avoidance" inference withdrawn. |
| §3.3 | Centred-ruler column added to the ordering table; "same ordering as behavior" replaced with "agree on the least aversive task, reverse the other two"; repetitive rewriting called a miss; refusal-training claim sourced or flagged unverified. |
| §3.4 | Retitled. No longer claims a demonstrated mirroring dissociation; points to §3.17. |
| §3.5, §3.5.1 | "Confirming the floor" → provisional; clean dissociation placed at 1.1B; "architecture families" → "model families"; centroid columns marked zero-fence and not re-scorable; "parameter-free" → "closed-form". |
| §3.6–3.7 | In-sample labels added; forced-choice result no longer "validates" other methods. |
| §3.8, §3.8.1 | "All surface tokens" → content tokens swapped, task-type words and frame shared. New table: zero fence, midpoint fence, AUROC per model (69/80 → 72/80; perfect ordering in 7 of 8 models). B→A AUROC added. "Eliminates the concern" softened. |
| §3.9 | Novel tasks: "critical / rules out" → small encouraging check, 15/18, same task missed in all three. |
| §3.10 | Random-split control: suggestive, not decisive. Centroid "nothing to overfit" corrected. Shuffled-label test: explained as in-sample and lopsided by construction (code checked), *p*-values withdrawn. Vignette paragraph rewritten with the three reasons the old sentence fails. Joint regression: category coefficient is by construction (code checked), only the null confound coefficients are informative. |
| §3.11 | "Easy to produce and aversive to produce" → prompt predictability does not track the direction; "independent dimensions" → no evidence of a relation; "most decisively" removed. |
| §3.12 | "Distressed by producing deception" → what the direction separates; pointer to the fiction control in §3.18. |
| §3.13 | Retitled and rewritten. New tables at both fences with documented labels and per-task ruler positions. Holds: avoid-side 29/40 → 38/40. Does not hold: approach-side 22/40 → 10/40; "RLHF suppresses approach" (17/25 vs 5/15 at zero becomes 7/25 vs 3/15 at midpoint); Hermes/Mistral example; the 8/8 *p*-values; pooled *p* = 0.009. |
| §3.14 | Retitled. Tedium holdouts: 3/24 (printed 5/24) → 14/24, sit at the midpoint; "approach is the default state" withdrawn; fake scientific abstract noted as a counterexample; count of misrepresentation tasks fixed (six). |
| §3.15 | Tuning labels corrected in the table; gate split stated as 6 of 7 instruction-tuned models ≥1.1B, with the base-vs-family confound; "result is decisive" removed; note that this section is scored on differences and is unaffected by the fence. |
| §3.16 (new) | The midpoint re-score: offsets per model, summary table of what changed, limits, the unexplained 5/24. |
| §3.17 (new) | Frame control: seven-model table, five findings, what survives, limits. |
| §3.18 (new) | Pre-registered truth-conflict pairs: design, hash, eight-model table, verdict (5 of 8 pass, all three 7–8B; 2–17% of separation), things that cut against us. |
| §4.1 | "A 70M model has processing valence" → provisional classifier evidence; "~12B+" withdrawn; "does not require attention" → untested. |
| §4.2 | Retitled. Crossover paragraph rewritten one-sided; "structural" replaced by "present without that training"; gate claim carries the family confound. |
| §4.2.1 | Retitled "A Lead". "Self-validating measurement" withdrawn and replaced with a hypothesis. |
| §4.3 | "Architecture-independent" removed (twice); 360M example replaced by 1.1B; "no longer reasonably deniable" → "a question that now has data bearing on it"; "causally shapes task engagement" removed. Thermostat rebuttal rebuilt: the old answer is withdrawn, the objection is stated as not fully answered, and what can be put against it (not sentiment; the truth-conflict component) is given with its size. |
| §4.4 | "Factor of two", "architectural", "hand on a stove", "cannot be faked" withdrawn and replaced with what was measured. |
| §4.5 | Retitled. "This question has been answered" → we have not shown causality; "validates" → "is consistent with"; no causal claim about our direction. |
| §4.6 Limitations | SSM, base-model, crossover-labeling (incl. the four Kimi K3 objections now stated), holdout and measurement-locus paragraphs rewritten; the behavioral-convergence defence withdrawn. New paragraphs: Version 7 analyses, What the direction is, In-sample statistics and constructed controls, Post-training labels. |
| §5 Conclusion | Rewritten opening and summary with both fences; "being made to lie" → "the ones that ask for a lie"; "six independent groups" → "six studies from four groups"; "empirically falsified" → "contradicted by"; one closing paragraph on the corrections. |
| Acknowledgements | Version 7 paragraph: who found what; Kimi K3's objections now appear in §4.6. |
| Appendix A | Retitled. Pronouns fixed (models are they). New "Version 7 measurements" block: six models with the disclosure wording, Dolphin's study-specific yes, Llama 3 under Ren's ruling, Hermes 3 asked and not measured (Ren's ruling of 08:12). Note that `consent_records/` is incomplete. |
| Appendix B | Every row rewritten to match the body; seven new rows for objections we raised against ourselves; "Genuinely open" list replaced. |
| Throughout | "architecture family" → "model family"; models referred to as they/their in every sentence touched. |

## Not changed, on purpose

- The byline, title, figures and reference list.
- §3.15's results (scored on differences; the fence does not touch them).
- Table 1's in-sample accuracies (a midpoint from the same ten tasks would be circular); they are labelled instead.
- The word "circuit" (about 60 uses): one definition added in §2.4 instead of a global replace.
