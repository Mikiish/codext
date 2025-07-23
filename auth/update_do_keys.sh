#!/usr/bin/env bash
set -euo pipefail

: "${DO_API_TOKEN:?DO_API_TOKEN not set}"

SSH_DIR="$HOME/.ssh"
AUTH_KEYS="$SSH_DIR/authorized_keys"

mkdir -p "$SSH_DIR"

for pub in "$SSH_DIR"/*.pub; do
  [ -e "$pub" ] || continue
  name=$(basename "$pub")
  key=$(cat "$pub")
  curl -sSL -X POST \
    -H "Authorization: Bearer $DO_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$name\", \"public_key\": \"$key\"}" \
    https://api.digitalocean.com/v2/account/keys
  cat "$pub" >> "$AUTH_KEYS"
done
