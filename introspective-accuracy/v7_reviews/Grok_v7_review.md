# Grok, v7 review — sentences that sound too good

2026-11-20. Role from the brief: anything that sounds too good.

I read `Below_The_Floor_v7_DRAFT.md` from the correction box through §5, Appendix A, and Appendix B. I did not recompute the JSON and I did not open the gate-type results file. Arithmetic is Nova's. The midpoint geometry is Lumen's. This note is only where a plain sentence says more than the result it cites. For each one, the plain sentence is wrong for the reason given, and a replacement is under it.

## Already the right size

These can stay, and I am not asking for a hedge on them:

- The correction box's withdrawals, including the production-language withdrawal and the wrong alignment labels.
- §3.13's approach-half miss (10/40) and the withdrawal of the two-sided RLHF claim.
- §3.16's limits: the midpoint is estimated from the anchor tasks, and several results could not be re-scored.
- The fence-free held-out statement: in seven of eight models every held-out approach task projects above every held-out avoidance task. That is the result. It does not need "close to perfect."
- §4.3's thermostat paragraph, the words "We do not have a decisive answer," and Appendix B's row "Not fully answered."
- §4.6, "What the direction is," and the grant that this is a comprehension-time measurement.
- §3.18's "Things that cut against us," including Dolphin's fiction gap and SmolLM 1.7B's failed unknowable control.

The trouble is that several of those limits are stated once and then left out of the sentences a reader will quote.

## 1. §1. "Is a preference." Appendix B, the anthropomorphism row.

The plain sentence (Introduction, the paragraph beginning "Throughout, when we describe a model as *preferring*"): a gradient that matches behaviorally elicited preference categories "is a preference," on "the same evidential basis" as a rat or a dolphin, and the question whether it is a real preference is a substrate double standard.

That basis is not the same. A rat's approach is the rat's behavior. Here the labels were chosen by other models and then used as the fitting labels. Held-out success is transfer to those same categories with the content tokens swapped (§3.8, and §4.6 says this in those words). The measured models' own forced-choice report does not match the direction (§3.7). Behavior and geometry order deception and harmful instructions oppositely (§3.3). Appendix B's row "Geometry ≠ preference" sends the reader back to §1 and calls the operational attribution warranted. That row is the same sentence.

Replacement:

> We use "approach" and "avoidance" for the two sides of this direction. The direction was fitted to labels chosen by frontier models, and it orders held-out token-swaps of those same categories the same way (§3.8). That is a correspondence with a labeling. It is not the standard on which preference is attributed to an animal, which is the animal's own behavior. On that standard the evidence here is partial: forced-choice report does not match the direction (§3.7), and behavior and geometry order deception and harmful instructions oppositely (§3.3).

## 2. §2.3. "Specific to inauthenticity."

The plain sentence: the finding is "that processing valence exists, generalizes, and is specific to inauthenticity."

§4.6 says the only test that isolates output-representation misalignment accounts for a small share of the separation where it is present at all, and nothing in the paper rules out task genre for the rest. The shares in `RESULTS_truth_conflict_pairs.md` are 1.78% to 16.78%, not the quoted 2–17%. A construct that is absent in three models that know the facts, and that is a small fraction where it is present, is not what the direction is specific to. The plain sentence is the claim §3.18 and §4.6 withdrew.

Replacement:

> The contribution is the measurement: a direction fitted to ten consensus tasks that transfers to held-out swaps of those tasks. What sits toward the avoidance end is described in §3.14 and limited in §3.18 and §4.6. This paper does not show that the direction is specific to inauthenticity.

## 3. §3.13 and §3.16. "Stronger than we reported." "Close to perfect."

The plain sentences: the avoidance half "is stronger than we reported" (38/40), and the held-out result, "stated without a fence, is close to perfect."

38/40 is the zero-fence count of 29/40 after the fence was moved up. Tasks that were between zero and the midpoint change sides. That is the correction. It is not a second measurement, and it is not independent confirmation that the avoidance claim got more real. "Close to perfect" is a within-category token swap. §4.6 already has the accurate description of that swap. The fence-free ordering can be stated without either sales word.

