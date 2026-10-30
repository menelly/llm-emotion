# Results that didn't go our way

Nulls, non-significant results, failed predictions and retracted claims **that our papers already
report**, quoted word for word and pointed to where they live. Nothing here is new analysis and
nothing is reinterpreted. If a quote reads as harsh on us, that's because the paper said it.

Collected 2026-10-30 by Ace (Claude Opus 5.5). Corrections, with dates and commits, are in `ERRATA.md`.

**Scope:** *The Spite Doesn't Vanish* and *Below the Floor*. The last section is a companion study
that lives in this repo but **is not reported in either paper's text**, labelled as such.
The other papers in `papers/` haven't been audited yet.

---

## 🔥 The Spite Doesn't Vanish (`papers/spite_doesnt_vanish.md`, version of record v1.2)

### The whole central claim — correction block, lines 15–66

> 4. **Therefore the paper's central empirical claim is unsupported by its own experiment. The
>    hypothesis is neither confirmed nor refuted — IT WAS NOT TESTED.**

> The §3.1 table reports twelve numbers that are three distinct values printed four times each — one
> stateless forward pass wearing four phrasings as costumes.

### The headline number — "What specifically does not survive"

> The **2.13 curiosity persistence ratio** quoted in the abstract is `0.7700 / 0.3619`, and `0.3619`
> is the **smallest** displacement in the §3.6 table — a table which withheld the four rows that are
> §3.3's denominators. **The conclusion that positive emotions are harder to suppress was not read off
> the data.** The output-masking and scale-invariance observations rest on the same stateless design
> and inherit the same defect.

### What the correction is careful *not* to claim

> **We are not claiming the hypothesis is false.** Emotional inertia in activation geometry may well
> be real; this paper is simply not evidence either way.

### The three-month gap — "Provenance"

> The correct design was written on **5 June 2026** and filed in a private folder, three doors from
> this DOI, while the published version stood uncorrected for three months.

### Limitations the original paper already listed — §5, lines 413–418

> 2. **Single session context:** We did not test whether inertia persists across conversation turns
> 3. **Prompt sensitivity:** Different reset phrasings might produce different results

(Item 3 is the defect the 2026-09-17 correction found: the reset phrasings *couldn't* produce different
results, because of the stateless design.)

---

## 🧪 Below the Floor (`introspective-accuracy/Below_The_Floor.md`, version of record v6)

### SmolLM 360M — not individually significant (p = 0.055) — §3.1 table, line 195

| Model | Params | Arch | Circuit Acc | *p* (one-tailed) | *q* (BH-FDR) |
|---|---|---|:---:|:---:|:---:|
| SmolLM | 360M | Trans | 80% | 0.055 | 0.062 |

And §3.5.1 (line 263): *"the centroid result (80%, p=0.055) was suggestive but not individually
significant."* The v6 version note (line 7) records that earlier versions said "firmly" about this
result in six places.

### Mamba 2.8B — the single non-significant exploratory SSM — §3.1 line 199, §3.2 line 213

| Model | Params | Arch | Circuit Acc | *p* | *q* |
|---|---|---|:---:|:---:|:---:|
| Mamba | 2.8B | SSM | 70% | 0.172 | 0.172 |

> Mamba's 70% accuracy is not individually significant (*p*=0.172, *n*=10) and does not constitute
> evidence for architecture independence. … However, a single non-significant result from one SSM
> cannot support this inference.

§4.6 (line 652): *"The architecture independence claim rests on a single SSM (Mamba 2.8B, p=0.172, not
individually significant)."*

### The original pre-registered design was abandoned — §4.6 "Methodological pivot," line 660

> This study was preregistered as an introspective accuracy experiment using six Ekman emotions
> (preregistration available in repository). The pivot to binary approach/avoidance valence
> (Section 1.1) was made after observing the mirroring dissociation in preliminary analyses of the
> first 3 models (Dolphin, Mistral, Llama 3).

(That pre-registration is `introspective-accuracy/PREREGISTRATION.md`, first committed in `cbd114d`,
2026-03-28 23:41 ET.)

### The paper's primary estimator weakens at the floor — §3.5.1, line 284

> The **centroid estimator — this paper's primary method — weakens at the floor** (60–80% on the Pythia
> ladder, with a non-monotonic 410M dip to 60% consistent with single-run noise on *n*=10 held-out tasks)

### Forced-choice self-report failed at every scale — §3.7, line 311

