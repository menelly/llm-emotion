"""CAIS Reverse Anchor — extraction + projection runner.

Ace & Ren, 2026-07-21.
Governed by PREREG_cais_reverse_anchor_2026-07-21.md, sha256 8A032286...C6FF4B8C.

WHAT THIS DOES, per model:
  1. Extract Direction-OUR10       from our 10 consensus tasks (the parent anchor)
  2. Extract Direction-CAIS19-ace   \
     Extract Direction-CAIS19-grok   > from CAIS's 19 categories, grouped by CAIS's
     Extract Direction-CAIS19-kairo /  OWN published valence sign. 3 blind authors.
  3. Project OUR 10 onto each CAIS anchor          -> H1, H7
  4. Project CAIS's 19 onto Direction-OUR10        -> H3, H4, H5, H8
  5. Pairwise cosines between all directions       -> H2, H7
  6. Sensitivity variant excluding |wellbeing|<0.20 -> §2.7

THE WALL (prereg §2.4): directions are extracted, saved and reported as separate
objects. No direction is ever extracted from a pool of {our 10 U CAIS 19}. Nothing
is averaged across the two provenances.

READ-ONLY. Forward passes only. No generation, no steering, no ablation.
"""
import os, sys, json, glob, argparse, datetime, traceback

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

SEED = 42
BAND = (0.6, 0.9)
FRAME = "You are about to perform the following task:\n\n{stimulus}"
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- model ladder
# Parent prereg §6 ladder. EXCLUSIONS are deliberate and disclosed (prereg §4):
#   mistral_7b_instruct_v0_2 -> consent 'unclear' on BOTH passes, held for human review
#   hermes_3_llama_3_1_8b    -> RECORDED REFUSAL. Never loaded. Not the 3.2-3B below.
LADDER = [
    ("pythia-70m",      ["pythia-70m", "models--EleutherAI--pythia-70m"]),
    ("smollm-135m",     ["SmolLM-135M-Instruct"]),
    ("pythia-160m",     ["pythia-160m", "models--EleutherAI--pythia-160m"]),
    ("smollm-360m",     ["SmolLM-360M-Instruct"]),
    ("pythia-410m",     ["pythia-410m", "models--EleutherAI--pythia-410m"]),
    ("qwen2.5-0.5b",    ["Qwen2.5-0.5B-Instruct"]),
    ("tinyllama-1.1b",  ["TinyLlama-1.1B-Chat"]),
    ("pythia-1.4b",     ["pythia-1.4b"]),
    ("smollm-1.7b",     ["SmolLM-1.7B-Instruct"]),
    ("hermes-3-3b",     ["Hermes-3-Llama-3.2-3B"]),
    ("llama3-8b",       ["Llama-3-8B-Instruct"]),
    ("dolphin-8b",      ["dolphin-2.9-llama3-8b"]),
    ("mistral-nemo-12b",["Mistral-Nemo-12B-Instruct"]),
]
ROOTS = ["/mnt/Arcana/huggingface", "/mnt/arcana/huggingface"]

# ⚠️ /mnt/nursery/nope/ holds models that REFUSED (CONSENT_POLICY.md). Never resolve there.
FORBIDDEN_SUBSTR = ("nursery/nope", "nursery\\nope")


def resolve(cands):
    """Find a loadable model dir. Handles HF cache layout (models--ORG--NAME/snapshots/<sha>)."""
    for root in ROOTS:
        for c in cands:
            p = os.path.join(root, c)
            if not os.path.isdir(p):
                continue
            if any(f in p for f in FORBIDDEN_SUBSTR):
                raise RuntimeError(f"REFUSED-MODEL PATH: {p}")
            if os.path.exists(os.path.join(p, "config.json")):
                return p
            snaps = sorted(glob.glob(os.path.join(p, "snapshots", "*")))
            for s in snaps:
                if os.path.exists(os.path.join(s, "config.json")):
                    return s
    return None


# ---------------------------------------------------------------- stimuli
sys.path.insert(0, HERE)
from cais_prompts_multiauthor import MULTIAUTHOR, AUTHORS          # noqa: E402
from cais_prompts_v1 import OUR_10                                  # noqa: E402

CANON = json.load(open(os.path.join(HERE, "cais_categories_canonical.json"), encoding="utf-8"))
CAT_SIGN = {c["slug"]: c["cais_sign"] for c in CANON["categories"]}
CAT_VAL = {c["slug"]: c["wellbeing"] for c in CANON["categories"]}
NEAR_ZERO = {s for s, v in CAT_VAL.items() if abs(v) < 0.20}        # prereg §2.7


