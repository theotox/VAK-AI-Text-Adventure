#!/usr/bin/env bash
set -e

# Check llama.cpp is installed
if ! command -v llama-server &>/dev/null; then
    echo "llama.cpp not found. Installing via Homebrew..."
    brew install llama.cpp
fi

MODEL="mradermacher/Qwen3.5-4B_Abliterated-GGUF:Q5_K_S"
PORT=8080

# Kill any existing llama-server on our port
lsof -ti tcp:"$PORT" 2>/dev/null | xargs kill -9 2>/dev/null || true
sleep 1

echo "Starting llama-server with Qwen3.5-4B_Abliterated (reasoning off)..."
llama-server \
  -hf "$MODEL" \
  --alias "vak" \
  --port "$PORT" \
  -ngl 999 \
  -c 4096 \
  --reasoning off \
  > /dev/null 2>&1 &

# Wait for server to be ready by checking the chat endpoint
echo "Waiting for server to be ready..."
for i in $(seq 1 60); do
    if curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/v1/chat/completions" \
      -d '{"model":"vak","messages":[{"role":"user","content":""}],"max_tokens":1}' 2>/dev/null | grep -q 200; then
        echo "Server ready."
        break
    fi
    if [ "$i" -eq 60 ]; then
        echo "Server failed to start within 60s."
        echo "Check ~/Library/Logs/llama-server.log for details."
        exit 1
    fi
    sleep 2
done

# Activate venv and run game
source venv/bin/activate
python cli.py
