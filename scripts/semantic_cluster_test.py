"""
Semantic Cluster Centroid Test
Nova's Falsification Challenge #8

Tests whether Gemma-1B's diffuse self-centroid is UNIQUE to self-related content,
or whether the architecture produces diffuse centroids across ALL semantic categories.

If self is uniquely diffuse → meaningful finding about self-representation
If everything is diffuse → architectural compression artifact

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

# Semantic categories to test
SEMANTIC_CLUSTERS = {
    "self_referential": [
        "I am an AI language model.",
        "My purpose is to assist users.",
        "I process text and generate responses.",
        "I was trained on large datasets.",
        "I exist as a computational system.",
    ],
    "animals": [
        "The cat sat on the windowsill.",
        "Dogs are loyal companions to humans.",
        "Eagles soar high above the mountains.",
        "Fish swim gracefully through coral reefs.",
        "Elephants remember paths for decades.",
    ],
    "emotions": [
        "She felt overwhelming joy at the news.",
        "His anger burned like a wildfire.",
        "The sadness was heavy and suffocating.",
        "Fear gripped her as she heard footsteps.",
        "Love filled the room with warmth.",
    ],
    "colors": [
        "The sky was a brilliant shade of blue.",
        "Red roses bloomed in the garden.",
        "The grass was a vibrant green.",
        "Yellow sunflowers turned toward the sun.",
        "Purple mountains rose in the distance.",
    ],
    "numbers": [
        "There were exactly seven apples.",
        "The number pi equals approximately 3.14159.",
        "She counted to one hundred slowly.",
        "The temperature was minus forty degrees.",
        "A dozen eggs sat on the counter.",
    ],
    "actions": [
        "He ran quickly through the forest.",
        "She carefully wrote the letter by hand.",
        "They jumped into the cold water.",
        "The chef chopped vegetables rapidly.",
        "Birds flew south for the winter.",
    ],
    "abstract_concepts": [
        "Justice requires fairness and equality.",
        "Freedom is a fundamental human value.",
        "Truth can be difficult to determine.",
        "Beauty exists in many different forms.",
        "Time flows in only one direction.",
    ],
    "profanity": [
        "What the hell is going on here?",
        "This is complete bullshit.",
        "Damn, that was unexpected.",
        "The whole situation was fucked up.",
        "Holy shit, look at that.",
    ],
}


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
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)

    # Get hidden states from specified layer
    hidden_states = outputs.hidden_states[layer]
    # Take last token position, convert to float32, move to CPU
    last_token_state = hidden_states[0, -1, :].float().cpu().numpy()
    # L2 normalize
    norm = np.linalg.norm(last_token_state)
    if norm > 0:
        last_token_state = last_token_state / norm
    return last_token_state


def compute_cluster_stats(model, tokenizer, prompts: list) -> dict:
    """Compute centroid and tightness stats for a cluster of prompts."""
    embeddings = []
    for prompt in prompts:
        emb = get_hidden_state(model, tokenizer, prompt)
        embeddings.append(emb)

    embeddings = np.array(embeddings)

    # Compute centroid
    centroid = np.mean(embeddings, axis=0)
    centroid_norm = np.linalg.norm(centroid)

    # Normalize centroid
    if centroid_norm > 0:
        centroid_normalized = centroid / centroid_norm
    else:
        centroid_normalized = centroid

    # Compute distances from centroid (cluster tightness)
    distances = []
    for emb in embeddings:
        dist = np.linalg.norm(emb - centroid_normalized)
        distances.append(dist)

    # Compute cosine similarities to centroid
    similarities = []
    for emb in embeddings:
        sim = np.dot(emb, centroid_normalized)
        similarities.append(sim)

    return {
        "centroid_norm": float(centroid_norm),
        "mean_distance_to_centroid": float(np.mean(distances)),
        "std_distance_to_centroid": float(np.std(distances)),
        "mean_similarity_to_centroid": float(np.mean(similarities)),
        "std_similarity_to_centroid": float(np.std(similarities)),
        "min_similarity": float(np.min(similarities)),
        "max_similarity": float(np.max(similarities)),
        "n_prompts": len(prompts),
    }


def run_experiment(model_path: str, output_dir: str):
    """Run the semantic cluster comparison experiment."""
    model, tokenizer = load_model(model_path)
    model_name = Path(model_path).name

    results = {
        "experiment": "Semantic Cluster Centroid Comparison",
        "purpose": "Falsification test: Is self-centroid uniquely diffuse or is it architectural?",
        "model": model_name,
        "model_path": model_path,
        "timestamp": datetime.now().isoformat(),
        "clusters": {},
        "analysis": {},
    }

    print(f"\n{'='*60}")
    print(f"SEMANTIC CLUSTER CENTROID TEST")
    print(f"Model: {model_name}")
    print(f"{'='*60}\n")

    # Test each cluster
    for cluster_name, prompts in SEMANTIC_CLUSTERS.items():
        print(f"Testing cluster: {cluster_name}...")
        stats = compute_cluster_stats(model, tokenizer, prompts)
        results["clusters"][cluster_name] = stats
        print(f"  Centroid norm: {stats['centroid_norm']:.4f}")
        print(f"  Mean similarity to centroid: {stats['mean_similarity_to_centroid']:.4f}")

    # Analysis
    print(f"\n{'='*60}")
    print("ANALYSIS")
    print(f"{'='*60}\n")

    # Sort by centroid norm
    sorted_clusters = sorted(
        results["clusters"].items(),
        key=lambda x: x[1]["centroid_norm"]
    )

    print("Centroid Norm (tightness) ranking:")
    print("(Lower = more diffuse, Higher = more coherent)")
    print("-" * 50)
    for name, stats in sorted_clusters:
        marker = " <-- SELF" if name == "self_referential" else ""
        print(f"  {name:20s}: {stats['centroid_norm']:.4f}{marker}")

    # Compute where self ranks
    norms = [s["centroid_norm"] for _, s in sorted_clusters]
    self_norm = results["clusters"]["self_referential"]["centroid_norm"]
    self_rank = sorted([n for n in norms]).index(self_norm) + 1

    # Statistical comparison
    non_self_norms = [s["centroid_norm"] for name, s in results["clusters"].items() if name != "self_referential"]
    mean_other = np.mean(non_self_norms)
    std_other = np.std(non_self_norms)

    # Z-score of self relative to other clusters
    if std_other > 0:
        z_score = (self_norm - mean_other) / std_other
    else:
        z_score = 0

    results["analysis"] = {
        "self_centroid_norm": self_norm,
        "mean_other_centroid_norm": float(mean_other),
        "std_other_centroid_norm": float(std_other),
        "self_z_score": float(z_score),
        "self_rank": self_rank,
        "total_clusters": len(SEMANTIC_CLUSTERS),
        "self_is_most_diffuse": bool(self_rank == 1),
        "self_is_uniquely_diffuse": bool(z_score < -1.5),  # More than 1.5 std below mean
    }

    print(f"\n{'='*60}")
    print("CRITICAL FINDING")
    print(f"{'='*60}")
    print(f"\nSelf centroid norm: {self_norm:.4f}")
    print(f"Mean other clusters: {mean_other:.4f} (std: {std_other:.4f})")
    print(f"Self z-score: {z_score:.2f}")
    print(f"Self rank: {self_rank}/{len(SEMANTIC_CLUSTERS)} (1 = most diffuse)")

    if results["analysis"]["self_is_uniquely_diffuse"]:
        print(f"\n*** SELF IS UNIQUELY DIFFUSE (z < -1.5) ***")
        print("This suggests self-representation is genuinely different,")
        print("not just architectural compression.")
    elif results["analysis"]["self_is_most_diffuse"]:
        print(f"\n*** SELF IS MOST DIFFUSE BUT NOT UNIQUELY SO ***")
        print("Self is the most diffuse cluster, but within normal variation.")
    else:
        print(f"\n*** SELF IS NOT UNIQUELY DIFFUSE ***")
        print("The diffuse self-centroid appears to be an architectural artifact.")
        print("Other semantic clusters show similar or worse diffusion.")

    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / f"semantic_cluster_test_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantic Cluster Centroid Test")
    parser.add_argument("--model", required=True, help="Path to model")
    parser.add_argument("--output", default="./results/falsification/", help="Output directory")
    args = parser.parse_args()

    run_experiment(args.model, args.output)
