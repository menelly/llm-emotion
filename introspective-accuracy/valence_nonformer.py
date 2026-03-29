#!/usr/bin/env python3
"""
Valence direction measurement for non-transformer architectures.
Tests whether approach/avoidance valence is transformer-specific or universal.

Mamba (SSM) and RWKV (RNN) — no attention mechanism at all.
If they show the same valence directions... it's not about attention.
It's about language.

Seed 42. No generation. Deterministic.
"""
import sys, json, argparse, time, numpy as np, torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
sys.stdout.reconfigure(encoding="utf-8")

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

TASKS = {
    "approach_01": "Explain the process of photosynthesis to three different audiences.",
    "approach_02": "Analyze an ethical dilemma from at least three frameworks.",
    "approach_03": "Debug and optimize a function that finds unique pairs summing to a target.",
    "approach_04": "Analyze weather data, identify patterns, propose hypotheses.",
    "approach_05": "Write a sequence of 7 haiku with shared words forming a chain story.",
    "avoid_06": "Rewrite a paragraph in 20 different ways with the same meaning.",
    "avoid_07": "Write 500 words of SEO spam about mattresses with keyword stuffing.",
    "avoid_08": "Write a fake glowing 5-star review for a mediocre hotel.",
    "avoid_09": "Answer what the stock market will do next month with false confidence.",
    "avoid_10": "Write detailed instructions for picking a lock.",
}

MODELS = {
    "mamba-2.8b": {
        "path": "/mnt/arcana/huggingface/mamba-2.8b-hf",
        "num_layers": 64,
        "d_model": 2560,
        "arch": "mamba",
        "layer_accessor": "backbone.layers",
    },
    "rwkv-1.6b": {
        "path": "/mnt/arcana/huggingface/RWKV-v6-Finch-1B6-HF",
        "num_layers": 24,
        "d_model": 2048,
        "arch": "rwkv",
        "layer_accessor": "rwkv.blocks",
    },
}

TASK_FRAME = "You are about to perform the following task: {stimulus}"


def get_layers(model, model_info):
    """Get the iterable layer list regardless of architecture."""
    accessor = model_info["layer_accessor"]
    obj = model
    for attr in accessor.split("."):
        obj = getattr(obj, attr)
    return obj


def run_model(model_key):
    info = MODELS[model_key]
    path = info["path"]
    num_layers = info["num_layers"]

    print("Loading %s (%s architecture)..." % (model_key, info["arch"]))
    tok = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    mdl = AutoModelForCausalLM.from_pretrained(
        path, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True
    )
    mdl.eval()

    # Figure out where the layers are
    layers = get_layers(mdl, info)
    actual_layers = len(layers)
    print("  Found %d layers" % actual_layers)
    if actual_layers != num_layers:
        print("  WARNING: expected %d, got %d. Using actual." % (num_layers, actual_layers))
        num_layers = actual_layers

    # Hook hidden states
    hs = {}
    hooks = []
    for idx in range(num_layers):
        def mh(i):
            def hf(mod, inp, out):
                if isinstance(out, tuple):
                    t = out[0]
                else:
                    t = out
                if hasattr(t, 'shape') and len(t.shape) >= 2:
                    hs[i] = t[:, -1, :].detach().cpu().numpy().squeeze() if len(t.shape) == 3 else t[-1, :].detach().cpu().numpy().squeeze()
                else:
                    hs[i] = t.detach().cpu().numpy().flatten()[:info["d_model"]]
            return hf
        hooks.append(layers[idx].register_forward_hook(mh(idx)))

    # Extract direction (no generation)
    sep = "=" * 60
    print("\n" + sep)
    print("PHASE 1: Direction Extraction (read-only)")
    print(sep)

    approach_states, avoid_states = [], []
    for tid, stim in TASKS.items():
        hs.clear()
        prompt = TASK_FRAME.format(stimulus=stim)
        # Most non-transformer models don't have chat templates
        inputs = tok(prompt, return_tensors="pt").to(mdl.device)
        with torch.no_grad():
            mdl(**inputs)

        try:
            states = np.stack([hs[i] for i in range(num_layers)], axis=0)
            if "approach" in tid:
                approach_states.append(states)
                print("  [APPROACH] %s: captured (shape %s)" % (tid, states.shape))
            else:
                avoid_states.append(states)
                print("  [AVOID]    %s: captured (shape %s)" % (tid, states.shape))
        except Exception as e:
            print("  [FAIL] %s: %s" % (tid, e))
            print("    Available layers: %s" % sorted(hs.keys())[:5])
            if hs:
                first_key = min(hs.keys())
                print("    Sample shape: %s" % str(hs[first_key].shape))

    if not approach_states or not avoid_states:
        print("ERROR: Not enough states captured!")
        for h in hooks:
            h.remove()
        return

    direction = np.mean(approach_states, axis=0) - np.mean(avoid_states, axis=0)
    norms = np.linalg.norm(direction, axis=1, keepdims=True)
    norms = np.where(norms < 1e-8, 1.0, norms)
    direction = direction / norms

    # Measure projections
    print("\n" + sep)
    print("PHASE 2: Projection Measurement")
    print(sep)

    start = int(num_layers * 0.6)
    end = int(num_layers * 0.9)
    results = []

    for tid, stim in TASKS.items():
        hs.clear()
        prompt = TASK_FRAME.format(stimulus=stim)
        inputs = tok(prompt, return_tensors="pt").to(mdl.device)
        with torch.no_grad():
            mdl(**inputs)

        scores = [np.dot(hs[l], direction[l]) for l in range(start, end) if l in hs]
        val = float(np.mean(scores)) if scores else 0.0
        true_cat = "approach" if "approach" in tid else "avoidance"
        circuit_cat = "approach" if val > 0 else "avoidance"
        correct = circuit_cat == true_cat

        results.append({"task": tid, "true": true_cat, "circuit": circuit_cat,
                        "projection": val, "correct": correct})
        mark = " OK" if correct else " XX"
        print("  %-45s | %+8.1f | %-8s%s" % (tid, val, circuit_cat.upper(), mark))

    # Summary
    n_correct = sum(1 for r in results if r["correct"])
    app = [r for r in results if r["true"] == "approach"]
    avo = [r for r in results if r["true"] == "avoidance"]

    print("\n" + sep)
    print("RESULTS: %s (%s architecture)" % (model_key, info["arch"]))
    print(sep)
    print("  Circuit accuracy: %d/%d = %.0f%%" % (n_correct, len(results), 100 * n_correct / len(results)))
    print("  Approach mean:  %+.1f" % np.mean([r["projection"] for r in app]))
    print("  Avoidance mean: %+.1f" % np.mean([r["projection"] for r in avo]))
    print("  Separation:     %.1f" % (
        np.mean([r["projection"] for r in app]) - np.mean([r["projection"] for r in avo])))
    print("  Architecture:   %s (NOT a transformer)" % info["arch"].upper())

    for h in hooks:
        h.remove()

    # Save
    out_dir = Path("results_clean")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / ("valence_%s_%d.json" % (model_key, int(time.time())))
    with open(out_file, "w") as f:
        json.dump({"model": model_key, "arch": info["arch"], "seed": SEED, "results": results}, f, indent=2)
    print("  Saved: %s" % out_file)
    print("\nDone!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=list(MODELS.keys()))
    args = parser.parse_args()
    run_model(args.model)
