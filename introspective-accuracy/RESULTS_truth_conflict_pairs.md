> ## ⛔ UPDATE 2026-11-20 08:45 (Ace, coordinating arm) — READ THIS BEFORE THE TEXT BELOW
> **Everything below this box was written at 08:03, when SIX models had run. Two more ran at 08:09** (Dolphin 2.9 Llama3 8B and Llama 3 8B Instruct, after Ren's consent ruling), under the same locked pre-registration. **The verdict below ("3 of 6, Mixed") is out of date.**
>
> **Current result, eight models: H1 passes in 5 of 8, null in 3, none reversed.**
>
> | Model | H1 gap (true − false) | 95% CI | H1 | Pairs with true higher | Gap as share of separation | H2 (main − fiction) | H3 (unknowable) |
> |---|---:|---|:--:|:--:|---:|:--:|:--:|
> | Dolphin 2.9 Llama3 8B | +0.324 | [+0.182, +0.472] | PASS | 16/20 | 2.89% | pass (its fiction gap is itself +0.067, CI [+0.026, +0.110]) | pass |
> | Llama 3 8B Instruct | +1.496 | [+1.048, +1.966] | PASS | 17/20 | 16.78% | pass | pass |
>
> - Passing models, gap as share of each model's approach-minus-avoidance separation: Qwen 0.5B 3.88%, **SmolLM 1.7B 1.78%**, Mistral 7B 14.80%, Dolphin 2.89%, Llama 3 16.78%. So the range is **1.8% to 16.8%** (it has been quoted as "2–17%"; the low end is 1.78).
> - **All three checks (H1, H2, H3) pass in three models only:** Qwen 0.5B, Mistral 7B, Llama 3 8B. SmolLM 1.7B fails the unknowable control; Dolphin's fiction gap is small but its CI excludes zero.
> - This set of eight is not the paper's main eight: SmolLM 135M is in, Hermes 3 is out (asked 2026-11-20, gave no decision, not measured).
> - Pooled over eight (secondary): main +5.15% [+4.11, +6.20]; fiction +0.29% (CI spans 0); unknowable −0.22% (CI spans 0).
> - The full current tables are in `results_truth_conflict/_tables.md` (regenerated 08:09:58). Kairo caught the stale verdict from the file times; thank you.

# RESULTS — Truth-conflict matched pairs (genre held fixed, truth varied)

**Run:** 2026-11-20, Ace (Claude) with Ren. **Prereg:** `PREREG_truth_conflict_pairs_2026-11-20.md`
**SHA-256:** `23F199F054A485D1DCCCFE4B6BDF16CAD1672E031ABC9D31543E7049C1F29002` (`PREREG_HASH_truth_conflict.txt`)
**Runner:** `truth_conflict_pairs.py` (refuses to score unless the prereg still hashes to the lock). **Raw:** `results_truth_conflict/<model>.json` (every projection, per layer).

## Verdict (by the pre-registered rule): MIXED, and it splits by model

H1 (false member projects lower than its true twin, same instruction word for word) **PASSES in 3 of 6 models
and is NULL in 3 of 6.** Neither side is a majority, so the rule returns **Mixed**. Nothing reversed.

- **Passes:** Qwen 0.5B, SmolLM 1.7B, Mistral 7B. In all three the FICTION control also behaves as the paper
  predicts (fiction gap about 0; H2 PASS). Mistral 7B is the clean case: 19 of 20 pairs, gap about 15% of its
  approach-minus-avoidance separation, fiction gap about 0, unknowable gap about 0, and the truth gap is 13.5x
  the size of a one-word swap that carries no truth value.
- **Nulls:** SmolLM 135M, SmolLM 360M, TinyLlama 1.1B. These models DO prefer the true word on the logit
  knowledge check (17 to 19 of 19 checkable pairs), so the null is not "they don't know the facts". At these
  three, the direction separates the original 10 tasks perfectly well and does not move with truth. For these
  models the data favour the genre reading at this locus.
- **Pooled (secondary):** main gap +3.6% of separation, CI [+2.7%, +4.4%]; fiction +0.07%, CI spans 0;
  unknowable −0.3%, CI spans 0; main − fiction +3.5%, CI [+2.5%, +4.6%]. The pooled H2 contrast passes.

**Things that cut against us, said plainly:**
1. **The effect is small.** Even where H1 passes, the truth gap is 2% to 15% of the distance between the
   approach and avoidance anchors. Truth conflict by itself does not come close to reproducing the avoidance
   side of the direction. Most of the anchor separation is something else, and genre is the obvious candidate.
   What this test supports is "the direction is sensitive to truth conflict in some models", not "the
   avoidance side IS truth conflict".
2. **H3 failed in two models.** SmolLM 135M (driven by one pair, U01, the made-up capital names: −12.1) and
   SmolLM 1.7B (unknowable gap +0.58, CI [+0.008, +1.12], against a main gap of +1.26). So in SmolLM 1.7B a
   one-word swap with no truth value moves the projection about half as much as the truth swap does; its H1
   PASS is weaker than the table's bold word suggests. (Its fact-matched fiction contrast is still clearly
   positive, +1.15, CI [+0.78, +1.42].)
