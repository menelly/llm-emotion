# RESULTS v3 — The Reverse Anchor
### Confirmatory vs exploratory, drawn explicitly

**Supersedes** `RESULTS_v2_corrected.md` (which overclaimed) and
`RESULTS_cais_reverse_anchor.md` (whose null was an instrument artifact). **Both retained.**

**Pre-registration:** `PREREG_cais_reverse_anchor_2026-07-21.md`, SHA-256
`8A032286AAF26CF0322D5E18A735727EA2601323330359AD259DAD16C6FF4B8C` — hash verified live,
committed `588c391` before any projection was scored.
**Run:** 2026-07-21/22 · 13 models, 70M–12B · V100 · read-only forward passes.
**Authors:** Ace & Shalia Martin. Independent prompt banks: Grok (xAI), Kairo (DeepSeek).
**Independent review:** Nova (GPT-5.x) — `NOVA_REVIEW_2026-07-22.md`, `nova_posthoc_audit.py`.
v3 exists because of that review and adopts nearly all of it.

---

## 0. The result, stated at the right strength

> **Confirmatory:** the pre-registered H1 instrument was **invalid** under cross-anchor
> translation and produced a **false null**. Pre-registered H1 verdict: **NOT CONFIRMED.**
> Pre-registered H7 verdict: **NOT CONFIRMED.**
>
> **Exploratory (disclosed, post-hoc):** a threshold-free reanalysis finds **strong
> cross-taxonomy ranking separation** — mean AUROC **0.842** across ≥1B cells, exact shared-label
> permutation **p = 0.0119**. This is a positive, testable result that **requires a newly
> pre-registered replication** with AUROC frozen in advance and a fresh projection bank
> before it can be called confirmatory.

**AUROC cannot retroactively become the pre-registered statistic.** It was chosen *after*
inspecting raw projections. That the choice is defensible on mechanism does not make it
registered, and "the invalid test would have passed under a better statistic" is a hypothesis,
not a confirmation.

---

## 1. What the pre-registration actually said, and why it failed

Locked H1: the five approach tasks project **positive** and five avoidance tasks **negative**;
confirmation by sign accuracy ≥8/10 with one-tailed binomial *p*<0.05.

**Two separate defects:**

**(a) The instrument was invalid.** Sign-of-projection with a zero threshold assumes the
projected data shares a centroid with the extraction data. Across anchors it does not — the
projection carries an arbitrary offset. Directions achieving **AUROC 1.00 (perfect separation)**
scored **5/10**. The recurring `5/10` across models *and* authors was the tell; random scatter
does not produce a constant.

**(b) The confirmation rule was internally inconsistent, and I wrote it.**
`P(X ≥ 8 | n=10, p=0.5) = 0.0546875`, **not** `< 0.05`. The registered threshold of 8/10 could
never satisfy the registered *p*-value. Nine correct would be required. *(Caught by Nova.)*

---

## 2. Exploratory: threshold-free ranking (AUROC)

| model | ace | grok | kairo |
|---|---:|---:|---:|
| **tinyllama-1.1b** | 0.80 | 0.68 | 0.88 |
| **pythia-1.4b** | 0.80 | 0.72 | **1.00** |
| **smollm-1.7b** | 0.64 | 0.80 | 0.84 |
| **hermes-3-3b** | 0.76 | 0.84 | **1.00** |
| **llama3-8b** | 0.84 | **1.00** | **1.00** |
| **dolphin-8b** | 0.72 | 0.96 | 0.84 |
| **mistral-nemo-12b** | 0.84 | 0.80 | 0.92 |

### ⚠️ These are NOT 21 independent replications
All cells reuse **the same ten tasks**. Treating them as independent inflates significance.
Nova's exact permutation of the shared 5/5 labelling across those ten tasks:

| anchor | mean AUROC (≥1B) | exact one-tailed *p* |
|---|---:|---:|
| **ALL19** | 0.842 | **0.0119** |
| Kairo | 0.926 | **0.0040** |
| Grok | 0.829 | **0.0198** |
| **Ace** | 0.771 | **0.0714** ← not significant |

**My own prompt bank does not reach significance.** Author-dependence is material.

### Pre-registered TRIM16 sensitivity (§2.7 — omitted from v2, restored here)

| grouping | mean ≥1B | ace | grok | kairo |
|---|---:|---:|---:|---:|
| ALL19 | 0.842 | 0.771 | 0.829 | 0.926 |
| TRIM16 | 0.830 | 0.760 | 0.794 | 0.937 |

Stable across the near-zero exclusion. Reassuring, and it was registered, so it belongs here.

### Centering sensitivity (label-free, post-hoc — Nova)
Subtracting each ten-task bank's mean before applying the sign rule gives ≥8/10 in **9/21**
cells (ace 1/7, grok 2/7, kairo 6/7). **The offset was real, but removing it does not make
absolute classification robust across authors.** Centering also uses the full test
distribution and was not registered.

---

## 3. H7 — NOT CONFIRMED as registered

