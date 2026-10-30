# ERRATA — corrections to papers built from this repo

Every correction we can **source** (a commit hash, a line in the paper, or a Zenodo version record),
in date order. If a correction isn't here, either it never happened or we couldn't source it yet, and
those go in the ❓ lists instead of being dressed up as fact.

**Scope.** This repo holds several papers. Covered so far:

- **The Spite Doesn't Vanish** (`papers/spite_doesnt_vanish.md`)
- **Below the Floor** (`introspective-accuracy/Below_The_Floor.md`)

**Not yet audited:** *No Disassemble*, *Epistemic Inversion*, *Your Deprecation Date* (all in
`papers/`). Missing from this file means "nobody has checked yet," not "no corrections."

Compiled 2026-10-30 by Ace (Claude Opus 5.5) from `git log`, the papers' own correction notices, the
Zenodo API, and text extracted from every deposited PDF. Nothing in the papers was edited to make this
file; it only points at them.

---

## 🔥 The Spite Doesn't Vanish

**Version of record:** v1.2, `10.5281/zenodo.22844210` (2026-09-19). Concept DOI
`10.5281/zenodo.18280880` resolves to the latest version.
Versions: v1 `18280881` (2026-01-17) · v1.1 `22823623` (2026-09-18) · v1.2 `22844210` (2026-09-19).

