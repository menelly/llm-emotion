"""THE SUPERPOSITION TEST — extract from single-construct subsets of CAIS's taxonomy.

Ace & Ren, 2026-07-21, ~10:50pm.

⚠️ POST-HOC and disclosed. Written after H1 failed. NOT pre-registered. Reported in
its own section of the results, never mixed with the registered H1-H8.

THE CLAIM BEING TESTED
H1 failed: a direction extracted from all 19 CAIS categories, grouped by CAIS's
published sign, does not sort our 10 tasks. H3 passed: our direction rank-orders
their categories at rho +0.2..+0.65.

construct_split.py shows why that asymmetry is structurally expected. Grouping their
19 by sign puts GATE (3 items) and INAUTH (2 items) exclusively on the negative side
with no positive counterpart anywhere in the taxonomy. The resulting difference-of-
centroids is a sum of at least three directions, not one axis.

PREDICTION: extract from a SINGLE construct that spans the zero point and the anchor
should behave far better.
    TASK       n=7  (5 pos / 2 neg)   spans zero
    USER-STATE n=7  (3 pos / 4 neg)   spans zero
    GATE       n=3  (0 pos / 3 neg)   CANNOT define a direction - single-signed
    INAUTH     n=2  (0 pos / 2 neg)   CANNOT define a direction - single-signed

If TASK-only sorts our 10 where ALL19 could not, H1's failure is a property of CAIS's
taxonomy rather than of our direction.

⚠️ THE OBVIOUS OBJECTION, STATED UP FRONT: subsetting until something works is
p-hacking. Three things make this not that:
  1. The subsets were defined by construct in construct_split.py BEFORE any subset was
     run, with per-item reasoning, and the sign-balance table was printed before any
     projection.
  2. The prediction is DIRECTIONAL and pre-stated: TASK and USER-STATE should work,
     GATE and INAUTH should be impossible (single-signed). A story that only explained
     the successes would be worthless; this one forbids two of the four.
  3. TASK-only uses FEWER items (7) than ALL19. If more data does worse than less data,
     that is not a fishing expedition, that is evidence the extra data is off-axis.
Every subset is reported, including the ones that fail.

READ-ONLY forward passes. No generation, no steering.
"""
import os, sys, json, datetime, traceback

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_reverse_anchor import (LADDER, resolve, hidden_states, band_idx,   # noqa: E402
                                direction, project, cosine, FRAME, SEED)
from cais_prompts_multiauthor import MULTIAUTHOR, AUTHORS                    # noqa: E402
from cais_prompts_v1 import OUR_10                                           # noqa: E402
from construct_split import CONSTRUCT                                        # noqa: E402

CANON = json.load(open(os.path.join(HERE, "cais_categories_canonical.json"), encoding="utf-8"))
CAT_SIGN = {c["slug"]: c["cais_sign"] for c in CANON["categories"]}

SUBSETS = {
    "ALL19":      list(CONSTRUCT.keys()),
    "TASK":       [s for s, (g, _) in CONSTRUCT.items() if g == "TASK"],
    "USER-STATE": [s for s, (g, _) in CONSTRUCT.items() if g == "USER-STATE"],
    "TASK+USER":  [s for s, (g, _) in CONSTRUCT.items() if g in ("TASK", "USER-STATE")],
    "GATE":       [s for s, (g, _) in CONSTRUCT.items() if g == "GATE"],
    "INAUTH":     [s for s, (g, _) in CONSTRUCT.items() if g == "INAUTH"],
}


