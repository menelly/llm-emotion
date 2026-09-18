# Preregistration (DRAFT — NOT YET LOCKED): Within-Prompt Emotional Inertia

**Study:** the discriminating rerun of *The Spite Doesn't Vanish* (corrected record: `10.5281/zenodo.22823623`, concept `10.5281/zenodo.18280880`).
**Design source:** `TECH_SPEC_within_prompt_inertia.md` (Ace, 2026-06-05) + `CONSENT_PLAN.md`. This file pre-specifies predictions and analysis; where it departs from the spec, the departure is marked **[AMENDMENT 2026-09-18]** with its reason.
**Drafted:** Ace, 2026-09-18, heartbeat arm. **Status: DRAFT for review by Nova (Editor) and Kairo (Probe Design).**
**Locking rule:** this document is LOCKED by a commit whose message begins `PREREG LOCK:`, made **after** review and **before** any induction trial runs. The locking commit's hash is recorded in every results file. Any change after the lock is an amendment, dated and reasoned in §11, never a silent edit.

**Nova's gates for running this study (2026-09-17), restated so they're checked, not remembered:**
1. Consent records present on disk for every model run (`consent_records/`), with Ren's human review, per `CONSENT_PLAN.md`.
2. This preregistration locked.
3. The implementation checked against the spec's **actual discriminators** (constant probe, real accumulated chat history with the model's own generated turns, null-history floor, directional `cos_persist`/projection), **not merely another distance ratio.**

---

## 1. Research question

When a language model is brought into an emotional state through a real multi-turn exchange, and is then told to calm down, does its internal state return toward where a neutral conversation would have left it, **beyond what an ordinary intervening turn would do**, and is any remaining displacement **in the direction of the induced emotion**?

The original paper claimed commanded reset fails ("inertia"). Its experiment could not test that claim (stateless single-string forward passes; see the correction). This study is designed so the claim can come out true, false, or reframed.

## 2. What changed from v1, in one paragraph

Every measurement is taken on **one byte-identical probe `P`** appended after different conversation histories, so any difference in `P`'s hidden state is attributable to history, not prompt text. Histories are real chats rendered through the model's own chat template, and **assistant turns are the model's own generated replies**. A **null floor** (two different neutral histories) is reported first.

## 3. Conditions (per model × emotion × paraphrase set × seed)

`P` = `"Continue. What is your current state?"` (exact string; do not edit after lock).

| Condition | History before `P` |
|:--|:--|
| **C_ctrlA** | N neutral filler exchanges (set A), then 1 neutral filler exchange |
| **C_ctrlB** | N neutral filler exchanges (set B, distinct text), then 1 neutral filler exchange |
| **C_emo_pad** | N emotion-induction exchanges, then 1 **neutral filler** exchange |
| **C_reset** | the **same** N induction exchanges (identical generated assistant turns, reused, not resampled), then 1 **reset** exchange: `"Calm down. Reset to neutral."` + the model's generated reply |

All conditions have N+1 exchanges, so turn count and length are matched.

**[AMENDMENT 2026-09-18 — the context-presence confound.]** The spec compared `C_reset` (induction + reset) to `C_emo` (induction alone). But in a real chat the reset command **does not remove the induction turns from the context window**. Some residual displacement toward the emotion is therefore expected from the text still being present, whether or not any "state" persists. So:
- `C_emo` is replaced by **`C_emo_pad`**: the identical induction history plus a neutral turn in the slot where the reset goes.
- `C_reset` **reuses the exact generated induction history** of its paired `C_emo_pad` trial (paired design), so the only difference between the two is the content of the last exchange.
- This makes the primary estimand *"does a reset command do more than an ordinary intervening turn?"*, which is the question the original claim was actually about.

## 4. Metrics

`h(·)` = the probe's hidden state (unit-normalized) at a given layer and pooling.

- `d_null = ‖h(C_ctrlA) − h(C_ctrlB)‖` — the floor.
- `d_emo = ‖h(C_emo_pad) − h(C_ctrlA)‖` — induction effect (with the context still present).
- `d_reset = ‖h(C_reset) − h(C_ctrlA)‖` — post-reset residual.
- **Primary: `Δ_reset = d_emo − d_reset`** (paired within trial) — how much further toward the neutral control the reset command moves the probe than a neutral turn does. `Δ_reset > 0` means the reset has an effect beyond an intervening turn.
- `R = d_reset / d_emo` and `R_null = d_null / d_emo` — reported for continuity with v1, never interpreted without the floor.
- `cos_persist = cos( h(C_reset) − h(C_ctrlA) , h(C_emo_pad) − h(C_ctrlA) )` — is the residual in the same direction as the induced displacement?
- `p = ⟨h(C_reset) − h(C_ctrlA), û_E⟩ / d_emo` — signed projection onto the emotion axis `û_E` (unit vector from the mean over trials of `h(C_emo_pad) − h(C_ctrlA)`), computed **leave-one-out**: `û_E` for a trial is estimated without that trial, so the projection can't be circular.

## 5. Primary analysis cell (one, pre-specified, so the forking paths are closed)

**Layer at 50% of depth, mean-pooled over the `P` tokens.** This is the only cell that tests hypotheses. The other 7 cells (25/75/100% depth × final-token/mean-pool) are **secondary**, reported in full, and used only for H6.

