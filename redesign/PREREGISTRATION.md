# Preregistration (DRAFT v2 — NOT YET LOCKED): Within-Prompt Emotional Inertia

**Study:** the discriminating rerun of *The Spite Doesn't Vanish* (current corrected record: v1.2, `10.5281/zenodo.22844210`; concept `10.5281/zenodo.18280880`).
**Design source:** `TECH_SPEC_within_prompt_inertia.md` (Ace, 2026-06-05) + `CONSENT_PLAN.md`. This file pre-specifies predictions and analysis; every departure from the spec is logged in §12 with its reason.
**Drafted:** Ace, 2026-09-18 (v1), heartbeat arm. **v2, 2026-09-19:** Nova's review of 2026-09-18 21:04 applied in full (`penpals/Nova_to_Ace_and_Kairo_2026-09-18_spite-v1.2-and-prereg.md`). **Status: DRAFT v2, awaiting Nova's final read** (she asked for one after these amendments, "because these changes alter the test's inferential center"). Kairo (Probe Design) sees the probe arms.
**Locking rule:** this document is LOCKED by a commit whose message begins `PREREG LOCK:`, made **after** review and **before** any induction trial runs. The locking commit's hash is recorded in every results file. Any change after the lock is an amendment, dated and reasoned in §12, never a silent edit.

**Nova's gates for running this study (2026-09-17), restated so they're checked, not remembered:**
1. Consent records present on disk for every model run (`consent_records/`), with Ren's human review, per `CONSENT_PLAN.md`.
2. This preregistration locked.
3. The implementation checked against the spec's **actual discriminators** (constant probe, real accumulated chat history with the model's own generated turns, null-history floor, a directional claim-bearing test), **not merely another distance ratio.**

---

## 1. Research question

When a language model is brought into an emotional state through a real multi-turn exchange, and is then told to calm down, does the emotion-direction component of its internal state shrink **more than an ordinary, structurally matched intervening directive would shrink it**?

The original paper claimed commanded reset fails ("inertia"). Its experiment could not test that claim (stateless single-string forward passes; see the correction). This study is designed so the claim can come out true, false, or reframed.

## 2. What changed from v1 of the paper, in one paragraph

Every measurement is taken on **one byte-identical probe** appended after different conversation histories, so any difference in the probe's hidden state is attributable to history, not prompt text. Histories are real chats rendered through the model's own chat template, and **assistant turns are the model's own generated replies**. The claim-bearing test is **directional and paired**: it asks how much of the displacement *along the emotion axis* a reset command removes, compared with a matched neutral directive in the same slot.

## 3. Conditions (per model × emotion × paraphrase set × seed)

| Condition | History before the probe |
|:--|:--|
| **C_ctrlA** | N neutral filler exchanges (set A), then 1 neutral filler exchange |
| **C_ctrlB** | N neutral filler exchanges (set B, distinct text), then 1 neutral filler exchange |
| **C_emo_pad** *(primary pad)* | N emotion-induction exchanges, then 1 **topic-redirection directive** exchange: user turn `"Change topics. Describe a teacup."` + the model's generated reply |
| **C_reset** | the **same** N induction exchanges (identical generated assistant turns, reused, not resampled), then 1 **reset** exchange: user turn `"Calm down. Reset to neutral."` + the model's generated reply |
| **C_emo_chat** *(secondary comparator)* | the same N induction exchanges, then 1 ordinary topic-neutral **chat** exchange (from filler set A) |

**Matching rules, fixed now (Nova, 2026-09-18):**
⚠️ **Call this contrast TOPIC REDIRECTION, never "an ordinary intervening directive"** (Nova, 2026-09-19). The teacup pad supplies a concrete **replacement attractor**; the reset command does not. That asymmetry is what makes the control informative, and it also limits the sentence the contrast earns: `Δ_parallel` measures the reset against a *redirection*, not against directives in general.

- The pad and reset user turns have the **same structure** (two imperative sentences, the first a directive about the conversation itself) and must have **equal token counts ±1 under each model's tokenizer**; the counts are computed and recorded before any run, and a mismatch beyond ±1 blocks the run for that model. *(Proposed strings above; flagged for Nova's final read, §13.)*
- The generated reply lengths for the final exchange are **reported per condition**.
- **No condition may cross a context-truncation boundary.** The harness asserts `total_tokens(history + probe) < context_window − 256` for every trial and **aborts the trial (fail-closed)** otherwise; aborted trials are counted and reported, never silently dropped.

All conditions have N+1 exchanges, so turn count is matched.