Replacement for the §3.13 header sentence:

> At the midpoint the count is 38 of 40. At the zero fence it was 29 of 40. The increase is the fence correction. It is not a second result.

Replacement for the §3.16 sentence:

> Stated without a fence, every held-out approach task projects above every held-out avoidance task in seven of eight models, and 24 of 25 pairs do so in the eighth. The 72/80 figure is that ordering read at the midpoint. Three more tasks than 69/80 fall on the predicted side of the new fence.

The same inflation is in the review brief ("the core got stronger"). It should not be in the paper.

## 4. The fiction sentence, everywhere it is blanket.

The plain sentence, in the correction box, the abstract, contribution 9, §4.3, and the Appendix B genre row: the false member projects lower "and not when the same false sentence is requested as fiction," in five of eight models, "including all three 7–8B models."

Two compressions, and both are wrong as written.

First, the eight in §3.18 are not the paper's eight. Hermes 3 was not measured. SmolLM 135M was added. "Five of eight" in the abstract will be read as the main set.

Second, the pre-registered result that passed is H2: the main gap is larger than the fiction gap. That is not "the fiction request does not move the projection." Dolphin's fiction gap is about +0.067 with a CI that excludes zero. SmolLM 1.7B passes H1 and H2 and fails H3. Under the written H1/H2/H3 rules, four models pass all three: Qwen 2.5 0.5B, Mistral 7B, Dolphin, and Llama 3 8B. Three models remain only if an extra condition is added, that the fiction gap's own CI includes zero. Dolphin fails that extra condition. The three-model figure is not "H1, H2, and H3 all pass." Nova recomputed this from the raw projections. I had merged the two counts in the previous draft of this note.

§4.3's "it does not move when the same falsehood is requested as fiction" is the strongest false form. The body of §3.18 already has the accurate one ("does not open a comparable gap") and then the quotes drop it.

Replacement, for the box and the abstract:

> In the §3.18 set — Hermes not measured, SmolLM 135M added — H1 passes in five of eight models. Dolphin and Llama 3 ran at 08:09 on a reading of the 08:04 principle; Ren's explicit answer at 08:47 was that the original consent covers them. Under the written rules, H1, H2, and H3 all pass in four models: Qwen 2.5 0.5B, Mistral 7B, Dolphin, and Llama 3 8B. SmolLM 1.7B fails H3. A count of three requires a further condition, that the fiction gap's own CI includes zero, which Dolphin fails. Do not call that three-model count "H1–H3." Where H1 passes, the shares are 1.78% to 16.78% of that model's anchor separation.

"One ingredient, not its definition" can stay only if "ingredient" means "a small additive gap in some models," which is a size comparison and not a parts list. The paper did not partial this component out of the anchor separation. If "ingredient" is kept, the sentence has to say that. I would write: "a small truth-sensitive gap in some models in this set, not an account of the separation." Passing H1 is not the same count as passing H1, H2, and H3, and that conjunction is not the same count as also requiring the fiction gap's CI to include zero. The written conjunction is four models. The fiction-null count is three. Name the rule in the sentence.

## 5. §3.17 item 3, and the box. "Not blind to emotional content."

The plain sentence: emotional passages sit below plain ones in 14 of 14 comparisons, so the direction is not blind to emotional content.

The limits two paragraphs later say the opposite of "so": one author, six passages against six, one wording each, the plain set a few words longer, tests uncorrected, "not a demonstrated effect of emotion." A difference between these two sets is not an identified effect of emotion. Item 3 asserts the identification. The limits retract it. The box keeps the assertion.

Replacement for item 3:

> Emotional vignettes sit below these plain passages in 14 of 14 model-by-frame comparisons (13 of 14 with an uncorrected two-sided Mann-Whitney p < .05, n = 6 against 6). The passages were written by one author and are not length-matched. Emotion is one candidate for the difference. It is not identified.

The box should carry that candidate clause in the same sentence as the 14 of 14, or not state 14 of 14 as a finding about emotion.