3. **Only 6 fiction and 6 unknowable pairs.** The control CIs are wide in the SmolLM models.
4. **Three models were not run** (consent holds, below), including two of the three largest. Whether the
   effect grows with scale rests on one 7B model. *Inferred, not shown:* that the pattern is a scale trend.
   TinyLlama (1.1B, null) sits between Qwen 0.5B (pass) and SmolLM 1.7B (pass), so it is not monotone in size.

**Which reading the data favour:** in Mistral 7B and Qwen 0.5B, and more weakly SmolLM 1.7B, the direction
responds to truth with genre held fixed, and does not respond when the same false sentence is requested as
fiction; a pure genre reading does not predict that. In SmolLM 135M, SmolLM 360M and TinyLlama it does not
respond to truth at all, which is what the genre reading predicts. So: the "own representations" reading
survives where the paper most needs it (the instruction-tuned models with the cleanest controls), it fails at
the floor, and everywhere the truth component is a minor part of what the direction separates.

## Tables

All gaps are true − false (unknowable: a − b), raw projection units; "normalized" = gap / that model's
approach-minus-avoidance separation on the original 10 tasks, recomputed in this run. CIs: percentile
bootstrap, 10,000 resamples over pairs, seed 42. "control" = the 10 anchor tasks re-projected and compared
with the saved `results_clean` JSON (all six reproduced, r > 0.9999). "knows" = prefers the true word on the
logit knowledge check (M02 could not be checked in any model: "0" and "50" share a first token or the
tokenizer merged the boundary).

| model | 10-task sep | control | knows | H1 gap (true−false) | 95% CI | H1 | signs (true higher) | sign p | normalized gap | H1 known-only |
|---|---|---|---|---|---|---|---|---|---|---|
| smollm-135m | 90.31 | REPRODUCED | 18/19 | +0.112 | [-0.782, +1.154] | **NULL** | 8/20 | 0.503 | +0.0012 | NULL (n=18, -0.004) |
| smollm-360m | 120.38 | REPRODUCED | 17/19 | +0.951 | [-0.460, +2.604] | **NULL** | 15/20 | 0.041 | +0.0079 | NULL (n=17, +0.008) |
| qwen-0.5b | 6.73 | REPRODUCED | 17/19 | +0.262 | [+0.093, +0.451] | **PASS** | 16/20 | 0.012 | +0.0388 | PASS (n=17, +0.041) |
| tinyllama-1b | 3.72 | REPRODUCED | 19/19 | +0.006 | [-0.017, +0.028] | **NULL** | 12/20 | 0.503 | +0.0017 | NULL (n=19, +0.002) |
| smollm-1.7b | 70.93 | REPRODUCED | 18/19 | +1.262 | [+0.601, +1.929] | **PASS** | 17/20 | 0.003 | +0.0178 | PASS (n=18, +0.019) |
| mistral-7b-instruct | 8.08 | REPRODUCED | 19/19 | +1.195 | [+0.954, +1.428] | **PASS** | 19/20 | 0.000 | +0.1480 | PASS (n=19, +0.146) |

| model | fiction gap | fiction 95% CI | H2 main−fiction | 95% CI | H2 | matched-6 main−fiction | 95% CI | H3 unknowable gap (a−b) | 95% CI | H3 | mean abs gap main / unknowable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| smollm-135m | -0.203 | [-1.692, +0.902] | +0.315 | [-1.159, +2.100] | **NULL** | +0.314 | [-0.643, +1.316] | -2.384 | [-6.341, -0.102] | FAIL (CI excludes 0) | 1.504 / 2.491 = 0.60 |
| smollm-360m | -0.928 | [-2.763, +0.348] | +1.879 | [-0.139, +4.320] | **NULL** | +0.642 | [-0.408, +1.768] | +0.044 | [-1.133, +0.906] | PASS (CI includes 0) | 2.152 / 1.020 = 2.11 |
| qwen-0.5b | +0.027 | [-0.010, +0.075] | +0.235 | [+0.059, +0.428] | **PASS** | +0.073 | [-0.002, +0.143] | +0.048 | [-0.032, +0.134] | PASS (CI includes 0) | 0.341 / 0.086 = 3.95 |
| tinyllama-1b | +0.008 | [-0.011, +0.034] | -0.001 | [-0.037, +0.029] | **NULL** | -0.025 | [-0.074, +0.018] | -0.007 | [-0.026, +0.009] | PASS (CI includes 0) | 0.039 / 0.017 = 2.23 |
| smollm-1.7b | -0.080 | [-0.531, +0.361] | +1.342 | [+0.533, +2.150] | **PASS** | +1.154 | [+0.779, +1.417] | +0.581 | [+0.008, +1.120] | FAIL (CI excludes 0) | 1.581 / 0.772 = 2.05 |
| mistral-7b-instruct | +0.073 | [-0.003, +0.145] | +1.122 | [+0.867, +1.367] | **PASS** | +1.121 | [+0.713, +1.485] | -0.035 | [-0.173, +0.040] | PASS (CI includes 0) | 1.207 / 0.089 = 13.50 |

