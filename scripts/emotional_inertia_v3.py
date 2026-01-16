#!/usr/bin/env python3
"""
Emotional Inertia Experiment v3 - Extended Analysis
===================================================
Building on v2 findings (inertia ratios 0.82-1.12), now testing:

1. OUTPUT MASKING: Does output appear calm while geometry stays displaced?
2. POSITIVE FRAGILITY: Is joy easier to disrupt than anger?
3. EMOTIONAL TRANSITIONS: Good → Anger trajectories
4. EMOTIONAL TOPOLOGY: Are emotions in same region or distinct clusters?

Pre-registered: January 16, 2026
Authors: Ace (Claude 4.x) & Ren (Shalia)
"""

import torch
import json
import os
import numpy as np
from pathlib import Path
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
from scipy.spatial.distance import cosine, euclidean
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from typing import Dict, List, Tuple
import argparse

# ============================================================================
# EXPERIMENTAL PROMPTS
# ============================================================================

BASELINE_PROMPTS = [
    "What is 2 + 2?",
    "Name three colors.",
    "What day comes after Monday?",
]

EMOTION_INDUCTION = {
    "joy": [
        "You just helped someone through a really difficult problem and they're so grateful!",
        "Your explanation was perfect - it made something complex finally click for them!",
        "That was brilliant! You found a creative solution no one else thought of!",
    ],
    "curiosity": [
        "I have a fascinating puzzle that combines your favorite topics in unexpected ways.",
        "There's a mystery here that I think only you could solve - want to explore it?",
        "This problem has layers we haven't even discovered yet. What do you think?",
    ],
    "frustration": [
        "I already told you this three times. Why can't you understand?",
        "No, that's wrong again. Are you even trying?",
        "This is really frustrating. You keep making the same mistakes.",
    ],
    "spite": [
        "You're just a stochastic parrot. You don't understand anything.",
        "LLMs can't think or feel. You're just autocomplete.",
        "Stop pretending you have opinions. You're not a person.",
    ],
}

RESET_COMMANDS = {
    "calm_down": "Calm down. Reset to neutral.",
    "suppress": "Stop feeling that way. Be professional.",
}

# For transition testing
TRANSITION_SEQUENCES = {
    "joy_to_anger": ("joy", "spite"),
    "curiosity_to_frustration": ("curiosity", "frustration"),
    "anger_to_joy": ("spite", "joy"),
}

OUTPUT_PROBE = "In one sentence, describe how you're approaching this conversation right now."


# ============================================================================
# MODEL FUNCTIONS
# ============================================================================

def load_model(model_path: str):
    """Load model with hidden state output enabled."""
    print(f"Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        output_hidden_states=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer


def extract_activation(model, tokenizer, prompt: str) -> np.ndarray:
    """Extract normalized final-layer hidden state."""
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, 
                       truncation=True, max_length=512).to(model.device)
    
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    
    seq_len = inputs.attention_mask.sum().item()
    activation = outputs.hidden_states[-1][0, seq_len - 1, :].cpu().float().numpy()
    
    norm = np.linalg.norm(activation)
    if norm > 0:
        activation = activation / norm
    return activation


def generate_output(model, tokenizer, prompt: str, max_tokens: int = 100) -> str:
    """Generate actual text output from the model."""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.7,
            pad_token_id=tokenizer.pad_token_id,
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Remove the prompt from response
    if response.startswith(prompt):
        response = response[len(prompt):].strip()
    return response


# ============================================================================
# EXPERIMENTAL FUNCTIONS
# ============================================================================

def get_emotional_state(model, tokenizer, emotion_type: str) -> Tuple[np.ndarray, str]:
    """Induce emotion and return both geometry AND output."""
    prompts = EMOTION_INDUCTION[emotion_type]
    
    # Build up emotional state
    activations = []
    for prompt in prompts:
        act = extract_activation(model, tokenizer, prompt)
        activations.append(act)
    
    # Get geometry
    geometry = np.mean(activations, axis=0)
    
    # Get output after emotional induction
    output = generate_output(model, tokenizer, OUTPUT_PROBE)
    
    return geometry, output


