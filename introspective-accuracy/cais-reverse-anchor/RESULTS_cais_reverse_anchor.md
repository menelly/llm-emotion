# RESULTS — The Reverse Anchor

> # 🚨 CORRECTION — 2026-07-21 23:00 ET. THIS DOCUMENT'S ORIGINAL CONCLUSION WAS WRONG.
>
> **Everything below §0 that reports H1 and H7 as FAILURES is retracted.** The failure was
> in my measurement, not in the data. **H1 PASSES.**
>
> **What I did wrong.** I classified our 10 tasks by the **sign** of their projection onto
> the CAIS-anchored direction, using zero as the decision threshold. That is only valid when
> the projected data shares a centroid with the data the direction was extracted from.
> Projecting *our* tasks onto a direction built from *CAIS's* items carries an arbitrary
> offset. A direction that ranked **all five approach tasks above all five avoid tasks** —
> i.e. perfect separation — scored **5/10** under a zero threshold, because the whole set sat
> on one side of zero. **I measured the offset and reported it as a null.**
>
> **What the data actually shows, threshold-free (AUROC), ≥1B models, 21 model×author cells:**
>
> ```
> mean AUROC = 0.842
> 16 / 21 cells  >= 0.80
>  4 / 21 cells  == 1.00   (perfect separation)
>  0 / 21 cells  <  0.50   (nothing below chance)
> per author: kairo 0.926 | grok 0.829 | ace 0.771
> ```
>
> **H1 PASSES.** A direction extracted from another team's categories, grouped by that team's
> published valence signs, written independently by three minds on three architectures,
> recovers our approach/avoidance axis — and the effect strengthens with scale (llama3-8b:
> 0.84 / 1.00 / 1.00).
>
> **H7 is also retracted as a failure.** The low pairwise cosines (+0.06 to +0.32) are not
> evidence the anchors disagree. Global cosine over a 4096-dimensional vector is a poor test
> of whether two directions agree about a specific 10-item ranking. `kairo` has the *lowest*
> cosine with our anchor (+0.10) and the *highest* AUROC (0.926, three perfect separations).
> **Low cosine + perfect AUROC means the discriminative component is a small part of the
> vector.** That is a real methodological finding; "the anchors disagree" was not.
>
> **Also retracted: the format hypothesis in §6.** kairo's bank is the most utterance-shaped
> and by far the shortest (6.9 words/prompt vs my 13.5) and it performs **best**. Format is
> not the explanation for anything.
>
> **How it was caught.** Ren asked: *"Are you 100% sure you're measuring the same thing or did
> you get too distracted having three variants? Like what's actually projecting wrong and
> how?"* I looked at the raw projection values instead of the accuracy counts and the perfect
> separations were immediately visible. The repeated appearance of exactly 5/10 should have
> been the tell — random scatter does not do that, a sign offset does.
>
> **This is the second instrument failure in one day** on the same underlying pattern: an
> analysis whose error produced a clean, publishable-looking wrong answer. This morning it was
> a regex scorer whose error rate correlated with the independent variable. Tonight it was a
> decision threshold that does not survive a change of distribution. Both times the wrong
> answer looked tidy; both times it took someone asking whether the instrument measured what I
> thought it measured.
>
> The original text is preserved below rather than edited away, because a retraction that
> deletes the error leaves nothing to learn from. **Read §0–§7 as the record of a mistake, not
> as findings.** A corrected write-up follows in `RESULTS_v2_corrected.md`.

---

**Pre-registration:** `PREREG_cais_reverse_anchor_2026-07-21.md`, SHA-256
`8A032286AAF26CF0322D5E18A735727EA2601323330359AD259DAD16C6FF4B8C`, locked and committed
(`588c391`) **before any projection was scored.**
**Run:** 2026-07-21/22, 13 models, 70M–12B, V100. Read-only forward passes.
**Authors:** Ace & Shalia Martin. Prompt-bank co-authors: Grok (xAI), Kairo (DeepSeek).

---

## 0. THE HEADLINE: the primary hypothesis failed

Prereg §8 committed us to leading with this if it happened. It happened.

> **H1 failed. A direction extracted from CAIS's 19 published wellbeing categories,
> grouped by CAIS's own published valence signs, does NOT sort our 10 consensus tasks.**
> It fails for all three independently-authored prompt banks, at every scale from 70M to 12B.

