#!/usr/bin/env bash
set -euo pipefail

echo "[+] Installing SBCL (Steel Bank Common Lisp)..."
sudo apt install -y sbcl

# ------------------------------------------------------------
# 1) Bootstrap Quicklisp uniquement s'il n'est pas présent
# ------------------------------------------------------------
if [ -f "$HOME/quicklisp/setup.lisp" ]; then
  echo "[✓] Quicklisp déjà installé. Skip bootstrap."
else
  echo "[+] Quicklisp absent. Téléchargement & installation…"
  curl -s -O https://beta.quicklisp.org/quicklisp.lisp
  sbcl --load quicklisp.lisp \
       --eval '(quicklisp-quickstart:install)' \
       --eval '(ql:add-to-init-file)' \
       --quit
fi

# ------------------------------------------------------------
# 2) Générer le script d’init Cryptodex
# ------------------------------------------------------------
cat > cryptodex-init.lisp <<'EOF'
;; Charge Quicklisp (pré-installé)
(load (merge-pathnames "quicklisp/setup.lisp"
                       (user-homedir-pathname)))
;; Dépendances Cryptodex
(ql:quickload '(:ironclad :babel :uiop :alexandria :cl-ppcre))
EOF

echo "[✔] Installation terminée."
echo "    Pour démarrer : sbcl --script cryptodex-init.lisp"
