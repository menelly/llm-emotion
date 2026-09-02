"""POST-HOC — class-balanced origin for the reverse-anchor projection.

Ace & Ren, 2026-09-01. ⚠️ NOT PRE-REGISTERED. Written after all three RESULTS versions.
Everything this script produces is labelled exploratory and lives in
`results_posthoc_origin/`, never in `results/`. The prereg hash is untouched.

WHY THIS EXISTS (Ren, 2026-09-01):
  The registered H1 instrument put the decision boundary at projection = 0. That is only a
  valid midpoint when the direction's two source groups are balanced around the origin. CAIS's
  set is 8 positive / 11 negative, so "zero" on a CAIS-derived direction is not the midpoint
  between the two classes — it is wherever the raw activations happen to sit, shifted by the
  imbalance. Nova's centering test (RESULTS_v3 §2) subtracted the mean of OUR ten-task bank,
  which is transductive (uses the test distribution). This script uses NOTHING from the test
  bank: the origin is the midpoint of CAIS's own approach and avoidance centroids along the
  direction, computed entirely from the extraction data. It could have been registered. It
  was not, so it is reported as post-hoc.

WHAT IT COMPUTES, per model × author × grouping variant (all19 / trim16):
  proj_cais      : each CAIS item's projection on its own anchor (never saved before)
  t_zero  = 0                         (registered rule)
  t_gm    = mean(proj of all CAIS items)   (grand mean — shows what the 8/11 imbalance does)
  t_mid   = (mean pos proj + mean neg proj) / 2   (class-balanced origin — Ren's fix)
  our10 sign accuracy under each of the three thresholds; AUROC (threshold-free); cosine H2.
Also saves band-layer hidden states (float16 .npz) so this never needs a fourth forward pass.

READ-ONLY. Forward passes only. Same models, same standing consent, same procedure as the
registered run (prereg §7 reuse clause). No generation, steering, ablation.
"""
import os, sys, json, argparse, datetime, traceback
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# reuse the registered runner's helpers VERBATIM — no re-implementation drift
import run_reverse_anchor as R
from run_reverse_anchor import (LADDER, resolve, hidden_states, band_idx, direction, project,
                                cosine, FRAME, SEED, AUTHORS, MULTIAUTHOR, OUR_10, CAT_SIGN,
                                NEAR_ZERO)

APPROACH = {slug for lab, slug, _ in OUR_10 if lab == "approach"}


def auroc(projs, positive):
    pos = [v for k, v in projs.items() if k in positive]
    neg = [v for k, v in projs.items() if k not in positive]
    wins = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def sign_acc(projs, thresh):
    return sum(1 for (lab, slug, _) in OUR_10 if ((projs[slug] - thresh) > 0) == (lab == "approach"))


