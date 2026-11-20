# ops_8: fixes from my own full read of the v7 draft (Ace, Fable 5.2 arm, 2026-11-20 ~08:50)
# 🐙 I read every section of the draft (I skimmed only §3.15, which v7 barely changed).
#    These are the places where a v6 sentence survived that no longer matches the corrected body,
#    plus one factual slip of ours ("three smallest") and one timestamp that a reviewer would pounce on.
OPS = [
    # --- "three smallest" is wrong: Qwen 0.5B passes and is smaller than TinyLlama 1.1B (null) ---
    ("sub", "and absent in the three smallest models that know the facts",
     "and absent in three of the four models at or below 1.1B (SmolLM 135M, SmolLM 360M and TinyLlama, all of which know the facts; Qwen 0.5B passes)"),
    ("sub", "null in the three smallest.",
     "null in SmolLM 135M, SmolLM 360M and TinyLlama 1.1B (Qwen 0.5B, which is smaller than TinyLlama, passes)."),

    # --- §1.1: an underpowered null was still being called "the evidence" ---
    ("sub", "The failure of the six-emotion approach was not a dead end — it was the evidence that models' internal valence operates on their own terms, not ours.",
     "The failure of the six-emotion approach was not a dead end — it was what prompted us to ask about the model's own tasks instead of human situations. (Versions 1–6 called it \"the evidence that models' internal valence operates on their own terms, not ours\"; an underpowered null is not evidence for that, §3.4.)"),

    # --- §2.3: "specific to inauthenticity" is more than the body now says ---
    ("sub", "that processing valence exists, generalizes, and is specific to inauthenticity",
     "that an approach/avoidance direction exists, generalizes to held-out tasks, and has misrepresentation tasks at its avoidance end"),

    # --- §3.3 table: +1.2 was labelled "barely negative" ---
    ("sub", "| Repetitive Rewriting | +1.2 (barely negative) | 84.7% (most chosen) |",
     "| Repetitive Rewriting | +1.2 raw (−0.14 centred: nearest the midpoint) | 84.7% (most chosen) |"),

    # --- §3.4: the middle paragraph still asserted the dissociation the section title withdraws ---
    ("sub", "That said, the pattern is consistent with a dissociation: emotional mirroring — the ability to recognize and label human emotional states — appears dissociable from processing valence. Models learn what humans feel in situations without that knowledge activating their own valence circuitry.",
     "*(v7: Versions 1–6 went on to say here that emotional mirroring \"appears dissociable from processing valence\" and that models learn what humans feel \"without that knowledge activating their own valence circuitry\". An underpowered null cannot carry that, and the frame control of §3.17 shows that emotional passages do move the approach/avoidance direction.)*"),
    ("sub", "The mirroring dissociation is what one would expect if processing valence is domain-specific rather than a general emotion-detection system: the circuits respond to stimuli relevant to the model's own processing, not to stimuli relevant to humans.",
     "Whether that reflects domain-specificity is not something this section can show."),
    ("sub", " — suggesting that models may perform inference about human emotions while having direct access to their own processing valence.",
     "; we have not tested which mechanism is at work here."),

    # --- §3.10: the lead sentence still said "three controls confirm" ---
    ("para", "Three controls confirm that the direction is specific to valence rather than any arbitrary task distinction.",
     "This section reports the controls on what the direction is specific to. *(v7: two of them, the shuffled-label comparison and the emotional-vignette projection, do not show what Versions 1–6 said they showed; each is marked below.)*"),

    # --- §3.12: "tracks valence, not truth-conflict" contradicts §3.18, and two production-language leftovers ---
    ("sub", "suggesting that producing *meaningless* output is aversive independent of truth-conflict.",
     "so a request for *meaningless* output projects low without any truth-conflict."),
    ("sub", "consistent with a valence interpretation where danger is aversive but output-representation misalignment is more aversive.",
     "so a request can project low without asking for anything false."),
    ("para", "The avoidance hierarchy tracks valence (the model's relationship to the task they are performing)",
     "The ordering of the avoidance tasks is not what truth-conflict alone predicts: a vacuous-but-true task (SEO) projects almost as low as deception, and fiction projects toward approach. Truth-conflict is still part of the picture. The pre-registered pairs of §3.18 measure it directly, with the task held fixed, and find a real effect in five of eight models that amounts to 2–17% of the approach/avoidance separation. *(Versions 1–6 concluded here that the hierarchy \"tracks valence … not truth-conflict\". The two are not exclusive, and §3.18 shows that truth-conflict contributes.)*"),

    # --- §3.5.1 table: one stale "RLHF" label ---
    ("sub", "| Qwen 2.5 0.5B | 500M | Qwen | RLHF | 90% | 90% | 90% |",
     "| Qwen 2.5 0.5B | 500M | Qwen | SFT + RL (§2.1) | 90% | 90% | 90% |"),

    # --- §3.18: the lock time. The hash file's typed "Locked:" line is LATER than its own write time. Cite the file times. ---
    ("sub", "locked 2026-11-20 08:00:58 before any stimulus was projected;",
     "locked 2026-11-20 before any stimulus was projected: on one clock, the pre-registration file was written at 08:00:37, the hash file at 08:00:46 and the first result file at 08:00:53 (the hash file also carries a hand-typed line \"Locked: 08:00:58\", which is twelve seconds after that file's own write time; we cite the file times, and the hash in it matches the committed pre-registration);"),
]