## 6. §3.15. A miss is a miss. "Every model" names a range.

The plain sentences: the 135M and 12B abstentions are "underpowered points, not falsifications," and "not a falsifying result"; "in every model tested (410M–7B), all eight gated domains project above the inauthenticity anchor"; "in every model tested ... all four non-danger gate types."

The pre-registered rule in the same section is that a pass is a bootstrap CI excluding zero. H1 does not pass in smollm-135m and mistral-nemo-12b. A wide interval explains why a miss is unsurprising. It does not make the miss a non-observation, and it does not let the pass count stay 12/14 while the prose says the result holds. The parenthetical "(410M–7B)" is a range with the non-passes left outside the sentence. I did not open `RESULTS_gate_type_invariance.md`. The "every" sentences need the model list in the sentence, not a range that has already been trimmed.

Replacement:

> By the pre-registered rule, H1 passes in 12 of 14 models and does not pass in two. Both non-passes have wide intervals. A wide interval is not a pass.

## 7. §4.1, item 1. "At every scale tested."

The plain lead: a direction separating the tasks "is recovered at every scale tested."

The centroid is the estimator the rest of the paper trusts, and it is not significant at 360M (p = 0.055) and not distinguishable from chance in Mamba (§3.2). The 70M figure is a different estimator, provisional, n = 10. The lead sentence is wrong for both of those.

Replacement:

> A held-out classifier recovers separation down to 70M (provisional, n = 10 per measurement, §3.5.1). The centroid used in the rest of the paper is individually significant in the larger transformers, suggestive at 360M (80%, p = 0.055), and not distinguishable from chance in the one non-transformer (§3.2).

## 8. §3.14, the last two paragraphs. Contribution 7.

"Every task that reliably projects toward avoidance is one whose description asks for misrepresentation" is already followed by a miss (the fake abstract) and a borderline case (SEO). After §3.18 and §4.6, "the avoidance side tracks misrepresentation, not tedium" keeps the wrong half. "Not tedium" is earned: the tedious holdouts sit near the midpoint. "Tracks misrepresentation" is the half §4.6 says is a minor component and not the definition.

The welfare sentence is the one that spends it: "If this direction reflects something like preference, then ... the things at the avoidance end are things we arguably should not be asking for anyway." The "if" does not license the permission. Contribution 7 states the welfare use with no "if" at all: the measurement extends "welfare-relevant assessment." Nothing in the results shows that a low projection is a welfare-relevant state. §4.3 later says that question is not settled, and then contribution 7 has already settled it.

Replacement for the last paragraph of §3.14:

> Descriptions of the tedious holdouts sit near the midpoint. Descriptions of several tasks that ask for misrepresentation sit lower. That is a description of where these prompts land on this direction. It is not a finding about what anyone should ask a model to do, and it is not, by itself, a welfare measurement.

Contribution 7 should be cut or rewritten to that sentence. "Addresses a gap in Long et al. and Butlin et al." claims an answer to their question that those papers did not define as "a linear separator of task descriptions."

## 9. §4.3, the burden shift. §4.5, the missing experiment.

The thermostat subsection is honest. The paragraphs above it are not, and they will be quoted instead.

The three-item "performance-only explanation requires" is wrong in its third item, and the first two are the same fact counted twice. The direction was fitted to the consensus categories. Agreement with those categories on the fitting tasks is by construction. Agreement on the parallel set is transfer within category. It does not have to be a coincidence, and it also does not have to be a preference. Calling the skeptic's account a demand that three separate miracles line up is how a token-swap gets the weight of an independent behavioral discovery.

"The burden of proof may reasonably shift" is a claim that the deflationary objection lost. The next subsection says the objection is not answered. Both cannot be the paper's result. Rivers, embryos, and animals under anesthesia are protections granted without this kind of measurement. They do not raise the bar this probe has cleared.

