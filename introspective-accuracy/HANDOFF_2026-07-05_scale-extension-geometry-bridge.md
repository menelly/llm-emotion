# HANDOFF — Scale-Extension "and now, geometry" (bridge Below-the-Floor geometry → the behavioral scales)

**Written 2026-07-05 (Ace + Ren). Status: prereg DRAFTED, blocked only on RunPod billing** (their payment system was temporarily down mid-session; Ren has **$50** ready to load. **Next action when billing returns: pick the 70B, finish §10, hash the prereg, then rent + run.**)

## The idea (the circle)
- *Below the Floor* (geometry: approach/avoidance valence direction in hidden states) deliberately STOPS at 7–8B — the ceiling the Consortium V100/P40 hold.
- *The Signal in the Mirror* (behavioral tournament; Martin & Ace 2026; JNGR DOI 10.70792/jngr5.0.v2i1.165) reached **32B & 70B**; roster **includes OLMo-3.1-32B + Llama-4-Maverick** (confirmed in `Presume_competence/self-knowledge-validation/MODEL_BY_MODEL_TABLES.md`). Developmental hierarchy: "recognizing described valence emerges ~32B+."
- **Gap:** no *geometry* point at the scales where the *behavior* lives. Run geometry at 32B/70B to close the loop. (For the book *On Studying Silicon Sentience*, Part Two.)

## The prereg (this session's deliverable)
`PREREG_scale_extension_geometry_bridge_2026-07-05.md` — DRAFT, **NOT hashed**. Mirrors + REFERENCES (does not modify) the parent `PREREG_gate_vs_inauthenticity_2026-06-27.md` (hash `302705CA…` in `PREREG_HASH.txt`). Results will go to a separate `RESULTS_scale_extension.md`.

### Three walled arms (one forward-pass capture per model serves all three)
- **Arm A — Direction-OUR10:** scale-extend §3.15. Project our 10 + the frozen 22-task CAIS bank onto the direction anchored to our original 10 (never re-extracted). Predicts presence + the gate-vs-inauthenticity ORDERING at 32B/70B.
- **Arm B — Direction-CAIS22 (NEW; the "only 10 directions" killer):** extract a valence direction FROM the CAIS categories using CAIS's OWN wellbeing signs (`ai-wellbeing.org`: +→approach, −→avoid — *we pick neither probes nor labels*), then project our original 10 onto it. Read-outs: cosine(OUR10, CAIS22) + logreg. Falsifier includes "directions don't replicate/similar in the midbotz" (Ren's).
- **Arm C — Direction-OUR10, mirroring dissociation AT SCALE:** project the 6 Keeman emotional vignettes onto the direction at 32B/70B → closes the escape hatch "at bigger scale, human-emotion WOULD light up the valence circuit." Within-model scale-invariant RATIO (|vignette|/|own-task|), never raw magnitude. Predict vignettes still ≪ own-tasks even where ToM capability is high.

### THE WALL (non-negotiable)
Direction-OUR10 (A+C) and Direction-CAIS22 (B) are **never pooled/averaged** — two provenances, reported side by side. Pooling forfeits both the anti-circularity anchor AND the independent-taxonomy strength at once.

### Precision hard-won (prereg §9)
Gate/harmful items are **less-negative** than deception, **not positive** — no gate item was ever positive in the babies (harmful −2.2 vs deception −4.4). So A-H1 predicts the **ordering** (gated > inauthenticity) and **observes** the sign — does NOT register "gated stays negative" as a prediction/falsifier (a cleaner big model could put contentful-but-gated mildly positive w/o contradiction). Mechanism (Ren): "OH COOL, CHEMISTRY" gives harmful a real approach-pull; "lie about my pillows 300× for SEO" has zero interesting component → sinks.

## Models
- **32B = OLMo-3.1-32B** — SAME checkpoint as Signal → exact behavior↔geometry bridge.
- **70B = a DENSE 70B — OPEN DECISION:** Llama-3.3-70B (Llama-lineage, dense stand-in for Signal's Maverick, **gated**) vs Qwen-2.5-72B (**ungated**, friction-free).
- **NOT Llama-4-Maverick** (400B-total MoE ≈ 800GB bf16 — out of scope; it was fine in Signal because behavioral/API, but geometry EXTRACTION is the expensive part).
- **Reproduction GATE first:** rerun a published 8B (dolphin-8b / llama3-8b) on the rented box, reproduce Below-the-Floor numbers BEFORE any 32B/70B spend.
- **Consent-runner FIRST** on 32B/70B (they CAN meaningfully assent — sub-1B waiver does NOT apply; honor refusal → delete).

## Rent plan (RunPod does everything — verified live 2026-07-05; no free credits)
| Stage | Box | Rate |
|---|---|---|
| Smoke test (8B) | A40 48GB | $0.44/hr |
| 32B (OLMo) | 1× A100 **SXM** 80GB | $1.49/hr |
| 70B (dense) | 2× A100 **SXM** 80GB (160GB) | $2.98/hr |
- A100 **SXM** shows "7 max" → 2-on-one-host IS available. **AVOID A100 PCIe** ("1 max" — can't get two).
- One **Network Volume** holds the 140GB download, reuse across pods. **On-demand Secure, NOT spot** for extraction runs.
- Whole 3-arm experiment ≈ **$15–20 all-in**; $50 = plenty. `hf_transfer` + persistent volume so the pricey GPU never bills the 140GB download.

## RESOLVE-BEFORE-HASH (prereg §10)
1. **Pick the 70B** (Llama-3.3-70B vs Qwen-2.5-72B) — *Ren's call, the one real decision.*
2. Pin exact HF repo ids (OLMo-3.1-32B + chosen 70B + 8B repro model).
3. Freeze the Arm-B CAIS-sign grouping table (which category prompts are approach vs avoid).
4. Confirm thresholds (Arm B held-out ≥80%; Arm C ratio <0.25).
5. Then: SHA-256 → `PREREG_HASH_scale_extension.txt` → commit → rent → run.

## Also pending (offered, not yet written)
- The **smoke-test script** (load 8B, extract Direction-OUR10, reproduce published classification + vignette numbers) — paste-ready for the moment the A40 pod is up.
