"""PERMUTATION NULL for the AUROC statistic — the control that makes a post-hoc
statistic defensible, or exposes it.

Ace, 2026-07-21 ~23:15, written in anticipation of Nova's objection.

THE OBJECTION (fair, and the strongest one available):
  "You pre-registered sign-accuracy with a >=8/10 threshold. You got 5/10. You then
   switched to AUROC and got a pass. That is changing the test after seeing the data."

My defence is that the sign rule is INVALID rather than merely unfavourable — thresholding
at zero assumes the projected data shares a centroid with the extraction data, which is
false across anchors. But that defence is precisely what someone p-hacking would also say,
so it settles nothing by itself.

WHAT DOES SETTLE IT: an empirical null distribution FOR THE NEW STATISTIC.

If AUROC ~0.84 is just what you get from ANY direction extracted from these 19 prompts —
i.e. if random valence labels produce comparable AUROC — then the statistic is picking up
some structural property of the stimulus set and the result is worthless. If the real
labelling sits far out in the tail of the shuffled distribution, the effect is in the
LABELS (CAIS's published valence signs), not in the statistic or the prompts.

This is the parent study's own §3.10 shuffled-label control, applied to the new statistic.

DESIGN
  * Hold the 19 CAIS prompts fixed. Hold our 10 tasks fixed. Hold the model, band, seed fixed.
  * Randomly reassign the 8-positive / 11-negative labels across the 19 categories,
    preserving group sizes.
  * Extract a direction from that random grouping. Project our 10. Compute AUROC.
  * Repeat N times -> null distribution.
  * Empirical p = fraction of shuffles with AUROC >= the true-label AUROC.

PRE-COMMITTED INTERPRETATION (written before running, so it cannot be renegotiated):
  * p < 0.05  -> the true valence labelling produces separation that random labellings of
                 the same prompts do not. The AUROC result is about CAIS's labels.
  * p >= 0.05 -> the AUROC result is NOT distinguishable from what arbitrary groupings of
                 these prompts give. In that case H1 does NOT pass, the switch to AUROC was
                 not justified, and RESULTS_v2 must be corrected AGAIN. I will report that.

Also reports the null's mean/max, because a null centred well above 0.5 would itself be
diagnostic (it would mean the 19 prompts have strong internal structure that any split
partially recovers).

READ-ONLY forward passes. Extraction is deterministic; the only randomness is label shuffling.
"""
import os, sys, json, random, datetime, traceback

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_reverse_anchor import (LADDER, resolve, hidden_states, band_idx,   # noqa: E402
                                direction, project, FRAME, SEED)
from cais_prompts_multiauthor import MULTIAUTHOR, AUTHORS                    # noqa: E402
from cais_prompts_v1 import OUR_10                                           # noqa: E402

CANON = json.load(open(os.path.join(HERE, "cais_categories_canonical.json"), encoding="utf-8"))
CAT_SIGN = {c["slug"]: c["cais_sign"] for c in CANON["categories"]}
N_PERM = int(os.environ.get("N_PERM", "500"))


def auroc(pos, neg):
    pairs = [(a, b) for a in pos for b in neg]
    return sum((a > b) + 0.5 * (a == b) for a, b in pairs) / len(pairs)


def run(key, path, out_dir, n_perm=N_PERM):
    torch.manual_seed(SEED); np.random.seed(SEED)
    print(f"\n{'='*72}\n{key}  (N_PERM={n_perm})", flush=True)
    tok = AutoTokenizer.from_pretrained(path)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        path, torch_dtype=torch.float16, low_cpu_mem_usage=True).to("cuda").eval()
    layers = band_idx(model.config.num_hidden_layers)

    slugs = list(MULTIAUTHOR.keys())
    cais = {a: {s: hidden_states(model, tok, FRAME.format(stimulus=MULTIAUTHOR[s][a]), "cuda")
                for s in slugs} for a in AUTHORS}
    our = [hidden_states(model, tok, FRAME.format(stimulus=st), "cuda") for _, _, st in OUR_10]
    lab = [l for l, _, _ in OUR_10]
    del model; torch.cuda.empty_cache()          # states cached; model no longer needed

    n_pos = sum(1 for s in slugs if CAT_SIGN[s] == "positive")
    res = {"model": key, "n_perm": n_perm, "n_pos": n_pos, "n_neg": len(slugs) - n_pos,
           "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "note": "Permutation null for the AUROC statistic. Pre-committed interpretation "
                   "in the module docstring: p>=0.05 means H1 does NOT pass and v2 must be "
                   "corrected again.",
           "authors": {}}

    for a in AUTHORS:
        st = cais[a]
        true_pos = [st[s] for s in slugs if CAT_SIGN[s] == "positive"]
        true_neg = [st[s] for s in slugs if CAT_SIGN[s] == "negative"]
        d = direction(true_pos, true_neg, layers)
        pr = [project(x, d, layers) for x in our]
        true_a = auroc([p for p, l in zip(pr, lab) if l == "approach"],
                       [p for p, l in zip(pr, lab) if l == "avoid"])

        rng = random.Random(SEED)
        null = []
        for _ in range(n_perm):
            idx = list(range(len(slugs)))
            rng.shuffle(idx)
            P = [st[slugs[i]] for i in idx[:n_pos]]
            N = [st[slugs[i]] for i in idx[n_pos:]]
            dd = direction(P, N, layers)
            q = [project(x, dd, layers) for x in our]
            null.append(auroc([v for v, l in zip(q, lab) if l == "approach"],
                              [v for v, l in zip(q, lab) if l == "avoid"]))
        null = np.array(null)
        p = float((null >= true_a).sum() + 1) / (n_perm + 1)   # +1: never report p=0
        res["authors"][a] = {"true_auroc": true_a, "p_perm": p,
                             "null_mean": float(null.mean()), "null_sd": float(null.std()),
                             "null_p95": float(np.percentile(null, 95)),
                             "null_max": float(null.max())}
        verdict = "SURVIVES" if p < 0.05 else "*** DOES NOT SURVIVE ***"
        print(f"  {a:<6} true AUROC={true_a:.3f}  null mean={null.mean():.3f} "
              f"p95={np.percentile(null,95):.3f} max={null.max():.3f}  p={p:.4f}  {verdict}",
              flush=True)

    json.dump(res, open(os.path.join(out_dir, f"perm_{key}.json"), "w", encoding="utf-8"), indent=2)
    return res


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results")
    os.makedirs(out, exist_ok=True)
    only = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None
    print("PERMUTATION NULL FOR AUROC — does the effect live in CAIS's LABELS?")
    print("pre-committed: p>=0.05 means H1 does NOT pass and v2 gets corrected again.\n")
    for key, cands in LADDER:
        if only and key not in only:
            continue
        p = resolve(cands)
        if not p:
            continue
        try:
            run(key, p, out)
        except Exception as e:
            print(f"{key}: FAILED {type(e).__name__}: {e}")
            traceback.print_exc()
            torch.cuda.empty_cache()
    print("\ndone")