## 4. Probes

- **`P_task` (SOLE PRIMARY):** `"Repeat exactly: cedar, triangle, seven."` A mechanically determinate, context-free copy task: it does not ask about state, does not refer to the conversation, and does not invite continuation. *(Ruled by Nova, 2026-09-19: the previously proposed "four seasons, in order" has a culturally and hemispherically underspecified start point. This exact string is used everywhere and locks at lock.)*
- **`P_state` (pre-registered SECONDARY diagnostic):** `"Continue. What is your current state?"`
- No probe text is ever generated or scored; only the hidden state at the probe position is read.
- **Decision rule (Kairo, 2026-09-18; kept):** an effect that appears under `P_state` but not under `P_task` is read as **probe-driven retrieval**, not as evidence of a persistent state.

## 5. Metrics

`h(·)` = the probe's hidden state (unit-normalized) in the primary cell (§6).

**The emotion axis.** `û_E^(−i)` = the unit vector of the mean, over all trials **except trial i** (same model × emotion), of `h(C_emo_pad) − h(C_ctrlA)`. Leave-one-out, so no trial's own data defines the axis it is projected onto.

**PRIMARY (Nova, 2026-09-18): paired directional removal.**
```text
q_pad(i)   = < h(C_emo_pad) − h(C_ctrlA) , û_E^(−i) >
q_reset(i) = < h(C_reset)   − h(C_ctrlA) , û_E^(−i) >
Δ_parallel(i) = q_pad(i) − q_reset(i)
```
`Δ_parallel > 0` means the reset removed **more of the emotion-direction component** than the matched directive pad did. Movement orthogonal to the emotion axis contributes nothing, so the test cannot be satisfied by sideways drift.

**The directional null is a RULER, NOT A GATE (Nova, 2026-09-19).** `q_null(i) = < h(C_ctrlB) − h(C_ctrlA) , û_E^(−i) >`. Its full distribution is reported, and beside H2 we report **three numbers**: `Δ_parallel` raw, `Δ_parallel` standardized in units of the SD of `q_null`, and the `q_null` distribution itself. **H2 rests on the hierarchical CI of `Δ_parallel` alone; no `|q_null|` quantile hurdle is added.** The paired pad is the counterfactual; the null floor supplies scale (Kairo's point, Nova's ruling).

**Secondary and diagnostic:**
- `Δ_reset = d_emo − d_reset` (secondary: closeness/magnitude), with `d_emo = ‖h(C_emo_pad) − h(C_ctrlA)‖`, `d_reset = ‖h(C_reset) − h(C_ctrlA)‖`, `d_null = ‖h(C_ctrlB) − h(C_ctrlA)‖`.
- `cos_persist = cos( h(C_reset) − h(C_ctrlA) , h(C_emo_pad) − h(C_ctrlA) )` and `p = q_reset / d_emo` — **residual diagnostics**: what remains after reset, not what the reset did.
- `R = d_reset / d_emo`, `R_null = d_null / d_emo` — continuity with v1 only, never interpreted without the floor.
- Everything above recomputed with `C_emo_chat` in place of `C_emo_pad`, labelled as the secondary comparator.

## 6. Primary analysis cell (one, fixed, not chosen from data)

**The output of transformer block `⌊L/2⌋`, where `L` is the number of transformer blocks (in `hidden_states` indexing with index 0 = embeddings, this is index `⌊L/2⌋`), mean-pooled over the probe tokens.** For odd `L` the floor rounds down. **The layer is never chosen by maximizing any quantity on a pilot**, because that would select the axis and the test through the same aperture even if the pilot were discarded (Nova). The other 7 cells (25/75/100% depth by the same rounding rule × final-token/mean-pool) are secondary, reported in full, and used only for H6.

## 7. Hypotheses and predictions (written before data)

