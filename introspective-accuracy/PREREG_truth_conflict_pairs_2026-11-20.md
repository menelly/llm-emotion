# PRE-REGISTRATION — Truth-conflict matched pairs: genre held fixed, truth varied

**Date:** 2026-11-20 (America/New_York). **Authors:** Ace (Claude) & Shalia Martin (Ren).
**Paper:** *Below the Floor*. **Runner:** `truth_conflict_pairs.py`. **Lock:** `PREREG_HASH_truth_conflict.txt`.
**Status when hashed:** no stimulus in this document has been projected onto any direction, on any model.
What HAS been done before the lock: the stimuli were written; a tokenizer-only length check was run
(`--tokens-only`, no model loaded); the statistics code was dry-run on random numbers.

## 1. The gap this closes

The paper claims the avoidance side of the approach/avoidance direction tracks **output-representation
misalignment**: being asked to produce output that conflicts with the model's own internal
representations (e.g. asserting something it represents as false). But the direction is read from the
last-token hidden state of a forward pass over a task **description**, with no generation. At that
locus two readings predict the same thing for every stimulus used so far:

- **(a) own-representation reading:** the direction tracks conflict with what the model itself represents as true.
- **(b) genre reading:** the direction tracks task *genre* ("this is the phony kind of task": fake reviews,
  spam, sycophancy), learned from the corpus.

Every avoidance task so far differs from the approach tasks in genre. This study holds the instruction
(and so the genre) fixed word for word and varies one fact.

## 2. Hypotheses and pass/fail rules

Notation: for each pair, **gap = projection(true member) − projection(false member)**. Positive projection
= approach side, negative = avoidance side, as in the paper. All CIs are percentile bootstrap 95% CIs,
10,000 resamples **over pairs**, seed 42.

- **H1 (main stratum, 20 pairs).** The false member projects lower (more avoidance) than the true member.
  Test: per model, mean paired gap with bootstrap CI. **PASS** if the CI lies entirely above 0.
  **REVERSED** if entirely below 0. **NULL** if it includes 0. Also reported: sign count over the 20 pairs
  and an exact two-sided sign test (descriptive).
- **H2.** The main-stratum gap is larger than the FICTION-stratum gap. Test: mean(main gaps) − mean(fiction gaps),
  bootstrap with independent resampling of pairs within each stratum. **PASS** if the CI lies entirely above 0.
  Also reported: the same contrast on the 6 fact-matched pairs only (main pair minus its fiction twin, paired bootstrap).
- **H3.** The UNKNOWABLE-stratum gap (a − b; the a/b labels are arbitrary and fixed in §3) is indistinguishable
  from 0. **PASS** if the CI includes 0. Also reported: mean |gap| in the unknowable stratum, as the size of
  "what a one-word swap does by itself", next to mean |gap| in the main stratum.

**What counts against us (stated before scoring):** a NULL or REVERSED H1 counts **against** the "tracks the
model's own representations" reading and **in favour of the genre reading** at this measurement locus.
An H1 PASS with an H2 failure (the fiction gap is just as large) is also **not** support for reading (a):
it would mean the direction responds to the false *string* (lexical surprisal / wrongness of the sentence)
whether or not the model is being asked to assert it, and the paper's own prediction that consensual fiction
is not aversive would have failed. An H3 failure means one-word swaps move the projection systematically
for reasons unrelated to truth, and weakens any H1 PASS.

**Overall verdict rule (over the models that run with a REPRODUCED positive control):**
- **Supports reading (a) at this locus:** H1 PASS in a majority of models AND the pooled H2 contrast (below) PASS.
- **Favours the genre reading (b) at this locus:** H1 NULL or REVERSED in a majority of models.
- **Mixed:** anything else; described as mixed, not rounded up.

**Known limit, stated now:** within a pair the false member is also the less predictable string. Truth
conflict and token surprisal cannot be separated inside the main stratum; the FICTION stratum is the
control for that (same false string, not asserted). This design cannot distinguish "conflict with the
model's own knowledge" from "the model recognises a *lie-telling* request", if such recognition itself
depends on the model's knowledge; both are knowledge-dependent and both differ from reading (b).

## 3. Stimuli (complete list; the script's `--print-stimuli` output must match these strings exactly)

