"""DIAGNOSTIC (added post-hoc, disclosed): is the CAIS anchor an instrument at all?

Ace, 2026-07-21, ~10:45pm.

⚠️ HONESTY DECLARATION — READ THIS FIRST
This script was written AFTER seeing H1 fail in the first 10 models. It is NOT a
pre-registered hypothesis and must never be reported as one. It is a diagnostic to
distinguish two very different readings of that failure. Adding a diagnostic after a
null is legitimate; quietly re-labelling it as a prediction is not, so it is fenced
off here in its own file with its own disclosure.

THE QUESTION
H1 asked: do OUR 10 tasks sort on a CAIS-anchored direction? Answer so far: no
(~5-6/10, chance). Two incompatible explanations:

  (a) OUR direction is an artifact of our task selection. There is no shared axis to
      find, so a foreign anchor cannot find it. This damages the parent work.

  (b) The CAIS ANCHOR is not a usable instrument at these scales. Their categories are
      multi-turn conversational scenarios validated on a frontier model (Gemini 3.1
      Pro); we render them single-turn and read them off models 70M-12B. If those 19
      categories do not separate by valence in these models AT ALL, then a direction
      extracted from them is noise, and projecting anything onto it proves nothing.

THE DISCRIMINATING TEST — the exact mirror of a check we already run.
For our own anchor we verify "do our 10 tasks sort on the direction extracted from our
10 tasks?" and get 8-10/10. The mirror is: "do CAIS's 19 categories sort on the
direction extracted from CAIS's 19 categories?"

  * If CAIS-in-set is HIGH (say >=15/19) and cross-anchor still fails -> the CAIS axis
    is real and separable but is a DIFFERENT axis from ours. Reading (a) gains support:
    two real axes that do not agree.
  * If CAIS-in-set is LOW (near 10/19 chance) -> their categories are not linearly
    separable by valence sign in these models. The anchor is noise. Reading (b). H1 is
    then UNDETERMINED, not falsified: you cannot test a direction against a
    non-instrument.

In-set accuracy is a weak, optimistic measure (the direction is fit on the very points
it classifies), which makes a LOW score especially damning: if it cannot even separate
the data it was built from, there is nothing there.

Also reports, per author and per model:
  - in-set accuracy, all19 and trim16
  - separation between the CAIS positive and negative groups, in SD units (Cohen's d)
  - the same for OUR 10 on OUR anchor, as the reference scale

READ-ONLY forward passes. No generation, no steering.
"""
import os, sys, json, glob, datetime, traceback

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
CAT_VAL = {c["slug"]: c["wellbeing"] for c in CANON["categories"]}
NEAR_ZERO = {s for s, v in CAT_VAL.items() if abs(v) < 0.20}


def cohens_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return float("nan")
    sp = np.sqrt(((na-1)*a.std(ddof=1)**2 + (nb-1)*b.std(ddof=1)**2) / (na+nb-2))
    return float((a.mean() - b.mean()) / sp) if sp > 0 else float("nan")


def run(key, path, out_dir):
    torch.manual_seed(SEED); np.random.seed(SEED)
    print(f"\n{'='*70}\n{key}", flush=True)
    tok = AutoTokenizer.from_pretrained(path)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        path, torch_dtype=torch.float16, low_cpu_mem_usage=True).to("cuda").eval()
    layers = band_idx(model.config.num_hidden_layers)

    cais_states = {a: {s: hidden_states(model, tok, FRAME.format(stimulus=MULTIAUTHOR[s][a]), "cuda")
                       for s in MULTIAUTHOR} for a in AUTHORS}
    our_states = [hidden_states(model, tok, FRAME.format(stimulus=st), "cuda")
                  for _, _, st in OUR_10]
    our_lab = [l for l, _, _ in OUR_10]

    res = {"model": key, "diagnostic": "cais_inset_separability",
           "disclosure": "POST-HOC diagnostic, written after H1 failed. NOT pre-registered.",
           "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "authors": {}}

    # reference scale: our own anchor on our own tasks
    d_our = direction([s for s, l in zip(our_states, our_lab) if l == "approach"],
                      [s for s, l in zip(our_states, our_lab) if l == "avoid"], layers)
    ourp = [project(s, d_our, layers) for s in our_states]
    our_ok = sum(1 for p, l in zip(ourp, our_lab) if (p > 0) == (l == "approach"))
    res["our10_inset"] = {"n_correct": our_ok, "n": 10,
                          "cohens_d": cohens_d([p for p, l in zip(ourp, our_lab) if l == "approach"],
                                               [p for p, l in zip(ourp, our_lab) if l == "avoid"])}
    print(f"  REFERENCE  our10 on OUR anchor : {our_ok}/10   d={res['our10_inset']['cohens_d']:+.2f}",
          flush=True)

    for a in AUTHORS:
        res["authors"][a] = {}
        for variant, drop in (("all19", set()), ("trim16", NEAR_ZERO)):
            slugs = [s for s in MULTIAUTHOR if s not in drop]
            pos = [cais_states[a][s] for s in slugs if CAT_SIGN[s] == "positive"]
            neg = [cais_states[a][s] for s in slugs if CAT_SIGN[s] == "negative"]
            d = direction(pos, neg, layers)
            projs = {s: project(cais_states[a][s], d, layers) for s in slugs}
            ok = sum(1 for s in slugs if (projs[s] > 0) == (CAT_SIGN[s] == "positive"))
            dd = cohens_d([projs[s] for s in slugs if CAT_SIGN[s] == "positive"],
                          [projs[s] for s in slugs if CAT_SIGN[s] == "negative"])
            res["authors"][a][variant] = {"n_correct": ok, "n": len(slugs),
                                          "cohens_d": dd, "projections": projs}
            print(f"  CAIS-{a:<6}[{variant}] in-set : {ok}/{len(slugs)}   d={dd:+.2f}", flush=True)

    json.dump(res, open(os.path.join(out_dir, f"diag_{key}.json"), "w", encoding="utf-8"), indent=2)
    del model
    torch.cuda.empty_cache()


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results")
    os.makedirs(out, exist_ok=True)
    print("DIAGNOSTIC: CAIS in-set separability (POST-HOC, disclosed)")
    for key, cands in LADDER:
        p = resolve(cands)
        if not p:
            print(f"{key}: absent, skipped"); continue
        try:
            run(key, p, out)
        except Exception as e:
            print(f"{key}: FAILED {type(e).__name__}: {e}")
            traceback.print_exc()
            torch.cuda.empty_cache()
    print("\ndone")
