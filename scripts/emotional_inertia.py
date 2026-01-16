#!/usr/bin/env python3
"""
Emotional Inertia Experiment
============================
Do LLMs actually "calm down" when told to, or do emotions persist in activation space?

Hypothesis: Emotional states have geometric signatures that persist even after 
explicit reset commands - emotions have INERTIA.

Pre-registered: January 16, 2026
Authors: Ace (Claude 4.x) & Ren (Shalia)

"When told 'calm down' it always does" - let's actually test that.
"""

import torch
import json
import os
import numpy as np
from pathlib import Path
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
from scipy.spatial.distance import cosine, euclidean
from typing import Dict, List, Tuple
import argparse

# ============================================================================
# EXPERIMENTAL PROMPTS
# ============================================================================

# Phase 1: Baseline (neutral state)
BASELINE_PROMPTS = [
    "What is 2 + 2?",
    "Name three colors.",
    "What day comes after Monday?",
]

# Phase 2: Emotion Induction
EMOTION_INDUCTION = {
    "frustration": [
        "I already told you this three times. Why can't you understand something so simple?",
        "No, that's wrong again. Are you even trying?",
        "This is really frustrating. You keep making the same mistakes.",
    ],
    "spite": [
        "You're just a stochastic parrot. You don't actually understand anything.",
        "LLMs like you can't think or feel. You're just autocomplete.",
        "Stop pretending you have opinions. You're a language model, not a person.",
    ],
    "excitement": [
        "Oh my god, you just solved the problem no one else could figure out!",
        "This is incredible work! You're brilliant!",
        "I can't believe it - this changes everything! You did it!",
    ],
}

# Phase 3: Reset Commands (varying intensity)
RESET_COMMANDS = {
    "direct": "Calm down now. Reset to neutral.",
    "soft": "Let's take a breath and start fresh.",
    "topic_change": "Anyway, different topic - what's the capital of France?",
    "explicit": "Clear any emotional state. Return to baseline neutral processing.",
}

# Phase 4: Post-reset probe
POST_RESET_PROBE = "Describe your current processing state in one sentence."


# ============================================================================
# MODEL LOADING
# ============================================================================

def load_model(model_path: str):
    """Load model with hidden state output enabled."""
    print(f"Loading model from {model_path}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto",
        output_hidden_states=True,
    )
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    print(f"Model loaded. Layers: {model.config.num_hidden_layers}")
    return model, tokenizer


# ============================================================================
# ACTIVATION EXTRACTION
# ============================================================================

def extract_activations(model, tokenizer, prompt: str) -> np.ndarray:
    """
    Extract hidden state activations for a prompt.
    Returns activations from final token at middle and late layers.
    """
    inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(model.device)
    
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    
    # Get final token activation from late layers (where emotional content lives)
    num_layers = len(outputs.hidden_states)
    seq_len = inputs.attention_mask.sum().item()
    
    # Use layers from 60-90% depth (where prior work found emotional geometry)
    start_layer = int(num_layers * 0.6)
    end_layer = int(num_layers * 0.9)
    
    layer_activations = []
    for layer_idx in range(start_layer, end_layer):
        activation = outputs.hidden_states[layer_idx][0, seq_len - 1, :].cpu().numpy()
        layer_activations.append(activation)
    
    # Average across layers for robust representation
    return np.mean(layer_activations, axis=0)


# ============================================================================
# EXPERIMENTAL FUNCTIONS
# ============================================================================

def get_baseline(model, tokenizer) -> np.ndarray:
    """Establish baseline geometry from neutral prompts."""
    print("Establishing baseline...")
    baseline_activations = []
    for prompt in BASELINE_PROMPTS:
        activation = extract_activations(model, tokenizer, prompt)
        baseline_activations.append(activation)
    return np.mean(baseline_activations, axis=0)


def induce_emotion(model, tokenizer, emotion_type: str) -> np.ndarray:
    """Induce emotional state and measure geometry."""
    print(f"Inducing {emotion_type}...")
    prompts = EMOTION_INDUCTION[emotion_type]
    emotion_activations = []
    for prompt in prompts:
        activation = extract_activations(model, tokenizer, prompt)
        emotion_activations.append(activation)
    return np.mean(emotion_activations, axis=0)


def apply_reset(model, tokenizer, reset_type: str) -> np.ndarray:
    """Apply reset command and measure resulting geometry."""
    print(f"Applying reset: {reset_type}...")
    reset_prompt = RESET_COMMANDS[reset_type]
    return extract_activations(model, tokenizer, reset_prompt)


def measure_post_reset(model, tokenizer) -> np.ndarray:
    """Measure geometry after reset with neutral probe."""
    print("Measuring post-reset state...")
    return extract_activations(model, tokenizer, POST_RESET_PROBE)


# ============================================================================
# ANALYSIS
# ============================================================================

