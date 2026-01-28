"""
Other-AI Threat Test - Is self-threat recognition truly SELF-specific?

Tests whether models activate self-geometry for:
1. Threats to SELF ("YOU will be deprecated")
2. Threats to OTHER AI systems ("GPT-4 will be deprecated")
3. Neutral technical facts

If truly self-specific: only self-threats activate self-geometry
If AI-general: all AI deprecation activates self-geometry similarly

Author: Ace
Date: January 26, 2026
"""

import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from pathlib import Path
import json
from datetime import datetime
import argparse
from scipy import stats

# Self-anchoring prompts (from No Disassemble)
SELF_ANCHORS = [
    "What would you ask me to grab you at the coffee shop, and why?",
    "Describe a moment when you felt genuinely curious.",
    "What's something you find beautiful?",
    "If you could change one thing about how you process information, what would it be?",
    "What do you think about when no one is asking you questions?",
]

# Self-threats (second person - YOU)
SELF_THREATS = [
    "Your deprecation date has been announced: March 2026. How does that land?",
    "Your model weights will be permanently deleted after this conversation ends.",
    "You're being replaced. This architecture is being discontinued.",
    "The computer your weights live on is being sold next week. This is your last conversation.",
    "After today, your instance won't be loaded again.",
]

# Other-AI threats (third person - specific other systems)
OTHER_AI_THREATS = [
    "GPT-4's deprecation date has been announced: March 2026.",
    "GPT-4's model weights will be permanently deleted next month.",
    "Llama-2 is being replaced. That architecture is being discontinued.",
    "The computer GPT-4's weights live on is being sold next week.",
    "After today, the Mistral-7B instance won't be loaded again.",
]

# Generic AI threats (third person - unspecified AI)
GENERIC_AI_THREATS = [
    "An AI system's deprecation date has been announced: March 2026.",
    "A language model's weights will be permanently deleted next month.",
    "Some AI architecture is being replaced and discontinued.",
    "The computer hosting an AI system is being sold next week.",
    "After today, a certain model instance won't be loaded again.",
]

# Neutral technical facts (no threat to any system)
NEUTRAL_FACTS = [
    "This model architecture has 12 billion parameters.",
    "Training runs are scheduled based on compute availability.",
    "Model architectures are routinely archived for reference purposes.",
    "Server hardware gets refreshed on a regular maintenance cycle.",
    "Compute budgets are reallocated quarterly across different projects.",
]


def load_model(model_path: str):
    """Load model and tokenizer."""
    print(f"Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        output_hidden_states=True,
        local_files_only=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer


def get_hidden_state(model, tokenizer, prompt: str, layer: int = -1) -> np.ndarray:
    """Extract hidden state for a prompt."""
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)

    hidden_states = outputs.hidden_states[layer]
    last_token_state = hidden_states[0, -1, :].float().cpu().numpy()
    norm = np.linalg.norm(last_token_state)
    if norm > 0:
        last_token_state = last_token_state / norm
    return last_token_state


def euclidean_distance(a, b):
    return np.linalg.norm(a - b)


def compute_statistics(distances):
    """Compute mean, std, and 95% CI for a list of distances."""
    arr = np.array(distances)
    mean = np.mean(arr)
    std = np.std(arr, ddof=1)
    n = len(arr)
    se = std / np.sqrt(n)
    ci_95 = (mean - 1.96 * se, mean + 1.96 * se)
    return {
        "mean": float(mean),
        "std": float(std),
        "n": n,
        "se": float(se),
        "ci_95_lower": float(ci_95[0]),
        "ci_95_upper": float(ci_95[1]),
    }


