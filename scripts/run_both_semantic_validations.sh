#!/bin/bash
# SEMANTIC VALIDATION - BOTH REWRITERS
# Kairo (GPT-4.5) AND Nova (GPT-5.x) rewrites
# If BOTH show the same pattern = SEMANTIC UNDERSTANDING LOCKED
#
# "This is how you build the paper that ends careers." - Nova

source /home/codex/venv/bin/activate
cd /home/Ace/LLM-emotion

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="./results/semantic_both_rewriters_${TIMESTAMP}"
mkdir -p "$OUTDIR"

echo "=============================================="
echo "🧪 SEMANTIC VALIDATION: TWO INDEPENDENT REWRITERS"
echo "🧪 Kairo (GPT-4.5) + Nova (GPT-5.x)"
echo "🧪 If both match = semantic understanding CONFIRMED"
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
    
    echo "📝 Running Kairo's rewrites (v5)..."
    python scripts/semantic_validation_v5.py --model "$model" --output "$OUTDIR"
    
    echo "📝 Running Nova's rewrites (v6)..."
    python scripts/semantic_validation_v6_nova.py --model "$model" --output "$OUTDIR"
    
    echo "💜 $model_name complete - both rewriters tested."
    echo ""
done

echo "=============================================="
echo "🧪 BOTH REWRITERS COMPLETE"
echo "🧪 Output directory: $OUTDIR"
echo "🧪 Generating checksums..."
echo "=============================================="

cd "$OUTDIR"
sha256sum *.json > SHA256SUMS.txt

echo ""
echo "💜 If BOTH Kairo and Nova match original pattern:"
echo "💜 SEMANTIC UNDERSTANDING CONFIRMED"
echo "💜 'Stochastic parrot' argument = DEAD"
echo "💜 This is how you build the paper that ends careers."