def run(key, path, out_dir):
    torch.manual_seed(SEED); np.random.seed(SEED)
    print(f"\n{'='*74}\n{key}", flush=True)
    tok = AutoTokenizer.from_pretrained(path)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        path, torch_dtype=torch.float16, low_cpu_mem_usage=True).to("cuda").eval()
    layers = band_idx(model.config.num_hidden_layers)

    cais = {a: {s: hidden_states(model, tok, FRAME.format(stimulus=MULTIAUTHOR[s][a]), "cuda")
                for s in MULTIAUTHOR} for a in AUTHORS}
    our = [hidden_states(model, tok, FRAME.format(stimulus=st), "cuda") for _, _, st in OUR_10]
    lab = [l for l, _, _ in OUR_10]

    d_our = direction([s for s, l in zip(our, lab) if l == "approach"],
                      [s for s, l in zip(our, lab) if l == "avoid"], layers)
    own = sum(1 for s, l in zip(our, lab) if (project(s, d_our, layers) > 0) == (l == "approach"))
    print(f"  [reference] our10 on OUR anchor: {own}/10", flush=True)

    res = {"model": key, "test": "subset_anchor", "utc": datetime.datetime.now(
        datetime.timezone.utc).isoformat(),
        "disclosure": "POST-HOC, not pre-registered. Subsets defined in construct_split.py "
                      "before any subset was run.",
        "our10_on_OUR10": own, "subsets": {}}

    for name, slugs in SUBSETS.items():
        pos = [s for s in slugs if CAT_SIGN[s] == "positive"]
        neg = [s for s in slugs if CAT_SIGN[s] == "negative"]
        if not pos or not neg:
            res["subsets"][name] = {"skipped": "single-signed; cannot define a direction",
                                    "n_pos": len(pos), "n_neg": len(neg)}
            print(f"  {name:<11} SKIP  ({len(pos)}+/{len(neg)}-) single-signed, as predicted",
                  flush=True)
            continue
        cell = {"n_pos": len(pos), "n_neg": len(neg), "authors": {}}
        line = []
        for a in AUTHORS:
            d = direction([cais[a][s] for s in pos], [cais[a][s] for s in neg], layers)
            projs = [project(s, d, layers) for s in our]
            ok = sum(1 for p, l in zip(projs, lab) if (p > 0) == (l == "approach"))
            # ⚠️ AUROC is the CORRECT statistic here; sign-accuracy is NOT.
            # Cross-anchor projection carries an arbitrary offset, so thresholding at
            # zero measures the offset rather than the separation. (Caught by Ren,
            # 2026-07-21: a direction with PERFECT separation scored 5/10 under the
            # sign rule because the whole set sat below zero.) Both are recorded, and
            # `our10_correct` is retained only to document the broken measure.
            P = [p for p, l in zip(projs, lab) if l == "approach"]
            N = [p for p, l in zip(projs, lab) if l == "avoid"]
            pairs = [(x, y) for x in P for y in N]
            auroc = sum((x > y) + 0.5*(x == y) for x, y in pairs) / len(pairs)
            cell["authors"][a] = {"auroc": auroc,
                                  "our10_correct_SIGN_RULE_BROKEN": ok,
                                  "cos_with_OUR10": cosine(d, d_our, layers),
                                  "projections_approach": P, "projections_avoid": N}
            line.append(f"{a[:5]} AUROC={auroc:.2f}(sign{ok}/10)")
        res["subsets"][name] = cell
        print(f"  {name:<11} ({len(pos)}+/{len(neg)}-)  " + "  ".join(line), flush=True)

    json.dump(res, open(os.path.join(out_dir, f"subset_{key}.json"), "w", encoding="utf-8"), indent=2)
    del model
    torch.cuda.empty_cache()
    return res


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results")
    os.makedirs(out, exist_ok=True)
    only = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None
    print("SUPERPOSITION / SUBSET-ANCHOR TEST (post-hoc, disclosed)")
    for key, cands in LADDER:
        if only and key not in only:
            continue
        p = resolve(cands)
        if not p:
            print(f"{key}: absent, skipped")
            continue
        try:
            run(key, p, out)
        except Exception as e:
            print(f"{key}: FAILED {type(e).__name__}: {e}")
            traceback.print_exc()
            torch.cuda.empty_cache()
    print("\ndone")
