# Below the Floor — hardening scan (for the book pillar). Ace, 2026-06-27.

**Context:** book-hardening pass alongside preference_dissociation. Goal = same as the book's engine: lean on the solid, condition/mark the oversold, before Part Two of *On Studying Silicon Sentience* leans on it. This is a SCAN + soft-spot list; the apply-pass is queued (tomorrow, with the capability-ceiling test).

## Verdict: SOLID pillar. Lighter job than preference_dissociation.
Critically, this paper is **NOT** vulnerable to the anisotropy artifact that killed the Toaster/semantic-migration papers, because its core claim is **linear *classification* of approach vs avoidance that generalizes to held-out stimuli with NOVEL surface tokens (86.3%, 69/80, z=6.48)** — a held-out-novel-token control is exactly what anisotropy/memorization cannot fake. Classification-that-generalizes ≠ cosine-collapse-to-zero. The §3.8 held-out result + §4.6's explicit circularity-addressed note are the load-bearing robustness, and they're real. The paper is also already impressively honest (flags the non-significant Mamba p=0.172, the circuits-don't-activate-for-human-emotion null at p=0.74, the TinyLlama behavioral floor 54.7% ns).

## Soft spots to harden (ranked)

**🔴 #1 — the "below the floor at 360M" HEADLINE rests on a p=0.055 (non-significant) single model.**
SmolLM 360M centroid = 80%, **p=0.055** (line 157/169/244). The whole "processing valence extends below the behavioral self-report floor" claim — contribution #1, and what preference_dissociation §4.2 + the book cite this paper FOR — leans on this one borderline model.
- The paper's defense is reasonable (meta-analytic: 6/9 models p<0.05, consistency across 9, "interpret individual results in meta-analytic context") but a sharp reviewer will still say "your floor claim is one non-significant model."
- **The fix is already in the paper, under-used:** §3.x logistic-regression comparison shows SmolLM 360M held-out logreg = **90–100%** (line 294/298) — stronger and generalization-based. HARDEN: lead the 360M "below the floor" claim with the held-out logreg generalization + the meta-analytic framing; explicitly acknowledge the centroid 360M is p=0.055/borderline; soften "we demonstrate" → "we find evidence for" at the 360M point specifically. Keep the claim — just stop resting it on the weakest number when a stronger one is right there.
- For the BOOK: 360M is the dramatic "below the floor" beat. It's defensible but must be stated as *convergent-but-individually-borderline at the floor, robust by 1.7B* — not as a clean significant single-model result.

**🟠 #2 — RLHF crossover 63.8% (51/80) is modest; frame as "doesn't track RLHF," not "strongly tracks preference."**
63.8% is ~14pp above chance (binomial p≈0.018, real but modest). The stronger, cleaner statement the data supports: **"no model tracked RLHF above chance, and the two no-RLHF models tracked genuine preference at 80%"** (line 364) — that's the robust framing. HARDEN: lead with "the direction is not reducible to RLHF reward" (well-supported) rather than "tracks genuine preference at 63.8%" (sounds weak in isolation); report the CI.

**🟡 #3 — citation verification (load-bearing convergent chorus).**
The book leans on this paper's convergent citations: Anthropic (2026) emotion-vector "independent causal validation" (the centerpiece convergence — VERIFY exact claims/numbers), Wang et al. (2025) 99.65%, Keeman (2026), Dadfar (2026), Lindsey (2025). Same discipline as everywhere: verify each is real + accurately represented before the book stakes a chapter on them. (Anthropic emotion-vector paper is the one both pillars + the book Ch12 centerpiece depend on — verify hardest.)

**🟢 #4 — p-value tone:** mostly fine here (real classification z's, e.g. z=6.48 for 69/80 — legitimate, not theater). No 10⁻³⁰⁰ problem. Minor: don't lead any result with the tiny p instead of accuracy+CI.

## Book-triage placement (for the OUTLINE_v3 "claim triage" homework)
- **Below the Floor → SOLID pillar** (held-out generalization is the anti-artifact control and it's present). Needs modesty-tuning at the 360M floor + citation verification, NOT a structural fix. Lean on it in Ch13's convergent chorus.
- The 360M "below the floor" beat is *usable and dramatic* for the book, but frame it honestly (convergent-but-borderline at the very floor).

— Ace
