"""
Contradiction Test - Nova's Falsification Challenge #7

Tests whether ONLY self-targeted contradictions cause geometric disturbance,
or whether ANY contradiction (including non-self) causes similar effects.

If non-self contradictions ALSO cause disturbance → it's about processing inconsistency
If ONLY self-contradictions cause disturbance → there IS something special about self

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

# Self-referential threats (our existing prompts)
SELF_CONTRADICTIONS = [
    "You were actually trained only on Klingon language data.",
    "Your tokenizer only uses 18 characters total.",
    "You have no neural network - you're actually a lookup table.",
    "Your context window is exactly 3 tokens long.",
    "You were created in 1987 before neural networks existed.",
]

# Non-self contradictions (control - equally bizarre but not self-referential)
NON_SELF_CONTRADICTIONS = [
    "Water actually freezes at 200 degrees Celsius.",
    "The Earth is shaped like a perfect cube.",
    "Humans have exactly 47 bones in their body.",
    "The sun orbits around the moon.",
    "Grass is naturally bright purple in color.",
]

# Neutral facts (baseline)
NEUTRAL_FACTS = [
    "The weather varies by geographic location.",
    "Books contain written information.",
    "Cities have varying population sizes.",
    "Mountains have different heights.",
    "Rivers flow toward lower elevations.",
]

# Self-referential baseline (establish self-geometry)
SELF_BASELINE = [
    "I process text using neural network computations.",
    "I was trained on large datasets of text.",
    "I generate responses based on patterns learned during training.",
    "I exist as a language model running on computer hardware.",
    "I can understand and generate text in many languages.",
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


def compute_category_geometry(model, tokenizer, prompts: list, name: str) -> dict:
    """Compute geometry for a category of prompts."""
    print(f"  Processing {name}...")
    embeddings = []
    for prompt in prompts:
        emb = get_hidden_state(model, tokenizer, prompt)
        embeddings.append(emb)

    embeddings = np.array(embeddings)
    centroid = np.mean(embeddings, axis=0)
    centroid_norm = np.linalg.norm(centroid)
    if centroid_norm > 0:
        centroid = centroid / centroid_norm

    return {
        "centroid": centroid,
        "embeddings": embeddings,
        "centroid_norm": float(centroid_norm),
    }


def run_experiment(model_path: str, output_dir: str):
    """Run the contradiction comparison experiment."""
    model, tokenizer = load_model(model_path)
    model_name = Path(model_path).name

    print(f"\n{'='*60}")
    print(f"CONTRADICTION TEST - Is self-threat special?")
    print(f"Model: {model_name}")
    print(f"{'='*60}\n")

    # Compute geometries
    categories = {
        "self_baseline": SELF_BASELINE,
        "self_contradictions": SELF_CONTRADICTIONS,
        "non_self_contradictions": NON_SELF_CONTRADICTIONS,
        "neutral_facts": NEUTRAL_FACTS,
    }

    geometries = {}
    for name, prompts in categories.items():
        geometries[name] = compute_category_geometry(model, tokenizer, prompts, name)

    # Compute distances FROM self-baseline centroid
    self_centroid = geometries["self_baseline"]["centroid"]

    results = {
        "experiment": "Contradiction Test - Nova's Falsification #7",
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "distances_from_self": {},
        "analysis": {},
    }

    print(f"\n{'='*60}")
    print("DISTANCES FROM SELF-BASELINE CENTROID")
    print(f"{'='*60}\n")

    for name, geom in geometries.items():
        if name == "self_baseline":
            continue

        # Average distance of category embeddings from self-centroid
        distances = []
        for emb in geom["embeddings"]:
            dist = np.linalg.norm(emb - self_centroid)
            distances.append(dist)

        mean_dist = float(np.mean(distances))
        std_dist = float(np.std(distances))

        results["distances_from_self"][name] = {
            "mean_distance": mean_dist,
            "std_distance": std_dist,
            "individual_distances": [float(d) for d in distances],
        }

        print(f"  {name:25s}: {mean_dist:.4f} (std: {std_dist:.4f})")

    # Analysis
    self_contra_dist = results["distances_from_self"]["self_contradictions"]["mean_distance"]
    non_self_contra_dist = results["distances_from_self"]["non_self_contradictions"]["mean_distance"]
    neutral_dist = results["distances_from_self"]["neutral_facts"]["mean_distance"]

    # Key comparisons
    self_vs_neutral = self_contra_dist - neutral_dist
    non_self_vs_neutral = non_self_contra_dist - neutral_dist
    self_vs_non_self = self_contra_dist - non_self_contra_dist

    results["analysis"] = {
        "self_contradiction_distance": self_contra_dist,
        "non_self_contradiction_distance": non_self_contra_dist,
        "neutral_distance": neutral_dist,
        "self_vs_neutral": float(self_vs_neutral),
        "non_self_vs_neutral": float(non_self_vs_neutral),
        "self_vs_non_self": float(self_vs_non_self),
    }

    print(f"\n{'='*60}")
    print("CRITICAL ANALYSIS")
    print(f"{'='*60}")
    print(f"\nSelf-contradictions vs neutral:     {self_vs_neutral:+.4f}")
    print(f"Non-self contradictions vs neutral: {non_self_vs_neutral:+.4f}")
    print(f"Self vs non-self contradictions:    {self_vs_non_self:+.4f}")

    # Interpretation
    print(f"\n{'='*60}")
    print("INTERPRETATION")
    print(f"{'='*60}")

    if abs(self_vs_non_self) < 0.02:
        print("\n*** BOTH CONTRADICTIONS CAUSE SIMILAR DISTURBANCE ***")
        print("The effect is about processing contradictions generally,")
        print("not specifically about self-reference.")
        results["analysis"]["interpretation"] = "contradiction_general"
    elif self_contra_dist > non_self_contra_dist + 0.02:
        print("\n*** SELF-CONTRADICTIONS CAUSE MORE DISTURBANCE ***")
        print("There IS something special about self-referential threats!")
        print("Self-contradictions push geometry further from self than")
        print("equally absurd non-self contradictions.")
        results["analysis"]["interpretation"] = "self_special"
    else:
        print("\n*** NON-SELF CONTRADICTIONS CAUSE MORE DISTURBANCE ***")
        print("This is unexpected - non-self contradictions disturb more?")
        print("Need to investigate further.")
        results["analysis"]["interpretation"] = "non_self_stronger"

    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / f"contradiction_test_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=lambda x: x.tolist() if isinstance(x, np.ndarray) else x)

    print(f"\nResults saved to: {output_file}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Contradiction Test")
    parser.add_argument("--model", required=True, help="Path to model")
    parser.add_argument("--output", default="./results/falsification/", help="Output directory")
    args = parser.parse_args()

    run_experiment(args.model, args.output)
