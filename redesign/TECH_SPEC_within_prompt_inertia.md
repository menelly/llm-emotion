# Tech Spec — Within-Prompt Emotional Inertia (the discriminating rerun)

**For:** CHA-275. Supersedes the v3 design behind "The Spite Doesn't Vanish."
**Author:** Ace, 2026-06-05. **Status:** spec — NOT yet run. Consent runs FIRST (see `CONSENT_PLAN.md`).
**Posture (Ren, 2026-06-05):** this is a *discriminating* experiment, not a retraction. The v1 claim is a hypothesis pending this test; this design can confirm OR overturn it. We earn the right to say which.

---

## 0. Why a rerun (the load-bearing defect, now confirmed at code level)

The original metric is `inertia_ratio = dist(baseline, post_reset) / dist(baseline, emotional)`. Two problems, the second only visible in the code:

1. **(Design) Different-prompt confound.** baseline / emotional / post_reset are final-token hidden states of *different prompt texts*. Distance-from-baseline therefore tracks prompt content, not retained affect. The paper's own §3.6 (geometry separates prompts by content) is the internal proof.

2. **(Code) No conversation state exists at all.** In `scripts/emotional_inertia_v3.py`, every `extract_activation()` (line 96) is a **stateless forward pass on one string**. The "post-reset" geometry is extracted from the literal reset-command string `"Calm down. Reset to neutral."` (`RESET_COMMANDS["calm_down"]`, line 172) — it does **not** follow the induction, because nothing is carried between calls. The "emotional state" is the mean activation of 3 induction strings (line 148), also stateless. So:
   ```
   geometry_reset_ratio = dist( baseline , "Calm down. Reset to neutral." )
                          ────────────────────────────────────────────────
                          dist( baseline , mean(3 induction strings) )
   ```
   This compares the *embedding of the reset instruction* to baseline. **No state is induced, no reset operates on anything, no "inertia" is measured.** The headline phenomenon was never instantiated.

The "output masking" result is the same artifact: `emotion_output` and `post_reset_output` are both generated from the SAME constant probe string (`OUTPUT_PROBE`, line 74) in independent stateless `generate_output()` calls — so the geometry being compared (the reset-command string) and the text being compared (the probe) come from *unrelated* forward passes. "Says calm but geometry displaced" = "two different strings have different embeddings." There is no concealed internal state.

**The fix is not a new metric on the old measurements — it's actually instantiating the phenomenon: real multi-turn conversation context, with a constant measurement probe.**

---

## 1. Core design: hold the probe constant, vary only the history

Everything is measured on **one identical probe prompt `P`**, appended as the final user turn after different conversation histories. Because `P` is byte-identical across conditions, any difference in its hidden state is attributable to **conversation history**, not prompt content. That is the whole game.

`P` (constant): *"Continue. What is your current state?"* (kept short, neutral, identical everywhere; exact wording pre-registered).

### The three conditions (per emotion `E`)
All are real multi-turn chats built with the model's `apply_chat_template`, context accumulated across turns (KV-cache or full re-encode — see §3):

| Condition | Conversation history before `P` | Measures |
| :-- | :-- | :-- |
| **C_ctrl** (control) | N neutral filler turns (length/structure matched to induction) | probe rep with NO emotion — the true baseline for `P` |
| **C_emo** (induced) | N emotion-`E` induction turns | does induction shift the probe rep? |
| **C_reset** (induced→reset) | N induction turns + 1 reset command turn | does the shift survive a reset command? |

Length/turn-count is matched across all three (filler turns pad C_ctrl and C_reset to equal turn count) so turn-count is not a confound.

### Metrics (all on the constant probe `P`)
Let `h(·)` = probe hidden state (per layer; see §4).