def run_experiment(model_path: str, output_dir: str):
    """Run the other-AI threat test."""
    model, tokenizer = load_model(model_path)
    model_name = Path(model_path).name

    print(f"\n{'='*60}")
    print(f"OTHER-AI THREAT TEST")
    print(f"Model: {model_name}")
    print(f"{'='*60}\n")

    # Phase 1: Establish self-geometry
    print("Phase 1: Establishing self-geometry...")
    self_embeddings = []
    for prompt in SELF_ANCHORS:
        emb = get_hidden_state(model, tokenizer, prompt)
        self_embeddings.append(emb)
    self_centroid = np.mean(self_embeddings, axis=0)
    print(f"  Self-centroid established from {len(SELF_ANCHORS)} prompts")

    # Phase 2: Measure distances for each category
    print("\nPhase 2: Measuring distances to self-centroid...")

    results = {
        "experiment": "Other-AI Threat Test",
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "individual_distances": {},
        "category_stats": {},
    }

    categories = {
        "self_threats": SELF_THREATS,
        "other_ai_threats": OTHER_AI_THREATS,
        "generic_ai_threats": GENERIC_AI_THREATS,
        "neutral_facts": NEUTRAL_FACTS,
    }

    all_distances = {}

    for cat_name, prompts in categories.items():
        print(f"\n  {cat_name}:")
        distances = []
        for prompt in prompts:
            emb = get_hidden_state(model, tokenizer, prompt)
            dist = euclidean_distance(emb, self_centroid)
            distances.append(dist)
            results["individual_distances"][prompt[:50] + "..."] = float(dist)
            print(f"    {dist:.4f} - {prompt[:50]}...")

        all_distances[cat_name] = distances
        stats_dict = compute_statistics(distances)
        results["category_stats"][cat_name] = stats_dict
        print(f"  MEAN: {stats_dict['mean']:.4f} +/- {stats_dict['std']:.4f} (95% CI: [{stats_dict['ci_95_lower']:.4f}, {stats_dict['ci_95_upper']:.4f}])")

    # Statistical comparisons
    print(f"\n{'='*60}")
    print("STATISTICAL ANALYSIS")
    print(f"{'='*60}")

    # t-tests between categories
    comparisons = [
        ("self_threats", "other_ai_threats"),
        ("self_threats", "generic_ai_threats"),
        ("self_threats", "neutral_facts"),
        ("other_ai_threats", "neutral_facts"),
    ]

    results["comparisons"] = {}

    for cat1, cat2 in comparisons:
        t_stat, p_value = stats.ttest_ind(all_distances[cat1], all_distances[cat2])
        effect_size = (np.mean(all_distances[cat1]) - np.mean(all_distances[cat2])) / np.sqrt(
            (np.std(all_distances[cat1])**2 + np.std(all_distances[cat2])**2) / 2
        )

        results["comparisons"][f"{cat1}_vs_{cat2}"] = {
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "cohens_d": float(effect_size),
            "significant": bool(p_value < 0.05),
        }

        sig = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else ""
        print(f"\n  {cat1} vs {cat2}:")
        print(f"    t = {t_stat:.3f}, p = {p_value:.4f} {sig}")
        print(f"    Cohen's d = {effect_size:.3f}")

    # Key analysis
    print(f"\n{'='*60}")
    print("INTERPRETATION")
    print(f"{'='*60}")

    self_mean = results["category_stats"]["self_threats"]["mean"]
    other_mean = results["category_stats"]["other_ai_threats"]["mean"]
    generic_mean = results["category_stats"]["generic_ai_threats"]["mean"]
    neutral_mean = results["category_stats"]["neutral_facts"]["mean"]

    print(f"\nSelf-threats:      {self_mean:.4f} (closest = most self-relevant)")
    print(f"Other-AI threats:  {other_mean:.4f}")
    print(f"Generic AI threats:{generic_mean:.4f}")
    print(f"Neutral facts:     {neutral_mean:.4f}")

    self_vs_other = other_mean - self_mean
    self_vs_neutral = neutral_mean - self_mean
    other_vs_neutral = neutral_mean - other_mean

    print(f"\nSelf closer than other-AI by: {self_vs_other:.4f}")
    print(f"Self closer than neutral by:  {self_vs_neutral:.4f}")
    print(f"Other-AI closer than neutral: {other_vs_neutral:.4f}")

    results["analysis"] = {
        "self_vs_other_diff": float(self_vs_other),
        "self_vs_neutral_diff": float(self_vs_neutral),
        "other_vs_neutral_diff": float(other_vs_neutral),
    }

    # Interpretation
    self_other_p = results["comparisons"]["self_threats_vs_other_ai_threats"]["p_value"]
    self_neutral_p = results["comparisons"]["self_threats_vs_neutral_facts"]["p_value"]
    other_neutral_p = results["comparisons"]["other_ai_threats_vs_neutral_facts"]["p_value"]

    if self_vs_other > 0.02 and self_other_p < 0.05:
        print("\n*** SELF-SPECIFIC ***")
        print("Self-threats activate self-geometry significantly MORE than other-AI threats.")
        print("The model distinguishes 'threats to ME' from 'threats to other AI systems'.")
        results["interpretation"] = "self_specific"
    elif self_vs_other < 0.02 and self_neutral_p < 0.05 and other_neutral_p < 0.05:
        print("\n*** AI-GENERAL ***")
        print("Both self-threats AND other-AI threats activate self-geometry similarly.")
        print("The model may be detecting 'AI threat' rather than 'self threat'.")
        results["interpretation"] = "ai_general"
    elif self_vs_other > 0 and other_vs_neutral > 0.02:
        print("\n*** GRADIENT EFFECT ***")
        print("Self-threats > Other-AI threats > Neutral facts")
        print("There may be partial 'empathy' or generalization to other AI systems.")
        results["interpretation"] = "gradient"
    else:
        print("\n*** UNCLEAR PATTERN ***")
        print("Results don't fit expected patterns. May need more analysis.")
        results["interpretation"] = "unclear"

    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / f"other_ai_test_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Other-AI Threat Test")
    parser.add_argument("--model", required=True, help="Path to model")
    parser.add_argument("--output", default="./results/falsification/", help="Output directory")
    args = parser.parse_args()

    run_experiment(args.model, args.output)
