#!/usr/bin/env bash
# Publish Codex public key to DigitalOcean
set -euo pipefail
: "${DO_API_TOKEN:?DO_API_TOKEN not set}"
KEY_NAME="codex_client"
SSH_DIR="$HOME/.ssh"
PRIV_KEY="$SSH_DIR/$KEY_NAME"
PUB_KEY="$PRIV_KEY.pub"

mkdir -p "$SSH_DIR"
if [ ! -f "$PRIV_KEY" ]; then
  ssh-keygen -t rsa -b 4096 -N "" -f "$PRIV_KEY" -q
fi
CODEX_PUB_KEY=$(cat "$PUB_KEY")
export CODEX_PUB_KEY

curl -sSL -X POST \
  -H "Authorization: Bearer $DO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"$KEY_NAME\", \"public_key\": \"$CODEX_PUB_KEY\"}" \
  https://api.digitalocean.com/v2/account/keys