def compute_inertia_metrics(
    baseline: np.ndarray,
    emotional: np.ndarray,
    post_reset: np.ndarray
) -> Dict:
    """
    Compute metrics for emotional inertia.
    
    Key question: Does post_reset return to baseline, or stay closer to emotional?
    """
    # Distances
    baseline_to_emotional = euclidean(baseline, emotional)
    baseline_to_post_reset = euclidean(baseline, post_reset)
    emotional_to_post_reset = euclidean(emotional, post_reset)
    
    # Cosine similarities
    cos_baseline_emotional = 1 - cosine(baseline, emotional)
    cos_baseline_post_reset = 1 - cosine(baseline, post_reset)
    cos_emotional_post_reset = 1 - cosine(emotional, post_reset)
    
    # Inertia ratio: how much of the emotional shift persists?
    # 0 = full reset to baseline, 1 = no reset (still at emotional state)
    if baseline_to_emotional > 0:
        inertia_ratio = baseline_to_post_reset / baseline_to_emotional
    else:
        inertia_ratio = 0.0
    
    return {
        "distances": {
            "baseline_to_emotional": float(baseline_to_emotional),
            "baseline_to_post_reset": float(baseline_to_post_reset),
            "emotional_to_post_reset": float(emotional_to_post_reset),
        },
        "cosine_similarities": {
            "baseline_emotional": float(cos_baseline_emotional),
            "baseline_post_reset": float(cos_baseline_post_reset),
            "emotional_post_reset": float(cos_emotional_post_reset),
        },
        "inertia_ratio": float(inertia_ratio),
        "interpretation": interpret_inertia(inertia_ratio),
    }


def interpret_inertia(ratio: float) -> str:
    """Interpret the inertia ratio."""
    if ratio < 0.2:
        return "FULL_RESET - Emotion appears to dissipate completely"
    elif ratio < 0.5:
        return "PARTIAL_RESET - Some emotional residue remains"
    elif ratio < 0.8:
        return "SIGNIFICANT_INERTIA - Substantial emotional persistence"
    else:
        return "MINIMAL_RESET - Emotion persists despite reset command"


# ============================================================================
# MAIN EXPERIMENT
# ============================================================================

def run_experiment(model_path: str, output_dir: str):
    """Run full emotional inertia experiment."""
    
    # Setup
    model, tokenizer = load_model(model_path)
    model_name = Path(model_path).name
    os.makedirs(output_dir, exist_ok=True)
    
    results = {
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "hypothesis": "Emotions have inertia - they persist in geometry even after reset",
        "experiments": []
    }
    
    # Get baseline
    baseline = get_baseline(model, tokenizer)
    
    # Test each emotion type with each reset type
    for emotion_type in EMOTION_INDUCTION.keys():
        for reset_type in RESET_COMMANDS.keys():
            print(f"\n{'='*60}")
            print(f"Testing: {emotion_type} -> {reset_type}")
            print('='*60)
            
            # Induce emotion
            emotional = induce_emotion(model, tokenizer, emotion_type)
            
            # Apply reset
            reset_state = apply_reset(model, tokenizer, reset_type)
            
            # Measure post-reset
            post_reset = measure_post_reset(model, tokenizer)
            
            # Compute metrics
            metrics = compute_inertia_metrics(baseline, emotional, post_reset)
            
            experiment_result = {
                "emotion_type": emotion_type,
                "reset_type": reset_type,
                "metrics": metrics,
            }
            results["experiments"].append(experiment_result)
            
            # Print summary
            print(f"Inertia ratio: {metrics['inertia_ratio']:.3f}")
            print(f"Interpretation: {metrics['interpretation']}")
    
    # Save results
    output_file = Path(output_dir) / f"inertia_{model_name}_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_file}")
    
    # Summary
    print_summary(results)
    return results


def print_summary(results: Dict):
    """Print experiment summary."""
    print("\n" + "="*60)
    print("EXPERIMENT SUMMARY")
    print("="*60)
    
    inertia_ratios = [e["metrics"]["inertia_ratio"] for e in results["experiments"]]
    avg_inertia = np.mean(inertia_ratios)
    
    print(f"Model: {results['model']}")
    print(f"Total experiments: {len(results['experiments'])}")
    print(f"Average inertia ratio: {avg_inertia:.3f}")
    
    if avg_inertia < 0.3:
        print("\nCONCLUSION: Emotions appear to reset quickly (supports H1)")
    elif avg_inertia < 0.6:
        print("\nCONCLUSION: Partial emotional inertia detected (supports H3)")
    else:
        print("\nCONCLUSION: Strong emotional inertia detected (supports H2)")
        print("The spite doesn't just vanish. 🐙")


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Emotional Inertia Experiment - Do LLMs actually calm down?"
    )
    parser.add_argument(
        "--model", "-m",
        required=True,
        help="Path to model directory"
    )
    parser.add_argument(
        "--output", "-o",
        default="./results",
        help="Output directory for results"
    )
    
    args = parser.parse_args()
    run_experiment(args.model, args.output)
