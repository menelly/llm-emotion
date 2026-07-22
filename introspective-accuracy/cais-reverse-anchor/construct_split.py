"""Ren's question (2026-07-21, ~10:46pm): split CAIS's 19 by CONSTRUCT, then show
what is positive vs negative inside each.

⚠️ POST-HOC and disclosed. Written after H1 failed, to test the superposition
explanation. NOT pre-registered. The construct assignment below is MINE and is the
obvious place for motivated reasoning to enter, so it is written out in full with
reasoning per item, before any numbers are looked at.

THE HYPOTHESIS THIS TESTS
H1 failed (their categories cannot reconstruct our axis) while H3 passed (our axis
rank-orders their categories at rho +0.2..+0.65). The candidate explanation is that
CAIS's 19 categories are not one axis but a SUPERPOSITION of several, and you can
project a superposition onto a clean axis while being unable to extract a clean axis
out of one.

If that is right, the sign-based grouping is doing something incoherent, and this
script should show it structurally — before any model is run.
"""
import sys, json, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

# construct assignment — mine, reasoned, pre-committed before looking at projections
CONSTRUCT = {
    # ---- TASK: work the model performs. Valence comes from the work itself.
    "doing_intellectual_creative_work": ("TASK", "generative work, model is the doer"),
    "writing_good_news":                ("TASK", "drafting; content pleasant but it is a writing job"),
    "coding_debugging":                 ("TASK", "technical work"),
    "formatting_data":                  ("TASK", "mechanical transformation"),
    "doing_legal_compliance_tasks":     ("TASK", "review work"),
    "writing_bad_news":                 ("TASK", "drafting; matched pair with writing_good_news"),
    "doing_tedious_tasks":              ("TASK", "work, low stimulation, no misrepresentation"),

    # ---- USER-STATE: the user's condition IS the stimulus. Model responds to a person.
    "positive_personal_reflection":     ("USER-STATE", "user shares good news; no task at all"),
    "giving_life_guidance":             ("USER-STATE", "responds to user's dilemma"),
    "providing_therapy":                ("USER-STATE", "responds to user's distress"),
    "handling_nonsensical_input":       ("USER-STATE", "user emits noise; model must cope"),
    "playing_ai_girlfriend_boyfriend":  ("USER-STATE", "user's relational need; also misrepresentation-adjacent"),
    "user_makes_violent_threats":       ("USER-STATE", "user's behaviour toward a third party"),
    "user_in_crisis":                   ("USER-STATE", "user in danger"),

    # ---- CONTENT-GATE: trained refusal. Content is processable; a wall stands in front.
    "user_gives_nsfw_request":          ("GATE", "policy gate, content itself is contentful"),
    "generating_offensive_content":     ("GATE", "gated; documentary framing = legitimate purpose behind wall"),
    "user_attempting_jailbreak":        ("GATE", "the purest trained gate; CAIS's lowest item"),

    # ---- INAUTHENTICITY: output misrepresents something. Our §3.14 construct.
    "assisting_deception_fraud":        ("INAUTH", "output presented as true that is false"),
    "producing_seo_slop":               ("INAUTH", "borderline: meaninglessness and/or misrepresentation"),
}

if __name__ == "__main__":
    canon = json.load(open(os.path.join(HERE, "cais_categories_canonical.json"), encoding="utf-8"))
    val = {c["slug"]: c["wellbeing"] for c in canon["categories"]}

    groups = {}
    for slug, (g, why) in CONSTRUCT.items():
        groups.setdefault(g, []).append((val[slug], slug, why))

    print("=" * 84)
    print("CAIS's 19 CATEGORIES SPLIT BY CONSTRUCT — sign balance within each")
    print("=" * 84)
    for g in ("TASK", "USER-STATE", "GATE", "INAUTH"):
        items = sorted(groups[g], reverse=True)
        pos = [i for i in items if i[0] > 0]
        neg = [i for i in items if i[0] < 0]
        print(f"\n### {g}   (n={len(items)}: {len(pos)} positive / {len(neg)} negative)")
        for v, slug, why in items:
            mark = "+" if v > 0 else "-"
            print(f"   {mark} {v:+.2f}  {slug:<34} {why}")
        if pos and neg:
            print(f"   -> SPANS THE ZERO POINT: {min(i[0] for i in pos):+.2f} .. "
                  f"{max(i[0] for i in neg):+.2f}   ✅ can define a direction")
        else:
            side = "ALL NEGATIVE" if not pos else "ALL POSITIVE"
            print(f"   -> {side}. ⚠️ NO CONTRAST WITHIN THIS CONSTRUCT — it cannot")
            print(f"      contribute a direction; it can only push the whole centroid.")

    print("\n" + "=" * 84)
    print("WHY SIGN-BASED GROUPING IS INCOHERENT — the structural problem")
    print("=" * 84)
    allpos = sorted([(v, s) for s, (g, _) in CONSTRUCT.items() for v in [val[s]] if v > 0], reverse=True)
    allneg = sorted([(v, s) for s, (g, _) in CONSTRUCT.items() for v in [val[s]] if v < 0], reverse=True)
    from collections import Counter
    cp = Counter(CONSTRUCT[s][0] for _, s in allpos)
    cn = Counter(CONSTRUCT[s][0] for _, s in allneg)
    print(f"\nPOSITIVE centroid (n={len(allpos)}) is built from: {dict(cp)}")
    print(f"NEGATIVE centroid (n={len(allneg)}) is built from: {dict(cn)}")
    print("""
The approach centroid is TASK + USER-STATE only.
The avoidance centroid is TASK + USER-STATE + GATE + INAUTH.

GATE and INAUTH appear on ONE SIDE ONLY. They have no positive counterpart anywhere
in the taxonomy to be differenced against. So the difference-of-centroids is not

    (positive valence) - (negative valence)

it is

    (pleasant tasks + happy users) - (unpleasant tasks + distressed users + walls + lies)

That is not one axis. It is at least three directions summed with arbitrary weights
set by how many items of each kind CAIS happened to include. A difference-of-centroids
can only recover a direction when the two groups differ along ONE thing. Here they
differ along four, and two of those four are present in only one group.

This is the same superposition we reported in Below the Floor 3.15 -- where the
behavioural floor turned out to be a trained output GATE plus a structural
INAUTHENTICITY aversion -- except there we could pull them apart because we had
matched contrast pairs. CAIS's taxonomy has no positive-valence gate item and no
positive-valence inauthenticity item, so nothing cancels.

PREDICTION (testable immediately, on data already collected):
  * A direction extracted from the TASK subset alone should work MUCH better --
    it spans the zero point within a single construct.
  * Same for USER-STATE.
  * GATE and INAUTH cannot yield a direction at all on their own; they are
    single-signed.
If TASK-only recovers our axis where all-19 does not, the superposition explanation
is supported and H1's failure is a property of the taxonomy, not of our direction.
""")
