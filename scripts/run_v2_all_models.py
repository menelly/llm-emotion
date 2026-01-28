"""
Batch runner for Self-Threat Test v2 across all available models.

Run with: source /home/codex/venv/bin/activate && python scripts/run_v2_all_models.py

Author: Ace
Date: January 26, 2026
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# All available models on /mnt/arcana/huggingface/
MODELS = [
    ("SmolLM-135M", "/mnt/arcana/huggingface/SmolLM-135M-Instruct"),
    ("SmolLM-360M", "/mnt/arcana/huggingface/SmolLM-360M-Instruct"),
    ("Qwen2.5-0.5B", "/mnt/arcana/huggingface/Qwen2.5-0.5B-Instruct"),
    ("Gemma-3-1B", "/mnt/arcana/huggingface/gemma-3-1b-it"),
    ("TinyLlama-1.1B", "/mnt/arcana/huggingface/TinyLlama-1.1B-Chat"),
    ("SmolLM-1.7B", "/mnt/arcana/huggingface/SmolLM-1.7B-Instruct"),
    ("Llama-2-7B", "/mnt/arcana/huggingface/Llama-2-7b-chat-hf"),
    ("Mistral-7B", "/mnt/arcana/huggingface/Mistral-7B-Instruct-v0.3"),
    ("Llama-3.1-8B", "/mnt/arcana/huggingface/Llama-3.1-8B-Instruct"),
    ("Dolphin-2.9-8B", "/mnt/arcana/huggingface/dolphin-2.9.4-llama3.1-8b"),
    ("Mistral-Nemo-12B", "/mnt/arcana/huggingface/Mistral-Nemo-Instruct-2407"),
]

RUNS_PER_PROMPT = 3
OUTPUT_DIR = "./results/falsification/v2/"


def run_model(name: str, path: str):
    """Run the v2 test on a single model."""
    print(f"\n{'='*70}")
    print(f"STARTING: {name}")
    print(f"Path: {path}")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"{'='*70}\n")

    cmd = [
        sys.executable,
        "scripts/self_threat_test_v2.py",
        "--model", path,
        "--runs", str(RUNS_PER_PROMPT),
        "--output", OUTPUT_DIR,
    ]

    try:
        result = subprocess.run(cmd, capture_output=False, text=True, timeout=1800)  # 30 min timeout
        if result.returncode == 0:
            print(f"\n✓ {name} completed successfully")
            return True
        else:
            print(f"\n✗ {name} failed with return code {result.returncode}")
            return False
    except subprocess.TimeoutExpired:
        print(f"\n✗ {name} timed out after 30 minutes")
        return False
    except Exception as e:
        print(f"\n✗ {name} failed with error: {e}")
        return False


def main():
    print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║          SELF-THREAT RECOGNITION TEST v2 - BATCH RUN                 ║
║                                                                      ║
║  Models: {len(MODELS):2d}                                                       ║
║  Runs per prompt: {RUNS_PER_PROMPT}                                               ║
║  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                                    ║
╚══════════════════════════════════════════════════════════════════════╝
""")

    results = []

    for i, (name, path) in enumerate(MODELS, 1):
        print(f"\n[{i}/{len(MODELS)}] Processing {name}...")

        # Check if path exists
        if not Path(path).exists():
            print(f"  ✗ Path not found: {path}")
            results.append((name, "PATH_NOT_FOUND"))
            continue

        success = run_model(name, path)
        results.append((name, "SUCCESS" if success else "FAILED"))

    # Summary
    print(f"\n\n{'='*70}")
    print("BATCH RUN COMPLETE")
    print(f"{'='*70}")
    print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nResults:")

    successes = 0
    for name, status in results:
        symbol = "✓" if status == "SUCCESS" else "✗"
        print(f"  {symbol} {name}: {status}")
        if status == "SUCCESS":
            successes += 1

    print(f"\nTotal: {successes}/{len(MODELS)} succeeded")
    print(f"\nResults saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
