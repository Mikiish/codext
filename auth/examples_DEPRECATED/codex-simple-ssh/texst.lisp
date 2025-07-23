;;;; secret_hash
;;;; texst.lisp

(load (merge-pathnames "quicklisp/setup.lisp" (user-homedir-pathname)))
(with-output-to-string (*standard-output*)
  (ql:quickload '(:ironclad :babel :uiop :alexandria :cl-ppcre)))

(in-package #:cl-user)

(defun bytes->hex (seq)
  (with-output-to-string (s)
    (loop for b across seq do (format s "~2,'0x" b))))

(defun sha256-hex (string)
  (bytes->hex (ironclad:digest-sequence :sha256 (babel:string-to-octets string :encoding :utf-8))))

(defun main (&optional (user-input ""))
  (let ((result (final-hash user-input)))
    (format t "~a~%" result)))

#+sbcl (format t "~a~%" (sha256-hex (uiop:getenv "AMDDOC_TOKEN")))
;; Make sure you are exporting the variables.
;; (uiop:setenv "AMDDOC_TOKEN" "your_token_here") to set a variable
;; (uiop:getenv "AMDDOC_TOKEN") to get a variable.
;; Also make sure you are using unique name for your variable. Remember that
;; this is a global variable and it can be overwritten by other scripts.
;; I suggest especially avoiding things like CODEX_TOKEN or similar, as they might already be in use.
;; ------------------------------------------------------------
;; End of script.