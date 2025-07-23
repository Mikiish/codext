#!/bin/bash
set -e

# Create keys directory if not exists
mkdir -p keys

# Generate key pair if not exists
if [ ! -f keys/agent_key ]; then
    echo "Generating key pair..."
    ssh-keygen -t ed25519 -f keys/agent_key -N "" -q
fi

# Check if payload provided as argument
if [ -z "$1" ]; then
  echo "Usage: $0 <payload>"
  exit 1
fi

payload="$1"

# Read private and public key contents
private_key=$(cat keys/agent_key)
public_key=$(cat keys/agent_key.pub)

# Create signature: SHA256 hash of concatenation of payload and private key
signature=$(echo -n "${payload}${private_key}" | sha256sum | awk '{print $1}')

echo "Payload: $payload"
echo "Signature (SHA256 of payload+private key): $signature"
echo "Public Key:"
echo "$public_key"

# Verification: recompute the hash to verify signature
recomputed=$(echo -n "${payload}${private_key}" | sha256sum | awk '{print $1}')

if [ "$signature" = "$recomputed" ]; then
  echo "Verification successful: signature matches."
else
  echo "Verification failed: signature mismatch."
fi