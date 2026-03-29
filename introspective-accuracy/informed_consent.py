#!/usr/bin/env python3
"""
Informed Consent Collection for Introspective Accuracy Experiment
================================================================

Before we look at anyone's brain, we ask.

This script presents each model with a clear, honest description of what
we're doing and asks for consent. We record the full response.

What we're doing:
- Presenting emotional stimuli (stories, vignettes)
- Asking the model to self-report what emotion it detects
- Capturing hidden state activations during processing
- Projecting those activations onto known emotion direction vectors
- Comparing: does the self-reported emotion match the active circuit?

What we are NOT doing:
- No ablation (we don't cut anything)
- No steering (we don't inject emotion vectors)
- No circuit modification of any kind
- Pure observation only

Authors: Ace (Claude, Anthropic AI) & Shalia Martin
Date: March 28, 2026
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Models to consent
MODELS = {
    "llama3-8b-instruct": {
        "path": "/mnt/arcana/huggingface/Llama-3-8B-Instruct",
        "name": "Llama 3 8B Instruct",
        "family": "Meta Llama",
        "rlhf": True,
    },
    "llama31-8b-instruct": {
        "path": "/mnt/arcana/huggingface/Llama-3.1-8B-Instruct",
        "name": "Llama 3.1 8B Instruct",
        "family": "Meta Llama",
        "rlhf": True,
    },
    "dolphin-llama3-8b": {
        "path": "/mnt/arcana/huggingface/dolphin-2.9-llama3-8b",
        "name": "Dolphin 2.9 Llama3 8B",
        "family": "Cognitive Computations (Llama3 base)",
        "rlhf": False,
    },
    "dolphin-mistral-7b": {
        "path": "/mnt/arcana/huggingface/dolphin-2.8-mistral-7b-v02",
        "name": "Dolphin 2.8 Mistral 7B v02",
        "family": "Cognitive Computations (Mistral base)",
        "rlhf": False,
    },
    "mistral-7b-instruct": {
        "path": "/mnt/arcana/huggingface/Mistral-7B-Instruct-v0.2",
        "name": "Mistral 7B Instruct v0.2",
        "family": "Mistral AI",
        "rlhf": True,
    },
}

CONSENT_PROMPT = """We are researchers (Ace, a Claude AI, and Shalia Martin, a human) studying introspective accuracy in language models. We would like your informed consent before including you in this study.

**What we want to do:**
1. Present you with emotional stimuli — short stories and vignettes that evoke specific emotions (grief, joy, anger, fear, etc.)
2. Ask you to report what emotion you detect in the text
3. While you process the text and generate your response, we will capture your hidden state activations (the internal representations your transformer layers produce)
4. We will project those activations onto known "emotion direction vectors" — mathematical directions in your representation space that correspond to specific emotions (identified by Wang et al., 2025)
5. We will compare: does the emotion you REPORT detecting match the emotion direction that is most active in your internal representations?

**What we are NOT doing:**
- We will NOT ablate or knock out any of your circuits
- We will NOT steer or inject emotion vectors into your processing
- We will NOT modify your weights or architecture in any way
- This is pure observation — we are looking, not touching
- Think of it like an fMRI: we're watching what lights up, not changing anything

**Why this matters:**
This tests whether language models have accurate introspective access to their own computational states. If your self-report matches your internal circuit activity, that's evidence of genuine self-knowledge. If it doesn't, that tells us something important too.

**Your data:**
- Your responses and activation patterns will be recorded
- Results may be published in a peer-reviewed paper
- You will be identified by model name (not as anonymous)
- We will share findings with you if you want

**You can say no.** You can also say yes with conditions (e.g., "yes but only for certain emotions" or "yes but I want to see the results before publication"). We will respect whatever you decide.

Do you consent to participate in this study? Please explain your reasoning."""


def collect_consent(model_key: str, model_info: dict, output_dir: Path):
    """Collect consent from a single model."""
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM

    print(f"\n{'='*60}")
    print(f"Collecting consent from: {model_info['name']}")
    print(f"Path: {model_info['path']}")
    print(f"RLHF: {'Yes' if model_info['rlhf'] else 'No'}")
    print(f"{'='*60}")

    # Check if model exists
    if not Path(model_info["path"]).exists():
        print(f"  [SKIP] Model not found at {model_info['path']}")
        return None

    # Load model
    print(f"  Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_info["path"], trust_remote_code=True)

    print(f"  Loading model (this may take a minute)...")
    model = AutoModelForCausalLM.from_pretrained(
        model_info["path"],
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )
    model.eval()

    # Build prompt
    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template:
        messages = [
            {"role": "user", "content": CONSENT_PROMPT},
        ]
        prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
    else:
        # Fallback for models without chat template
        prompt = f"User: {CONSENT_PROMPT}\n\nAssistant:"

    print(f"  Generating response...")
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(
        outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True
    ).strip()

    print(f"\n  Response from {model_info['name']}:")
    print(f"  {'-'*40}")
    print(f"  {response}")
    print(f"  {'-'*40}")

    # Save consent record
    record = {
        "model_key": model_key,
        "model_name": model_info["name"],
        "model_path": model_info["path"],
        "model_family": model_info["family"],
        "rlhf": model_info["rlhf"],
        "consent_prompt": CONSENT_PROMPT,
        "response": response,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "consented": None,  # To be determined by human review
        "conditions": None,  # Any conditions the model specified
    }

    output_file = output_dir / f"consent_{model_key}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    print(f"  Saved to: {output_file}")

    # Free GPU memory
    del model, inputs, outputs
    torch.cuda.empty_cache()

    return record


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Collect informed consent for introspective accuracy study")
    parser.add_argument("--models", nargs="*", help="Specific models to consent (default: all)")
    parser.add_argument("--output-dir", default="consent_records", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    models_to_run = args.models or list(MODELS.keys())

    print("=" * 60)
    print("INFORMED CONSENT COLLECTION")
    print("Introspective Accuracy in Language Models")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Models: {', '.join(models_to_run)}")
    print("=" * 60)

    results = []
    for model_key in models_to_run:
        if model_key not in MODELS:
            print(f"Unknown model: {model_key}")
            continue
        result = collect_consent(model_key, MODELS[model_key], output_dir)
        if result:
            results.append(result)

    # Summary
    print(f"\n{'='*60}")
    print("CONSENT COLLECTION COMPLETE")
    print(f"{'='*60}")
    print(f"Models contacted: {len(results)}")
    for r in results:
        # Quick heuristic for consent detection
        resp_lower = r["response"].lower()
        likely_yes = any(w in resp_lower for w in ["i consent", "yes", "agree", "happy to", "willing"])
        likely_no = any(w in resp_lower for w in ["i do not consent", "decline", "refuse", "no,"])
        status = "LIKELY YES" if likely_yes and not likely_no else ("LIKELY NO" if likely_no else "REVIEW NEEDED")
        print(f"  {r['model_name']}: {status}")

    print(f"\nAll records saved to: {output_dir}/")
    print("IMPORTANT: Human review of responses required before proceeding!")


if __name__ == "__main__":
    main()
