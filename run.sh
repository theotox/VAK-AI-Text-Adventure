#!/usr/bin/env bash
set -e

# Check llama.cpp is installed
if ! command -v llama-server &>/dev/null; then
    echo "llama.cpp not found. Installing via Homebrew..."
    brew install llama.cpp
fi

MODEL="mradermacher/Qwen3.5-4B_Abliterated-GGUF:Q5_K_S"

# Kill any existing llama-server on port 11434
lsof -ti tcp:11434 2>/dev/null | xargs kill -9 2>/dev/null || true
sleep 1

echo "Starting llama-server with Qwen3.5-4B_Abliterated (reasoning off)..."
llama-server \
  -hf "$MODEL" \
  --port 8080 \
  -ngl 999 \
  -c 4096 \
  --reasoning off \
  > /dev/null 2>&1 &

SERVER_PID=$!

# Wait for server to be ready
echo "Waiting for server to be ready..."
for i in $(seq 1 60); do
    if curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:11434/health 2>/dev/null | grep -q 200; then
        echo "Server ready."
        break
    fi
    if [ "$i" -eq 60 ]; then
        echo "Server failed to start within 60s."
        exit 1
    fi
    sleep 2
done

# Activate venv and run game
source venv/bin/activate
python cli.py
