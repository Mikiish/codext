#!/usr/bin/env bash
# Run puzzle algorithm and export CODEX_USERNAME, CODEX_PASSWORD and CODEX_TIMESTAMP
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# Evaluate the Lisp script which prints export commands
eval "$(sbcl --script "$SCRIPT_DIR/puzzle.lisp")"
