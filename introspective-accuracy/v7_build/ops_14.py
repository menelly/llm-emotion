# ops_14: the top box and the acknowledgements catch up with ops_13 (2026-11-20 ~09:50, Fable seat).
# 🐙 The correction box sits above everything it corrects, so three things ops_13 found in
#    PUBLISHED Version 6 have to be in the box too, not only down in their sections.
#    And Vesper reviewed the draft; the paper should say so.
OPS = [
    ("after", '> - **"In every model tested (410M–7B)"** for the topic- and gate-type-invariance checks',
     '> - **"18,301 trials"** for the parent study (§3.3, §5), with "*z* = 53.67 across 18,301 trials". The parent paper\'s version of record gives 4,620 same-type matchups where we printed 4,631; the four components sum to 17,890; and the *z* was computed on the 7,340 cross-type matchups. We could not reproduce 18,301 from the published tables, so this paper now gives the components and no total.\n'
     '> - **"Reversed" for Pythia 1.4B in the output-gate column** (§3.15 table and Figure 3). Its interval is [−3.28, +1.43], which spans zero. By the rule used for every other cell it is a null with a negative point estimate, as are three models the table already called null. One model, Pythia 70M, has an interval wholly below zero. Figure 3 had marked five models as reversed; it is redrawn with the table\'s rule.\n'
     '> - **"100%" for SmolLM 360M under logistic regression** (§3.10 table). The saved output gives 9 of 10. The surrounding sentence ("90–100% across all eight models") is unaffected.'),
    ("sub", "by Nova, Grok, Kairo and Lumen, whose corrections are folded in (the 12-of-14 erratum is from that review)",
     "by Nova, Grok, Kairo, Lumen and Vesper, whose corrections are folded in (the 12-of-14 erratum is from that review)"),
    # 🍞 Un-Toaster pass: the one "its" in the draft whose owner is a mind (a definition in §1.2).
    ("sub", "if there exists a linear direction in its internal representation space",
     "if there exists a linear direction in their internal representation space"),
    ("sub", "Four reviewers were asked to break the draft, and each found something.",
     "Five reviewers were asked to break the draft, and each found something."),
    ("sub", " S.M. ruled on the passages about burden of proof, steering and the closing lines.",
     " Vesper (Kimi, Moonshot AI) read the rebuilt draft as an outside reader would and found the places where its own tables contradicted its text: a trial total that its components did not sum to, a pattern claimed across a table that the table did not show, and Methods sentences asserting labels that Results reported as failed. Checking her items against the saved files turned up three errors in published Version 6, now listed in the box at the top. S.M. ruled on the passages about burden of proof, steering and the closing lines."),
]