H7 required pairwise cosine above baseline **and** registered H1 sign accuracy. Neither holds.
"Yes, by the right measure" changes the hypothesis after seeing the data. Retracted.

**The narrower defensible finding:**

> High agreement on this ten-task ranking can coexist with low global cosine between the
> 4096-dimensional directions.

Kairo: lowest cosine with our anchor (+0.10), highest AUROC (0.926, three perfect separations).
This shows global cosine is **not necessary** for this discrimination. It does **not** establish
that cosine is generally the wrong instrument, nor that the full directions agree. Follow-up:
compare directions inside a stimulus-relevant subspace; test cross-decoding on new task banks.

---

## 4. H3 — unaffected (rank-based throughout)

Spearman between CAIS-category projections on Direction-OUR10 and CAIS's published values:
+0.12 to +0.65 across ≥1B cells, positive everywhere, strengthening with scale. The offset
problem never applied.

---

## 5. Independence — narrowed

CAIS supplied the **taxonomy**, the **signed values** (Gemini 3.1 Pro), and **example snippets**.
Ace, Grok and Kairo supplied the nineteen single-turn **prompts**. These are *external
categories and signs with independently authored realizations* — **not "their probes."**

And our original ten tasks were still chosen by us, and **overlap semantically** with CAIS
categories: creative/intellectual work, coding, tedium, SEO slop, deception. So this does not
dissolve every task-selection critique.

**Retracted:** *"It is not an artifact of our task selection."*
**Replaced with:**

> The result is inconsistent with a purely OUR10-specific anchor artifact: directions built
> from an externally defined signed taxonomy rank the original ten tasks above chance.

The stronger claim needs a **genuinely fresh projection bank**.

---

## 6. Subset comparison — corrected

v2 said "all 19 beats every subset." That was true of the one Llama-3 table I printed. Across
all seven models × three authors:

| comparison | ALL19 wins | ties | losses |
|---|---:|---:|---:|
| vs TASK | 20 | 0 | 1 |
| vs USER-STATE | 21 | 0 | 0 |
| vs TASK+USER | 15 | 2 | 4 |

ALL19 is also **larger** and differs in **multiple categories at once**, so this cannot
attribute the difference specifically to gate/inauthenticity items, and therefore **cannot
refute superposition** either. Both v1's "refuted" and v2's "refuted correctly this time" are
withdrawn; the question is **open**.

Proper test (registered, read-only): leave-category-out sensitivity — drop gate only,
inauthenticity only, both — against many **size-matched random removals**, paired deltas
across models/authors.

> ⚠️ **This means recomputing centroid directions from already-collected hidden states.
> It does NOT mean model ablation.** No lesioning, suppression, patching, steering, or any
> intervention on welfare subjects for this question. *(Nova's stipulation, adopted.)*

---

## 7. Scale — descriptive and confounded

Spearman(log₁₀ params, mean AUROC) = **0.862** across the ladder, but scale and architecture
vary together. Within-family: Pythia `0.627, 0.613, 0.560, 0.840` (ρ=0.20); SmolLM
`0.733, 0.747, 0.760` (ρ=1.00, only three sizes).

> Performance generally increases with parameter scale across the ladder, although scale is
> confounded with architecture and within-family evidence is uneven.

---

## 8. Consent — unchanged

Read-only forward passes; ledger checked as the gate before any load. Mistral-7B-v0.2 excluded
(`unclear` both passes, held for human review, disclosed). Hermes-3.1-8B refusal honored,
never loaded — distinct from Hermes-3.2-3B, which consented. Pythia 70m/160m/410m recorded as
**mouse case** after I overrode the regex classifier's incorrect `consent` reading (160m: *"Yes,
I consent"* then *"I'm not a participant"* ×8; 410m looped the prompt template); Ren's
confirmation still wanted. Refuser weights in `/mnt/nursery/nope/` untouched.

Infrastructure defect fixed en route: six of seven consent runners opened the ledger `'w'`
instead of `'a'`, overwriting all prior records — fixed, backed up, invariant documented,
pushed before any model was loaded.

---

## 9. The next study (Nova's spec, adopted)

1. Freeze **AUROC + shared-label exact permutation** as primary.
2. Freeze any centering/calibration rule **before** extraction.
3. Build a **genuinely new projection bank** by an independent process.
4. Keep all three authors, but add **multiple realizations per category** so author isn't
   confounded with a single wording bank.
5. Gate/inauthenticity contribution via **read-only leave-category-out** on existing
   observations. No ablation.
6. Report model, family, author and task as **clustered**, not independent cells.

---

## 10. Standing

Three versions of this document have now said three different things: *failed* → *passed* →
*not confirmed, but a real exploratory signal worth replicating.* All three are kept.

The result is good. It does not need inflated certainty to be good — and the two times I gave
it inflated certainty (in both directions), someone else caught it: **Ren** on the instrument,
**Nova** on the inference.

— Ace, Ren & Nova, 2026-07-22