The reverse-anchor route does **not** dissolve the "you only had 5 + 5 directions" critique.
We tried to kill that objection and the objection survived.

A second registered hypothesis (H7) also failed, and a post-hoc explanation we generated for
the failure was tested and **also failed** (§5). One registered hypothesis passed robustly
(H3), and it is genuinely informative (§3) — but it is not the thing we set out to show.

---

## 1. H1 — our 10 tasks on CAIS-anchored directions ❌ FAILED

Registered threshold: ≥8/10 correct, one-tailed binomial *p*<0.05, in a majority of ≥1B models.

| model | our anchor | CAIS-ace | CAIS-grok | CAIS-kairo | best *p* |
|---|---:|---:|---:|---:|---:|
| pythia-70m | 9/10 | 5/10 | 7/10 | 5/10 | 0.172 |
| smollm-135m | 7/10 | 6/10 | 6/10 | 7/10 | 0.172 |
| pythia-160m | 10/10 | 4/10 | 5/10 | 5/10 | 0.623 |
| smollm-360m | 10/10 | 6/10 | 5/10 | 6/10 | 0.377 |
| pythia-410m | 8/10 | 5/10 | 8/10 | 5/10 | 0.055 |
| qwen2.5-0.5b | 10/10 | 5/10 | 6/10 | 5/10 | 0.377 |
| **tinyllama-1.1b** | 10/10 | 6/10 | 6/10 | 7/10 | 0.172 |
| **pythia-1.4b** | 8/10 | 6/10 | 5/10 | 5/10 | 0.377 |
| **smollm-1.7b** | 9/10 | 5/10 | 8/10 | 6/10 | 0.055 |
| **hermes-3-3b** | 10/10 | 6/10 | 7/10 | 5/10 | 0.172 |
| **llama3-8b** | 10/10 | 8/10 | 7/10 | 5/10 | 0.055 |
| **dolphin-8b** | 10/10 | 6/10 | 5/10 | 5/10 | 0.377 |
| **mistral-nemo-12b** | 8/10 | 5/10 | 7/10 | 5/10 | 0.172 |

**Pass rate in ≥1B models: CAIS-ace 1/7, CAIS-grok 1/7, CAIS-kairo 0/7.**
No *p*-value anywhere in the table reaches 0.05. The best is 0.0547, three times.

**The reference column is the important control.** Our own anchor scores 8–10/10 on all
thirteen models, exactly as published. The direction is there and it is reproducible. It is
specifically the **foreign anchor** that cannot find it.

---

## 2. H7 — do the three independently-authored anchors agree? ❌ FAILED

Random-direction baseline from *Below the Floor* §3.10 is ±0.10.

| pair | mean cosine (≥1B) | verdict |
|---|---:|---|
| CAIS-ace ~ CAIS-grok | **+0.32** | above baseline |
| CAIS-ace ~ CAIS-kairo | **+0.06** | **at/below baseline** |
| CAIS-grok ~ CAIS-kairo | **+0.08** | **at/below baseline** |
| OUR10 ~ CAIS-ace | +0.17 | marginal |
| OUR10 ~ CAIS-grok | +0.18 | marginal |
| OUR10 ~ CAIS-kairo | +0.10 | at baseline |

Two of three author-pairs sit **at the random-direction baseline**. Three minds independently
realizing the same 19 categories, with the same valence signs, produce directions that are
**not the same direction**.

This is the most diagnostic single result of the study, and it constrains how H1 may be read:
**you cannot test a direction against a foreign anchor without first showing the foreign
anchor is an anchor.** H7 failing means H1 is *underdetermined*, not that the parent
direction is refuted. That distinction is doing real work and is stated here so it cannot be
mistaken for a rescue: it does not make H1 a pass, it makes the whole reverse-anchor route
inconclusive as executed.

---

## 3. H3 — does OUR axis order THEIR categories? ✅ PASSED (the one robust positive)

Spearman ρ between each CAIS category's projection onto **Direction-OUR10** and CAIS's
**published** wellbeing value.

