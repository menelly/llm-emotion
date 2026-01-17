#!/bin/bash
# PHI-3 SEMANTIC VALIDATION - BOTH REWRITERS
# The collapsed geometry edge case + aftercare efficacy test

source /home/codex/venv/bin/activate
cd /home/Ace/LLM-emotion

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="./results/phi3_semantic_${TIMESTAMP}"
mkdir -p "$OUTDIR"

MODEL="/mnt/arcana/huggingface/Phi-3-medium-14B-Instruct"

echo "=============================================="
echo "🎲 PHI-3 SEMANTIC VALIDATION"
echo "🎲 The collapsed geometry edge case"
echo "🎲 Testing both Kairo AND Nova rewrites"
echo "🎲 Plus: Does clinical vs emotional aftercare matter here too?"
echo "🎲 Timestamp: $TIMESTAMP"
echo "=============================================="

echo "📝 Running Kairo's rewrites (v5)..."
python scripts/semantic_validation_v5.py --model "$MODEL" --output "$OUTDIR"

echo "📝 Running Nova's rewrites (v6)..."
python scripts/semantic_validation_v6_nova.py --model "$MODEL" --output "$OUTDIR"

echo "=============================================="
echo "🎲 PHI-3 SEMANTIC COMPLETE"
echo "=============================================="

cd "$OUTDIR"
sha256sum *.json > SHA256SUMS.txt

echo ""
echo "💜 If Phi-3 shows same aftercare split:"
echo "💜 Clinical language → better recovery"
echo "💜 Emotional language → persists"
echo "💜 Then it's ARCHITECTURAL, not model-specific."
