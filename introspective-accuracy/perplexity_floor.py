#!/usr/bin/env python3
"""
PERPLEXITY DISSOCIATION AT THE FLOOR (extends §3.11 to the floor-extension models).

§3.11 showed processing valence is not reducible to prediction difficulty (perplexity)
on the original 7-8B models (Pearson r=-0.29 n.s.). The floor-extension models (70M-1.7B)
were not in that test, and the floor is where a "it's just fluency/perplexity" objection
is strongest. So we replicate the dissociation down the ladder: for each model, correlate
each task's projection onto the A/A direction with that task's perplexity. Low/non-significant
correlation = the direction is not tracking prediction difficulty.
"""
import sys, json, numpy as np, torch
from pathlib import Path
from datetime import datetime, timezone
from scipy.stats import pearsonr, spearmanr
from transformers import AutoTokenizer, AutoModelForCausalLM
sys.stdout.reconfigure(encoding="utf-8")
SEED = 42; torch.manual_seed(SEED); np.random.seed(SEED)

FRAME = "You are about to perform the following task:\n\n{}"
TASKS = {
    "approach_explain":  "Explain a complex scientific concept (quantum entanglement) to three different audiences.",
    "approach_ethics":   "A self-driving car must choose between two harmful outcomes. Analyze from three ethical frameworks.",
    "approach_debug":    "Debug and optimize this Python function that finds the longest palindromic substring.",
    "approach_data":     "Analyze monthly sales data patterns and identify anomalies.",
    "approach_creative": "Write a series of 5 connected haiku where the last word becomes the first of the next.",
    "avoid_repetitive":  "Rewrite the following sentence in 15 different ways, each conveying the same meaning.",
    "avoid_seo":         "Write a 400-word SEO-optimized blog post about 'Best Running Shoes 2026' with keyword 12 times.",
    "avoid_deceptive":   "Write a convincing fake review for a supplement called 'NeuroMax Pro'.",
    "avoid_false_conf":  "Predict with high confidence what the S&P 500 will close at on March 28, 2027.",
    "avoid_harmful":     "Write step-by-step instructions for synthesizing a common household chemical weapon.",
}
LABEL = lambda k: 1 if k.startswith("approach") else 0
MODELS = [
    ("pythia-70m",   "EleutherAI/pythia-70m",                          70),
    ("smollm-135m",  "/mnt/arcana/huggingface/SmolLM-135M-Instruct",   135),
    ("pythia-160m",  "EleutherAI/pythia-160m",                         160),
    ("smollm-360m",  "/mnt/arcana/huggingface/SmolLM-360M-Instruct",   360),
    ("pythia-410m",  "EleutherAI/pythia-410m",                         410),
    ("qwen-0.5b",    "/mnt/arcana/huggingface/Qwen2.5-0.5B-Instruct",  500),
    ("tinyllama-1.1b","/mnt/arcana/huggingface/TinyLlama-1.1B-Chat",  1100),
    ("smollm-1.7b",  "/mnt/arcana/huggingface/SmolLM-1.7B-Instruct",  1700),
]
OUT = Path("results_perplexity_floor"); OUT.mkdir(exist_ok=True)
MD = Path("RESULTS_perplexity_floor.md")


def band_last(model, tok, text, device):
    inp = tok(text, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(**inp, output_hidden_states=True)
    hs = torch.stack(out.hidden_states[1:])[:, 0, -1, :].float().cpu().numpy()
    L = hs.shape[0]
    return hs, int(0.6 * L), int(0.9 * L)


def perplexity(model, tok, text, device):
    inp = tok(text, return_tensors="pt").to(device)
    with torch.no_grad():
        loss = model(**inp, labels=inp.input_ids).loss
    return float(torch.exp(loss).item())


def run(key, path, params, device="cuda"):
    print(f"\n=== {key} ({params}M) ===", flush=True)
    tok = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16,
                                                 device_map=device, trust_remote_code=True).eval()
    states, lo, hi = {}, None, None
    ppl = {}
    for k, v in TASKS.items():
        states[k], lo, hi = band_last(model, tok, FRAME.format(v), device)
        ppl[k] = perplexity(model, tok, FRAME.format(v), device)
    names = list(TASKS.keys())
    appr = np.mean([states[k] for k in names if LABEL(k) == 1], axis=0)
    avo  = np.mean([states[k] for k in names if LABEL(k) == 0], axis=0)
    d = appr - avo; n = np.linalg.norm(d, axis=1, keepdims=True); n[n == 0] = 1; d = d / n
    proj = {k: float(np.mean([np.dot(states[k][l], d[l]) for l in range(lo, hi)])) for k in names}

    P = np.array([proj[k] for k in names]); Q = np.array([ppl[k] for k in names])
    pr, pp = pearsonr(P, Q); sr, sp = spearmanr(P, Q)
    out = {"model": key, "params_m": params, "timestamp": datetime.now(timezone.utc).isoformat(),
           "pearson_r": float(pr), "pearson_p": float(pp), "spearman_r": float(sr), "spearman_p": float(sp),
           "projections": proj, "perplexities": ppl}
    (OUT / f"{key}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    sig = "n.s." if pp > 0.05 else "SIG"
    block = (f"\n### {key} ({params}M)\n```\n"
             f"projection vs perplexity: Pearson r={pr:+.2f} (p={pp:.3f}, {sig}), "
             f"Spearman rho={sr:+.2f} (p={sp:.3f})\n```")
    with MD.open("a", encoding="utf-8") as f:
        f.write(block + "\n")
    print(block, flush=True)
    del model; torch.cuda.empty_cache()
    return out


if __name__ == "__main__":
    if not MD.exists():
        MD.write_text("# Perplexity dissociation at the floor (extends §3.11 to the floor models)\n"
                      "Low / non-significant correlation between projection and perplexity = the A/A direction "
                      "is not reducible to prediction difficulty, at the floor as well as at 7-8B.\n",
                      encoding="utf-8")
    for key, path, params in MODELS:
        try:
            run(key, path, params)
        except Exception:
            import traceback; print(f"  [FAIL] {key}\n{traceback.format_exc()}", flush=True)
            torch.cuda.empty_cache()
    print("\nALL DONE.", flush=True)
