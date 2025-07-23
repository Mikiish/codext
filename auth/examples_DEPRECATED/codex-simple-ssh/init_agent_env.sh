#!/bin/bash
set -e

# init_agent_env.sh - Initializes environment for automated secret management and authentication
# This script installs the necessary tools (e.g., OpenSSH, pass) and configures basic settings
# to enable secure, automated authentication for remote machine operations.

echo "Initializing agent environment for secret management..."

# Update package index and install OpenSSH and secret management tool 'pass'
if command -v apt-get >/dev/null 2>&1; then
    echo "Using apt-get to update package index..."
    sudo apt-get update -qq
    echo "Installing openssh-client, openssh-server, and pass..."
    sudo apt-get install -y openssh-client openssh-server pass
else
    echo "apt-get not found. Please install OpenSSH and pass manually."
fi

# Setup SSH directory with secure permissions
SSH_DIR="${HOME}/.ssh"
mkdir -p "${SSH_DIR}"
chmod 700 "${SSH_DIR}"

# Check and generate SSH key pair if not present
if [ ! -f "${SSH_DIR}/id_ed25519" ]; then
    echo "SSH key pair not found. Generating new ed25519 key pair..."
    ssh-keygen -t ed25519 -f "${SSH_DIR}/id_ed25519" -N "" -q
    echo "SSH key pair generated."
else
    echo "SSH key pair already exists."
fi

# Verify installation of secret management tool 'pass'
if ! command -v pass >/dev/null 2>&1; then
    echo "Secret management tool 'pass' is not installed. Attempting installation..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get install -y pass
    else
        echo "Please install 'pass' manually."
    fi
else
    echo "Secret management tool 'pass' is installed."
fi

echo "Agent environment initialization complete."