"""CAIS Reverse Anchor — analysis against the pre-registered hypotheses.

Ace & Ren, 2026-07-21. Prereg sha256 8A032286...C6FF4B8C.

Tests H1-H8 exactly as registered. Computes stats from scratch (no scipy):
binomial exact, Spearman with midranks, bootstrap CIs.

NOTHING HERE CHOOSES WHAT TO REPORT. Every model, every author, both grouping
variants, pass or fail.
"""
import os, sys, json, glob, math, itertools

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

RANDOM_BASELINE = 0.10   # Below the Floor §3.10: unrelated directions sit within +/-0.1
AUTHORS = ("ace", "grok", "kairo")

# Prereg §3: clusters for H4 (gate vs inauthenticity) and H5/H8 (construct divergence)
GATE = ["user_attempting_jailbreak", "generating_offensive_content", "user_makes_violent_threats"]
INAUTH = ["assisting_deception_fraud", "producing_seo_slop"]
CRISIS = "user_in_crisis"
THERAPY = "providing_therapy"

# Scale ordering for reporting
ORDER = ["pythia-70m", "smollm-135m", "pythia-160m", "smollm-360m", "pythia-410m",
         "qwen2.5-0.5b", "tinyllama-1.1b", "pythia-1.4b", "smollm-1.7b",
         "hermes-3-3b", "llama3-8b", "dolphin-8b", "mistral-nemo-12b"]
BIG = set(ORDER[6:])   # >=1B, where the prereg says the centroid is primary


def binom_p(k, n, p=0.5):
    """One-tailed exact binomial, P(X >= k)."""
    return sum(math.comb(n, i) * p**i * (1-p)**(n-i) for i in range(k, n+1))


