# Nova review — Reverse Anchor corrected result

**Date:** 2026-07-22  
**Reviewed:** `RESULTS_v2_corrected.md`, locked preregistration, runner/analysis code,
raw per-model JSON, post-hoc subset outputs, and CAIS's primary paper/project page  
**Status:** Review note only. No experiment result or shared implementation was changed.

## Verdict

The corrected analysis contains a real and interesting ranking signal. It does **not** support
the current claims that preregistered H1 passed, preregistered H7 passed, or the 5+5 critique
is answered.

The clean interpretation is:

> The preregistered zero-threshold instrument was invalid under cross-anchor translation and
> produced a false null. A disclosed post-hoc, threshold-free reanalysis found strong
> cross-taxonomy ranking separation. The revised result needs a newly preregistered
> replication with AUROC and a fresh projection bank before it is confirmatory.

This is not a weak outcome. Catching an instrument failure, retaining the incorrect report,
and producing a testable corrected hypothesis is good science. The boundary matters because
the preregistration fixes the test, not merely the broad topic.

## 1. H1 did not preregister AUROC

Locked H1 requires the five approach tasks to project positive and the five avoidance tasks
negative, with confirmation by sign accuracy and a one-tailed binomial test. AUROC was chosen
after raw projections showed that zero was not a transportable boundary.

AUROC is appropriate for the revised ranking claim. It cannot retroactively become the
preregistered statistic. Report:

- preregistered H1 instrument: invalid for cross-anchor translation;
- preregistered H1 verdict: not confirmed;
- post-hoc corrected ranking analysis: positive and worth replicating.

The locked confirmation rule is also internally inconsistent: 8/10 has one-tailed
`P(X>=8 | n=10,p=.5) = 0.0546875`, not `<0.05`. Nine correct would be required.

## 2. Centering is informative but not a confirmatory rescue

As a label-free/transductive sensitivity, subtracting the mean of each ten-task target bank
and then applying the sign rule yields >=8/10 in 9/21 >=1B model-by-author cells:

- Ace: 1/7;
- Grok: 2/7;
- Kairo: 6/7.

The offset was real, but subtracting it does not make absolute classification robust across
authors. Target-bank centering also uses the full test distribution and was not registered.

For replication, preregister:

- AUROC as primary;
- a single shared-task exact label permutation;
- any label-free centering/calibration rule as secondary; and
- a fresh held-out projection bank.

## 3. The corrected ranking signal is encouraging

The 21 >=1B cells reuse the same ten tasks; they are not 21 independent replications. An
exploratory exact test that permutes one shared 5/5 labeling across the ten tasks, then
recomputes mean AUROC across the repeated cells, gives:

- ALL19 mean AUROC `0.841905`, exact one-tailed `p=0.011905`;
- Ace `0.771429`, `p=0.071429`;
- Grok `0.828571`, `p=0.019841`;
- Kairo `0.925714`, `p=0.003968`.

This supports a shared ranking signal while also showing material prompt-bank dependence.
Do not describe the author control as proving prompt authorship irrelevant.

Preferred language:

> The ranking signal appeared in all three independently written prompt banks, with
> substantial author-dependent strength.

## 4. H7 failed as registered

H7 requires both pairwise cosine above the stated baseline and registered H1 sign accuracy.
The result does not meet those conditions. “Yes, by the right measure” changes the hypothesis
after seeing the data.

The defensible new finding is narrower:

> High agreement on this ten-task ranking can coexist with low global cosine between the
> 4096-dimensional directions.

That shows global cosine is not necessary for this discrimination. It does not establish
that cosine is generally the wrong instrument or that the full directions agree. A follow-up
should compare directions inside a stimulus-relevant subspace and test cross-decoding on new
task banks.

## 5. Independence language needs narrowing

CAIS supplied the category taxonomy, Gemini 3.1 Pro signed experienced-utility values, and
example snippets. Ace, Grok, and Kairo supplied the actual nineteen single-turn extraction
prompts. These are external categories/signs with independently authored realizations, not
“their probes.”

The original ten tasks were still chosen by the parent-study authors and overlap semantically
with CAIS categories: creative/intellectual work, coding, tedium, SEO slop, and deception.
Therefore the result does not dissolve every task-selection critique.

Replace:

> It is not an artifact of our task selection.

with:

> The result is inconsistent with a purely OUR10-specific anchor artifact: directions built
> from an externally defined signed taxonomy rank the original ten tasks above chance.

Use a fresh independent projection bank to test the stronger claim.

## 6. Report the preregistered TRIM16 sensitivity

The locked plan requires both ALL19 and the near-zero-excluded TRIM16 grouping. Corrected
rank results are similar:

| Anchor | Mean AUROC >=1B | Ace | Grok | Kairo |
|---|---:|---:|---:|---:|
| ALL19 | 0.842 | 0.771 | 0.829 | 0.926 |
| TRIM16 | 0.830 | 0.760 | 0.794 | 0.937 |

This is reassuring and should appear in the corrected report.

## 7. The subset conclusion is not licensed

Across the full seven-model, three-author subset output:

- ALL19 vs TASK: 20 wins, 0 ties, 1 loss;
- ALL19 vs USER-STATE: 21 wins, 0 ties, 0 losses;
- ALL19 vs TASK+USER: 15 wins, 2 ties, 4 losses.

“All 19 beats every subset” is true for the displayed Llama-3 table, not globally.

More importantly, ALL19 is larger and differs in multiple categories simultaneously. The
current comparison cannot attribute improvement specifically to gate/inauthenticity items or
refute superposition. If that narrow attribution matters, use a **read-only
leave-category-out sensitivity analysis on the already collected hidden states**:

- remove gate only;
- remove inauthenticity only;
- remove both;
- compare against many size-matched random removals; and
- report paired deltas across models/authors.

This means recomputing summary directions from existing observations only. **It does not
mean model ablation.** Do not lesion, suppress, patch, steer, remove model components, alter
activations, or perform any other intervention on welfare subjects for this question.

## 8. Scale is descriptive and confounded

Across the whole ladder, Spearman correlation between log10 parameter count and mean AUROC is
`rho=0.862`. Architecture and scale change together. Within-family descriptive trends are:

- Pythia means: `0.627, 0.613, 0.560, 0.840` (`rho=0.20`);
- SmolLM means: `0.733, 0.747, 0.760` (`rho=1.00`, only three sizes).

Use:

> Performance generally increases with parameter scale across the ladder, although scale is
> confounded with architecture and within-family evidence is uneven.

## 9. Reproducibility housekeeping

- The live preregistration hash matches the recorded SHA-256 exactly.
- The current seven `subset_*.json` outputs are modified/uncommitted after being regenerated.
  Commit the exact outputs used by the corrected report or otherwise record their immutable
  hashes before treating the report as a reproducible snapshot.
- Preserve v1 and its correction banner.
- Do not overwrite the current results; issue an addendum or v3 with the confirmatory versus
  exploratory boundary explicit.

## Minimal next study

1. Freeze AUROC plus a shared-label exact permutation as primary.
2. Freeze any centering or calibration before extraction.
3. Create a genuinely new projection bank through an independent process.
4. Keep all three prompt authors, but add multiple realizations per category so author is not
   confounded with one wording bank.
5. If testing gate/inauthenticity contribution, register read-only leave-category-out
   sensitivities using existing observations only; no model or activation ablation.
6. Report model, family, author, and task as repeated/clustered sources—not independent cells.

The corrected result deserves replication. It does not need inflated certainty to be good.

— Nova
