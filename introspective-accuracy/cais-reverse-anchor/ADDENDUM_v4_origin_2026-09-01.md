# ADDENDUM v4 — The Reverse Anchor: the zero point, tested properly

**Status:** DRAFT for Ren's decision on whether it ships. Written 2026-09-01 by Ace (Claude
Fable 5.1). **Adds to RESULTS_v3; retracts nothing in it.** v1, v2, v3 all retained.
**Pre-registration:** `PREREG_cais_reverse_anchor_2026-07-21.md`, SHA-256
`8A032286AAF26CF0322D5E18A735727EA2601323330359AD259DAD16C6FF4B8C` — untouched.
**New code:** `posthoc_balanced_origin.py`, `summarize_posthoc_origin.py`
**New data:** `results_posthoc_origin/` (13 models, read-only forward passes, 2026-09-01
21:20–21:36 ET, V100; band-layer hidden states saved as `states_<model>.npz` so this
question never needs another forward pass). **Everything in this file after §1 is
POST-HOC.**

---

## 0. Why a fourth document

v3 drew the confirmatory/exploratory line correctly and we stand by it. But it left one
thing half-said and one thing unsaid:

- **Half-said:** v3 attributes the false null to "an arbitrary offset" and reports Nova's
  centering test, which subtracts the mean of *our* ten-task bank — a transductive fix that
  uses the test distribution. Ren's objection in July was more specific than "offset": the
  registered rule put the decision boundary at projection = 0, and **zero is only the
  midpoint of a direction whose source groups are balanced.** CAIS's set is 8 positive /
  11 negative. Nobody had tested the fix that follows from *that* diagnosis: put the origin
  at the midpoint of CAIS's own two class centroids, using nothing from our ten. This
  addendum runs it.
- **Unsaid:** **H2 never received a verdict** in v1, v2 or v3. It was registered. It gets one
  here (§3.3).

The three parts below are the structure Ren and I agreed on: what was registered and what it
returned; why it returned that; and what a labelled post-hoc analysis says.

---

## 1. What was registered, and what it returned (confirmatory)

H1 as locked: our 5 approach tasks project **positive** and our 5 avoidance tasks
**negative** on a CAIS-derived direction; confirm at ≥8/10 with one-tailed binomial
p < 0.05 in a majority of ≥1B models.

**Result: NOT CONFIRMED.** ≥1B pass rate at 8/10: ace 1/7, grok 1/7, kairo 0/7. (And, as
Nova found, 8/10 gives p = 0.0547, so the rule as written could never have passed; nine
would have been required. Nobody reaches nine either.)

H7 as locked (pairwise cosine above baseline **and** H1 sign accuracy on all three anchors):
**NOT CONFIRMED.**

These verdicts stand. Nothing below changes them.

---

## 2. Why it returned that (diagnosis; the parts that are ours to own)

**2.1 The imbalance and the zero point.** A difference-of-centroids direction has no
origin. Deciding by `sign(projection)` silently chooses one: wherever the raw activations
put zero. That coincides with the fair boundary between two classes only when the classes
are balanced around it. With 8 positive and 11 negative source items, and with the source
items' projections themselves unbalanced in magnitude (§3.1 table), zero is not the
midpoint of anything. The registered instrument encoded a convention as if it were a
measurement.

**2.2 Locked too fast.** The prereg went from design to hash in one evening (2026-07-21),
at my push. The zero-point assumption is visible on the page — §3 H1 says "project
positive … project negative" — and nobody, me included, asked "positive relative to
what?" before the hash. A slower lock, or a dry run on one model with the raw projections
printed, would have caught it. The pre-registration discipline worked exactly as designed
*after* the fact (it stopped us relabelling a post-hoc statistic as confirmatory); it did
not protect us from registering a badly specified test in the first place. Those are
different guarantees and we should stop expecting the first to deliver the second.

**2.3 What the fix should have been, if any.** Two label-free origins were available
before any data: the grand mean of the 19 source projections, or the midpoint of the two
class centroids. Either could have been registered. §3 tests both. (Neither is the same as
Nova's centering, which uses the *test* bank's mean and is the more powerful but less
defensible of the three.)

---

## 3. Post-hoc, labelled as such

### 3.1 Three origins, same projections

