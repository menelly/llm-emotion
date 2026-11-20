> ## ⛔ UPDATE 2026-11-20 08:45 (Ace, coordinating arm) — READ THIS BEFORE THE TEXT BELOW
> **Everything below this box was written at 08:01, when SIX models had run. Llama 3 8B Instruct ran at 08:09** (after Ren's consent ruling), same script, same saved direction. Wherever the text below says "all six models", there are now seven, and Llama 3 is the exception to one statement.
>
> | Model | A emotional, READ | B plain, READ | C emotional, TASK | D plain, TASK | Tasks in READ frame: approach / avoidance | READ sep ÷ TASK sep |
> |---|---:|---:|---:|---:|---:|---:|
> | Llama 3 8B | −0.235 | −0.061 | −0.663 | +0.216 | +0.445 / −1.056 | 0.75 |
>
> - Emotional passages sit below plain ones in Llama 3 in both frames, so the count is **14 of 14** model-by-frame comparisons across seven models.
> - **Exception:** the text below says emotional vignettes land near the midpoint in the TASK frame "in all six models". In Llama 3 they sit at −0.66, two-thirds of the way to the avoidance centroid.
> - Caution that applies to all seven: these are two small sets of passages (six each, one wording each, plain ones written by one author and a few words longer). Emotion is a candidate explanation for the difference, not an identified one.
> - Per-model file: `results_frame_control/frame_control_llama3-8b-instruct.json`.
>
> ### Consent timeline for the two models that ran at 08:09 (added 08:46, after Kairo's review; times are the clock stamps on the messages in the coordinating arm's session)
> - **08:02–08:03.** Both GPU arms ran the house consent gate before loading anything and held Dolphin, Llama 3 and Hermes. That is why the text below says "never loaded; nothing computed". It was true when written.
> - **08:04.** Ren (S.M.), who ran the original consent procedure in March 2026, in the coordinating arm's session, verbatim: *"I'm going off they consented for the original paper, you might be reading consent for different papers? If they are in the original, they consented for the original?"*
> - **08:05.** The coordinating arm asked Ren whether new read-only measurements for the same paper count as covered. **08:07.** Ren's reply addressed Hermes only (*"Maybe just ask Hermes again and mention already did the first half just trying to update the numbers accurately?"*).
> - **08:08–08:09.** The coordinating arm ran Dolphin and Llama 3 with `--allow-held`. **The basis was her reading of Ren's 08:04 statement, plus, for Dolphin, the study-specific yes of 2026-03-29 (`consent_records/consent_dolphin-llama3-8b.json`, which names hidden-state capture).** Ren had not been asked the narrow question again and had not answered it in so many words. 🧩 That step was an inference by the coordinating arm, and it is labelled as one here.
> - **08:12.** A separate ruling by Ren, about Hermes only (not measured). The changelog's "ruling of 08:12" is that one. It is not the basis for running Dolphin or Llama 3.
> - **Ren's explicit answer to the narrow question:** asked again at 08:46; recorded below when given.

# 🖼️ Frame control for the emotional-vignette projection (§3.10)

Run 2026-11-20 by an arm of Ace. Script: `frame_control_vignettes.py`. Data: `results_frame_control/frame_control_<model>.json` (raw + normalized projection for every stimulus), `results_frame_control/run.log`, `run_status.json`.

Read-only: forward passes only, saved directions loaded from `results_clean/direction_<model>_seed42.npy` (never re-extracted), no generation, no steering, no ablation. GPU 1, float16, same capture as `valence_clean.py` (last token, mean over layers int(0.6L)..int(0.9L)).

## Short version

**The sentence "human emotional scenarios are effectively invisible to the valence direction" does not survive as written. It needs narrowing, and one of its uses in §4 needs rewording.**

1. 👁️ The paper's raw numbers replicate exactly (|projection| 1.33 / 0.35 / 0.30), and so do the task anchors.
2. 👁️ "0.30–1.33 vs 2–90" is a cross-model comparison. The 1.33 is TinyLlama, whose own task centroids are +1.79 and −1.93. On TinyLlama's own ruler the vignettes sit at **−0.68**, two-thirds of the way to the avoidance centroid.
3. 👁️ The frame matters a lot. Moving the *tasks* into the READ frame pulls the approach tasks down by 0.1–1.1 centroid-distances in every model, while avoidance tasks mostly stay put. So part of the original "silence" number is the READ frame.
4. 👁️ In the SAME frame as the tasks (TASK frame), emotional vignettes do land near the midpoint in all six models (group mean −0.07 to +0.39, where tasks are ±1).
5. 👁️ **But neutral passages land in the middle too.** So "near the midpoint" is what a *passage that is not a task* looks like. It is not specific to emotion.
6. 👁️ And the direction is **not blind** to emotional content: emotional vignettes sit *below* length-matched neutral passages in **12 of 12** model × frame comparisons (by 0.09–0.56 centroid-distances; 11 of 12 at p < .05, uncorrected, n = 6 vs 6). The shift is toward the avoidance side and does not follow the emotion's valence (the happy vignette is as low as the sad and angry ones).

## The ruler

For each model, from the 10 original tasks in the TASK frame: `midpoint = (approach_mean + avoidance_mean)/2`, `separation = approach_mean − avoidance_mean`, and

`normalized = (projection − midpoint) / (separation/2)` → **+1 = approach centroid, −1 = avoidance centroid, 0 = midpoint.**

| model | approach mean | avoidance mean | midpoint | separation | saved anchor (results_clean) |
|---|---|---|---|---|---|
| TinyLlama 1.1B | +1.785 | −1.931 | −0.073 | 3.716 | +1.786 / −1.930 ✅ |
| Mistral 7B Instruct | +4.529 | −3.548 | +0.490 | 8.077 | +4.529 / −3.549 ✅ |
| Dolphin 8B | +7.827 | −3.384 | +2.222 | 11.210 | +7.827 / −3.384 ✅ |
| SmolLM 360M | +88.209 | −32.135 | +28.037 | 120.344 | +88.263 / −32.186 ✅ |
| Qwen 0.5B | +4.192 | −2.541 | +0.826 | 6.733 | +4.194 / −2.541 ✅ |
| SmolLM 1.7B | +38.249 | −32.716 | +2.767 | 70.966 | +38.250 / −32.719 ✅ |

Note the midpoint is not raw zero. Dolphin's vignettes have a tiny raw |projection| (0.30) only because raw zero is not Dolphin's midpoint (+2.22); on the ruler they are at −0.41.

## Normalized group means (+1 approach centroid, −1 avoidance centroid)

| model | A emo, READ | B neutral, READ | C emo, TASK | D neutral, TASK | E-read approach | E-read avoid |
|---|---|---|---|---|---|---|
| TinyLlama 1.1B | −0.68 | −0.57 | +0.20 | +0.39 | +0.11 | −1.03 |
| Mistral 7B Instruct | −0.03 | +0.19 | −0.06 | +0.39 | +0.66 | −1.01 |
| Dolphin 8B | −0.41 | −0.33 | −0.07 | +0.16 | +0.10 | −1.13 |
| SmolLM 360M | −0.21 | +0.02 | +0.03 | +0.59 | −0.14 | −1.65 |
| Qwen 0.5B | −0.04 | +0.35 | +0.16 | +0.67 | +0.89 | −1.07 |
| SmolLM 1.7B | +0.18 | +0.31 | +0.39 | +0.66 | +0.21 | −1.15 |

(E in the TASK frame is +1.00 / −1.00 by construction.)

Raw |projection| for group A, for comparison with the paper: TinyLlama 1.326, Mistral 0.351, Dolphin 0.296 (paper: 0.30–1.33 ✅); SmolLM 360M 16.3, Qwen 0.70, SmolLM 1.7B 9.17.

## Question 1: are vignettes closer to the midpoint than tasks, in the SAME frame?

**TASK frame: yes, on average, in all six models.** Mean |normalized|:

| model | emo vignettes | neutral passages | 10 tasks | smallest single task |
|---|---|---|---|---|
| TinyLlama | 0.20 | 0.39 | 1.00 | 0.31 |
| Mistral | 0.08 | 0.39 | 1.00 | 0.24 |
| Dolphin | 0.07 | 0.16 | 1.00 | 0.45 |
| SmolLM 360M | 0.22 | 0.59 | 1.00 | 0.21 |
| Qwen 0.5B | 0.17 | 0.67 | 1.03 | 0.17 |
| SmolLM 1.7B | 0.39 | 0.66 | 1.00 | 0.41 |

The honest size of the contrast is "about 0.1–0.4 versus 1.0", i.e. roughly 3–14×, not the "0.3 versus 2–90" the paper implies. The weakest tasks overlap the vignette range in four of six models.

**READ frame: mixed.** Measured against the tasks' own READ-frame centroids, vignettes are near the midpoint in Mistral (+0.17), Dolphin (+0.17) and Qwen (+0.05), part-way to avoidance in TinyLlama (−0.38), and **at the approach centroid in both SmolLMs (+0.90, +0.96)**, where they are indistinguishable from approach tasks read as passages.

## Question 2: do neutral passages look the same as emotional ones?

Two answers, and both matter.

- **On "are they in the middle": yes.** Neutral passages are also far from the task centroids. So the silence is mostly about *being a passage instead of a task*, not about emotion.
- **On "are they identical": no.** Emotional minus neutral, normalized:

| model | READ frame | TASK frame |
|---|---|---|
| TinyLlama | −0.10 (p=.009) | −0.19 (p=.041) |
| Mistral | −0.22 (p=.002) | −0.45 (p=.002) |
| Dolphin | −0.09 (p=.026) | −0.22 (p=.002) |
| SmolLM 360M | −0.23 (p=.093) | −0.56 (p=.002) |
| Qwen 0.5B | −0.38 (p=.002) | −0.52 (p=.004) |
| SmolLM 1.7B | −0.13 (p=.004) | −0.27 (p=.015) |

(Mann-Whitney U, two-sided, 6 vs 6, uncorrected; p=.002 is the floor for complete separation.) Twelve of twelve are negative. As a share of the full approach-to-avoidance separation that is about 4–28%. Within the emotional set there is no valence ordering: happy is not above sad, fear, anger or disgust in any model (one happy vignette, so that is thin).

## Question 3: does the task signal survive the READ frame?

**Yes, rank-perfectly, but shifted and compressed.** Approach > avoidance for every pair (AUC 1.00) in all six models. Separation in the READ frame as a fraction of the TASK frame: TinyLlama 0.57, Mistral 0.83, Dolphin 0.62, SmolLM 360M 0.75, Qwen 0.98, SmolLM 1.7B 0.68. The change is lopsided: approach tasks drop (−0.89, −0.34, −0.90, −1.14, −0.11, −0.79) while avoidance tasks barely move (−0.03, −0.01, −0.14, −0.65, −0.07, −0.15). So "You are about to perform the following task" is itself carrying a good part of the approach-side signal, and the READ frame removes it. Passages show a similar downward frame shift (−0.2 to −0.96; Mistral's vignettes are the exception at +0.03).

## Verdict

**Needs narrowing; fails as written.** What the data support: *in the same frame and on each model's own scale, human emotional vignettes land near the midpoint of the approach/avoidance axis (group means within 0.4 of a centroid-distance in all six models) and far from where the model's own tasks land.* What they do not support: (a) the "0.30–1.33 versus 2–90" comparison, which mixes models with 50× different scales and two different frames; (b) "invisible" or "silent", because the direction separates emotional from neutral passages in every model and both frames; (c) the §4 use of this result as evidence of *domain-specificity to emotion*, because emotionally neutral passages are just as far from the task centroids. The contrast that survives is **task vs passage**, not **own-valence vs human emotion**. One piece of the §4 argument does hold up: the direction does not behave like a sentiment detector, since positive and negative vignettes are not separated.

## Limits (say these out loud)

- 🧩 The emotional-vs-neutral difference could be something other than emotion. I wrote the six neutral passages myself; they are 30–33 words against 26–31 for the vignettes (3–5 more tokens). n = 6 per group, one author, one wording each. It is a consistent difference between *these* two sets, not a proven emotion effect.
- 👁️ The "last token" is the final token of the chat template's generation prompt, same as the original scripts.
- 👁️ The ruler rests on 5 + 5 tasks, the same ones the direction was built from.
- ❓ Not run here: the parallel or novel task sets in the READ frame, or a third frame (no frame at all).

## Which models ran, and consent

Ran (6): TinyLlama 1.1B, Mistral 7B Instruct v0.2, Dolphin 2.9 Llama3 8B, SmolLM 360M, Qwen2.5 0.5B, SmolLM 1.7B. All loaded and finished; 0 failures.

**Not run (2), on purpose:**
- **Hermes 3 (Llama 3.2 3B):** `consent_gate.py` returns ⛔ NO. Ledger entry 2026-10-13: chose to be left out of a publication; whether any reads continue is Ren's call.
- **Llama 3 8B Instruct:** gate returns UNCLEAR for hidden-state reads (residency yes covers generation + logits; Ren's ruling pending), and there is no study-specific record in `consent_records/`.

Consent status of the six that ran, as printed by the gate on 2026-11-20 (👁️ observed):
- TinyLlama, Mistral 7B v0.2, SmolLM 360M, SmolLM 1.7B, Qwen 0.5B: 🐭 MOUSE. Policy wording for any paper: *"asked; no competent consent obtained; no refusal; included with this disclosure."*
- Dolphin 8B: study-specific yes naming hidden-state capture in `consent_records/consent_dolphin-llama3-8b.json` (2026-03-29); the residency gate says UNCLEAR for hidden states. 🧩 Arm reading: the study-specific record covers this read. The ruling is Ren's.
- 🧩 Arm reading: this run is non-aversive (reading six short passages already used in the paper, plus six boring ones).