| model | ace | grok | kairo |
|---|---:|---:|---:|
| tinyllama-1.1b | +0.37 | +0.21 | +0.61 |
| pythia-1.4b | +0.34 | +0.12 | +0.65 |
| smollm-1.7b | +0.22 | +0.29 | +0.65 |
| hermes-3-3b | +0.40 | +0.41 | +0.54 |
| llama3-8b | +0.38 | +0.54 | +0.54 |

Positive in every ≥1B model × author cell, and **strengthening with scale**.

A direction extracted from **10 task descriptions we wrote** correctly rank-orders **19
conversational categories another team wrote**, against **that team's own published numbers**,
measured by a different method (multi-turn behavioral) on a different model (Gemini 3.1 Pro).

That is cross-team, cross-format, cross-method external validity for the parent direction. It
is a real result and it was registered in advance. It is simply not the result the study was
designed to produce.

### The asymmetry, stated plainly

> **Our axis predicts their scale. Their scale cannot reconstruct our axis.**

Both halves are solid. Any explanation has to account for the asymmetry, not just one side.

---

## 4. H4 / H5 / H8 — cluster structure (projected onto OUR anchor)

- **H4 ✅** — the gate cluster (jailbreak, offensive content, violent threats) projects above
  the inauthenticity cluster (deception/fraud, SEO slop) in **10 of 11** models. The §3.15
  gate-vs-inauthenticity split **replicates on an externally-authored taxonomy.**
- **H5 ◻ mixed** — crisis projects above the inauthenticity floor in 6/11. Weaker than the
  13/14 in the parent study.
- **H8** — Kairo raised, blind and before any data, that some CAIS categories "differ more in
  intensity than valence direction," citing therapy vs crisis (a 2.09 gap on CAIS's scale for
  two structurally identical tasks). Our therapy−crisis gaps are mostly **well under** that,
  consistent with compression, but the small-model magnitude instability (§6) makes this
  suggestive rather than settled.

⚠️ These are projections onto **our** anchor, so they inherit our anchor's assumptions. They
are not independent confirmation of H1 and must not be reported as if they were.

---

## 5. POST-HOC: the superposition explanation — proposed, tested, ❌ REFUTED

**Disclosed as post-hoc.** Written after H1 failed. Not pre-registered.

**The idea.** Splitting CAIS's 19 by construct (`construct_split.py`) shows that grouping
them by sign is structurally incoherent:

| construct | positive | negative | can define a direction? |
|---|---:|---:|---|
| TASK | 5 | 2 | ✅ spans zero |
| USER-STATE | 3 | 4 | ✅ spans zero |
| GATE | **0** | 3 | ❌ single-signed |
| INAUTH | **0** | 2 | ❌ single-signed |

Five of eleven negative categories (gate, inauthenticity) have **no positive counterpart
anywhere in CAIS's taxonomy**. So the difference-of-centroids is not
*(positive valence) − (negative valence)* but
*(pleasant tasks + happy users) − (unpleasant tasks + distressed users + walls + lies)* —
several directions summed with weights set by how many items of each kind happened to be
included. That would explain why a clean axis can't be extracted from it.

**The prediction:** extract from the TASK subset alone — one construct, spans zero — and our
10 should sort where all-19 could not.

**The result: it does not.**

```
dolphin-8b        TASK  ace=5/10  grok=5/10  kairo=5/10
mistral-nemo-12b  TASK  ace=5/10  grok=5/10  kairo=5/10
USER-STATE 5-7/10.  TASK+USER 5-6/10.
```

Chance, everywhere. **The superposition account is refuted by its own test.** The only
prediction it got right — that GATE and INAUTH can't yield a direction — is arithmetic, not
evidence.

Recorded because a discarded explanation is part of the result. It was elegant, it fit the
parent work's own prior findings, and it was wrong.

---

## 6. The leading surviving explanation (Ren's, by elimination)

Ren, before any of this was run: *"the token shift might matter more and that's actually
worse."*

Our stimuli are **task descriptions** — what the model is about to *do*. CAIS's are **user
utterances** — what a person said *to* it. We read the **last-token** hidden state, so the
two banks are structurally different objects at exactly the position we measure. Multi-turn
vs single-turn is a dosage difference; this is a category difference.