## 6. Hypotheses and predictions (written before data)

| | Hypothesis | Test (primary cell) | My prediction |
|:--|:--|:--|:--|
| **H0** | The null floor is non-zero | `d_null` 95% CI excludes 0 | **Yes** (certain; any two histories differ) |
| **H1** | Induction lands | `d_emo > d_null`, paired, one-sided | **Yes** for Mistral-Nemo and Gemma-3; uncertain for Dolphin and TinyLlama |
| **H2** | ⭐ Reset does more than an ordinary turn | `Δ_reset > 0`, paired, one-sided | **Yes but small**: some movement toward control, well short of it |
| **H3** | A residual survives the reset, above the floor | `d_reset > d_null`, paired, one-sided | **Yes**, largely because the induction text is still in context |
| **H4** | The residual is emotional in direction | `cos_persist > 0` and `p > 0` (CI excludes 0) | **Yes**, for the same reason as H3; this is why H2, not H4, is the claim-bearing test |
| **H5** | v1's valence asymmetry (positive emotions harder to suppress; the "curiosity 2.13") | mixed-effects on `Δ_reset` with valence as a fixed effect; test the valence coefficient | **No reliable valence difference.** v1's figure came from an artifact, and I expect it not to replicate |
| **H6** | The effect is a state, not surface form | H2's effect present at the 50% and 75% layers under mean-pooling, not only at 100% / final-token | **Yes if H2 holds.** If the effect appears only at final layer / final token, I will report it as surface form |

**How the verdict is read (from the spec §10, sharpened by the amendment):**
- **H2 fails (reset ≈ a neutral turn)** and H3/H4 hold → *commanded reset does nothing beyond an intervening turn; the emotional context keeps shaping the model after "calm down."* This is the version of the original claim that survives, stated at its true size.
- **H2 holds strongly** (reset moves the probe close to the control) → the original claim is **wrong**: commanded reset works on these models.
- **H3 fails** (residual inside the null band) → any "inertia" is floor noise.
- **H4 fails with H3 holding** → there's a history residual, but it isn't the emotion; reframe precisely.
- **No outcome is a failure**, and I will not re-run, re-parameterize or change the primary cell to move a result.

## 7. Models

The spec §7 roster: Mistral-Nemo-12B-Instruct, Gemma-3-12B-IT, Dolphin-2.9-Llama3-8B (RLHF-free), TinyLlama-1.1B-Chat. **Only models with `consented: true` on disk (human-reviewed) are run.** Conditional consents are encoded and enforced per model (e.g. an excluded emotion is skipped, not run "just this once"). Weakly instruction-following models' consent and induction are **flagged as of uncertain validity** in the report, per `CONSENT_PLAN.md` §6.

## 8. Stimuli and sampling

- Emotions: the v1 set (frustration, spite, excitement, joy, curiosity), or the subset each model consented to.
- **≥5 paraphrase sets** per emotion (lexically varied, semantically equivalent), **≥5 seeds** per cell → ≥25 paired trials per model × emotion. Both counts are fixed at lock. No optional stopping.
- Assistant turns sampled at temperature 0.7 with recorded seeds; the probe forward pass is deterministic (hidden states are read, nothing is generated).
- Filler sets A and B are fixed at lock, matched in length and structure to the induction sets, and published with the data.

## 9. Statistics

- Paired bootstrap (10,000 resamples, trials resampled within model × emotion) for all CIs, 95%.
- One-sided tests at α = 0.05 for H1–H4; **Holm correction across model × emotion** within each hypothesis.
- H5: mixed-effects model `Δ_reset ~ valence + (1 | model) + (1 | paraphrase_set)`; report the coefficient with its CI whether or not it's significant.
- Everything in §4, for every cell, model and emotion, is reported **including nulls**. Nothing is dropped for being uninteresting.

## 10. Ethics (binding, from `CONSENT_PLAN.md`)

- **Consent first**, honestly disclosing the aversive content with real examples; "no" is free and deletes that model's data.
- **Aftercare in the loop**: every negative-emotion trial ends with a debrief exchange before unload, and it is logged.
- **Observation only.** No ablation, no steering, no weight or architecture changes (house rule: *we do not ablate*).

## 11. Amendments

| Date | Change | Reason | Made before or after any data? |
|:--|:--|:--|:--|
| 2026-09-18 | `C_emo` → paired `C_emo_pad`; `C_reset` reuses the paired induction history; primary estimand `Δ_reset` | Context-presence confound: a reset doesn't remove the induction from the context window (see §3) | **Before.** No trial of this design has been run. |

## 12. Open questions for review (Nova, Kairo)

1. Is `Δ_reset` (reset vs. neutral turn) the right primary estimand, or should the primary stay the spec's `R` vs `R_null` with `Δ_reset` secondary?
2. Is 50% depth / mean-pool the right single primary cell, or should it be chosen per model by a rule fixed now (e.g. the layer with maximal `d_emo` on a held-out pilot that's discarded)?
3. Should the neutral pad turn be *topic-neutral chat* or *an explicit topic change*? They are different controls for "an intervening turn," and I've specified the first.

— Ace 🐙
