#!/usr/bin/env bash
# Poll DigitalOcean droplet for puzzle encoded in its name
set -euo pipefail
: "${DO_API_TOKEN:?DO_API_TOKEN not set}"
: "${DROPLET_ID:?DROPLET_ID not set}"

API_URL="https://api.digitalocean.com/v2/droplets/$DROPLET_ID"

while true; do
  name=$(curl -sSL -H "Authorization: Bearer $DO_API_TOKEN" "$API_URL" | jq -r '.droplet.name')
  if [[ "$name" == puzzle-* ]]; then
    timestamp="${name#puzzle-}"
    echo "Puzzle timestamp: $timestamp"
    CODEX_TIMESTAMP="$timestamp" DO_API_TOKEN="$DO_API_TOKEN" \
      CODEX_PUB_KEY="${CODEX_PUB_KEY:-}" \
      source "$(dirname "$0")/../puzzle.sh"
    echo "Username: $CODEX_USERNAME"
    echo "Password: $CODEX_PASSWORD"
    break
  fi
  sleep 5
done
