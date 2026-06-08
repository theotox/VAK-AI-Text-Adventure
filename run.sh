#!/usr/bin/env bash
set -e

MODEL="mradermacher/Qwen3.5-4B_Abliterated-GGUF:Q5_K_S"
PORT=8080
ALIAS="vak"

# Install llama.cpp if missing
if ! command -v llama-server &>/dev/null; then
    if command -v brew &>/dev/null; then
        echo "llama.cpp not found. Installing via Homebrew..."
        brew install llama.cpp
    else
        echo "llama.cpp not found and Homebrew not available."
        echo "Downloading pre-built binaries from GitHub..."
        LATEST=$(curl -sL https://api.github.com/repos/ggml-org/llama.cpp/releases/latest \
            | grep '"tag_name":' | cut -d'"' -f4)
        echo "Latest release: $LATEST"
        ZIP="llama-${LATEST#b}-bin-macos-arm64.zip"
        URL="https://github.com/ggml-org/llama.cpp/releases/download/$LATEST/$ZIP"
        curl -L -o /tmp/llama.zip "$URL"
        sudo unzip -o /tmp/llama.zip -d /usr/local/bin/ > /dev/null
        rm /tmp/llama.zip
        echo "llama.cpp installed to /usr/local/bin"
    fi
fi

# Check if the right llama-server is already running and responsive
if curl -s "http://127.0.0.1:$PORT/v1/chat/completions" \
    -d '{"model":"'"$ALIAS"'","messages":[{"role":"user","content":""}],"max_tokens":1}' \
    -o /dev/null -w '%{http_code}' 2>/dev/null | grep -q 200; then
    echo "llama-server already running with model '$ALIAS' on port $PORT."
else
    echo "Killing any existing llama-server instances to free RAM..."
    killall llama-server 2>/dev/null || true
    sleep 1

    echo "Starting llama-server with Qwen3.5-4B_Abliterated (reasoning off)..."
    llama-server \
      -hf "$MODEL" \
      --alias "$ALIAS" \
      --port "$PORT" \
      -ngl 999 \
      -c 4096 \
      --reasoning off \
      > /dev/null 2>&1 &

    # Wait for server to be ready
    echo "Waiting for server to be ready..."
    for i in $(seq 1 60); do
        if curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/v1/chat/completions" \
          -d '{"model":"'"$ALIAS"'","messages":[{"role":"user","content":""}],"max_tokens":1}' 2>/dev/null | grep -q 200; then
            echo "Server ready."
            break
        fi
        if [ "$i" -eq 60 ]; then
            echo "Server failed to start within 60s."
            exit 1
        fi
        sleep 2
    done
fi

# Set up virtual environment and install package if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

if ! python -c "import vak" 2>/dev/null; then
    echo "Installing vak package and dependencies..."
    pip install --upgrade pip setuptools -q
    pip install -e .
fi

python cli.py