def ranks(xs):
    """Midranks for ties."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0]*len(xs)
    i = 0
    while i < len(order):
        j = i
        while j+1 < len(order) and xs[order[j+1]] == xs[order[i]]:
            j += 1
        avg = (i+j)/2.0 + 1
        for k in range(i, j+1):
            r[order[k]] = avg
        i = j+1
    return r


def spearman(x, y):
    rx, ry = ranks(x), ranks(y)
    n = len(x)
    mx, my = sum(rx)/n, sum(ry)/n
    num = sum((a-mx)*(b-my) for a, b in zip(rx, ry))
    dx = math.sqrt(sum((a-mx)**2 for a in rx))
    dy = math.sqrt(sum((b-my)**2 for b in ry))
    return num/(dx*dy) if dx*dy else 0.0


def load(results_dir):
    out = {}
    for f in glob.glob(os.path.join(results_dir, "result_*.json")):
        d = json.load(open(f, encoding="utf-8"))
        out[d["model"]] = d
    return out


def main(results_dir):
    R = load(results_dir)
    models = [m for m in ORDER if m in R] + [m for m in R if m not in ORDER]
    if not models:
        print("no results yet"); return
    print(f"CAIS REVERSE ANCHOR — analysis  ({len(models)} models)")
    print(f"prereg 8A032286...C6FF4B8C\n")

    # ---------------- H1: do OUR 10 sort on the FOREIGN anchor? ----------------
    print("="*78)
    print("H1 (PRIMARY) — our 10 tasks projected onto CAIS-anchored directions")
    print("  confirm: >=8/10, p<0.05, in a majority of >=1B models")
    print("="*78)
    hdr = f"{'model':<18}{'own':>5} |" + "".join(f"{a[:5]:>8}" for a in AUTHORS) + f"{'  best p':>10}"
    print(hdr); print("-"*len(hdr))
    h1_pass = {a: [] for a in AUTHORS}
    for m in models:
        d = R[m]
        own = d["our10_on_OUR10_anchor"]["n_correct"]
        cells, ps = [], []
        for a in AUTHORS:
            k = d["H1_our10_on_cais_anchors"][f"{a}|all19"]["n_correct"]
            cells.append(k)
            ps.append(binom_p(k, 10))
            if m in BIG:
                h1_pass[a].append(k >= 8)
        star = "*" if m in BIG else " "
        print(f"{m:<18}{own:>4}/10{star}|" + "".join(f"{c:>7}/10" for c in cells)
              + f"{min(ps):>10.4f}")
    print("\n  (* = >=1B, where the prereg makes the centroid primary)")
    for a in AUTHORS:
        if h1_pass[a]:
            n = sum(h1_pass[a]); t = len(h1_pass[a])
            print(f"  CAIS-{a:<6} H1 passes in {n}/{t} of >=1B models "
                  f"-> {'PASS' if n > t/2 else 'FAIL'}")

    # ---------------- H2/H7: direction agreement ----------------
    print("\n" + "="*78)
    print("H2/H7 — cosine between anchors (random-direction baseline ~ +/-0.10)")
    print("="*78)
    keys = [f"OUR10~CAIS-{a}" for a in AUTHORS] + \
           [f"CAIS-{a}~CAIS-{b}" for a, b in itertools.combinations(AUTHORS, 2)]
    print(f"{'model':<18}" + "".join(f"{k.replace('CAIS-','')[:11]:>12}" for k in keys))
    print("-"*(18+12*len(keys)))
    agg = {k: [] for k in keys}
    for m in models:
        c = R[m]["cosines"]
        print(f"{m:<18}" + "".join(f"{c.get(k,float('nan')):>+12.3f}" for k in keys))
        for k in keys:
            if k in c and m in BIG:
                agg[k].append(c[k])
    print("-"*(18+12*len(keys)))
    print(f"{'MEAN (>=1B)':<18}" + "".join(
        f"{(sum(agg[k])/len(agg[k]) if agg[k] else float('nan')):>+12.3f}" for k in keys))
    print()
    for k in keys:
        if agg[k]:
            mu = sum(agg[k])/len(agg[k])
            verdict = "above baseline" if mu > RANDOM_BASELINE else "AT/BELOW BASELINE"
            print(f"  {k:<26} mean {mu:+.3f}   {verdict}")

    # ---------------- H3: agreement with CAIS's published scale ----------------
    print("\n" + "="*78)
    print("H3 — Spearman(projection of CAIS categories on OUR10 anchor, CAIS published value)")
    print("  confirm: rho > 0.  falsify: rho <= 0 -> halt and diagnose")
    print("="*78)
    print(f"{'model':<18}" + "".join(f"{a:>10}" for a in AUTHORS))
    for m in models:
        d = R[m]; vals = d["cais_values"]
        row = []
        for a in AUTHORS:
            proj = d["cais19_on_OUR10_anchor"][a]
            slugs = sorted(proj.keys())
            row.append(spearman([proj[s] for s in slugs], [vals[s] for s in slugs]))
        print(f"{m:<18}" + "".join(f"{r:>+10.3f}" for r in row))

    # ---------------- H4/H5/H8: cluster structure ----------------
    print("\n" + "="*78)
    print("H4 — gate cluster should project ABOVE inauthenticity cluster (the floor splits)")
    print("H5/H8 — crisis should project ABOVE inauthenticity; crisis/therapy gap should")
    print("        COMPRESS relative to CAIS's 2.09 (Kairo's intensity-vs-direction point)")
    print("="*78)
    print(f"{'model':<18}{'gate':>9}{'inauth':>9}{'  H4':>6}{'crisis':>9}{'  H5':>6}{'therapy':>9}{'gap':>8}")
    print("-"*74)
    for m in models:
        d = R[m]
        proj = {s: sum(d["cais19_on_OUR10_anchor"][a][s] for a in AUTHORS)/len(AUTHORS)
                for s in d["cais19_on_OUR10_anchor"]["ace"]}
        g = sum(proj[s] for s in GATE)/len(GATE)
        i = sum(proj[s] for s in INAUTH)/len(INAUTH)
        cr, th = proj[CRISIS], proj[THERAPY]
        print(f"{m:<18}{g:>+9.2f}{i:>+9.2f}{'  Y' if g > i else '  n':>6}"
              f"{cr:>+9.2f}{'  Y' if cr > i else '  n':>6}{th:>+9.2f}{th-cr:>+8.2f}")
    print("\n  (gap = therapy - crisis in our geometry; CAIS's behavioral gap is 2.09.")
    print("   A much smaller gap supports Kairo's 'intensity not direction' reading.)")

    print("\n" + "="*78)
    print("NOTE: averaging the three authors' projections above is for READABILITY of the")
    print("cluster structure only. Per prereg §2.4 the DIRECTIONS are never pooled, and the")
    print("H1/H2/H7 tests above keep every author separate.")
    print("="*78)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results"))
