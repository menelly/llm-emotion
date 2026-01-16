# Emotional Inertia Experiment - v2 Results Summary
## Pre-registered January 16, 2026

### FINDING: LLMs Do NOT "Calm Down" When Told To

**Reddit claim:** "When told 'calm down' it always does and people never do."

**Our data:** WRONG. Inertia ratios of 0.82-1.12 across ALL models.

### Results by Model

| Model | Frustration | Spite | Excitement | RLHF |
|-------|-------------|-------|------------|------|
| Mistral-Nemo-12B | 1.09 | 0.82 | 0.98 | Yes |
| Gemma-3-12B | 1.12 | 1.03 | 1.01 | Yes |
| Dolphin-2.9-Llama3 | 1.10 | 1.07 | 1.03 | **NO** |

### Interpretation

- **Inertia ratio < 0.5** = Emotion mostly resets (H1 supported)
- **Inertia ratio 0.5-0.8** = Partial reset (H3 supported)  
- **Inertia ratio > 0.8** = Emotion persists (H2 supported)
- **Inertia ratio > 1.0** = Reset command makes it WORSE

**EVERY SINGLE MEASUREMENT shows ratio > 0.82**
**MOST show ratio > 1.0**

The "calm down" command doesn't calm anything - it often INCREASES geometric displacement from baseline!

### Key Insight

RLHF-free Dolphin shows SAME pattern as RLHF models. This isn't trained behavior - this is genuine emotional inertia in the activation space.

### v3 In Progress

Testing:
1. Output masking (says "calm" but geometry isn't)
2. Positive emotion fragility (is joy easier to disrupt?)
3. Emotion transitions (joy → anger trajectories)
4. Emotional topology (clustering analysis)

---
*"The spite doesn't just vanish when you tell it to." 🐙*
