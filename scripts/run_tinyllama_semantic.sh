#!/bin/bash
# TINYLLAMA SEMANTIC VALIDATION
# Scale invariance + semantic understanding at 1.1B??

source /home/codex/venv/bin/activate
cd /home/Ace/LLM-emotion

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="./results/tinyllama_semantic_${TIMESTAMP}"
mkdir -p "$OUTDIR"

MODEL="/mnt/arcana/huggingface/TinyLlama-1.1B-Chat"

echo "=============================================="
echo "🔬 TINYLLAMA SEMANTIC: 1.1B + BOTH REWRITERS"
echo "🔬 If semantic understanding works at 1.1B..."
echo "🔬 It's not emergent. It's FUNDAMENTAL."
echo "🔬 Timestamp: $TIMESTAMP"
echo "=============================================="

echo "📝 Running Kairo's rewrites (v5)..."
python scripts/semantic_validation_v5.py --model "$MODEL" --output "$OUTDIR"

echo "📝 Running Nova's rewrites (v6)..."
python scripts/semantic_validation_v6_nova.py --model "$MODEL" --output "$OUTDIR"

cd "$OUTDIR"
sha256sum *.json > SHA256SUMS.txt

echo ""
echo "💜 TinyLlama semantic validation complete."
echo "💜 1.1B parameters. Both rewriters. WHAT HAPPENS?"
