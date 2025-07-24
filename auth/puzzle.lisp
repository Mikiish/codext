(load (merge-pathnames "cryptodex-init.lisp" (or *load-pathname* (user-homedir-pathname))))
(ql:quickload '(:ironclad :babel :uiop))

(in-package #:cl-user)

(defun sha256-hex (str)
  (ironclad:byte-array-to-hex-string
    (ironclad:digest-sequence :sha256 (babel:string-to-octets str :encoding :utf-8))))

(defun compute-password (token pubkey)
  (sha256-hex (concatenate 'string token pubkey)))

(defun compute-username (timestamp password)
  (sha256-hex (concatenate 'string timestamp password)))

(defun main ()
  (let* ((token (uiop:getenv "DO_API_TOKEN"))
         (pub (uiop:getenv "CODEX_PUB_KEY"))
         (timestamp (or (uiop:getenv "CODEX_TIMESTAMP")
                        (write-to-string (get-universal-time))))
         (password (compute-password token pub))
         (username (compute-username timestamp password)))
    (format t "export CODEX_USERNAME='~A'~%" username)
    (format t "export CODEX_PASSWORD='~A'~%" password)
    (format t "export CODEX_TIMESTAMP='~A'~%" timestamp)))

(main)
