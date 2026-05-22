#!/bin/bash
# ═══════════════════════════════════════════════════════
#  FRAYMUS CENTAUR — Unified Launcher
#  DeepThought Zero · Living Organism
#  by Vaughn Scott
# ═══════════════════════════════════════════════════════

JAR="$(dirname "$0")/deepthought-zero-1.0.0.jar"
VIDEOCORTEX="$(dirname "$0")/../Asset-Manager/VideoCortex.py"

# Defaults
DIM=512
HZ=4
BREATHS=100
FLAGS=""

usage() {
    echo "╔══════════════════════════════════════════════╗"
    echo "║  FRAYMUS CENTAUR — DeepThought Zero         ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""
    echo "Usage: ./centaur.sh [mode] [options]"
    echo ""
    echo "Modes:"
    echo "  quick       10 breaths, fast demo"
    echo "  live        Infinite loop with persistence"
    echo "  full        All subsystems: persist + visual + QR + Ollama"
    echo "  server      Start as primary node (port 9999)"
    echo "  replica     Connect to a primary node"
    echo "  showcase    Run the module showcase demo"
    echo ""
    echo "Options:"
    echo "  --dim N          Cortex dimensions (default: 512)"
    echo "  --hz N           Heartbeat Hz (default: 4)"
    echo "  --breathes N     Number of breaths (default: 100)"
    echo "  --ollama         Enable Ollama voice"
    echo "  --persist        Enable state persistence"
    echo "  --visual         Enable VideoCortex dreaming"
    echo "  --qr             Generate QR soul seed on exit"
    echo "  --server PORT    Run as replication primary"
    echo "  --connect H P    Connect to primary node"
    echo "  --infinite       Run forever (Ctrl+C to stop)"
    echo "  --all            Enable all subsystems"
    echo ""
}

case "${1:-}" in
    quick)
        echo "⚡ Quick demo — 10 breaths"
        java -jar "$JAR" --dim 256 --hz 10 --breathes 10 --qr
        ;;
    live)
        echo "⚡ Live mode — infinite with persistence"
        java -jar "$JAR" --dim "$DIM" --hz "$HZ" --persist --qr --infinite
        ;;
    full)
        echo "⚡ Full Centaur — all systems online"
        ARGS="--dim $DIM --hz $HZ --breathes ${BREATHS} --all"
        if [ -f "$VIDEOCORTEX" ]; then
            ARGS="$ARGS --videocortex $VIDEOCORTEX"
        fi
        java -jar "$JAR" $ARGS
        ;;
    server)
        PORT="${2:-9999}"
        echo "⚡ Primary node — listening on port $PORT"
        java -jar "$JAR" --dim "$DIM" --hz "$HZ" --persist --qr --server "$PORT" --infinite
        ;;
    replica)
        HOST="${2:-localhost}"
        PORT="${3:-9999}"
        echo "⚡ Replica node — connecting to $HOST:$PORT"
        java -jar "$JAR" --dim "$DIM" --hz "$HZ" --persist --connect "$HOST" "$PORT" --infinite
        ;;
    showcase)
        echo "⚡ Module showcase"
        java -cp "$(dirname "$0")/out" io.fraymus.deepthought.demo.Showcase 2>/dev/null || \
        java -jar "$JAR" --dim 256 --hz 10 --breathes 30 --persist --qr
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        # Pass all args through
        if [ $# -gt 0 ]; then
            java -jar "$JAR" "$@"
        else
            usage
            echo ""
            echo "Run './centaur.sh quick' for a fast demo."
        fi
        ;;
esac

# Open QR soul seed if it was generated
if [ -f "organism_state/soul_seed.html" ]; then
    echo ""
    echo "📱 Soul Seed QR available: organism_state/soul_seed.html"
fi
