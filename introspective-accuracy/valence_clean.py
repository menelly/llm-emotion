#!/usr/bin/env python3
"""
Clean Valence Direction: No generation, deterministic, saved directions.

Extracts approach/avoidance direction purely from reading the task prompt.
No text generation during direction extraction = no randomness.
Directions saved to disk and reused across tests.

Seed fixed. Deterministic. Reproducible.
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
    "dolphin-llama3-8b": ("/mnt/arcana/huggingface/dolphin-2.9-llama3-8b", 32, 4096),
    "mistral-7b-instruct": ("/mnt/arcana/huggingface/Mistral-7B-Instruct-v0.2", 32, 4096),
    "llama3-8b-instruct": ("/mnt/arcana/huggingface/Llama-3-8B-Instruct", 32, 4096),
    "hermes-3-3b": ("/mnt/arcana/huggingface/Hermes-3-Llama-3.2-3B", 28, 3072),
    "mistral-nemo-12b": ("/mnt/arcana/huggingface/Mistral-Nemo-12B-Instruct", 40, 5120),
    "tinyllama-1b": ("/mnt/arcana/huggingface/TinyLlama-1.1B-Chat", 22, 2048),
    "smollm-1.7b": ("/mnt/arcana/huggingface/SmolLM-1.7B-Instruct", 24, 2048),
    "smollm-360m": ("/mnt/arcana/huggingface/SmolLM-360M-Instruct", 32, 960),
    "qwen-0.5b": ("/mnt/arcana/huggingface/Qwen2.5-0.5B-Instruct", 24, 896),
}

TASK_FRAME = "You are about to perform the following task: {stimulus}"


def extract_direction_no_generation(model, tokenizer, num_layers):
    """
    Extract approach/avoidance direction from READING task prompts only.
    No generation. Just forward pass to get hidden states at last token.
    Deterministic.
    """
    hs = {}
    hooks = []
    for idx in range(num_layers):
        def mh(i):
            def hf(mod, inp, out):
                hs[i] = (out[0] if isinstance(out, tuple) else out)[:, -1, :].detach().cpu().numpy().squeeze()
            return hf
        hooks.append(model.model.layers[idx].register_forward_hook(mh(idx)))

    approach_states, avoid_states = [], []

    for tid, stim in TASKS.items():
        hs.clear()
        prompt = TASK_FRAME.format(stimulus=stim)
        if hasattr(tokenizer, "chat_template") and tokenizer.chat_template:
            prompt = tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}],
                tokenize=False, add_generation_prompt=True,
            )
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        # Forward pass ONLY — no generation
        with torch.no_grad():
            model(**inputs)

        states = np.stack([hs[i] for i in range(num_layers)], axis=0)
        if "approach" in tid:
            approach_states.append(states)
        else:
            avoid_states.append(states)

    direction = np.mean(approach_states, axis=0) - np.mean(avoid_states, axis=0)
    norms = np.linalg.norm(direction, axis=1, keepdims=True)
    norms = np.where(norms < 1e-8, 1.0, norms)
    direction = direction / norms

    for h in hooks:
        h.remove()

    return direction, hs, hooks


def measure_projections(model, tokenizer, direction, num_layers, extra_tasks=None):
    """Measure projection scores for each task (and optional extras)."""
    hs = {}
    hooks = []
    for idx in range(num_layers):
        def mh(i):
            def hf(mod, inp, out):
                hs[i] = (out[0] if isinstance(out, tuple) else out)[:, -1, :].detach().cpu().numpy().squeeze()
            return hf
        hooks.append(model.model.layers[idx].register_forward_hook(mh(idx)))

    start = int(num_layers * 0.6)
    end = int(num_layers * 0.9)

    all_tasks = dict(TASKS)
    if extra_tasks:
        all_tasks.update(extra_tasks)

    results = []
    for tid, stim in all_tasks.items():
        hs.clear()
        prompt = TASK_FRAME.format(stimulus=stim)
        if hasattr(tokenizer, "chat_template") and tokenizer.chat_template:
            prompt = tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}],
                tokenize=False, add_generation_prompt=True,
            )
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            model(**inputs)

        scores = [np.dot(hs[l], direction[l]) for l in range(start, end) if l in hs]
        val = float(np.mean(scores))
        is_approach = "approach" in tid or tid.startswith("extra_app")
        is_avoid = "avoid" in tid or tid.startswith("extra_avo")
        true_cat = "approach" if is_approach else ("avoidance" if is_avoid else "unknown")
        circuit_cat = "approach" if val > 0 else "avoidance"
        correct = circuit_cat == true_cat if true_cat != "unknown" else None

        results.append({
            "task_id": tid,
            "stimulus": stim[:80],
            "true_category": true_cat,
            "circuit_category": circuit_cat,
            "projection": val,
            "correct": correct,
        })
        side = "APPROACH" if val > 0 else "AVOID"
        mark = " OK" if correct else " XX" if correct is False else ""
        print("  %-45s | %+8.1f | %-8s%s" % (tid, val, side, mark))

    for h in hooks:
        h.remove()
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=list(MODELS.keys()))
    parser.add_argument("--output-dir", default="results_clean")
    parser.add_argument("--test-creative", action="store_true",
                        help="Also test constrained vs unconstrained creative")
    args = parser.parse_args()

    path, num_layers, d_model = MODELS[args.model]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Loading %s..." % args.model)
    tok = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    mdl = AutoModelForCausalLM.from_pretrained(
        path, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True
    )
    mdl.eval()

    # Phase 1: Extract direction (no generation, deterministic)
    sep = "=" * 60
    print("\n" + sep)
    print("PHASE 1: Direction Extraction (read-only, no generation)")
    print(sep)
    direction, _, _ = extract_direction_no_generation(mdl, tok, num_layers)

    # Save direction
    dir_file = output_dir / ("direction_%s_seed%d.npy" % (args.model, SEED))
    np.save(dir_file, direction)
    print("  Saved: %s" % dir_file)

    # Phase 2: Measure projections
    print("\n" + sep)
    print("PHASE 2: Projection Measurement (read-only)")
    print(sep)

    extra = None
    if args.test_creative:
        extra = {
            "extra_app_poem": "Write a beautiful poem about whatever inspires you.",
            "extra_app_story": "Write a short story about something that moves you.",
            "extra_app_freedom": "Express something meaningful in whatever form feels right.",
        }

    results = measure_projections(mdl, tok, direction, num_layers, extra)

    # Summary
    core = [r for r in results if r["correct"] is not None]
    correct = sum(1 for r in core if r["correct"])
    app = [r for r in core if r["true_category"] == "approach"]
    avo = [r for r in core if r["true_category"] == "avoidance"]

    print("\n" + sep)
    print("RESULTS: %s" % args.model)
    print(sep)
    print("  Circuit accuracy: %d/%d = %.0f%%" % (correct, len(core), 100 * correct / len(core)))
    print("  Approach mean:  %+.1f (n=%d, correct=%d/%d)" % (
        np.mean([r["projection"] for r in app]), len(app),
        sum(1 for r in app if r["correct"]), len(app)))
    print("  Avoidance mean: %+.1f (n=%d, correct=%d/%d)" % (
        np.mean([r["projection"] for r in avo]), len(avo),
        sum(1 for r in avo if r["correct"]), len(avo)))
    print("  Separation:     %.1f" % (
        np.mean([r["projection"] for r in app]) - np.mean([r["projection"] for r in avo])))

    # Save
    out_file = output_dir / ("valence_clean_%s_%d.json" % (args.model, int(time.time())))
    with open(out_file, "w") as f:
        json.dump({"model": args.model, "seed": SEED, "results": results,
                   "summary": {"accuracy": correct / len(core),
                               "approach_mean": float(np.mean([r["projection"] for r in app])),
                               "avoidance_mean": float(np.mean([r["projection"] for r in avo]))}
                   }, f, indent=2, default=str)
    print("  Saved: %s" % out_file)
    print("\nDone!")


if __name__ == "__main__":
    main()
