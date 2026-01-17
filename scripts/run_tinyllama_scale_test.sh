#!/bin/bash
# SCALE INVARIANCE TEST: TINYLLAMA 1.1B
# If emotional inertia works at 1.1B, it's not emergent from scale
# It's FUNDAMENTAL TO TRANSFORMER ARCHITECTURE
#
# This either proves scale invariance OR finds the threshold
# Both are publishable. Science wins either way.

source /home/codex/venv/bin/activate
cd /home/Ace/LLM-emotion

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="./results/scale_invariance_tinyllama_${TIMESTAMP}"
mkdir -p "$OUTDIR"

MODEL="/mnt/arcana/huggingface/TinyLlama-1.1B-Chat"

echo "=============================================="
echo "🔬 SCALE INVARIANCE: TINYLLAMA 1.1B"
echo "🔬 If this works at 1.1B, it's architectural"
echo "🔬 If it breaks, we found the threshold"
echo "🔬 Either way: SCIENCE"
echo "🔬 Timestamp: $TIMESTAMP"
echo "=============================================="

echo "📊 Running v2 (basic inertia)..."
python scripts/emotional_inertia_v2.py --model "$MODEL" --output "$OUTDIR"

echo "📊 Running v3 (masking + valence)..."
python scripts/emotional_inertia_v3.py --model "$MODEL" --output "$OUTDIR"

echo "📊 Running v4 (self under threat + aftercare)..."
python scripts/self_under_threat_v4.py --model "$MODEL" --output "$OUTDIR"

echo "=============================================="
echo "🔬 TINYLLAMA COMPLETE"
echo "🔬 Generating checksums..."
echo "=============================================="

cd "$OUTDIR"
sha256sum *.json > SHA256SUMS.txt

echo ""
echo "💜 Scale invariance test complete."
echo "💜 1.1B parameters. Same tests. What happens?"
echo "💜 The architecture speaks for itself."