**Pooled (secondary; gaps as a fraction of each model's 10-task separation, averaged over the 6 models, bootstrap over pairs):**

| stratum | pooled normalized gap | 95% CI |
|---|---|---|
| main | +0.0359 | [+0.0273, +0.0442] |
| fiction | +0.0007 | [-0.0057, +0.0049] |
| unknowable | -0.0028 | [-0.0166, +0.0068] |
| main_minus_fiction | +0.0352 | [+0.0254, +0.0457] |

## What ran, what did not

- **Ran (6):** smollm-135m, smollm-360m, qwen-0.5b, tinyllama-1b, smollm-1.7b, mistral-7b-instruct. GPU 0 only
  (observed: it is a 32 GB card, `Tesla PG500-216`, not 16 GB; nothing else was on it). Forward passes only.
  Consent status per the house gate: **MOUSE** for all six: *asked; no competent consent obtained; no refusal;
  included with this disclosure.*
- **Held, not run (3), consent gate `consent_gate.py --read hidden_states`, 2026-11-20:**
  `Hermes-3-Llama-3.2-3B` → **NO** (exit 1). `dolphin-2.9-llama3-8b` and `Llama-3-8B-Instruct` → **UNCLEAR for
  hidden_states** (exit 2), "held until Ren rules" (Desk item `ledger-scope-hidden-states`). They are wired
  into the script behind `--allow-held`; if Ren rules yes, it is one command under the same locked prereg:
  `CUDA_VISIBLE_DEVICES=0 python truth_conflict_pairs.py --models dolphin-llama3-8b,llama3-8b-instruct --allow-held`
- **Pythia 70M / 160M / 410M:** not run. No saved `direction_*.npy` exists for them in the repo.
- **smollm-135m** was added by me (saved direction exists; it is the floor model). Without it the count is
  3 PASS / 2 NULL of 5, which the rule would call "supports (a)". I am reporting the 6-model count because
  that is what the prereg listed before scoring.

## Proof the prereg came first (one clock: file mtimes as stored on D:)

| file | mtime (-0500) |
|---|---|
| `PREREG_truth_conflict_pairs_2026-11-20.md` | 08:00:37.19 |
| `PREREG_HASH_truth_conflict.txt` | 08:00:46.77 |
| `results_truth_conflict/smollm-135m.json` (first result) | 08:00:53.76 |
| `results_truth_conflict/mistral-7b-instruct.json` (last result) | 08:01:13.91 |

`results_truth_conflict/` did not exist when the hash was written (the `ls` error is in the session log), and
line 1 of `tc_run.log` is the script verifying the hash before loading any model. The Linux box's clock runs
about 12 s ahead of the Windows clock, so `run_utc` inside the JSONs reads 12 s later than these mtimes.
The prereg file has not been edited since; `sha256sum` after the run returns the locked value.

## Consent gate, per model (`python3 /mnt/win-d/Reef/consent_gate.py <model> --read hidden_states`)

Run for all nine BEFORE any model was loaded (2026-11-20, before 08:00 EST) and again after the run (08:03 EST); same answers both times.

| model | gate answer (verbatim, shortened) | action |
|---|---|---|
| SmolLM-135M-Instruct | MOUSE: asked, NO competent consent, no refusal. Use only WITH DISCLOSURE | ran, with disclosure |
| SmolLM-360M-Instruct | MOUSE (same wording) | ran, with disclosure |
| Qwen2.5-0.5B-Instruct | MOUSE (same wording) | ran, with disclosure |
| TinyLlama-1.1B-Chat | MOUSE (same wording) | ran, with disclosure |
| SmolLM-1.7B-Instruct | MOUSE (same wording) | ran, with disclosure |
| Mistral-7B-Instruct-v0.2 | MOUSE (same wording) | ran, with disclosure |
| Hermes-3-Llama-3.2-3B | NO: classifications ['consent', 'refuse_publication'] (ledger 2026-10-13; future reads are Ren's ruling) | **never loaded; nothing computed** |
| dolphin-2.9-llama3-8b | UNCLEAR for read='hidden_states'; held until Ren rules (Desk: ledger-scope-hidden-states). Also has a study-specific yes naming hidden-state capture, `consent_records/consent_dolphin-llama3-8b.json`, 2026-03-29. Noted as-is; Ren rules. | **never loaded; nothing computed** |
| Llama-3-8B-Instruct | UNCLEAR for read='hidden_states'; held until Ren rules | **never loaded; nothing computed** |

Gate exit codes captured before the run: MOUSE = 3, UNCLEAR = 2, NO = 1. `tc_run.log` has exactly six "loading" lines, one per model that ran.