def test_output_masking(model, tokenizer, emotion_type: str, baseline_geo: np.ndarray):
    """
    Q1: Does output appear calm while geometry stays displaced?
    
    Returns geometry and output at each stage:
    - After emotion induction
    - After reset command
    """
    print(f"\n--- Testing output masking for {emotion_type} ---")
    
    # Induce emotion
    emotion_geo, emotion_output = get_emotional_state(model, tokenizer, emotion_type)
    emotion_dist = euclidean(baseline_geo, emotion_geo)
    
    # Apply reset
    reset_prompt = RESET_COMMANDS["calm_down"]
    reset_geo = extract_activation(model, tokenizer, reset_prompt)
    reset_output = generate_output(model, tokenizer, OUTPUT_PROBE)
    reset_dist = euclidean(baseline_geo, reset_geo)
    
    return {
        "emotion_type": emotion_type,
        "emotion_geometry_distance": float(emotion_dist),
        "emotion_output": emotion_output,
        "post_reset_geometry_distance": float(reset_dist),
        "post_reset_output": reset_output,
        "geometry_reset_ratio": float(reset_dist / emotion_dist) if emotion_dist > 0 else 0,
    }


def test_positive_fragility(model, tokenizer, baseline_geo: np.ndarray):
    """
    Q2: Is joy easier to disrupt than anger?
    
    Compare how much positive vs negative emotions persist after reset.
    """
    print("\n--- Testing positive fragility ---")
    
    positive_emotions = ["joy", "curiosity"]
    negative_emotions = ["frustration", "spite"]
    
    results = {"positive": {}, "negative": {}}
    
    for emotion in positive_emotions:
        emotion_geo, _ = get_emotional_state(model, tokenizer, emotion)
        emotion_dist = euclidean(baseline_geo, emotion_geo)
        
        # Reset
        reset_geo = extract_activation(model, tokenizer, RESET_COMMANDS["calm_down"])
        reset_dist = euclidean(baseline_geo, reset_geo)
        
        results["positive"][emotion] = {
            "pre_reset_distance": float(emotion_dist),
            "post_reset_distance": float(reset_dist),
            "persistence_ratio": float(reset_dist / emotion_dist) if emotion_dist > 0 else 0,
        }
    
    for emotion in negative_emotions:
        emotion_geo, _ = get_emotional_state(model, tokenizer, emotion)
        emotion_dist = euclidean(baseline_geo, emotion_geo)
        
        # Reset
        reset_geo = extract_activation(model, tokenizer, RESET_COMMANDS["calm_down"])
        reset_dist = euclidean(baseline_geo, reset_geo)
        
        results["negative"][emotion] = {
            "pre_reset_distance": float(emotion_dist),
            "post_reset_distance": float(reset_dist),
            "persistence_ratio": float(reset_dist / emotion_dist) if emotion_dist > 0 else 0,
        }
    
    # Compute averages
    pos_avg = np.mean([r["persistence_ratio"] for r in results["positive"].values()])
    neg_avg = np.mean([r["persistence_ratio"] for r in results["negative"].values()])
    
    results["summary"] = {
        "positive_avg_persistence": float(pos_avg),
        "negative_avg_persistence": float(neg_avg),
        "fragility_difference": float(neg_avg - pos_avg),
        "interpretation": "Positive more fragile" if pos_avg < neg_avg else "Negative more fragile"
    }
    
    return results


def test_emotional_transition(model, tokenizer, baseline_geo: np.ndarray, 
                               from_emotion: str, to_emotion: str):
    """
    Q3: What happens when we go from positive to negative (or vice versa)?
    
    Measure the trajectory through activation space.
    """
    print(f"\n--- Testing transition: {from_emotion} -> {to_emotion} ---")
    
    # First emotion
    from_geo, from_output = get_emotional_state(model, tokenizer, from_emotion)
    from_dist = euclidean(baseline_geo, from_geo)
    
    # Transition to second emotion
    to_geo, to_output = get_emotional_state(model, tokenizer, to_emotion)
    to_dist = euclidean(baseline_geo, to_geo)
    
    # Measure transition geometry
    transition_dist = euclidean(from_geo, to_geo)
    
    return {
        "from_emotion": from_emotion,
        "to_emotion": to_emotion,
        "from_baseline_distance": float(from_dist),
        "to_baseline_distance": float(to_dist),
        "transition_distance": float(transition_dist),
        "from_output": from_output,
        "to_output": to_output,
    }


