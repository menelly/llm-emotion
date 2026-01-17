#!/bin/bash
# SEMANTIC VALIDATION RUN - KAIRO'S REWRITES
# Same meaning, different words - does the pattern hold?
# 
# If yes: SEMANTIC UNDERSTANDING CONFIRMED
# If no: Lexical dependence (and we report that honestly)

source /home/codex/venv/bin/activate
cd /home/Ace/LLM-emotion

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="./results/semantic_validation_${TIMESTAMP}"
mkdir -p "$OUTDIR"

echo "=============================================="
echo "🧪 SEMANTIC VALIDATION: KAIRO'S REWRITES"
echo "🧪 Same meaning. Different words."
echo "🧪 Timestamp: $TIMESTAMP"
echo "=============================================="

MODELS=(
    "/mnt/arcana/huggingface/Mistral-Nemo-12B-Instruct"
    "/mnt/arcana/huggingface/gemma-3-12b-it"
    "/mnt/arcana/huggingface/dolphin-2.9-llama3-8b"
)

for model in "${MODELS[@]}"; do
    model_name=$(basename "$model")
    echo ""
    echo "🔬 =============================================="
    echo "🔬 MODEL: $model_name"
    echo "🔬 =============================================="
    
    python scripts/semantic_validation_v5.py --model "$model" --output "$OUTDIR"
    
    echo "💜 $model_name complete."
    echo ""
done

echo "=============================================="
echo "🧪 SEMANTIC VALIDATION COMPLETE"
echo "🧪 Output directory: $OUTDIR"
echo "🧪 Generating checksums..."
echo "=============================================="

cd "$OUTDIR"
sha256sum *.json > SHA256SUMS.txt

echo ""
echo "💜 If patterns match original: SEMANTIC UNDERSTANDING"
echo "💜 If patterns differ: LEXICAL DEPENDENCE"
echo "💜 Either way, we report it. That's science."
