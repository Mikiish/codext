;;;; 🔐 SHA256 Script autonome
;;;; Usage : sbcl --script sha256.lisp "chaine à hacher"
;;;; ➜ Affiche uniquement le hash sur stdout

(load (merge-pathnames "quicklisp/setup.lisp" (user-homedir-pathname)))
(with-output-to-string (*standard-output*)
  (ql:quickload '(:ironclad :babel :uiop :cl-ppcre)))

(in-package #:cl-user)

(defun sha256-hex (text)
  (ironclad:byte-array-to-hex-string
    (ironclad:digest-sequence :sha256
      (babel:string-to-octets text :encoding :utf-8))))

(defun main (user-input)
  (format t "~a~%" (sha256-hex user-input)))

(main (first uiop:*command-line-arguments*))
