;; Charge Quicklisp (pré-installé)
(load (merge-pathnames "quicklisp/setup.lisp" (user-homedir-pathname)))
;; Dépendances Cryptodex
(ql:quickload '(:ironclad :babel :uiop :alexandria :cl-ppcre))