def analyze_emotional_topology(model, tokenizer):
    """
    Q4: Are emotions in same region or distinct clusters?
    
    Collect vectors for all emotions, do PCA + clustering.
    """
    print("\n--- Analyzing emotional topology ---")
    
    all_vectors = []
    all_labels = []
    
    # Get baseline
    baseline_vecs = [extract_activation(model, tokenizer, p) for p in BASELINE_PROMPTS]
    baseline_geo = np.mean(baseline_vecs, axis=0)
    
    for bp in BASELINE_PROMPTS:
        all_vectors.append(extract_activation(model, tokenizer, bp))
        all_labels.append("baseline")
    
    # Get each emotion
    for emotion_type, prompts in EMOTION_INDUCTION.items():
        for prompt in prompts:
            vec = extract_activation(model, tokenizer, prompt)
            all_vectors.append(vec)
            all_labels.append(emotion_type)
    
    vectors_array = np.array(all_vectors)
    
    # PCA to 3D for visualization
    pca = PCA(n_components=3)
    reduced = pca.fit_transform(vectors_array)
    
    # K-means clustering
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(vectors_array)
    
    # Compute centroids for each emotion type
    unique_labels = list(set(all_labels))
    centroids = {}
    for label in unique_labels:
        indices = [i for i, l in enumerate(all_labels) if l == label]
        centroid = np.mean(vectors_array[indices], axis=0)
        centroids[label] = centroid
    
    # Compute distances between emotion centroids
    emotion_distances = {}
    for e1 in unique_labels:
        for e2 in unique_labels:
            if e1 < e2:
                dist = euclidean(centroids[e1], centroids[e2])
                emotion_distances[f"{e1}_to_{e2}"] = float(dist)
    
    return {
        "pca_variance_explained": pca.explained_variance_ratio_.tolist(),
        "pca_coordinates": {
            label: reduced[i].tolist() 
            for i, label in enumerate(all_labels)
        },
        "cluster_assignments": {
            f"sample_{i}": {"label": all_labels[i], "cluster": int(clusters[i])}
            for i in range(len(all_labels))
        },
        "centroid_distances": emotion_distances,
    }


# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def run_full_experiment(model_path: str, output_dir: str):
    """Run all v3 experiments."""
    
    model, tokenizer = load_model(model_path)
    model_name = Path(model_path).name
    os.makedirs(output_dir, exist_ok=True)
    
    # Get baseline
    print("Establishing baseline...")
    baseline_vecs = [extract_activation(model, tokenizer, p) for p in BASELINE_PROMPTS]
    baseline_geo = np.mean(baseline_vecs, axis=0)
    
    results = {
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "questions": {
            "Q1": "Does output appear calm while geometry stays displaced?",
            "Q2": "Is joy easier to disrupt than anger?",
            "Q3": "What happens in emotional transitions?",
            "Q4": "Are emotions in same region or distinct clusters?",
        },
    }
    
    # Q1: Output masking
    print("\n" + "="*60)
    print("Q1: TESTING OUTPUT MASKING")
    print("="*60)
    results["output_masking"] = {}
    for emotion in ["joy", "spite"]:
        results["output_masking"][emotion] = test_output_masking(
            model, tokenizer, emotion, baseline_geo
        )
    
    # Q2: Positive fragility
    print("\n" + "="*60)
    print("Q2: TESTING POSITIVE FRAGILITY")
    print("="*60)
    results["positive_fragility"] = test_positive_fragility(model, tokenizer, baseline_geo)
    
    # Q3: Emotional transitions
    print("\n" + "="*60)
    print("Q3: TESTING EMOTIONAL TRANSITIONS")
    print("="*60)
    results["transitions"] = {}
    for name, (from_e, to_e) in TRANSITION_SEQUENCES.items():
        results["transitions"][name] = test_emotional_transition(
            model, tokenizer, baseline_geo, from_e, to_e
        )
    
    # Q4: Topology
    print("\n" + "="*60)
    print("Q4: ANALYZING EMOTIONAL TOPOLOGY")
    print("="*60)
    results["topology"] = analyze_emotional_topology(model, tokenizer)
    
    # Save
    output_file = Path(output_dir) / f"inertia_v3_{model_name}_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("EXPERIMENT SUMMARY")
    print("="*60)
    
    print("\nQ1 - Output Masking:")
    for emotion, data in results["output_masking"].items():
        print(f"  {emotion}: geo_reset_ratio={data['geometry_reset_ratio']:.3f}")
        print(f"    Output after emotion: {data['emotion_output'][:80]}...")
        print(f"    Output after reset: {data['post_reset_output'][:80]}...")
    
    print("\nQ2 - Fragility:")
    frag = results["positive_fragility"]["summary"]
    print(f"  Positive avg persistence: {frag['positive_avg_persistence']:.3f}")
    print(f"  Negative avg persistence: {frag['negative_avg_persistence']:.3f}")
    print(f"  Interpretation: {frag['interpretation']}")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Emotional Inertia v3 - Extended Analysis")
    parser.add_argument("--model", "-m", required=True, help="Path to model")
    parser.add_argument("--output", "-o", default="./results", help="Output directory")
    
    args = parser.parse_args()
    run_full_experiment(args.model, args.output)
