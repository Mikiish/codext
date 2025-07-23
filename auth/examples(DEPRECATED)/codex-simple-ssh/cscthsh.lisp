;;;; secret_hash
;;;; cscthsh.lisp

(load (merge-pathnames "quicklisp/setup.lisp" (user-homedir-pathname)))
(with-output-to-string (*standard-output*)
  (ql:quickload '(:ironclad :babel :uiop :alexandria :cl-ppcre)))

(in-package #:cl-user)

;; ------------------------------------------------------------
(defun bytes->hex (seq)
  (with-output-to-string (s)
    (loop for b across seq do (format s "~2,'0x" b))))

(defun sha256-hex (string)
  (bytes->hex (ironclad:digest-sequence :sha256 (babel:string-to-octets string :encoding :utf-8))))

(defun final-hash (user-input)
  (let* ((concat (concatenate 'string (uiop:getenv "TOKEN_HASH") user-input)))
    (sha256-hex concat)))

(defun main (&optional (user-input ""))
  (let ((result (final-hash user-input)))
    (format t "~a~%" result)))
;; Silent exit when run as script.
#+sbcl (main (uiop:getenv "USER_INPUT"))
;; ------------------------------------------------------------
;; End of script.