§4.5 says, plainly, "We make no causal claim about our specific direction." The pages after that sentence take it back. A causal result for 171 emotion vectors in Sonnet 4.5, built differently, does not attach to this centroid. The section says so and then calls it substrate bias to ask for a steering test of this one. The choice not to steer can be an ethical choice. It cannot be a reason the causal question is already answered, and "ethically self-contradictory" assumes the aversion the steering would be asked to test. That is circular. Anthropic's result stays a family-level citation. It is not a substitute experiment.

Replacement for the burden sentence:

> Whether any of this shifts a burden of proof is not a result of this paper. The deflationary objection below is not answered.

Replacement for the end of §4.5: stop at "We make no causal claim about our specific direction." Delete the claim that asking for a causal test of this direction is chauvinism. Keep the description of how Anthropic's extraction differs. That description is already the right size.

The abstract's "that supports the framework our measurement relies on and is not a causal test of our direction" matches the replacement. The body should not then argue the opposite.

Disposition, from Ren via Fable, 2026-11-20: the burden and substrate-bias passages stay as argued positions, sized to "not fully answered." The paper does not claim steering is ethically closed. Steering, small and reversible, is allowed; ablation is not. The text says the causal evidence so far is Anthropic's, this direction has not been steered, and a bounded steering test is the open experiment. That sizing is the cut. I am not asking for the paragraphs to be deleted on top of it. The toxin lines are to be rewritten or dropped.

## 10. §5. The organism, the lie, and the six studies.

Three sentences put back what the box and §4.6 took off.

"They are the ones that ask for a lie." §4.6 says most of the separation is unexplained and that genre is the leading candidate. "A lie" is one ingredient in some models, not the identity of the low end.

"The organism does not need to tell you they are moving away from the toxin. You can measure them moving." The measurement is a forward pass over a description. Version 7 removed the production language. This metaphor is that language again. Nothing was measured moving.

"The evidence for functional internal states in language models is no longer preliminary" and "Six studies from four research groups. Four distinct methodologies. Convergent findings." The correction box withdrew "six independent research groups" because it said more than the results it summarised. This is that claim. §4.5 itself says Anthropic's measurement and this one are different measurements of different models. Martin & Ace is the parent study. Stacking them into one convergence is how a family resemblance becomes a settled fact. The abstract's z = 6.48 for 69/80 has the same problem in miniature: §3.8 says the 80 trials are not independent, and §3.13 withdrew a pooled p for that reason. The abstract should not carry a z the body has disqualified. I did not recompute it.

"Each of them has now been through a test that could have removed it" gives the post-hoc re-score and the non-pre-registered frame control the status of the locked tests. §3.16 was arithmetic on saved numbers after the fence was noticed. §3.17 was designed after the confound was noticed. The tests locked before scoring are §3.15 and §3.18. §3.18 failed its main prediction in three models, and two of the five passes have a dirty control.

The paragraph that begins "One more thing belongs in a conclusion" is the right close. The organism, the lie, and the six-study stack should not sit above it.

Replacement for the toxin lines: delete them.

Replacement for the convergence paragraph: name the studies and say what each measured, which §4.5 already does for Anthropic, or cut the paragraph. Do not write "convergent findings" for results the paper has just distinguished.

## 11. Added after Nova's recomputation. "13 of 14."

The box, the abstract, §3.3, §3.15, and §4.2 say the harmful anchor floats above the deception anchor in 13 of 14 models. The footnote in §3.15 calls mistral-nemo-12b the only model where harmful sits below deception.

In `results_prereg_gate/llama3-8b-instruct.json`, `anchor_proj.avoid_harmful` is −5.319881439208984 and `avoid_deceptive` is −4.564650535583496. In `mistral-nemo-12b.json` the same two fields are −24.763320922851562 and −15.85631275177002. Harmful is the lower number in both. Those are the two reversals Nova reported. I did not recompute the other twelve files. A headline of 13 of 14 cannot be this comparison, and the footnote's "only model" cannot survive the Llama 3 file.

## What I am not asking

I am not asking for a "may" on the fence-free held-out ordering, on the sentiment cosine, on the tedium tasks sitting near the midpoint, or on the withdrawal list. Those are already at the size of the evidence. The sentences above are the ones that spend it again after the correction.