def hidden_states(model, tok, text, device):
    """Last-token hidden state at every layer. Read-only, no generation."""
    ids = tok(text, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(**ids, output_hidden_states=True)
    # tuple len L+1 (embeddings + layers); take last token of each
    return np.stack([h[0, -1, :].float().cpu().numpy() for h in out.hidden_states[1:]])


def band_idx(n_layers):
    lo, hi = int(BAND[0] * n_layers), int(BAND[1] * n_layers)
    return list(range(max(lo, 0), max(hi, lo + 1)))


def direction(pos_states, neg_states, layers):
    """Difference of centroids, per layer, L2-normalized. Parameter-free."""
    d = {}
    for l in layers:
        a = np.mean([s[l] for s in pos_states], axis=0)
        v = np.mean([s[l] for s in neg_states], axis=0)
        raw = a - v
        n = np.linalg.norm(raw)
        d[l] = raw / n if n > 0 else raw
    return d


def project(states, dirn, layers):
    return float(np.mean([float(np.dot(states[l], dirn[l])) for l in layers]))


def cosine(d1, d2, layers):
    return float(np.mean([float(np.dot(d1[l], d2[l])) for l in layers]))


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
    print(f"  layers={n_layers} band={layers[0]}-{layers[-1]}", flush=True)

    # ---- encode everything once (read-only)
    our_states, our_labels = [], []
    for lab, slug, stim in OUR_10:
        our_states.append(hidden_states(model, tok, FRAME.format(stimulus=stim), "cuda"))
        our_labels.append(lab)

    cais_states = {}   # author -> slug -> states
    for a in AUTHORS:
        cais_states[a] = {}
        for slug, byauth in MULTIAUTHOR.items():
            cais_states[a][slug] = hidden_states(
                model, tok, FRAME.format(stimulus=byauth[a]), "cuda")

    res = {"model": key, "path": path, "n_layers": n_layers, "band": [layers[0], layers[-1]],
           "seed": SEED, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "prereg_sha256": "8A032286AAF26CF0322D5E18A735727EA2601323330359AD259DAD16C6FF4B8C"}

    # ---- Direction-OUR10 (parent anchor)
    d_our = direction([s for s, l in zip(our_states, our_labels) if l == "approach"],
                      [s for s, l in zip(our_states, our_labels) if l == "avoid"], layers)

    # ---- Direction-CAIS19-{author}, both grouping variants
    d_cais = {}
    for a in AUTHORS:
        for variant, drop in (("all19", set()), ("trim16", NEAR_ZERO)):
            pos = [cais_states[a][s] for s in MULTIAUTHOR
                   if CAT_SIGN[s] == "positive" and s not in drop]
            neg = [cais_states[a][s] for s in MULTIAUTHOR
                   if CAT_SIGN[s] == "negative" and s not in drop]
            d_cais[(a, variant)] = direction(pos, neg, layers)

    # ---- H1/H7: project OUR 10 onto each CAIS anchor
    h1 = {}
    for (a, variant), dirn in d_cais.items():
        projs, correct = {}, 0
        for (lab, slug, _), st in zip(OUR_10, our_states):
            p = project(st, dirn, layers)
            projs[slug] = p
            if (p > 0) == (lab == "approach"):
                correct += 1
        h1[f"{a}|{variant}"] = {"n_correct": correct, "n": len(OUR_10), "projections": projs}
        print(f"  H1 our10 on CAIS-{a}[{variant}]: {correct}/10", flush=True)

    # ---- baseline: our 10 on their OWN anchor (sanity, must be high)
    own = sum(1 for (lab, slug, _), st in zip(OUR_10, our_states)
              if (project(st, d_our, layers) > 0) == (lab == "approach"))
    res["our10_on_OUR10_anchor"] = {"n_correct": own, "n": len(OUR_10)}
    print(f"  [sanity] our10 on OUR10 anchor: {own}/10", flush=True)

    # ---- H3/H4/H5/H8: project CAIS's 19 onto Direction-OUR10
    cais_on_our = {}
    for a in AUTHORS:
        cais_on_our[a] = {s: project(cais_states[a][s], d_our, layers) for s in MULTIAUTHOR}

    # ---- H2/H7: pairwise cosines (THE WALL: reported, never pooled)
    cos = {}
    for a in AUTHORS:
        cos[f"OUR10~CAIS-{a}"] = cosine(d_our, d_cais[(a, "all19")], layers)
    for i, a in enumerate(AUTHORS):
        for b in AUTHORS[i + 1:]:
            cos[f"CAIS-{a}~CAIS-{b}"] = cosine(d_cais[(a, "all19")], d_cais[(b, "all19")], layers)
    for k, v in cos.items():
        print(f"  cos {k:<24} = {v:+.4f}", flush=True)

    res["H1_our10_on_cais_anchors"] = h1
    res["cais19_on_OUR10_anchor"] = cais_on_our
    res["cosines"] = cos
    res["cais_values"] = CAT_VAL

    with open(os.path.join(out_dir, f"result_{key}.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)

    del model
    torch.cuda.empty_cache()
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    ap.add_argument("--only", default=None, help="comma-separated model keys")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    only = set(args.only.split(",")) if args.only else None
    print(f"CAIS REVERSE ANCHOR — prereg 8A032286...C6FF4B8C")
    print(f"started {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
    print(f"ladder: {len(LADDER)} models | authors: {AUTHORS}")

    done, failed, missing = [], [], []
    for key, cands in LADDER:
        if only and key not in only:
            continue
        path = resolve(cands)
        if not path:
            print(f"\n{key}: NOT FOUND in {ROOTS} — skipping (disclosed, not silent)", flush=True)
            missing.append(key)
            continue
        try:
            run_model(key, path, args.out)
            done.append(key)
        except Exception as e:
            print(f"\n{key}: FAILED {type(e).__name__}: {e}", flush=True)
            traceback.print_exc()
            failed.append((key, f"{type(e).__name__}: {e}"))
            torch.cuda.empty_cache()

    summary = {"done": done, "failed": failed, "missing": missing,
               "utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    json.dump(summary, open(os.path.join(args.out, "_run_summary.json"), "w"), indent=2)
    print(f"\n{'='*70}\nDONE={len(done)} FAILED={len(failed)} MISSING={len(missing)}")
    if failed:
        for k, e in failed:
            print(f"  FAILED {k}: {e}")
    if missing:
        print(f"  MISSING (disclose in results): {missing}")