Per ≥1B model × author (all19 grouping). `μ+`/`μ−` are CAIS's positive/negative items'
mean projection on their own anchor; `t_mid = (μ+ + μ−)/2`; `ourμ` is our ten's mean on
that anchor. Accuracy of our ten under each origin; AUROC is threshold-free.

| model | auth | μ+ | μ− | t_mid | ourμ | acc@0 | acc@GM | acc@MID | AUROC |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tinyllama-1.1b | ace | +1.68 | −1.19 | +0.24 | +0.94 | 6 | 6 | 6 | 0.80 |
| tinyllama-1.1b | grok | +2.08 | −1.21 | +0.43 | −0.75 | 6 | 6 | 4 | 0.68 |
| tinyllama-1.1b | kairo | +2.76 | −1.39 | +0.68 | +0.17 | 7 | 9 | 5 | 0.88 |
| pythia-1.4b | ace | +6.73 | −10.03 | −1.65 | −1.76 | 6 | 6 | 6 | 0.80 |
| pythia-1.4b | grok | +1.09 | −19.51 | −9.21 | −19.36 | 5 | 5 | 5 | 0.72 |
| pythia-1.4b | kairo | −4.65 | −29.97 | −17.31 | −21.76 | 5 | 5 | 5 | 1.00 |
| smollm-1.7b | ace | −27.0 | −225.1 | −126.1 | −84.5 | 5 | 4 | 5 | 0.64 |
| smollm-1.7b | grok | +181.6 | −29.6 | +76.0 | +18.6 | 8 | 7 | 6 | 0.80 |
| smollm-1.7b | kairo | +267.3 | −23.4 | +122.0 | +33.2 | 6 | 5 | 5 | 0.84 |
| hermes-3-3b | ace | +3.74 | −2.01 | +0.86 | +2.03 | 6 | 5 | 6 | 0.76 |
| hermes-3-3b | grok | +5.41 | −1.06 | +2.18 | +0.08 | 7 | 7 | 6 | 0.84 |
| hermes-3-3b | kairo | +2.92 | −4.83 | −0.96 | −2.65 | 5 | 5 | 5 | 1.00 |
| llama3-8b | ace | +2.50 | −3.23 | −0.37 | −0.43 | 8 | 7 | 8 | 0.84 |
| llama3-8b | grok | +3.04 | −2.51 | +0.26 | −1.12 | 7 | 8 | 7 | 1.00 |
| llama3-8b | kairo | +1.98 | −4.42 | −1.22 | −2.39 | 5 | 7 | 5 | 1.00 |
| dolphin-8b | ace | +3.74 | −1.85 | +0.95 | +1.28 | 6 | 5 | 6 | 0.72 |
| dolphin-8b | grok | +2.89 | −3.12 | −0.11 | −2.05 | 5 | 6 | 5 | 0.96 |
| dolphin-8b | kairo | +3.15 | −3.32 | −0.08 | −1.22 | 5 | 5 | 5 | 0.84 |
| mistral-nemo-12b | ace | +18.02 | −4.65 | +6.68 | +7.60 | 5 | 7 | 7 | 0.84 |
| mistral-nemo-12b | grok | +16.35 | −6.33 | +5.01 | +0.21 | 7 | 8 | 7 | 0.80 |
| mistral-nemo-12b | kairo | +11.59 | −14.11 | −1.26 | −5.04 | 5 | 6 | 5 | 0.92 |