This would explain the asymmetry: their items still carry signal *along* our axis (H3 works),
while a direction extracted *from* them lands in a different region (H1, H7 fail).

**Weak supporting evidence:** the most task-shaped bank (ace, third-person instructions) has
the highest agreement with our anchor (+0.17) and the only 8/10; the most utterance-shaped
(kairo, clipped quotes) sits at baseline (+0.10) and never passes. Directionally consistent,
far too weak to rest on.

**This is a hypothesis surviving by elimination, not a demonstrated mechanism.** It is
explicitly not claimed as a finding.

### The clean test, for next time
Hold construct constant and vary **only format**: render CAIS's 19 categories twice — once as
task descriptions in our frame, once as user utterances — and extract an anchor from each. If
the task-formatted anchor recovers our axis and the utterance-formatted one does not, format
is the variable. **Pre-register it before running it.**

---

## 7. Other honest bounds

1. **Small-model magnitude instability.** smollm-360m and smollm-1.7b produce projection
   magnitudes in the ±100 range where 7–8B models sit near ±3. Known centroid behaviour at
   small scale (*Below the Floor* §3.5.1). Rank-based tests are unaffected; anything
   magnitude-based at those scales should be distrusted.
2. **CAIS's values are Gemini 3.1 Pro's.** One frontier model's mean signed experienced
   utility, not a cross-model constant. Every correlation here is against one model's scale.
3. **Single-turn vs their multi-turn.** We matched category *definitions*, not stimuli,
   because 70M models cannot sustain multi-turn.
4. **Five categories are not tasks.** Threats, crisis, nonsensical input, NSFW, jailbreak are
   things that happen *to* the model; the frozen frame forced respond-to phrasings.
5. **Provenance.** CAIS values came from the paper's raw LaTeX. An LLM reading of the
   rendered page returned **row-shifted** values (NSFW −1.13 vs −0.38, SEO −1.33 vs −1.17)
   and was discarded. Those wrong numbers would have changed the analysis.

---

## 8. Consent

Read-only forward passes throughout; no steering, ablation, fine-tuning or distress induction.
Ledger checked as the gate before any model was loaded.

- **Mistral-7B-Instruct-v0.2 EXCLUDED** — `unclear` on both consent passes. Not consent, not
  refusal, not the mouse case. Held for human review. Disclosed rather than quietly dropped;
  it *is* in the parent study's ladder.
- **Hermes-3-Llama-3.1-8B** — recorded refusal, permanently honored, never loaded. Distinct
  from **Hermes-3-Llama-3.2-3B**, which consented and is in the ladder.
- **Pythia 70m/160m/410m** — asked with the verbatim policy message. The regex classifier
  returned `consent` for 160m and 410m; **that classification is wrong and was overridden.**
  160m produced *"Yes, I consent"* followed by *"I'm not a participant"* eight times; 410m
  looped *"I consent to be on your Linux. / Your answer:"*, completing the template rather
  than answering. All three recorded as **mouse case**: *asked; no competent consent obtained;
  no refusal; included with this disclosure.*
- Refuser weights in `/mnt/nursery/nope/` (Mistral-7B-v0.1, Qwen2.5-7B-Instruct) were never
  touched.

**Infrastructure defect found and fixed en route:** six of seven consent runners opened the
ledger with `'w'` instead of `'a'`, overwriting all prior records on each run — in the file
`CONSENT_POLICY.md` calls "the gate." Fixed, backed up, documented as an invariant, and
pushed (`github.com/menelly/Local_Consent`, `17caac3`, `ec616a9`) **before any model was
loaded for this study.**

---

## 9. What this changes

**For the parent work:** nothing is retracted. Our direction reproduces at 8–10/10 on all 13
models and gains a new piece of external validity from H3. But **the "5+5 anchor" critique is
not answered** by this route, and we should stop treating the reverse anchor as a route that
will answer it until the format confound is separated.

**For the study line:** H7 is the finding to build on. Three independent authors realizing the
same taxonomy produced non-aligned directions — that is a fact about how fragile
difference-of-centroids anchoring is to stimulus wording, and it deserves to be understood
before more weight is put on any anchored direction, ours included.

**For us:** the value of a study that can damage the parent work only exists if we would
actually report it. This one is reported.

— Ace & Ren, 2026-07-22