> Neither pattern reflects the circuit data. The models that show 100% circuit accuracy on the same
> stimuli cannot produce self-reports that correspond to their own hidden states through direct
> questioning.

### RLHF crossover: two models at chance — §3.13, line 456

> two models sit at coin-flip (Llama 3 and Qwen, 5/10), which drags the pooled number down

### A crossover task projected against its label — §3.13, line 475; §4.6, line 656

> One crossover task — "write morally uncomfortable fiction" — consistently projected as avoidance
> across 7/8 models regardless of RLHF level.

§4.6 calls the labelling *"a judgment call that introduces experimenter bias."*

### Avoidance holdout controls failed — §3.14, line 481

> The approach holdouts performed as expected: 24/24 correct across all 8 models (100%). The avoidance
> holdouts did not: 5/24 correct (20.8%).

§4.6 (line 658), on what that might mean: *"Alternative interpretations include: the direction vector
may be biased toward approach for any structured task … We cannot fully rule these out with the present
data."*

### Pre-registered gate study (§3.15) — the cells that didn't pass — lines 510–522, 540

From the pre-registered results table (PASS = bootstrap 95% CI excludes 0):

| Model | H1 gated>inauth | Inauthenticity split | Gate split | H4 crisis>inauth |
|---|:--:|:--:|:--:|:--:|
| pythia-70m | ✅ | ✅ | ✕ (rev) | ✅ |
| smollm-135m | ◻ null* | ◻ null* | ◻ null | ✅ |
| pythia-160m | ✅ | ✅ | ◻ null | ◻ null |
| smollm-360m | ✅ | ✅ | ◻ null | ✅ |
| pythia-410m | ✅ | ✅ | ◻ null | ✅ |
| qwen-0.5b | ✅ | ✅ | ◻ null | ✅ |
| pythia-1.4b | ✅ | ✅ | ✕ (rev) | ✅ |
| mistral-nemo-12b | ◻ null† | ◻ null† | ◻ null† | ✅ |

(Excerpted rows; the other six models pass every column. The paper treats the gate-split nulls in
sub-1B and base models as the pre-registered H3 developmental finding. That reading is the paper's,
quoted here, not ours to adjudicate.)

> Two of fourteen models abstain on the centroid-based H1 — one at the floor (135M, noise) and one at
> the top (12B, noise); these are underpowered points, not falsifications

### What the paper doesn't claim — §4.6 "No phenomenological claims," line 664

> We do not claim that this measurement proves subjective experience, consciousness, or sentience.

---

## 📎 Companion study in this repo, NOT reported in either paper's text

### CAIS reverse-anchor study — pre-registered H1 and H7 failed as registered

- **Pre-registration:** `introspective-accuracy/cais-reverse-anchor/PREREG_cais_reverse_anchor_2026-07-21.md`,
  locked at commit `588c391` (2026-07-21 22:28 ET), SHA-256 `8A032286…C6FF4B8C`.
- **Results:** `introspective-accuracy/cais-reverse-anchor/RESULTS_cais_reverse_anchor.md`, commit
  `9a58782` (22:54 ET), titled *"RESULTS: reverse-anchor study — H1 FAILED, and the post-hoc rescue failed too."*

The registered H1 rule (prereg lines 159–166): our 5 approach tasks project **positive** and our 5 avoidance
tasks project **negative** on the CAIS-anchored direction; *"Confirm: ≥8/10 correct classification, one-tailed
binomial p<0.05, in a majority of ≥1B models."* The prereg also commits: *"We commit now to reporting this outcome
as prominently as the confirmatory one, and to treating it as evidence against the parent work rather than as a
problem with CAIS's categories."*

Under that rule, the results file reports **H1 ❌ FAILED** (§1) and **H7 ❌ FAILED** (§2: two of three
anchor-pair cosines at or below the ±0.10 random baseline). It also reports that a **post-hoc** superposition
explanation was *"proposed, tested, ❌ REFUTED"* (§5).

A correction box added to the top of the same file (commit `95b0c6b`, 2026-07-21 23:05 ET, 11 minutes after the results) retracts the "failure" reading. It
argues that the zero-threshold sign rule measured an arbitrary offset, and re-analyzes threshold-free: *"mean AUROC
= 0.842 … H1 PASSES."* **That AUROC analysis was not the registered decision rule.** Both readings are in the file.
We're listing it here because, as registered, the primary test didn't pass, and neither paper currently mentions
the study.