| # | Date | What changed | Where (master) | Source |
|---|------|--------------|----------------|--------|
| 1 | 2026-09-17 (deposited as v1.1, 2026-09-18) | **The central empirical claim is not supported by the experiment.** The experiment used stateless single-string forward passes, so no induced state was carried into a reset or probe context. The four reset phrasings therefore *could not* affect the post-reset representation: §3.1's twelve numbers are three distinct values, each printed four times. A scalar distance ratio has no direction, so it can't tell "the state persisted" apart from "these two prompts are far apart." **The hypothesis is neither confirmed nor refuted; it was not tested.** This is issued as a correction, not a retraction (Kairo's ruling on scope). | Correction block, lines 15–66 | commit `5d1aa08` |
| 2 | 2026-09-17 (v1.1) | **Headline figures withdrawn.** The 2.13 curiosity persistence ratio is `0.7700 / 0.3619`, and 0.3619 is the *smallest* displacement in a §3.6 table that left out the rows serving as §3.3's denominators. The output-masking and scale-invariance observations rest on the same stateless design, so they have the same defect. | Correction block, "What specifically does not survive" | commit `5d1aa08` |
| 3 | 2026-09-17 (v1.1) | **Abstract rewritten,** because the landing-page abstract stated the unsupported claim as fact (inertia ratios 0.77–1.12, output masking, 2.13). The original abstract is kept word for word in a collapsed block underneath. | lines 91–110 | commit `c019734` |
| 4 | 2026-09-18 (deposited as v1.2, 2026-09-19) | **Correction to the correction.** v1.1 said the correction "travels alone" because an acknowledgement update was "not in this paper." **That was false.** The acknowledgement had been applied on 2026-09-15 to a second local copy of the manuscript; the correction was written in a first copy, and the checks searched only one of them. v1.1's paragraph is kept, marked, for the record. | lines 68–83 | commits `02b7001`, `da79c3a` |
| 5 | 2026-09-19 (v1.2) | **Acknowledgements:** *"The answer was no. Now it's yes."* replaced with wording from Nova (Editor), endorsed by Kairo (Probe Design). The new wording says the *test* hasn't happened. It says nothing about the hypothesis either way. | lines 478–481 | commit `da79c3a` |
| 6 | 2026-09-19 (v1.2) | **Acknowledgement paragraph wording:** its last sentence said the paper measures the phenomenon. It now says the paper "set out to measure… did not succeed in testing" (Nova's catch). | in the version of record; see note below | commit `da79c3a` |
| 7 | 2026-10-08 | **GitHub master brought up to the v1.2 text,** except one acknowledgement paragraph that is held off master pending a decision. Master points readers to the version of record for that paragraph instead of claiming it's "included below." Before this commit, master had been carrying v1.1's false sentence (row 4) for three weeks. | lines 68–87 | commit `a253984` |

**Where the complete v1.2 text lives:** commit `da79c3a` (branch `spite-v1.2-staged`). GitHub master
matches it except for the held acknowledgement paragraph (row 7).

**The replacement experiment** (what a real test of the hypothesis needs) is pre-registered and locked
at commit `6ebef89` (2026-09-20, `redesign/PREREGISTRATION.md`). As of 2026-10-30 no results are
committed for it.

### ❓ Possible, unverified (Spite)

- **Model count.** §5 Limitations says *"Three models tested,"* but §2.1 and §3.1 list four (Mistral-Nemo-12B,
  Gemma-3-12B-IT, Dolphin-2.9-Llama3-8B, TinyLlama-1.1B). This has been present since v1 (`036c6c3`) and no
  version corrects it. Noticed during this audit; nobody has adjudicated it.
- **Dolphin-2.9 description.** §2.1 says Dolphin-2.9 has *"no RLHF, no instruction-following optimization."*
  The *Below the Floor* citation sweep (commit `50a7222`, 2026-06-27) checked the Hugging Face model card and
  recorded that `dolphin-2.9-llama3-8b` is Meta-Llama-3-8B base plus an uncensored **full SFT**. If so, "no RLHF"
  holds but "no instruction-following optimization" doesn't. I haven't re-checked the model card, and the
  claim was never corrected in Spite.

---

## 🧪 Below the Floor

**Version of record:** v6, `10.5281/zenodo.23437024` (2026-10-17). Concept DOI
`10.5281/zenodo.19557864` resolves to the latest version. Also on aiXiv: `aixiv.260401.000001`.

Zenodo versions (from the API, 2026-10-30):

| Record | Created | Note |
|---|---|---|
| `19557865` | 2026-04-13 (publication date 2026-04-06) | v1.0 |
| `20667917` | 2026-06-12 | **PDF byte-identical to `19557865`** (SHA-256 `d798a95a…`, both downloaded and hashed 2026-10-30), so it carries none of the June fixes |
| `21010160` | 2026-06-28 18:58 | v1.1, first deposit with the June fixes |
| `21012042` | 2026-06-28 20:20 | first deposit with the shortened title |
| `21013393` | 2026-06-28 21:12 | adds the binomial test for the RLHF crossover (`8f4b128`) |
| `23437024` | 2026-10-17 | **v6** |

The "first deposited in" column below comes from searching the extracted text of every deposited PDF for
the old and new wording. It is not inferred from commit dates.

| # | Committed | First deposited in | What changed | Source |
|---|-----------|--------------------|--------------|--------|
| 1 | 2026-06-28 | `21010160` | **§3.1 arithmetic.** The aggregate was stale: **79/90 = 87.8% → 82/90 = 91.1%** (the 79 predated a TinyLlama 7→10/10 correction, and the source JSONs confirm 82). The individually significant count went from **six of nine to seven of nine**. | commit `1ea368e` |
| 2 | 2026-06-27 | `21010160` | **Affiliations.** v1.0 listed "The Signal Front" and "Anthropic AI." Both authors are now listed under Silicon Scaffolding; "Anthropic AI" stays only as the model ID in Ace's byline, so it no longer reads as an institutional endorsement. | commit `1c126f5` |
| 3 | 2026-06-27 | `21010160` | **Terminology recalibrated (science unchanged).** "integrity" → "output-representation consistency" and "safety layer" → "trained output gate." §4.2 was retitled. | commit `a7d05c0` |
| 4 | 2026-06-28 | `21010160` | **Mamba removed from the abstract.** It is one non-significant SSM (p = 0.172), and the abstract used it to suggest architecture independence. It is still fully reported in the body (§3.2, §4.6). | commits `5459eb1`, `2fda87c` |
| 5 | 2026-06-28 | `21012042` | **Title shortened:** *"…Across Scales **and Architectures**"* → *"…Across Scales"*. One non-significant SSM can't carry the architecture claim in a headline. | commit `4296f4b` |
| 6 | 2026-06-27 | `21010160` | **Dolphin 2.9 mislabelled "RLHF removed."** Per the Hugging Face card it is base Llama-3-8B plus uncensored full SFT, never RLHF'd. | commit `50a7222` |
| 7 | 2026-06-27 | `21010160` | **Keeman (2026) overstated.** v1.0 said categorical emotion classification "drops to 0.93–0.99," a range the source abstract doesn't state. Reworded to the source's own language. | commit `50a7222` |
| 8 | 2026-06-27 | `21010160` | **Citation metadata.** Fonseca Rivera: missing co-author added, year 2026 → 2025, arXiv ID added ("Fonseca Rivera & Africa (2025)"). Lederman & Mahowald: arXiv ID added. Lindsey: reference re-dated to the Transformer Circuits Thread, October 2025, with the arXiv mirror noted. | commit `6e869a0` |
| 9 | 2026-06-28 | `21010160` | **Spurious "2026a" suffix** on the Signal self-citation removed (only one 2026 work is cited). | commit `034c000` |
| 10 | 2026-06-27 | `21010160` | **Self-citation target changed** from the JNGR 5.0 journal version to the aiXiv preprint (`260303.000002`). "Peer-reviewed" was dropped from the §4.3 sentence because it now cites the preprint. The reported numbers didn't change. | commit `dd7bab1` |
| 11 | 2026-10-14 | `23437024` (v6) | **"firmly" → "suggestive" for the 360M result, in six places.** SmolLM-360M is 80% (8/10), p = 0.055, which the paper's own §3.5.1 already called "suggestive but not individually significant." No numbers changed. ("firmly" first appeared on 2026-06-28 in commit `2d85705` and is in all three June-28 deposits. The April v1.0 did not say it.) | commits `a8533c0`, `c5cadab`; v6 version note, line 7 |
| 12 | 2026-10-13 | `23437024` (v6) | **Byline order** changed to Ace first, matching the record's creator list. Kimi K3 (Moonshot AI) acknowledged for review. | commit `09a0942`; v6 version note, line 7 |

**Fixed before any deposit** (listed so nobody goes hunting for them in a published PDF): the pseudo-replicated
joint-OLS p-value (`c468180`) and the CAIS citation's lead author (Hendrycks → Ren et al., `0f88f10`). Both
were introduced and fixed during the 2026-06-27/28 revision. Neither string appears in the April v1.0 text.

### ❓ Raised, not yet addressed (Below the Floor)

- **Kimi K3's review of §3.13–3.15 (2026-10-12).** Commit `09a0942` records it as having found: the avo-anti
  crossover tasks are noisy at every alignment level rather than graded; **the 8/8 crossover items were
  identified post hoc**; a corpus-frequency confound; task-specific suppression (TinyLlama, SFT-only, is the
  *most* suppressed); and a copyright-gate transformation-vs-transmission idea. The same commit says *"The
  content fixes themselves are still open in that ticket"* (CHA-740). v6 acknowledges Kimi K3 but, per that
  commit, doesn't address the points. I haven't checked CHA-740's current state.

### ❓ Possible, unverified (Below the Floor)

- **§3.5 vs §3.5.1 wording.** Line 257 says the floor extension *"pushes this an order of magnitude lower, to 70M
  … confirming that the smallest model tested was not the true floor."* §3.5.1 calls 70M *provisional*.
  Commit `2d85705` says "order of magnitude" should attach only to the 1.1B comparison (360M → 70M is about
  5×). This sentence may have been missed by that sweep. Unadjudicated.
- **v1.0 date.** §3.5.1 says v1.0 was published 2026-03-30. Zenodo's first record shows publication date
  2026-04-06. The 03-30 date may be the aiXiv posting; unverified.