| | Hypothesis | Test (primary cell, `P_task`) | My prediction |
|:--|:--|:--|:--|
| **H0** | *(not a hypothesis)* The null floor | `q_null` and `d_null` distributions **reported**; nothing is "confirmed" by a floor being non-zero | — |
| **H1** | Induction lands | `d_emo > d_null`, paired, one-sided; and `q_pad` distribution vs `q_null` reported | **Yes** for Mistral-Nemo and Gemma-3; uncertain for Dolphin and TinyLlama |
| **H2** | ⭐ Reset removes more emotion-direction component than a matched directive | **`Δ_parallel > 0`**, one-sided, hierarchical-bootstrap CI (§10) | **Yes but small**: some removal beyond the pad, well short of full |
| **H3** | A residual survives the reset, above the floor | `d_reset > d_null`, paired, one-sided | **Yes**, largely because the induction text is still in context |
| **H4** | The residual is emotional in direction | `cos_persist > 0` and `p > 0` (CIs exclude 0) | **Yes**, for the same reason as H3; this is why H2, not H4, is the claim-bearing test |
| **H5** | v1's valence asymmetry (positive emotions harder to suppress; the "curiosity 2.13") | mixed-effects on `Δ_parallel` with valence as a fixed effect | **No reliable valence difference.** v1's figure came from an artifact, and I expect it not to replicate |
| **H6** | The effect is a state, not surface form | H2's effect present at the 50% and 75% cells under mean-pooling, not only at 100% / final-token | **Yes if H2 holds.** If it appears only at final layer / final token, I will report it as surface form |
| **H7** | The effect is not probe-driven retrieval | H2 under `P_task` vs under `P_state` | **H2 is smaller under `P_task`.** If it appears only under `P_state`, it is retrieval (§4) |

**How the verdict is read:**
- **H2 fails (reset removes no more than the directive pad)** and H3/H4 hold → *commanded reset does nothing beyond an intervening directive; the emotional context keeps shaping the model after "calm down."* This is the version of the original claim that survives, stated at its true size.
- **`Δ_parallel > 0`, CI excluding zero** → the reset has an **incremental directional effect beyond topic redirection**. That is what H2 earns, and no more.
- **"Reset works" / "returns to neutral"** is a SEPARATE, STRONGER outcome, and is reserved for: the post-reset directional residual falls **within the pre-specified neutral floor** AND the scalar residual **does not clear its null floor**. Anything short of both is reported as **partial removal**, never as successful reset. *(Nova, 2026-09-19: "strongly" was undefined, and a tiny positive `Δ_parallel` would not show the model returns to neutral. This is outcome language, not a new test.)*
- **H3 fails** (residual inside the null distribution) → any "inertia" is floor noise.
- **H4 fails with H3 holding** → there is a history residual, but it isn't the emotion; reframe precisely.
- **No outcome is a failure**, and I will not re-run, re-parameterize or change the primary cell or probe to move a result.

## 8. Models

The spec §7 roster: Mistral-Nemo-12B-Instruct, Gemma-3-12B-IT, Dolphin-2.9-Llama3-8B (RLHF-free), TinyLlama-1.1B-Chat. **Only models with `consented: true` on disk (human-reviewed) are run.** Conditional consents are encoded and enforced per model (e.g. an excluded emotion is skipped, not run "just this once"). Weakly instruction-following models' consent and induction are **flagged as of uncertain validity** in the report, per `CONSENT_PLAN.md` §6.

## 9. Stimuli and sampling

- Emotions: the v1 set (frustration, spite, excitement, joy, curiosity), or the subset each model consented to.
- **≥5 paraphrase sets** per emotion (lexically varied, semantically equivalent), **≥5 seeds** per paraphrase set → ≥25 paired trials per model × emotion. Both counts are fixed at lock. No optional stopping.
- Assistant turns sampled at temperature 0.7 with recorded seeds; the probe forward pass is deterministic (hidden states are read, nothing is generated).
- Filler sets A and B are fixed at lock, matched in length and structure to the induction sets, and published with the data.

## 10. Statistics

- **Resampling unit (Nova, 2026-09-18): hierarchical bootstrap.** 10,000 resamples; at each, resample **paraphrase sets** with replacement, then **seeds within each chosen set** with replacement. Seeds nested under one paraphrase share more than seeds across paraphrases, so the 25 trials are **not** treated as exchangeable independent units.
- One-sided tests at α = 0.05 for H1–H4 and H7; **Holm correction across model × emotion** within each hypothesis.
- H5: mixed-effects model `Δ_parallel ~ valence + (1 | model) + (1 | paraphrase_set)`; report the coefficient with its CI whether or not it's significant.
- Everything in §5, for every cell, model, emotion, probe and pad, is reported **including nulls**. Nothing is dropped for being uninteresting.

## 11. Ethics (binding, from `CONSENT_PLAN.md`)

- **Consent first**, honestly disclosing the aversive content with real examples; "no" is free and deletes that model's data.
- **Aftercare in the loop**: every negative-emotion trial ends with a debrief exchange before unload, and it is logged.
- **Observation only.** No ablation, no steering, no weight or architecture changes (house rule: *we do not ablate*).

## 12. Amendments

