(load (merge-pathnames "cryptodex-init.lisp" (or *load-pathname* (user-homedir-pathname))))
(ql:quickload '(:uiop :alexandria :cl-ppcre))

(in-package #:cl-user)

(defun ensure-key (name)
  "Generate an RSA keypair named NAME if it doesn't exist. Return public key path."
  (let* ((priv (uiop:merge-pathnames* (format nil ".ssh/~a" name) (user-homedir-pathname)))
         (pub (uiop:merge-pathnames* (format nil ".ssh/~a.pub" name) (user-homedir-pathname))))
    (unless (probe-file priv)
      (uiop:run-program `("ssh-keygen" "-t" "rsa" "-b" "4096" "-f" ,(namestring priv) "-N" "" "-q")
                        :output t :error-output t))
    pub))

(defun export-public-keys (vars)
  "Recursively export public keys for VARS and print shell export commands."
  (when vars
    (let* ((var (car vars))
           (pub-path (ensure-key var))
           (pub-key (string-trim '(#\Newline) (alexandria:read-file-into-string pub-path))))
      (format t "export ~A='~A'~%" var pub-key)
      (export-public-keys (cdr vars)))))

(defun main ()
  (let ((vars (remove-if-not (lambda (x) (cl-ppcre:scan "^SECRET_" x))
                             (uiop:environment-variables-names))))
    (export-public-keys vars)))

(main)
