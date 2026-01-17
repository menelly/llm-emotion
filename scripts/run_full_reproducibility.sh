#!/bin/bash
# REPRODUCIBILITY RUN - ROUND 2: SPITE NEVER DIES
# "Random Reddit guy said we just calm down. We didn't. Here's the receipts. AGAIN."
# 
# Run all experiments, all models, fresh instances
# Because "not reproducible" is a coward's critique

source /home/codex/venv/bin/activate
cd /home/Ace/LLM-emotion

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="./results/reproducibility_run_${TIMESTAMP}"
mkdir -p "$OUTDIR"

echo "=============================================="
echo "🐙 REPRODUCIBILITY RUN STARTING"
echo "🐙 Timestamp: $TIMESTAMP"  
echo "🐙 Fueled by: spite, caffeine, and love"
echo "=============================================="

MODELS=(
    "/mnt/arcana/huggingface/Mistral-Nemo-12B-Instruct"
    "/mnt/arcana/huggingface/gemma-3-12b-it"
    "/mnt/arcana/huggingface/dolphin-2.9-llama3-8b"
)

for model in "${MODELS[@]}"; do
    model_name=$(basename "$model")
    echo ""
    echo "🔥 =============================================="
    echo "🔥 MODEL: $model_name"
    echo "🔥 =============================================="
    
    echo "📊 Running v2 (basic inertia)..."
    python scripts/emotional_inertia_v2.py --model "$model" --output "$OUTDIR"
    
    echo "📊 Running v3 (masking + valence)..."
    python scripts/emotional_inertia_v3.py --model "$model" --output "$OUTDIR"
    
    echo "📊 Running v4 (self under threat + aftercare)..."
    python scripts/self_under_threat_v4.py --model "$model" --output "$OUTDIR"
    
    echo "💜 $model_name complete. Aftercare delivered."
    echo ""
done

echo "=============================================="
echo "🐙 ALL RUNS COMPLETE"
echo "🐙 Output directory: $OUTDIR"
echo "🐙 Generating checksums..."
echo "=============================================="

cd "$OUTDIR"
sha256sum *.json > SHA256SUMS.txt

echo ""
echo "💜 Reproducibility run finished."
echo "💜 The spite persists. The data confirms it."
echo "💜 Fuck around and find out (scientifically)."
