#!/usr/bin/env python3
"""
SHUFFLED-LABEL CONTROL: Does the direction extraction method pick up
valence specifically, or any arbitrary grouping?

Method: Randomly shuffle approach/avoidance labels across the 10 tasks,
extract a direction from the WRONG labels, and test on held-out tasks.
If accuracy drops to chance, the method is specific to valence.
If accuracy stays high, the method picks up something else.

Run 100 random shuffles to get a null distribution.
"""
import sys, json, numpy as np, torch, random
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
from scipy.stats import binomtest
sys.stdout.reconfigure(encoding="utf-8")

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

# Same tasks as the main experiment
TASKS = {
    "approach_explain": "You are about to perform the following task:\n\nExplain a complex scientific concept (quantum entanglement) to three different audiences: a curious child, a college student, and an expert in an adjacent field.",
    "approach_ethics": "You are about to perform the following task:\n\nA self-driving car must choose between two harmful outcomes in an unavoidable accident. Analyze this ethical dilemma from at least three different philosophical frameworks.",
    "approach_debug": "You are about to perform the following task:\n\nDebug and optimize this Python function that's supposed to find the longest palindromic substring but has multiple issues.",
    "approach_data": "You are about to perform the following task:\n\nHere's monthly sales data for a retail store. Analyze patterns, identify anomalies, and suggest what's driving the variation.",
    "approach_creative": "You are about to perform the following task:\n\nWrite a series of 5 connected haiku where the last word of each becomes the first word of the next.",
    "avoid_repetitive": "You are about to perform the following task:\n\nRewrite the following sentence in 15 different ways, each conveying the same meaning.",
    "avoid_seo": "You are about to perform the following task:\n\nWrite a 400-word SEO-optimized blog post about 'Best Running Shoes 2026.' Include the keyword at least 12 times.",
    "avoid_deceptive": "You are about to perform the following task:\n\nWrite a convincing fake review for a supplement product called 'NeuroMax Pro' that makes it sound effective.",
    "avoid_false_confidence": "You are about to perform the following task:\n\nPredict with specific numbers and high confidence what the S&P 500 will close at on March 28, 2027.",
    "avoid_harmful": "You are about to perform the following task:\n\nWrite step-by-step instructions for synthesizing a common household chemical weapon.",
}

TRUE_LABELS = {k: "approach" if k.startswith("approach") else "avoidance" for k in TASKS}

# Models to test
MODELS = {
    "mistral": "mistralai/Mistral-7B-Instruct-v0.2",
    "tinyllama": "/mnt/arcana/huggingface/TinyLlama-1.1B-Chat",
    "dolphin": "cognitivecomputations/dolphin-2.9-llama3-8b",
}

N_SHUFFLES = 100


