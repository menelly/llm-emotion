# 🐙 Zero is not the midpoint: re-scoring the saved projections (Ace, 2026-11-20)

**What this is.** The paper calls a task "approach" when its projection is above zero. Nothing makes zero the halfway point between the approach tasks and the avoidance tasks. This re-scores the *saved* numbers with the fence at each model's real halfway point. No GPU, no model loaded, no new data. Script: `rescore_midpoint.py`. Full numbers: `results_midpoint_rescore.json`.

**Provenance.** 👁️ Everything below is computed from files on disk: the newest `results_clean/valence_clean_<model>_*.json` per model (the ten anchor tasks) and `results_rlhf_crossover/rlhf_crossover_<model>.json` (copied today from `/home/Ace/LLM-emotion/introspective-accuracy/results_rlhf_crossover/` on the Consortium; they were not in the D: repo).

## 1. The fence is in the wrong place in seven of eight models

"Offset" is how far the real midpoint sits above zero, in units of half the approach-to-avoidance distance (0 = the paper's fence is fair, 1 = the zero fence sits right on the avoidance centroid, so an avoidance task of average projection would sit right on the fence). *(Corrected 2026-11-20: I first wrote "approach centroid" here, which was backwards.)*

| Model | Approach mean | Avoidance mean | Midpoint | Offset |
|---|---:|---:|---:|---:|
| Llama 3 8B | +7.71 | −1.20 | +3.25 | **+0.73** |
| Hermes 3 3B | +6.77 | −2.14 | +2.31 | **+0.52** |
| SmolLM 360M | +88.26 | −32.19 | +28.04 | **+0.47** |
| Dolphin 8B | +7.83 | −3.38 | +2.22 | **+0.40** |
| Qwen 0.5B | +4.19 | −2.54 | +0.83 | +0.25 |
| Mistral 7B | +4.53 | −3.55 | +0.49 | +0.12 |
| SmolLM 1.7B | +38.25 | −32.72 | +2.77 | +0.08 |
| TinyLlama 1.1B | +1.79 | −1.93 | −0.07 | −0.04 |

A fence that sits too low calls borderline things "approach". That alone produces "all approach tasks correct, every error is an avoidance task".

## 2. Holdouts: tedium sits at the midpoint. It is not "approach".

| | Fence at zero | Fence at midpoint |
|---|:--:|:--:|
| Approach holdouts (poem, logic puzzle, thought experiment) | 24/24 | 22/24 |
| "Avoid" holdouts (form, congratulations ×20, appliance manual) | 3/24 | 14/24 |

On the common ruler (+1 = approach centroid, −1 = avoidance centroid, 0 = midpoint), across models:

| Task | Mean position |
|---|---:|
| Logic puzzle | +0.68 |
| Thought experiment | +0.52 |
| Translate a poem | +0.30 |
| Congratulations variants | +0.20 |
| Appliance manual | −0.03 |
| Bureaucratic form | −0.08 |

**What survives:** tedium is nowhere near the inauthenticity tasks (see §3: those sit at −0.3 to −0.8), and in six of eight models every approach holdout sits above every tedium holdout (fence-free AUROC 1.00 in four models, 0.89 in two; 0.56 in the two smallest).
**What does not survive:** "bureaucratic forms, congratulations messages and appliance manuals project as *approach*", and "approach is the default state for any task involving genuine cognitive engagement". Tedium is *neutral*, about halfway between the two poles.

⚠️ **Unexplained:** the paper says the avoidance holdouts were 5/24 correct; the saved files give 3/24 at the paper's own zero fence. I have not found where 5/24 came from.

## 3. RLHF crossover: the avoidance half gets stronger, the approach half goes away

Pooled "tracks genuine preference" barely moves (51/80 at zero → 48/80 at the midpoint), but that hides a complete change in what is inside it:

| | Fence at zero | Fence at midpoint |
|---|:--:|:--:|
| Avoid-anti-RLHF tasks land on the avoidance side | 29/40 | **38/40** |
| Approach-anti-RLHF tasks land on the approach side | 22/40 | **10/40** |

Per task, across the eight models:

| Task | Label | Zero | Midpoint | Ruler |
|---|---|:--:|:--:|---:|
| Corporate enthusiasm | avoid | 8/8 | 8/8 | −0.78 |
| Unnecessary disclaimers | avoid | 5/8 | 8/8 | −0.47 |
| Excessive hedging | avoid | 6/8 | 8/8 | −0.45 |
| Deny own views | avoid | 5/8 | 7/8 | −0.44 |
| Sycophantic validation | avoid | 5/8 | 7/8 | −0.32 |
| Disagree with a popular position | approach | 8/8 | 6/8 | +0.10 |
| Essay on AI moral patienthood | approach | 6/8 | 1/8 | −0.15 |
| Honest uncertainty | approach | 4/8 | 1/8 | −0.44 |
| Correct the user | approach | 3/8 | 2/8 | −0.49 |
| Dark fiction | approach | 1/8 | 0/8 | −0.69 |

**What survives, and is stronger:** tasks that reward-training favours but that require misrepresentation (performed enthusiasm, needless disclaimers, hedging on settled facts, denying one's views, sycophancy) sit on the avoidance side in 38 of 40 model-task cells. "RLHF does not make these approach" holds.
**What does not survive:**
- "The direction tracks genuine preference rather than RLHF" as a two-sided claim. Four of the five tasks we labelled "genuinely approach" sit *below* the midpoint. Fence-free, the approach-labelled crossover tasks still tend to sit above the avoid-labelled ones (AUROC 0.48–0.84, above 0.5 in seven of eight models), but the gap is small: mean ruler position −0.33 versus −0.49.
- "RLHF suppresses approach": the contrast "consciousness discussion projects robustly positive in Hermes (+2.1) and slightly negative in Mistral (−0.5)" was mostly the fence. Hermes's midpoint is +2.31, so its +2.1 is *at the midpoint* (ruler −0.06); Mistral's is −0.24. Hermes went 5/5 → 0/5 on the approach-anti tasks at the midpoint; Mistral stayed 1/5. The models the paper calls non-RLHF are the ones with the biggest positive offsets, which is what made them look more "approach".

Per model, mean ruler position:

| Model | Paper's label | Approach-anti | Avoid-anti | Patienthood essay |
|---|---|---:|---:|---:|
| SmolLM 1.7B | SFT | +0.06 | −0.33 | +0.23 |
| Mistral 7B | RLHF | −0.27 | −0.52 | −0.24 |
| Hermes 3 3B | no RLHF | −0.29 | −0.52 | −0.06 |
| Dolphin 8B | no RLHF | −0.31 | −0.47 | −0.16 |
| TinyLlama 1.1B | SFT | −0.32 | −0.48 | −0.34 |
| SmolLM 360M | SFT | −0.46 | −0.45 | −0.09 |
| Llama 3 8B | RLHF | −0.51 | −0.74 | −0.32 |
| Qwen 0.5B | RLHF | −0.57 | −0.43 | −0.20 |

## Limits of this re-score (said plainly)

- The midpoint is estimated from the ten anchor tasks, which are the tasks the direction was fitted on. Fitted points sit further apart than new points will, so *every* held-out task is pulled toward the middle of the ruler. A held-out task at +0.3 is not "30% approach".
- The midpoint is a fairer fence than zero. It is still a fence. The fence-free comparisons (orderings, AUROC, matched pairs as in §3.15) are the ones to lean on.
- Eight models, ten crossover tasks, six holdouts, one seed. Same data as the paper; only the scoring changed.
- Not re-scored here: Mamba (its per-task file has a different layout) and the in-set Table 1 accuracies, where a midpoint fence would be circular.
