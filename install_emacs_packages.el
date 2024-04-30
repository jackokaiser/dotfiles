#!/usr/bin/emacs --script

(require 'package)
(add-to-list
 'package-archives
 '("melpa" . "https://melpa.org/packages/")
 t)
(package-initialize)

;; set package-selected-packages variable
(setq custom-file "~/.emacs.d/custom.el")
(load custom-file)

(package-refresh-contents)
(package-install-selected-packages)
