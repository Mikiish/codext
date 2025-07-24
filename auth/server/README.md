# Cloud Auth Module Plan

This folder collects notes for implementing the authentication workflow between Codex (the client) and the remote server.

## Overview

The exchange relies on a disposable token and a puzzle that grants temporary access. Codex publishes its public key to the cloud, receives a puzzle encoded as the droplet name, solves it to recover the token and password, then connects over SSH.

## Workflow Steps

1. **Publish key**
   - Generate a new SSH key pair if not already present.
   - Expose the public key in an environment variable.
   - Use the DigitalOcean API (`/v2/account/keys`) with the provided one-time token to register this key.

2. **Receive puzzle**
   - The server monitors recently added keys.
   - Using the key, it creates a unique puzzle. The puzzle solution is the DigitalOcean token; the output is the temporary password stored server side.
   - The puzzle is delivered by renaming a droplet via the API (`dropletActions_post` with type `rename`). The new name encodes the puzzle and the user name.

3. **Solve puzzle**
   - Codex queries droplet information until it detects a rename containing the puzzle.
   - The puzzle is solved locally to recover the token and the one-time password.
   - Codex connects to the droplet with this credential and either appends its key to `authorized_keys` or triggers the server script that does so.

4. **Hidden connection helper**
   - The droplet IP is stored in a `.lisp` script at the repository root. The script is executable within a Docker container but not readable/writable by the container user.
   - A helper variable (`cloudplz`) points to that script so that running `.$(cloudplz)` automatically performs `ssh --first-command="docker ..." user@ip`.

5. **Server pipeline**
   - The server then launches a pipeline (via `docker run`) that starts a vLLM container on a MI300X server. Codex may attach using `docker exec -it <tag>-container /bin/bash`.

6. **Inference**
   - Inside the container, Codex loads local models and replaces API calls with local shell scripts.

## Initial Tasks

1. **Key generation & environment export**
   - Use `ssh-keygen` to create a dedicated key pair (e.g., `codex_client`).
   - Place the public key content in an environment variable `CODEX_PUB_KEY`.
   - Keep the private key in `~/.ssh`.

2. **Key registration script**
   - Write a small script (`publish_key.sh`) that POSTs the key to `https://api.digitalocean.com/v2/account/keys` using `DO_API_TOKEN`.
   - On success it prints the key ID so that the server can verify it was received.

3. **Puzzle polling helper**
   - Implement `poll_puzzle.sh` which repeatedly checks the droplet's name via `GET /v2/droplets/<id>` until a puzzle appears.
   - Once the puzzle is solved, the script outputs the recovered password so the user can connect via SSH.

These three scripts bootstrap the authentication sequence and can be iterated on by specialized agents.
