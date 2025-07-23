#!/bin/bash

# Vérifie qu'on a bien un argument
if [ -z "$1" ]; then
    echo "Usage: $0 <string-to-hash>"
    exit 1
fi

# Hash SHA256
echo -n "$1" | sha256sum | awk '{print $1}'