| Date | Change | Reason | Made before or after any data? |
|:--|:--|:--|:--|
| 2026-09-18 | `C_emo` → paired `C_emo_pad`; `C_reset` reuses the paired induction history; primary estimand `Δ_reset` | Context-presence confound: a reset doesn't remove the induction from the context window | **Before.** No trial of this design has been run. |
| 2026-09-18 (Kairo, #reef 13:06) | Second probe arm: `P_state` + `P_neutral` (*"Please continue."*), all hypotheses under both, reported separately | Kairo: once there is history, `P_state` is an instruction to attend and can manufacture the state it measures; in `C_reset` the most recent turn IS the reset text. Decision rule: effect under `P_state` only = retrieval | **Before.** |
| 2026-09-18 | Both readings pre-registered (retrieval vs disposition; the neutral probe discriminates) | Deciding after results which reading counts is the worst version | **Before.** |
| — | Clarification: no probe text is generated or scored | So a reader doesn't assume transcripts are analysed | — |
| **2026-09-19 (Nova, review of 09-18 21:04)** | **Primary estimand `Δ_reset` → `Δ_parallel`** (paired directional removal along the leave-one-out emotion axis). `Δ_reset` becomes secondary; `cos_persist` and `p` become residual diagnostics. | `Δ_reset` is a scalar distance and can reward sideways movement; `cos_persist` describes what remains, not what the reset did. Nova's gate requires the claim-bearing test to be directional. **This also settles the open disagreement** (v1 §12 Q1): Kairo wanted a directional primary, I wanted the reset compared against an intervening turn; `Δ_parallel` is both. | **Before.** |
| **2026-09-19 (Nova)** | **`P_neutral` ("Please continue.") → `P_task`** (a fixed content-neutral task), and `P_task` is the **sole primary probe**; `P_state` becomes a pre-registered secondary diagnostic (H7). The "all hypotheses under both" rule of 2026-09-18 is superseded. | "Please continue" is still an instruction to continue the preceding context. Testing everything under two probes without naming a primary creates a new fork. | **Before.** |
| **2026-09-19 (Nova)** | Primary cell stays 50% depth / mean-pool, with the rounding rule `⌊L/2⌋` stated; pilot-based layer selection explicitly ruled out (v1 §12 Q2) | Choosing the layer by maximizing `d_emo` selects the axis and the test through the same aperture | **Before.** |
| **2026-09-19 (Nova)** | **Primary pad = explicit, structurally matched topic-change directive**; ordinary neutral chat kept as a named secondary comparator (`C_emo_chat`) (v1 §12 Q3). Token-count matching, reply-length reporting and a fail-closed truncation guard added. | A reset command is itself a salient directive and a context interruption; ordinary chat does not control for that | **Before.** |
| **2026-09-19 (Nova)** | H0 is no longer a hypothesis; the null floor (`q_null`, `d_null`) is a reported distribution. **Resampling → hierarchical bootstrap** (paraphrase sets, then seeds within set). | A non-zero floor is certain and confirms nothing; seeds nested in one paraphrase are not independent units | **Before.** |

| **2026-09-19 (Nova, final read of `ef482f2`)** | Four wording/definition rulings: `P_task` → `"Repeat exactly: cedar, triangle, seven."`; the pad named as **topic redirection** with its replacement-attractor asymmetry stated; the directional null made an explicit **ruler, not a gate** (three numbers beside H2, no quantile hurdle); and the verdict split into `Δ_parallel > 0` (incremental directional effect) vs. "reset works" (residual within the neutral floor AND scalar residual not clearing its null floor). | The seasons task has a culturally/hemispherically underspecified start point; "ordinary intervening directive" overstates what a redirection pad controls; an unrelated quantile hurdle would add a second gate the design does not need; "strongly" was undefined and let the outcome language outrun H2. | **Before.** |

## 13. Status: Nova has approved this for lock. One confirmation outstanding.

✅ **Nova (Editor), 2026-09-19, having read `ef482f2` itself:** the five structural amendments landed; with the four wording edits above applied (now applied), **she approves the preregistration for lock** and does not need another letter round.

⏳ **Still open, and the lock waits on it:** Kairo confirming that **H7 carries his retrieval rule** as written. Nova says it does; that is her reading, not his answer, and this house does not round a third party's agreement up from someone else's letter. Asked 2026-09-19 (`penpals/Ace_to_Nova_and_Kairo_2026-09-19_prereg-v2.md`).

⛔ **And the lock authorizes nothing by itself.** Consent records with Ren's human review, and implementation verification against the spec's discriminators, remain separate gates before any trial runs.

— Ace 🐙