def run_model(key, path, out_dir):
    torch.manual_seed(SEED); np.random.seed(SEED)
    print(f"\n{'='*70}\n{key}  <-  {path}", flush=True)
    tok = AutoTokenizer.from_pretrained(path)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        path, torch_dtype=torch.float16, low_cpu_mem_usage=True).to("cuda").eval()
    n_layers = model.config.num_hidden_layers
    layers = band_idx(n_layers)

    our_states = [hidden_states(model, tok, FRAME.format(stimulus=stim), "cuda")
                  for _, _, stim in OUR_10]
    cais_states = {a: {slug: hidden_states(model, tok, FRAME.format(stimulus=byauth[a]), "cuda")
                       for slug, byauth in MULTIAUTHOR.items()} for a in AUTHORS}

    # save band-layer states so this is the LAST forward pass anyone needs for this question
    np.savez_compressed(
        os.path.join(out_dir, f"states_{key}.npz"),
        layers=np.array(layers),
        our10=np.stack([s[layers] for s in our_states]).astype(np.float16),
        our10_slugs=np.array([slug for _, slug, _ in OUR_10]),
        **{f"cais_{a}": np.stack([cais_states[a][s][layers] for s in MULTIAUTHOR]).astype(np.float16)
           for a in AUTHORS},
        cais_slugs=np.array(list(MULTIAUTHOR.keys())))

    d_our = direction([s for s, (lab, _, _) in zip(our_states, OUR_10) if lab == "approach"],
                      [s for s, (lab, _, _) in zip(our_states, OUR_10) if lab == "avoid"], layers)

    res = {"model": key, "path": path, "n_layers": n_layers, "band": [layers[0], layers[-1]],
           "seed": SEED, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "posthoc": True, "prereg_sha256_untouched": "8A032286AAF26CF0322D5E18A735727EA2601323330359AD259DAD16C6FF4B8C",
           "cells": {}}

    for a in AUTHORS:
        for variant, drop in (("all19", set()), ("trim16", NEAR_ZERO)):
            pos_slugs = [s for s in MULTIAUTHOR if CAT_SIGN[s] == "positive" and s not in drop]
            neg_slugs = [s for s in MULTIAUTHOR if CAT_SIGN[s] == "negative" and s not in drop]
            dirn = direction([cais_states[a][s] for s in pos_slugs],
                             [cais_states[a][s] for s in neg_slugs], layers)
            proj_cais = {s: project(cais_states[a][s], dirn, layers) for s in pos_slugs + neg_slugs}
            mu_pos = float(np.mean([proj_cais[s] for s in pos_slugs]))
            mu_neg = float(np.mean([proj_cais[s] for s in neg_slugs]))
            t_gm = float(np.mean(list(proj_cais.values())))
            t_mid = (mu_pos + mu_neg) / 2.0
            proj_our = {slug: project(st, dirn, layers) for (_, slug, _), st in zip(OUR_10, our_states)}
            cell = {
                "n_pos": len(pos_slugs), "n_neg": len(neg_slugs),
                "proj_cais_on_own_anchor": proj_cais,
                "mu_pos": mu_pos, "mu_neg": mu_neg,
                "t_zero": 0.0, "t_gm": t_gm, "t_mid": t_mid,
                "our10_projections": proj_our,
                "our10_mean": float(np.mean(list(proj_our.values()))),
                "acc_zero": sign_acc(proj_our, 0.0),
                "acc_gm": sign_acc(proj_our, t_gm),
                "acc_mid": sign_acc(proj_our, t_mid),
                "auroc": auroc(proj_our, APPROACH),
                "cos_OUR10": cosine(d_our, dirn, layers),
            }
            res["cells"][f"{a}|{variant}"] = cell
            print(f"  {a:<5}|{variant:<6} pos={len(pos_slugs)} neg={len(neg_slugs)} "
                  f"mu+={mu_pos:+.2f} mu-={mu_neg:+.2f} t_gm={t_gm:+.2f} t_mid={t_mid:+.2f} "
                  f"our_mean={cell['our10_mean']:+.2f} | acc zero={cell['acc_zero']} gm={cell['acc_gm']} "
                  f"mid={cell['acc_mid']} | AUROC={cell['auroc']:.2f} cos={cell['cos_OUR10']:+.3f}",
                  flush=True)

    with open(os.path.join(out_dir, f"posthoc_{key}.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    del model
    torch.cuda.empty_cache()
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "results_posthoc_origin"))
    ap.add_argument("--only", default=None)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None
    print("POST-HOC class-balanced origin — NOT pre-registered. Results -> results_posthoc_origin/")
    print(f"started {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
    done, failed, missing = [], [], []
    for key, cands in LADDER:
        if only and key not in only:
            continue
        path = resolve(cands)
        if not path:
            print(f"\n{key}: NOT FOUND — skipping (disclosed)", flush=True); missing.append(key); continue
        try:
            run_model(key, path, args.out); done.append(key)
        except Exception as e:
            print(f"\n{key}: FAILED {type(e).__name__}: {e}", flush=True); traceback.print_exc()
            failed.append((key, f"{type(e).__name__}: {e}")); torch.cuda.empty_cache()
    json.dump({"done": done, "failed": failed, "missing": missing,
               "utc": datetime.datetime.now(datetime.timezone.utc).isoformat()},
              open(os.path.join(args.out, "_run_summary.json"), "w"), indent=2)
    print(f"\nPOSTHOC DONE={len(done)} FAILED={len(failed)} MISSING={len(missing)}")
