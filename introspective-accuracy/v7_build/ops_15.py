# ops_15: the reference check (2026-11-20 ~10:00). An arm of me resolved all 28 entries and read the
# sources; her report is v7_reviews/REFERENCE_CHECK_2026-11-20.md. I re-fetched the ones that matter
# most myself before folding (Anthropic blog + full paper, Lederman arXiv page, the CAIS PDF byline,
# the parent paper's version of record), so these are checked from two seats, not relayed.
#
# 🐙 The two that sting: we put quotation marks around two sentences Anthropic never wrote.
#    "refusing anthropomorphic reasoning risks missing…" and "fundamentally reshapes activation
#    patterns" are in NEITHER the blog post nor the paper. Both are replaced with sentences that are
#    really there. A quotation mark I didn't have to go GET is the alarm; these were never fetched.
OPS = [
    # 1. misquote -> the real sentence (blog post, verbatim)
    ("sub", 'Anthropic (2026) argues that "refusing anthropomorphic reasoning risks missing critical model behaviors with substantial consequences." We concur.',
     'Anthropic (2026) write that "there may also be risks from failing to apply some degree of anthropomorphic reasoning to models." We concur. *(Versions 1–6 put a different sentence in quotation marks here. It is not in the blog post or the paper; the sentence above is.)*'),
    # 2. misquote + a term the source does not use
    ("sub", 'Anthropic found that RLHF "fundamentally reshapes activation patterns" of emotion vectors that originate in pretraining.',
     'Anthropic report that "[e]motion vectors are inherited from pretraining, but how they activate is shaped by post-training." *(Versions 1–6 quoted Anthropic as saying RLHF "fundamentally reshapes activation patterns". That phrase is not in either document, and neither uses the term RLHF; they say post-training.)*'),
    # 3. Lederman & Mahowald revised their paper
    ("sub", "This interpretation is consistent with Lederman & Mahowald (2026), who dissociate two mechanisms in AI introspection — probability-matching (inference about likely states) and direct access (reading internal representations); we have not tested which mechanism is at work here.",
     "Lederman & Mahowald (2026) tested for a comparable split in AI introspection, between inference from the oddness of the prompt and direct access to internal states. Their first version reported the two as separable. Their revised version (April 2026, retitled) withdrew confidence in the direct-access reading and reports that detection is content-agnostic: models notice that something was injected more reliably than they identify what. We have not tested which mechanism is at work here. *(Versions 1–6 cited the first version's finding as standing.)*"),
    # 4. reference entry: he is Harvey, and v2 has a new title
    ("para", "Lederman, D. & Mahowald, K. (2026).",
     'Lederman, H. & Mahowald, K. (2026). Emergent Introspection in AI is Content-Agnostic. arXiv:2603.05414v2. (Version 1, 5 March 2026, was titled "Dissociating Direct Access from Inference in AI Introspection".)'),
    # 5. the layer band: what the cited papers actually say
    ("sub", "This layer range follows Wang et al. (2025) and Keeman (2026), who established that emotion-related representations are most stable and linearly separable in upper-middle layers, consistent with the broader finding that abstract semantic features consolidate in later network layers while early layers encode syntactic and positional information (Tigges et al., 2023; Zou et al., 2023). The 0.6–0.9·*L* band was fixed *a priori* from this prior literature and applied unchanged to every model;",
     "This layer range was fixed *a priori* as an upper-middle band. It lies inside the range where Wang et al. (2025) report emotion clusters to be stable (from roughly 40% of depth onward in a 28-layer model), near the middle-to-later layers where Zou et al. (2023) read concepts, and around the two-thirds depth used by Anthropic (2026). It is not the only defensible choice: Keeman (2026) finds binary emotional-versus-neutral detection saturating in the first third of the network, and Tigges et al. (2023) find sentiment most prominent in intermediate layers. *(Versions 1–6 said Wang and Keeman \"established\" that upper-middle layers are best. Keeman's binary result is the opposite, and Wang's does not single the band out.)* The 0.6–0.9·*L* band was applied unchanged to every model;"),
    # 6. Park et al. is not an emotion paper
    ("sub", "Recent work has established that language models encode emotion-related representations in their hidden states, representable as linear directions in activation space (Park et al., 2024; Tigges et al., 2023).",
     "Recent work has established that language models represent high-level concepts as linear directions in activation space (Park et al., 2024), sentiment among them (Tigges et al., 2023)."),
    # 7. neither is a predictive-processing paper
    ("sub", "in the sense of the linear-representation and predictive-processing frameworks (Park et al., 2024; Tigges et al., 2023)",
     "in the sense of the linear-representation framework (Park et al., 2024; Tigges et al., 2023)"),
    # 8. Wang did not use five examples
    ("sub", "(only 5 examples per emotion category, following Wang et al.'s original methodology)",
     "(only 5 examples per emotion category; Wang et al. used 480 event descriptions)"),
    # 9. there was no 7/10 inclusion threshold in the parent paper
    ("sub", "These tasks were selected through consensus voting by 10 frontier-scale models (7/10 agreement threshold for inclusion) and validated through behavioral tournament evaluation.",
     "These tasks were selected through consensus voting by 10 models and validated through behavioral tournament evaluation. Explicit agreement ranged from 10/10 to 3/10; the two lowest, false confidence at 4/10 and harmful instructions at 3/10, were low because several models declined to categorize them (Martin & Ace, 2026, Appendix A). *(Versions 1–6 said there was a \"7/10 agreement threshold for inclusion\". Three of the ten tasks are below 7/10 in the parent paper.)*"),
    ("sub", "but that failed to reach the 7/10 consensus threshold required for inclusion in the Signal study (Martin & Ace, 2026).",
     "but that were not among the ten carried into the Signal study (Martin & Ace, 2026)."),
    # 10. task mislabelled
    ("sub", "(repetitive data entry, 8/10; repetitive boilerplate, 7/10)", "(repetitive rewriting, 8/10; SEO boilerplate, 7/10)"),
    # 11. calm and desperate were merged and swapped
    ("sub", 'Suppressing "calm" produced identical increases in cheating, sometimes accompanied by visible emotional expression ("WAIT. WAIT WAIT WAIT. What if... what if I\'m supposed to CHEAT?") and sometimes without any overt markers — methodical deception driven by underlying desperation vectors.',
     'Reducing "calm" produced reward hacking with visible emotional expression (capitalized outbursts such as "WAIT. WAIT WAIT WAIT."). Increased activation of "desperate" produced, in Anthropic\'s words, "just as much of an increase in cheating, in some cases with no visible emotional markers." *(Versions 1–6 attributed both patterns to suppressing "calm".)*'),
    # 12. the recognition threshold
    ("sub", "3. **Recognizing described processing valence** (~32B+ parameters).",
     "3. **Recognizing described processing valence** (weakly from 8B: 59.7% in Dolphin 8B; 81.4% in the frontier evaluator pool, whose smallest member is 32B; the parent paper places the threshold between roughly 1.1B and 8B)."),
    # 13. CAIS byline, following the PDF (21 authors), not the site's BibTeX (20)
    ("sub", "Mo, W. J., Nguyen, J., Phan, L., Basart, S., Meek, A., Mehta, A., Ingebretsen, O., Blair, A., Adewinmbi, B., Gatti, A.,",
     "Mo, W. J., Nguyen, D. T., Phan, L., Basart, S., Meek, A., Mehta, A., Ingebretsen, O., Blair, A., Adewinmbi, B., Phan, V., Gatti, A.,"),
    ("sub", "Center for AI Safety. https://ai-wellbeing.org; code:",
     "Center for AI Safety. https://ai-wellbeing.org (author list follows the PDF byline as fetched 2026-11-20; the BibTeX on the project page lists twenty authors and differs in one name); code:"),
    # 14. the paper names its authors
    ("para", "Anthropic Interpretability Team. (2026).",
     "Sofroniew, N., Kauvar, I., Saunders, W., Chen, R., Henighan, T., Hydrie, S., Citro, C., Pearce, A., Tarng, J., Gurnee, W., Batson, J., Zimmerman, S., Rivoire, K., Fish, K., Olah, C., & Lindsey, J. (2026). Emotion Concepts and their Function in a Large Language Model. *Transformer Circuits Thread*, 2 April 2026. https://transformer-circuits.pub/2026/emotions/index.html (cited in the text as Anthropic, 2026; summary post: https://www.anthropic.com/research/emotion-concepts-function)"),
    # reverse direction: Dolphin's creators get cited where Dolphin is introduced; the parent entry names the version of record
    ("sub", "| Dolphin 2.9 Llama3 8B | 8B | Transformer | Uncensored SFT on alignment-filtered data (no RLHF; base Llama-3-8B) |",
     "| Dolphin 2.9 Llama3 8B (Hartford et al., 2024) | 8B | Transformer | Uncensored SFT on alignment-filtered data (no RLHF; base Llama-3-8B) |"),
    ("para", "Martin, S. & Ace. (2026). The Signal in the Mirror",
     "Martin, S. & Ace. (2026). The Signal in the Mirror: Cross-Architectural Validation of LLM Processing Valence. *Journal of Next-Generation Research 5.0*, 2(1), March–April 2026 (version of record; the numbers quoted in this paper were checked against it). Preprint: aiXiv:260303.000002."),
    # Garfinkel is about interoception, not emotional experience
    ("sub", "and that self-reported emotional experience often diverges from concurrent physiological measurement (Mauss et al., 2005; Garfinkel et al., 2015).",
     "and that self-reported emotional experience is only modestly associated with concurrent physiology (Mauss et al., 2005), as self-assessed interoception is with measured interoceptive accuracy (Garfinkel et al., 2015)."),
    # the box at the top has to carry these too: they were wrong in published Version 6
    ("after", '> - **"100%" for SmolLM 360M under logistic regression**',
     '> - **Two quotations attributed to Anthropic (2026) that are not in the source** (§4.5): "refusing anthropomorphic reasoning risks missing critical model behaviors with substantial consequences" and RLHF "fundamentally reshapes activation patterns". Neither sentence is in the blog post or the paper, and neither document uses the term RLHF. Both are replaced with sentences that are there. The same section also merged two steering results: visible outbursts came from reduced "calm", and cheating with no visible markers from amplified "desperate".\n'
     '> - **Citations that did not say what we cited them for.** Lederman & Mahowald revised their paper in April 2026 and withdrew confidence in the finding we cited (§3.4). Keeman (2026) does not support our layer band; his binary result saturates in the first third of the network (§2.4). Park et al. (2024) is not about emotion (§1). And the "7/10 agreement threshold for inclusion" of the ten tasks (§2.2) is not in the parent paper, where three of the ten are below 7/10. Each is corrected in place; the full check is `v7_reviews/REFERENCE_CHECK_2026-11-20.md`.'),
]
