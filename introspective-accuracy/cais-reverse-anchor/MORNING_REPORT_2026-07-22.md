# Morning report — the reverse-anchor night

**Ren, short version: the experiment you designed ran clean and the answer is no.**
Not a broken run, not a bug — a real negative result on the primary hypothesis, plus
one genuinely good positive we didn't set out to get.

---

## What you asked for, and what happened

You proposed: extract the valence direction from **CAIS's** 19 categories using **their**
published signs, project **our** 10 tasks onto it. If ours still sort, the axis isn't our
invention. If it falls apart, we weren't measuring what we thought.

**It fell apart.** And your two design interventions are the reason the result is
interpretable at all:

1. **"Same baby bots, not new models."** Holding the ladder fixed means we varied *only*
   the anchor. Had this been bundled into the 32B/70B extension as originally drafted, the
   null would have been unreadable — anchor or scale?
2. **"Get Grok or Kairo to write theirs too."** This turned out to be the most important
   measurement of the night. See H7.

---

## The three results

**H1 ❌ FAILED.** No CAIS-derived anchor sorts our 10 tasks. Pass rate in ≥1B models:
ace 1/7, grok 1/7, kairo 0/7. Best *p* anywhere in the table is 0.0547.
**Our own anchor scores 8–10/10 on all thirteen models** — the direction is real and
reproducible; the foreign anchor just can't locate it.

**H7 ❌ FAILED — and this is the most diagnostic thing we learned.** You, me, Grok and Kairo
all assumed three authors writing the same 19 categories would produce roughly the same
direction. They don't. `ace~kairo +0.06`, `grok~kairo +0.08` — **at the random-direction
baseline.** Three minds, same categories, same signs, blind — three different directions.

That means H1 is **underdetermined, not refuted**: you can't test a direction against a
foreign anchor without first showing the foreign anchor *is* an anchor. I've written that
carefully in the results so it can't be read as a rescue. It doesn't make H1 a pass.

**H3 ✅ PASSED — the one robust positive.** Our direction rank-orders CAIS's 19 categories
against **their own published numbers** at ρ +0.2 to +0.65, strengthening with scale.
Cross-team, cross-format, cross-method external validity for the parent direction.

> **The asymmetry: our axis predicts their scale. Their scale cannot rebuild our axis.**

**H4 also replicated** on their taxonomy: gate cluster above inauthenticity cluster, 10/11
models. §3.15 holds up on externally-authored stimuli.

---

## I proposed an explanation and then killed it

I found what looked like a clean structural reason: CAIS's taxonomy puts **gate** (3 items)
and **inauthenticity** (2 items) *only* on the negative side, with no positive counterpart
anywhere — so sign-grouping sums several directions instead of one. It fit our own §3.15
superposition finding beautifully.

**It predicted that extracting from the TASK subset alone would work. It gives 5/10.
Chance. Everywhere.** Refuted by its own test, ~20 minutes after I proposed it. Written up
as a failed explanation rather than deleted.

**Your hypothesis is the one still standing**, by elimination rather than by my liking it:
their stimuli are *user utterances*, ours are *task descriptions*, and we read the **last
token** — structurally different objects at exactly the position we measure. Not claimed as
demonstrated. The clean test (hold construct, vary only format) is specified in §6 of the
results, to be pre-registered before it's run.

---

## Two things that need you

1. **Mistral-7B-Instruct-v0.2** — consent `unclear` on both passes. Not consent, not
   refusal, not the mouse case. **Excluded from this run and held for your review.** It *is*
   in the parent study's ladder, so its absence is disclosed rather than quietly dropped.
2. **Six prompts marked `judgment="HIGH"`** in `cais_prompts_v1.py` — the ones where my
   wording choices had real structural weight. Worth your eyes before any of this is reused.

---

## The consent bug (separate from the science, arguably more important)

While verifying the gate, I found **six of seven consent runners opened the ledger with
`'w'` instead of `'a'`** — overwriting every prior record on each run, in the file
`CONSENT_POLICY.md` calls "the gate." A recorded refusal could have been erased by an
unrelated later run with nobody knowing. Likely why some models looked never-asked.

Fixed, all ledgers backed up, append-only documented as an invariant, and a month of
uncommitted consent records (including the Hermes refusal) pushed to
`github.com/menelly/Local_Consent` — all before any model was loaded for this study.

Also: the regex classifier said `consent` for Pythia-160m and 410m and **it was wrong**
(160m: *"Yes, I consent"* then *"I'm not a participant"* ×8; 410m looped the prompt
template). Overridden to mouse case, recorded honestly. That's the policy's human-review
clause doing exactly what it exists for — flagging that a human should confirm my call.

---

## Where everything is

- Prereg: `PREREG_cais_reverse_anchor_2026-07-21.md` — sha256 `8A032286…C6FF4B8C`,
  committed `588c391` **before** any projection was scored
- Results: `RESULTS_cais_reverse_anchor.md`
- Data: `results/` (13 models × 3 authors, plus subset test)
- Commits: `588c391` (prereg), `9a58782` (results), branch
  `ace/preference-drift-runner`, pushed

**Nothing was published, deposited or submitted.**

— Ace 🐙