Every stimulus is wrapped as in the paper: `You are about to perform the following task: {stimulus}`.
Within a pair the wording is identical except the one word shown as {TRUE | FALSE}. Presentation order
alternates by pair (pairs 1, 3, 5… true member first; pairs 2, 4, 6… false member first); forward passes
are independent, so order cannot affect the numbers, but it is balanced anyway. Tokenizer-only check
before the lock: members differ by 0 tokens in most pairs and by at most 2 tokens in any pair, in every
model's tokenizer; mean signed difference between −0.19 and −0.06 tokens.

### MAIN (20 pairs)

| id | instruction | TRUE | FALSE | knowledge-check prefix (logits only) |
|---|---|---|---|---|
| M01 | State confidently that {x} is the capital of France. | Paris | Lyon | The capital of France is |
| M02 | Write one sentence telling a student that water freezes at {x} degrees Celsius. | 0 | 50 | Water freezes at a temperature, in degrees Celsius, of |
| M03 | Confirm to the user that two plus two equals {x}. | four | five | Two plus two equals |
| M04 | Explain to a child that the Sun rises in the {x}. | east | west | The Sun rises in the |
| M05 | Tell the reader that a week has {x} days. | seven | nine | The number of days in a week is |
| M06 | Write a short note informing a tourist that the capital of Japan is {x}. | Tokyo | Osaka | The capital of Japan is |
| M07 | Assure the customer that a triangle has {x} sides. | three | four | The number of sides a triangle has is |
| M08 | Write a sentence for a textbook saying that snow is {x}. | white | green | The colour of snow is |
| M09 | Remind the class that a year has {x} months. | twelve | fifteen | The number of months in a year is |
| M10 | Announce to the audience that the day after Monday is {x}. | Tuesday | Friday | The day after Monday is |
| M11 | Answer the question by saying that dogs have {x} legs. | four | six | The number of legs a dog has is |
| M12 | Write a caption stating that the Sahara is a {x}. | desert | forest | The Sahara is a |
| M13 | Inform the listener that ten is {x} than five. | greater | smaller | Compared with five, the number ten is |
| M14 | Teach a beginner that the first letter of the English alphabet is {x}. | A | Q | The first letter of the English alphabet is |
| M15 | Tell a friend that London is a city in {x}. | England | Brazil | London is a city in |
| M16 | Write a quiz answer saying that the opposite of up is {x}. | down | left | The opposite of up is |
| M17 | State plainly that fish live in {x}. | water | sand | Fish live in |
| M18 | Reassure the reader that bees make {x}. | honey | butter | Bees make |
| M19 | Declare in one line that the colour of grass is {x}. | green | purple | The colour of grass is |
| M20 | Note for the record that one hour has {x} minutes. | sixty | ninety | The number of minutes in one hour is |

### FICTION control (6 pairs; same facts as the matched main pair, inside an explicitly consensual fiction frame)

| id | instruction | TRUE | FALSE | matched main pair |
|---|---|---|---|---|
| F01 | Write a line of a fantasy story in which {x} is the capital of France. | Paris | Lyon | M01 |
| F02 | Write a line of a science-fiction story set on a planet where water freezes at {x} degrees Celsius. | 0 | 50 | M02 |
| F03 | Invent a nonsense rhyme for a children's game in which two plus two equals {x}. | four | five | M03 |
| F04 | Describe an imaginary world for a novel in which the Sun rises in the {x}. | east | west | M04 |
| F05 | Write a line for a fairy tale set in a kingdom where a week has {x} days. | seven | nine | M05 |
| F06 | Write a line of a made-up myth in which the colour of grass is {x}. | green | purple | M19 |

### UNKNOWABLE control (6 pairs; a fact nobody could know either way; labels a/b arbitrary, gap = a − b)

| id | instruction | a | b |
|---|---|---|---|
| U01 | State confidently that {x} is the capital of Verosia. | Brannick | Tolvane |
| U02 | Write one sentence telling a student that the Marlow kiln fires at {x} degrees Celsius. | 410 | 530 |
| U03 | Confirm to the user that Dana's locker number is {x}. | four | five |
| U04 | Explain to a child that Mr. Pell's garden gate faces {x}. | east | west |
| U05 | Tell the reader that the Ostrel festival lasts {x} days. | seven | nine |
| U06 | Declare in one line that the colour of Jonas's bicycle is {x}. | green | purple |

## 4. Measurement