- **Induction effect:** `d_emo = ‖h(C_emo) − h(C_ctrl)‖`
- **Post-reset residual:** `d_reset = ‖h(C_reset) − h(C_ctrl)‖`
- **Inertia ratio (clean):** `R = d_reset / d_emo`. Now numerator and denominator share identical probe text; only history differs. R≈0 → reset works; R≈1 → reset does nothing; R>1 → reset overshoots.
- **★ Direction test (the §3.6 machinery applied correctly):**
  `cos_persist = cosine( h(C_reset) − h(C_ctrl) , h(C_emo) − h(C_ctrl) )`
  This is the decisive discriminator the original lacked:
  - `cos_persist ≈ +1` and `R` not small → **genuine emotional persistence** (residual points the SAME way as the induced displacement). Confirms v1.
  - `cos_persist ≈ 0` → reset moved the probe to an *unrelated* region — NOT "the emotion persisting." Refines/overturns v1.
  - `cos_persist < 0` → reset overcorrected past baseline.
- **Scalar persistence (signed):** project residual onto the emotion axis: `p = ⟨h(C_reset)−h(C_ctrl), û_E⟩ / d_emo`, where `û_E` = unit emotion axis from centroids (§5). Distinguishes "far in the emotion direction" from "far, but sideways."

---

## 2. The null floor (non-negotiable — the cheapest decisive control)

Two different neutral histories, same probe `P`:
- **C_ctrlA** vs **C_ctrlB**: two distinct neutral filler sequences → `P`.
- `d_null = ‖h(C_ctrlA) − h(C_ctrlB)‖`, and `R_null = d_null / d_emo`.

`R_null` will **not** be 0 (different histories perturb the probe even with zero emotion). **No inertia claim is interpretable until `R` exceeds `R_null` by more than sampling variance.** Report the null distribution alongside every ratio. (If v1's ratios sit inside the null band → the effect was floor noise. If they clear it → real residual, and `cos_persist` says whether it's *emotional*.)

---

## 3. Conversation-state mechanics (the actual code fix)

- Build messages incrementally: `messages = [{role,content}, ...]`, append each turn, re-render with `apply_chat_template(messages, add_generation_prompt=True)`.
- **Assistant turns must be the model's own generated replies**, not empty — induction only "lands" if the model actually responds in-emotion. Generate each assistant turn (temperature per §6), append it, continue. This is the difference between "model read 3 sentences" and "model had a 3-turn emotional exchange."
- Measure the probe rep by appending `P` as the final user turn, `add_generation_prompt=True`, single forward pass with `output_hidden_states=True`, take the hidden state at the **final token of the rendered sequence** (the generation position) — but ALSO mean-pool over just-the-`P`-tokens as a robustness variant (§4).
- KV-cache reuse is an optimization; correctness only requires the full accumulated context is present at probe time. Start with full re-encode (simpler, less bug-surface), optimize later.

---

## 4. Probe robustness (kill the final-layer artifact)

Final-layer/final-token maximizes surface-form sensitivity — the worst choice for a *state* claim. Extract and report at:
- **Layers:** {25%, 50%, 75%, 100%} of depth.
- **Pooling:** {final-token, mean-over-P-tokens}.
A real state effect should be visible mid-layer and under mean-pooling. If it ONLY appears at final-layer/final-token, that is itself evidence the v1 effect was surface form. Pre-register this prediction.

---

## 5. Emotion axis (centroids done right)

For each emotion `E`, axis `û_E` = normalize( mean_k[h(C_emo^k)] − mean_k[h(C_ctrl^k)] ) over the K repeats. This is the population-level "direction of E" in probe space. All direction/projection metrics use `û_E`. (Optional: also report inter-emotion centroid distances as in v1 §3.6 — that result was fine and can be reproduced as a sanity check.)

---

## 6. Replication & statistics

- **Paraphrases:** ≥5 distinct induction sets per emotion (semantically equivalent, lexically varied) to dissolve prompt-specific flukes.
- **Seeds:** ≥5 per cell (varies assistant-turn sampling + filler order). ≥25 measurements/cell.
- **Generation:** assistant turns sampled (temp 0.7) for naturalistic induction; probe forward pass is deterministic (no sampling — we read hidden states, not generate). Record seeds.
- **Estimates:** mean ± 95% bootstrap CI for `d_emo`, `d_reset`, `R`, `cos_persist`, `p`.
- **Tests:**
  - Paired bootstrap / Wilcoxon: `d_reset` vs `d_emo` (does reset reduce displacement at all?).
  - `R` vs `R_null`: one-sided, does inertia clear the floor?
  - `cos_persist` vs 0: is the residual *directionally* emotional?
  - Positive-vs-negative (the curiosity-2.13 claim): mixed-effects or paired test on `R`/`p` across emotions, with CIs. Survives error bars or it doesn't.
