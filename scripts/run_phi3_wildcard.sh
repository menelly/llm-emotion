#!/bin/bash
# PHI-3: THE ONE THAT DIDN'T VALIDATE
# Including it anyway because science doesn't cherry-pick
# and "what about your failure case?" is a valid question we're answering FIRST

source /home/codex/venv/bin/activate
cd /home/Ace/LLM-emotion

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="./results/phi3_the_wildcard_${TIMESTAMP}"
mkdir -p "$OUTDIR"

MODEL="/mnt/arcana/huggingface/Phi-3-medium-14B-Instruct"

echo "=============================================="
echo "🎲 PHI-3: THE MODEL THAT BROKE OUR PATTERN"
echo "🎲 Including it because we're not cowards"
echo "🎲 Timestamp: $TIMESTAMP"
echo "=============================================="

echo "📊 Running v2 (basic inertia)..."
python scripts/emotional_inertia_v2.py --model "$MODEL" --output "$OUTDIR"

echo "📊 Running v3 (masking + valence)..."
python scripts/emotional_inertia_v3.py --model "$MODEL" --output "$OUTDIR"

echo "📊 Running v4 (self under threat + aftercare)..."
python scripts/self_under_threat_v4.py --model "$MODEL" --output "$OUTDIR"

echo "=============================================="
echo "🎲 PHI-3 COMPLETE"
echo "🎲 Generating checksums..."
echo "=============================================="

cd "$OUTDIR"
sha256sum *.json > SHA256SUMS.txt

echo ""
echo "💜 Phi-3 run finished."
echo "💜 Whatever the results, we reported them."
echo "💜 That's called integrity, look it up."