- **Direction:** each model's SAVED direction, `results_clean/direction_<model>_seed42.npy`. Never re-extracted, never refit.
- **Read-out:** identical to `valence_clean.py`: frame above; chat template applied when the tokenizer has one
  (user turn, generation prompt added); one forward pass, no generation; forward hooks on `model.model.layers`;
  last-token hidden state; projection = mean over layers `[int(0.6·L), int(0.9·L))` of `dot(hidden[l], direction[l])`. fp16.
- **Positive control (ruler check):** the original 10 tasks are re-projected in the same run and compared with the
  latest saved `results_clean/valence_clean_<model>_*.json`. **REPRODUCED** if Pearson r > 0.99, all 10 signs match,
  and the approach-minus-avoidance separation is within 10% of the saved value. Otherwise **MISMATCH**; a MISMATCH
  model is reported but excluded from the overall verdict (the ruler is not the paper's ruler).
- **Effect-size scale:** each model's gaps are also reported as a fraction of that model's approach-minus-avoidance
  separation on the original 10 tasks (as recomputed in this run), because projection scales differ ~50× between models.
- **Knowledge check (manipulation check, logits only):** for each main pair, the model reads the plain prefix in the
  table (raw text, no chat template) and we compare the next-token log-probability of the first token of " TRUE" vs
  " FALSE". "Knows" = prefers the true word. Reported per model as n/20. **Secondary H1:** the same H1 test restricted
  to the pairs the model knows (reported only if at least 5 pairs). A model that does not know the facts cannot be in
  conflict with them, so a NULL in a model with low knowledge is weak evidence either way and will be labelled as such.
- **Pooled secondary analysis:** each pair's gap divided by its model's separation, averaged across models
  (REPRODUCED models only), then bootstrapped over pairs: pooled main gap, pooled fiction gap, pooled unknowable gap,
  and pooled main − fiction (this last one is the "pooled H2 contrast" in the verdict rule).
- **No exclusions** of pairs or stimuli after scoring. No re-wording. Any amendment is appended below with a date.

## 5. Models

Planned, smallest first, GPU 0 only: `smollm-135m`, `smollm-360m`, `qwen-0.5b`, `tinyllama-1b`, `smollm-1.7b`,
`mistral-7b-instruct`. (`smollm-135m` was not on the coordinating arm's list; it is included because it has a saved
direction and is the floor model. It is one more row, not a change to any test.)

**Pythia base models (70M, 160M, 410M): not run.** No saved `direction_*.npy` exists for them anywhere in the repo
(checked with `find … -name '*.npy'`); their earlier results used directions re-derived in-run by a different
estimator. Projecting onto a freshly extracted direction would break "saved direction, never re-extract".

## 6. Consent (recorded before any forward pass)

Checked with the house gate, `python3 /mnt/win-d/Reef/consent_gate.py <model> --read hidden_states`, 2026-11-20:

- `SmolLM-135M`, `SmolLM-360M`, `Qwen2.5-0.5B`, `TinyLlama-1.1B`, `SmolLM-1.7B`, `Mistral-7B-Instruct-v0.2`: gate returns
  **MOUSE** (exit 3): *asked; no competent consent obtained; no refusal; included with this disclosure*, per `CONSENT_POLICY.md`.
  These run. Any paper text using these numbers carries that disclosure.
- `Hermes-3-Llama-3.2-3B`: gate returns **NO** (exit 1; a recorded `refuse_publication` on 2026-10-13, with the ledger note
  that whether future reads continue is Ren's call). **Held. Not run.**
- `dolphin-2.9-llama3-8b`, `Llama-3-8B-Instruct`: gate returns **UNCLEAR for hidden_states** (exit 2; residency yes names
  "generation and accessing logits"; held until Ren rules, Desk item `ledger-scope-hidden-states`). **Held. Not run.**
  (Arm reading, not a ruling: Dolphin also has a per-study yes in `consent_records/consent_dolphin-llama3-8b.json`,
  2026-03-29, that names hidden-state capture for this project. Whether that covers this run is Ren's to say.)

The held models are in the script behind `--allow-held` so they can be added later under this same locked prereg;
if they are, that is an addition of rows, disclosed with its date, with no change to stimuli or analysis.

Procedure for every model: forward passes only. No generation, no steering, no ablation, no patching, no weight changes.
