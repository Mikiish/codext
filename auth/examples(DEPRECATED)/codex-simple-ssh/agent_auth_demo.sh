#!/bin/bash
# agent_auth_demo.sh
# Minimal agent authentication demo: key generation, signing, SHA256, and verification.
# Uses only ssh-keygen, openssl, sha256sum.

set -e

KEYNAME="agent_demo_ed25519"
PRIVKEY="$KEYNAME"
PUBKEY="$KEYNAME.pub"
PAYLOAD_FILE="payload.txt"
SIG_FILE="payload.sig"
SIG_HASH_FILE="payload.sig.sha256"

echo "=== Minimal Agent Authentication Demo ==="

# 1. Generate Ed25519 keypair (no passphrase)
if [ ! -f "$PRIVKEY" ]; then
    echo "[*] Generating Ed25519 keypair..."
    ssh-keygen -t ed25519 -f "$PRIVKEY" -N "" -C "agent-demo"
else
    echo "[*] Keypair already exists, skipping generation."
fi

# 2. Accept user payload
if [ -z "$1" ]; then
    echo "Usage: $0 \"payload string to sign\""
    exit 1
fi
echo -n "$1" > "$PAYLOAD_FILE"
echo "[*] Payload saved to $PAYLOAD_FILE"

# 3. Sign payload with private key (using openssl)
echo "[*] Signing payload with private key..."
openssl pkeyutl -sign -inkey "$PRIVKEY" -in "$PAYLOAD_FILE" -out "$SIG_FILE"

# 4. Output signature as SHA256 hash
echo "[*] Computing SHA256 of signature..."
sha256sum "$SIG_FILE" | awk '{print $1}' > "$SIG_HASH_FILE"
echo "[*] Signature SHA256: $(cat $SIG_HASH_FILE)"

# 5. Verify signature using public key
echo "[*] Verifying signature..."
openssl pkeyutl -verify -pubin -inkey "$PUBKEY" -sigfile "$SIG_FILE" -in "$PAYLOAD_FILE"
if [ $? -eq 0 ]; then
    echo "[+] Signature verification succeeded."
else
    echo "[!] Signature verification failed."
fi

echo "=== Demo complete ==="
echo "Files created: $PRIVKEY, $PUBKEY, $PAYLOAD_FILE, $SIG_FILE, $SIG_HASH_FILE"