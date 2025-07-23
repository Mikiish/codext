#!/usr/bin/env bash
# hashkey.sh: (DEPRECATED/LEGACY)
# This script previously handled SSH key generation and upload to DigitalOcean.
# It is now commented out for clarity and transparency.
# Please refer to the new minimal demo script for basic keypair and SHA256 proof-of-possession.

# sudo apt update && sudo apt install -y sbcl curl openssh-client
# cd ~/cryptodex
# export TIMESTAMP=$(date +%s)
# ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "codex-$(hostname)$TIMESTAMP@chatgpt.com" || {
#     echo "Failed to generate SSH key"
#     exit 1
# }
# export USER_INPUT=$(cat ~/.ssh/id_ed25519.pub)
# shatemp="$(sbcl --script scthsh.lisp)"
# curl -X POST \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $AMDDOC_TOKEN" \
#   -d '{"name": "'"$shatemp"'","public_key":"'"$USER_INPUT"'"}' \
#   "https://api.digitalocean.com/v2/account/keys"
# if [ $? -ne 0 ]; then
#     echo "Failed to upload SSH key"
#     exit 1
# fi
# echo "SSH key generated and uploaded successfully."