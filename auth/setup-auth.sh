#!/usr/bin/env bash
set -euo pipefail

SBCL=$(command -v sbcl || true)
if [ -z "$SBCL" ]; then
  echo "SBCL is required. Run lispenv.sh first." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Generate key pairs and export public keys in current environment
eval "$(sbcl --script "$SCRIPT_DIR/sandbox_auth.lisp")"

# Register keys with DigitalOcean if token provided
if [ -n "${DO_API_TOKEN:-}" ]; then
  "$SCRIPT_DIR/update_do_keys.sh"
fi