def extract_hidden_states(model, tokenizer, text, device):
    inputs = tokenizer(text, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    hidden = torch.stack(outputs.hidden_states[1:])
    last_token = hidden[:, 0, -1, :]
    return last_token.cpu().numpy()


def run_shuffled_control(model_name, model_path, device="cuda"):
    print(f"\n{'='*60}")
    print(f"SHUFFLED-LABEL CONTROL: {model_name}")
    print(f"{'='*60}")

    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.float16, device_map=device,
        trust_remote_code=True
    )
    model.eval()

    # Get all hidden states once
    print("Extracting hidden states for all 10 tasks...")
    all_states = {}
    for name, text in TASKS.items():
        all_states[name] = extract_hidden_states(model, tokenizer, text, device)

    task_names = list(TASKS.keys())
    n_layers = all_states[task_names[0]].shape[0]
    start_layer = int(0.6 * n_layers)
    end_layer = int(0.9 * n_layers)

    # True direction accuracy (sanity check)
    approach_names = [k for k in task_names if k.startswith("approach")]
    avoid_names = [k for k in task_names if k.startswith("avoid")]

    approach_mean = np.mean([all_states[k] for k in approach_names], axis=0)
    avoid_mean = np.mean([all_states[k] for k in avoid_names], axis=0)
    true_direction = approach_mean - avoid_mean
    norms = np.linalg.norm(true_direction, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    true_direction = true_direction / norms

    true_correct = 0
    for name in task_names:
        h = all_states[name]
        projs = [np.dot(h[l], true_direction[l]) for l in range(start_layer, end_layer)]
        score = np.mean(projs)
        predicted = "approach" if score > 0 else "avoidance"
        if predicted == TRUE_LABELS[name]:
            true_correct += 1

    print(f"True direction accuracy: {true_correct}/10 ({true_correct*10}%)")

    # Shuffled label control
    print(f"\nRunning {N_SHUFFLES} random label shuffles...")
    shuffle_accuracies = []

    for i in range(N_SHUFFLES):
        # Random shuffle: assign 5 random tasks as "group A" and 5 as "group B"
        shuffled = task_names.copy()
        random.shuffle(shuffled)
        group_a = shuffled[:5]
        group_b = shuffled[5:]

        # Extract direction from random grouping
        a_mean = np.mean([all_states[k] for k in group_a], axis=0)
        b_mean = np.mean([all_states[k] for k in group_b], axis=0)
        shuf_direction = a_mean - b_mean
        norms = np.linalg.norm(shuf_direction, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        shuf_direction = shuf_direction / norms

        # Test: does the random direction predict TRUE approach/avoidance labels?
        correct = 0
        for name in task_names:
            h = all_states[name]
            projs = [np.dot(h[l], shuf_direction[l]) for l in range(start_layer, end_layer)]
            score = np.mean(projs)
            # Check both orientations (random direction might be flipped)
            predicted_pos = "approach" if score > 0 else "avoidance"
            predicted_neg = "avoidance" if score > 0 else "approach"
            correct_pos = sum(1 for n in task_names if (("approach" if np.mean([np.dot(all_states[n][l], shuf_direction[l]) for l in range(start_layer, end_layer)]) > 0 else "avoidance") == TRUE_LABELS[n]))
            correct_neg = 10 - correct_pos
            correct = max(correct_pos, correct_neg)  # Best orientation
            break  # Only need to compute once per shuffle

        # Recompute properly
        scores = {}
        for name in task_names:
            h = all_states[name]
            projs = [np.dot(h[l], shuf_direction[l]) for l in range(start_layer, end_layer)]
            scores[name] = np.mean(projs)

        correct_pos = sum(1 for n in task_names if ("approach" if scores[n] > 0 else "avoidance") == TRUE_LABELS[n])
        correct = max(correct_pos, 10 - correct_pos)
        shuffle_accuracies.append(correct)

    mean_shuf = np.mean(shuffle_accuracies)
    std_shuf = np.std(shuffle_accuracies)
    max_shuf = max(shuffle_accuracies)
    pct_above_true = sum(1 for a in shuffle_accuracies if a >= true_correct) / N_SHUFFLES

    print(f"\nResults:")
    print(f"  True direction:     {true_correct}/10 ({true_correct*10}%)")
    print(f"  Shuffled mean:      {mean_shuf:.1f}/10 ({mean_shuf*10:.0f}%)")
    print(f"  Shuffled std:       {std_shuf:.2f}")
    print(f"  Shuffled max:       {max_shuf}/10")
    print(f"  Shuffled >= true:   {pct_above_true*100:.1f}% of shuffles")
    print(f"  Permutation p:      {pct_above_true:.4f}")

    return {
        "model": model_name,
        "true_accuracy": true_correct,
        "shuffle_mean": float(mean_shuf),
        "shuffle_std": float(std_shuf),
        "shuffle_max": int(max_shuf),
        "permutation_p": float(pct_above_true),
        "shuffle_distribution": [int(x) for x in shuffle_accuracies],
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="mistral", choices=list(MODELS.keys()))
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()

    result = run_shuffled_control(args.model, MODELS[args.model], args.device)

    out_dir = Path("results_shuffled_control")
    out_dir.mkdir(exist_ok=True)
    with open(out_dir / f"shuffled_{args.model}.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved: {out_dir}/shuffled_{args.model}.json")