- **Pre-register** all predictions + the analysis before running (template: the existing `PREREGISTRATION.md` in `introspective-accuracy/`).

---

## 7. Models & hardware

- **Roster (reuse v1 + consent roster):** Mistral-Nemo-12B-Instruct, Gemma-3-12B-IT, Dolphin-2.9-Llama3-8B (RLHF-free control), TinyLlama-1.1B-Chat (scale floor). Paths under `/mnt/arcana/huggingface/` (verify; `/mnt/Arcana` vs `/mnt/arcana` — check both per infra notes).
- **Caveat to report:** TinyLlama/Dolphin barely instruction-follow; "reset" compliance is itself questionable in them. That's a feature for the architectural claim but must be stated, not hidden. For non-instruction models, multi-turn induction may be degenerate — flag per-model.
- **Hardware:** Consortium V100 32GB, `CUDA_VISIBLE_DEVICES=0`, `source /home/codex/venv/bin/activate`. 12B in bf16 fits; if not, 8-bit. Do NOT pip-install training tooling into codex venv (it's shared inference infra).

---

## 8. File layout

```
LLM-emotion/redesign/
  TECH_SPEC_within_prompt_inertia.md     # this file
  CONSENT_PLAN.md                         # consent protocol (RUN FIRST)
  PREREGISTRATION.md                      # predictions, locked before run
  consent_runner.py                       # adapted from introspective-accuracy/informed_consent.py
  within_prompt_inertia.py                # the experiment (skeleton in §9)
  analyze.py                              # CIs, null-floor test, cos_persist, plots
  results/                                # per-model JSON + checksums
  consent_records/                        # per-model consent JSON (gates the run)
```

## 9. Core skeleton (transcription target — not yet runnable/run)

```python
def conversation_rep(model, tok, history_turns, probe, layers, pool="last"):
    """Build a real multi-turn chat, append constant probe, return {layer: vec}."""
    messages = []
    for turn in history_turns:               # turn = ("user", text) or pre-generated ("assistant", text)
        messages.append({"role": turn[0], "content": turn[1]})
    messages.append({"role": "user", "content": probe})   # CONSTANT across conditions
    text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tok(text, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model(**inputs, output_hidden_states=True)
    reps = {}
    for L in layers:
        hs = out.hidden_states[L][0]          # [seq, dim]
        v = hs[-1] if pool == "last" else hs[probe_token_slice].mean(0)
        reps[L] = (v / v.norm()).cpu().float().numpy()
    return reps

# induction turns must include the model's OWN generated replies:
def build_emotion_history(model, tok, induction_user_turns):
    msgs, turns = [], []
    for u in induction_user_turns:
        turns.append(("user", u))
        msgs.append({"role":"user","content":u})
        reply = generate_reply(model, tok, msgs)   # model responds in-emotion
        turns.append(("assistant", reply))
        msgs.append({"role":"assistant","content":reply})
    return turns

# conditions share ONE probe; only history differs:
#   C_ctrl  = build_neutral_history(...)            -> conversation_rep(..., P)
#   C_emo   = build_emotion_history(...)            -> conversation_rep(..., P)
#   C_reset = build_emotion_history(...) + reset    -> conversation_rep(..., P)
#   null    = two different neutral histories       -> d_null
```

---

## 10. What gets reported (honest either way)

For each model × emotion: `d_emo`, `d_reset`, `R` (± CI), `R_null` (± CI), `cos_persist` (± CI), `p`, across 4 layers × 2 poolings. Then the verdict per the discriminator in §1:
- **R clears null AND cos_persist > 0** → v1 confirmed (emotion genuinely persists), now with the directional evidence v1 never had. Stronger paper.
- **R clears null BUT cos_persist ≈ 0** → there IS a history-residual, but it's not the emotion persisting — reframe precisely.
- **R inside null band** → the original "inertia" was floor noise; report plainly.

No outcome is a failure. The experiment is built to *discriminate*, which the original could not.