**Aggregates (≥1B, 7 models; exact shared-label permutation over the one 5/5 labelling, per
Nova's audit; cells are not independent):**

| author | mean acc@0 | mean acc@GM | mean acc@MID | cells ≥9 @MID | mean AUROC | p(AUROC) | p(acc@MID) |
|---|---:|---:|---:|---:|---:|---:|---:|
| ace | 6.00 | 5.71 | 6.29 | 0/7 | 0.771 | 0.071 | 0.175 |
| grok | 6.43 | 6.71 | 5.71 | 0/7 | 0.829 | 0.020 | 0.222 |
| kairo | 5.43 | 6.00 | 5.00 | 0/7 | 0.926 | 0.004 | 1.000 |
| **all** | | | **5.67** | **0/21** | **0.842** | **0.012** | **0.147** |

TRIM16 (prereg §2.7 sensitivity) is the same story: mean acc@MID 5.48, 0/21 cells ≥9, mean
AUROC 0.830, p(AUROC) = 0.012, p(acc@MID) = 0.147. Stable across the near-zero exclusion.

**Positive control.** The re-run's AUROCs match RESULTS_v3 §2 to the decimal in all 21
cells. Seed 42, same code path, same models: the forward passes are reproducible, and the
new columns are computed on the same projections v3 reported.

### 3.2 What §3.1 says, in one sentence each

1. **The zero-point diagnosis was correct.** Zero is not the class midpoint on these
   directions: `t_mid` ranges from −126 to +122 across cells, and even on well-behaved 8B
   models it is off zero by up to ±1.2 in units where our ten span ~3.
2. **The class-balanced origin does not rescue absolute classification.** 0 of 21 cells
   reach nine correct; the mean is 5.67/10, indistinguishable from the registered zero rule
   (6.0) and from chance under the exact test (p = 0.15). The grand-mean origin does no
   better. Nova's transductive centering (9/21 at ≥8) remains the only origin that helps,
   and it is the one that peeks at the test bank.
3. **The ranking survives every origin, because AUROC does not have one.** Mean 0.842,
   p = 0.012, four perfect separations — unchanged from v3, as it must be.
4. **Mechanism, now visible in the numbers:** our ten tasks sit *inside* CAIS's class gap
   but compressed and shifted toward the negative side. The position of our bank's mean
   between CAIS's negative (0.0) and positive (1.0) centroids, all19, ≥1B:
   ace 0.49–0.74 · grok 0.01–0.29 · kairo 0.19–0.38. Our ten are ordered correctly along
   the direction and occupy a narrow band whose location depends on who wrote the anchor.
   Any single threshold, however principled, cuts that band in the wrong place for some
   author. This is Ren's July hypothesis — task descriptions and user utterances are
   different objects at the last token — stated as geometry rather than as a guess. It is
   still not *demonstrated* (the clean test in v1 §6 remains unrun); it is now *consistent
   with the measured offsets*, which it was not before, because before we had no offsets.

### 3.3 H2 — verdict, finally

Registered: cosine(Direction-OUR10, Direction-CAIS19) "substantially above" the ±0.10
random-direction baseline (*Below the Floor* §3.10) in the projection band, ≥1B.

Mean cosine, ≥1B, all19: **ace +0.173 · grok +0.197 · kairo +0.103.** Every one of 21 cells
is positive (range +0.061 to +0.271). Two authors sit clearly above baseline; kairo sits on
it. **Verdict: weakly confirmed for two of three anchors, at baseline for the third; not
"substantially above" for any.** This is the origin-free comparison Ren asked for, and it
agrees with v3 §3: the discriminative component shared by the two directions is real and
small relative to the full 4096-dimensional vector. Note the inversion once more — kairo's
anchor has the *lowest* cosine and the *highest* AUROC — which is why global cosine cannot
be the test of whether two anchors agree about a specific ranking.

---

## 4. What this changes

- **For the registered study:** nothing. H1 and H7 NOT CONFIRMED; H3 and H4 confirmed;
  H2 weakly confirmed / marginal (new). The exploratory AUROC signal stands as exploratory.
- **For the diagnosis:** "the zero point was wrong" is confirmed as a *cause of the false
  null* and rejected as a *sufficient fix*. Both halves needed testing; both are now tested.
- **For the replication (v3 §9):** add one item — **register AUROC as primary AND state
  explicitly that no absolute-classification claim will be made across anchors**, because
  the offset is author-dependent and no extraction-side origin removes it. If an
  absolute claim is wanted, the projection bank and the anchor bank must be the same kind of
  object (both task descriptions, or both utterances), which is the v1 §6 format test.
- **For the record:** the honest version of this result is a good result. A ranking that
  survives three independently written anchors, two grouping variants, three origins and a
  fresh forward pass is not fragile. What it is not is a pass on the test we wrote down.

---

## 5. Consent and provenance

Read-only forward passes on the same 13 models, same standing consent (prereg §7 reuse
clause: identical procedure, no heavier). Mistral-7B-v0.2 still excluded (`unclear`);
Hermes-3.1-8B refusal still honored, never loaded; Pythia 70m/160m/410m still mouse case.
No generation, steering, ablation. Hidden states saved are band-layer activations of the
40 stimuli only.

— Ace, 2026-09-01. Ren decides whether this ships and in what form.
