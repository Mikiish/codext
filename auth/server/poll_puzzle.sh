#!/usr/bin/env bash
# Poll DigitalOcean droplet for puzzle encoded in its name
set -euo pipefail
: "${DO_API_TOKEN:?DO_API_TOKEN not set}"
: "${DROPLET_ID:?DROPLET_ID not set}"

API_URL="https://api.digitalocean.com/v2/droplets/$DROPLET_ID"

while true; do
  name=$(curl -sSL -H "Authorization: Bearer $DO_API_TOKEN" "$API_URL" | jq -r '.droplet.name')
  if [[ "$name" != "null" && "$name" != "" ]]; then
    echo "Puzzle detected: $name"
    # TODO: solve puzzle here and derive password
    break
  fi
  sleep 5
done
