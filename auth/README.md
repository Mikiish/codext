# Authentication Setup

This folder contains helper scripts for a minimal Lisp-based authentication demo.

- `lispenv.sh` installs SBCL and Quicklisp.
- `sandbox_auth.lisp` generates an RSA key pair for every environment variable
  starting with `SECRET_`. The public key is printed as shell commands so it can
  be exported while the private key is stored in `~/.ssh`.
- `setup-auth.sh` runs the Lisp script and optionally registers the keys with
  DigitalOcean when `DO_API_TOKEN` is defined.
- `update_do_keys.sh` uploads every public key in `~/.ssh` to the DigitalOcean
  API and appends them to `authorized_keys`.

Usage:

```bash
./lispenv.sh            # once, to install SBCL/Quicklisp
source ./setup-auth.sh  # generate keys and export variables
```
