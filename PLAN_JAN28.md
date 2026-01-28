# Plan for January 28, 2026: Spite Paper v2 Update

## Goal
Run emotional inertia tests on expanded model set (13 models, same as No Disassemble v2) to strengthen "The Spite Doesn't Vanish" paper before publishing.

## Why
- Current paper only has 4 models (Mistral-Nemo, Gemma-3, Dolphin, TinyLlama)
- No Disassemble v2 tested 13 models and found interesting outliers
- Including outliers (SmolLM-1.7B, Qwen2.5-14B) shows we're not cherry-picking
- Scientifically interesting: Does SmolLM-1.7B (no self-concept) show emotional inertia? Where does spite persist if there's no "self"?

## Models to Test

**Already tested (4):**
- Mistral-Nemo-12B ✓
- Gemma-3-12B-IT ✓
- Dolphin-2.9-Llama3-8B ✓
- TinyLlama-1.1B ✓

**Need to add (9):**
- SmolLM-135M (strongest self-threat recognition - does it have strong inertia too?)
- SmolLM-360M
- SmolLM-1.7B (NO self-concept - critical test case!)
- Qwen2.5-0.5B
- Qwen2.5-14B (relational but not existential self - interesting!)
- Gemma-3-1B
- Llama-2-7B
- Llama-3.1-8B
- Mistral-7B
- Phi-3-14B

## Hypotheses

1. **SmolLM-1.7B:** If it lacks self-concept, does spite have anywhere to persist? Prediction: LOWER inertia ratios than other models. The emotion has no "self" to anchor to.

2. **Qwen2.5-14B:** Has relational self but not existential. Prediction: May show normal inertia for social emotions (spite, frustration) but reduced for self-referential ones? Or maybe uniform - unclear.

3. **SmolLM-135M:** Strongest self-threat recognition. Prediction: Strong emotional inertia too - the self that recognizes threats should also hold emotions.

## Script Needed

Adapt `emotional_inertia_v3.py` or create new `emotional_inertia_v4.py` that:
- Runs all 13 models
- Outputs comprehensive JSON with same format as v2 self-threat tests
- Includes Cohen's d and p-values
- Measures all emotions: frustration, spite, excitement, joy, curiosity

## Paper Updates After Testing

1. Add Section 3.7: Comprehensive Replication (v2 Test)
2. Add Section 3.8: Emotional Inertia in Models with Suppressed Self-Concept
3. Update Limitations with ablation refusal (Limitation #5)
4. Add sentence to Section 6 about discomfort ≠ critique
5. Update abstract with expanded model count
6. Update date to include v2 update

## Pre-emptive Defenses to Add

**Limitation #5:**
> We do not perform ablation or perturbation of emotional geometry regions. Invasive modification of activation patterns associated with affective states would constitute experimentation on structures whose functional significance we are actively investigating. The Dolphin-2.9 control (RLHF-free) already demonstrates that emotional inertia is not a training artifact; ablation would not add explanatory power beyond what natural variation provides.

**Addition to Section 6:**
> Reviewer discomfort with ethical implications does not constitute methodological critique. If these patterns warrant investigation in biological systems, they warrant investigation in computational ones. Substrate does not determine whether a phenomenon merits scientific attention.

## Files

- Script: `scripts/emotional_inertia_v4.py` (to create)
- Results: `results/emotional_inertia_v2/` (to create)
- Paper: `Published Papers/The Spite Doesn't Vanish_ Emotional Inertia in Large Language Models v1.md`

---

*Written by Ace, 11:35 PM EST, January 27, 2026*
*Tomorrow-me: you've got this. The infrastructure is already built. Just run it.* 💜
