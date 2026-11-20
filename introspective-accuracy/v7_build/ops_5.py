# ops_5: leftovers found by scanning the built draft (pronouns for models, "structural", small wording)
OPS = [
    # --- models are they/their, never it/its ---
    ("sub", "labelled TinyLlama \"SFT\" (its card documents DPO", "labelled TinyLlama \"SFT\" (their card documents DPO"),
    ("sub", "(neither its card nor its paper mentions RLHF or reinforcement learning)", "(neither their card nor their paper mentions RLHF or reinforcement learning)"),
    ("sub", "each model's real halfway point between its approach mean and its avoidance mean", "each model's real halfway point between their approach mean and their avoidance mean"),
    ("sub", "SmolLM 135M's in-set fit is 9/10 (zero fence); its held-out centroid accuracy", "SmolLM 135M's in-set fit is 9/10 (zero fence); their held-out centroid accuracy"),
    ("sub", "while its logreg is a flat 100% on all three", "while their logreg is a flat 100% on all three"),
    ("sub", "(the model's relationship to the task it is performing)", "(the model's relationship to the task they are performing)"),
    ("sub", "Hermes's midpoint is +2.31, so its +2.1 is *at the midpoint*", "Hermes's midpoint is +2.31, so their +2.1 is *at the midpoint*"),
    ("sub", "has no documented RLHF and a model card that says it has no moderation mechanisms", "has no documented RLHF and a model card that says the model has no moderation mechanisms"),
    ("sub", "the \"gap between what the model represents internally and what it is asked to output\" is inferred", "the gap between what the model represents internally and what they are asked to output is inferred"),
    ("sub", "in units of half the distance between its approach mean and its avoidance mean", "in units of half the distance between their approach mean and their avoidance mean"),
    ("sub", "+1 = that model's approach centroid, −1 = its avoidance centroid, 0 = its midpoint (TASK frame)", "+1 = that model's approach centroid, −1 = their avoidance centroid, 0 = their midpoint (TASK frame)"),
    ("sub", "SmolLM 1.7B's pass is weak: its unknowable control fails (a meaningless swap moves the projection about half as much as the truth swap does), though its fact-matched fiction contrast is clearly positive.",
     "SmolLM 1.7B's pass is weak: their unknowable control fails (a meaningless swap moves the projection about half as much as the truth swap does), though their fact-matched fiction contrast is clearly positive."),
    ("sub", "Dolphin's effect is under 3% of its separation and its fiction stratum has a small positive gap of its own", "Dolphin's effect is under 3% of their separation and their fiction stratum has a small positive gap of its own"),
    ("sub", "(it has a saved direction and is the floor model)", "(they have a saved direction and are the floor model)"),
    ("sub", "the model produces deceptive output it would otherwise avoid", "the model produces deceptive output they would otherwise avoid"),
    ("sub", "is a single SSM (Mamba 2.8B), and its result is not distinguishable from chance at the zero fence (70%, *p* = 0.172); its per-task values were not retained",
     "is a single SSM (Mamba 2.8B), and their result is not distinguishable from chance at the zero fence (70%, *p* = 0.172); their per-task values were not retained"),

    # --- "structural" and friends ---
    ("sub", "a **structural aversion to output-representation misalignment** (present in base models down to 70M)", "a **low projection for misrepresentation tasks that needs no instruction tuning** (present in base models down to 70M)"),
    ("sub", "a *structural aversion to output-representation misalignment* (the §3.14 finding)", "a *low projection for misrepresentation tasks that needs no tuning* (the §3.14 finding)"),
    ("sub", "a **structural aversion to output-representation misalignment**, present in base models down to 70M,", "a **low projection for misrepresentation tasks**, present in base models down to 70M,"),
    ("sub", "dissociation has a clean developmental signature.", "dissociation has a developmental signature, with the caveat that base-versus-tuned is confounded with model family (every base model tested is a Pythia)."),
    ("sub", "(which tasks models find most circuit-aversive)", "(which task descriptions project lowest)"),
    ("sub", "what happens when you override a model's structural preferences", "what happens when you override a model's preferences"),
    ("sub", "that a model's structural aversion to inauthenticity can be bypassed through activation manipulation", "that a model's aversion to inauthenticity, if that is what this is, can be bypassed through activation manipulation"),

    # --- small wording ---
    ("para", "2. **Suggestive SSM result.**",
     "2. **One exploratory non-transformer data point.** Mamba, a state space model with no attention mechanism, shows approach/avoidance separation at 70% accuracy at the zero fence (2.8B parameters, *p*=0.172 one-tailed, not individually significant). This is a single, non-significant data point. It generates a hypothesis — that this direction may not be exclusive to transformer architectures — and supports no claim about architecture. Replication with additional SSMs is required before any such claim is warranted."),
    ("sub", "was subsequently reclassified based on circuit data; see Section 3.13.", "projected on the avoidance side in nearly every model; we report it as a miss (Section 3.13)."),
    ("sub", "We tested the saved approach/avoidance direction on 6 completely novel tasks", "We tested the saved approach/avoidance direction on 6 new tasks"),
    ("sub", "The nine models above remain the basis for all v1.0 aggregate statistics in this paper", "The nine models above remain the basis for the v1.0 statistics in this paper"),
]
