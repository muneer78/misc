(setq custom-file (locate-user-emacs-file "custom.el"))
(load custom-file :no-error-if-file-is-missing)

;; Set up the package manager

(defvar bootstrap-version)
(let ((bootstrap-file
       (expand-file-name "straight/repos/straight.el/bootstrap.el" user-emacs-directory))
      (bootstrap-version 5))
  (unless (file-exists-p bootstrap-file)
    (with-current-buffer
        (url-retrieve-synchronously
         "https://raw.githubusercontent.com/raxod502/straight.el/develop/install.el"
         'silent 'inhibit-cookies)
      (goto-char (point-max))
      (eval-print-last-sexp)))
  (load bootstrap-file nil 'nomessage))

(straight-use-package 'use-package)

(setq straight-use-package-by-default t)

(use-package org)
(use-package yasnippet)

					; Basic behaviour

(setq inhibit-splash-screen t)
(setq inhibit-startup-message t)

(setq-default bidi-display-reordering 'left-to-right
              bidi-paragraph-direction 'left-to-right)
(setq bidi-inhibit-bpa t)

(setq-default cursor-in-non-selected-windows nil)
(setq highlight-nonselected-windows nil)

(setq tab-always-indent 'complete)

;; wrapped lines respect the indentation of the original line
(global-visual-wrap-prefix-mode 1)

;; store backup files in the tmp dir
(setq backup-directory-alist
      `((".*" . ,temporary-file-directory)))

;; store auto-save (#) files in ~/.emacs/temp
(let ((auto-save-dir (expand-file-name "~/.emacs.d/temp")))
  (unless (file-exists-p auto-save-dir)
    (make-directory auto-save-dir t))
  (setq auto-save-file-name-transforms
        `((".*" ,(concat auto-save-dir "/") t))))

;; enable y/n answers
(setq use-short-answers t)

(setq frame-title-format
      '((:eval (if (buffer-file-name)
                   (abbreviate-file-name (buffer-file-name))
                 "%b"))))

;; improving kill-ring
(setq save-interprogram-paste-before-kill t)
(setq kill-do-not-save-duplicates t)

;; Restore Opened Files
(progn
  (desktop-save-mode 1)
  ;; save when quit
  (setq desktop-save t)

  ;; no ask if crashed
  (setq desktop-load-locked-desktop t)

  (setq desktop-restore-frames t)

  (setq desktop-auto-save-timeout 300)

  ;; save some global vars
  (setq desktop-globals-to-save nil)
  )

(recentf-mode 1)
(setq recentf-max-menu-items 20)
(setq recentf-max-saved-items 50)
(global-set-key "\C-x\ \C-r" 'recentf-open-files)

					; Org mode configuration
;; Enable Org mode
(require 'org)
;; Make Org mode work with files ending in .org
(add-to-list 'auto-mode-alist '("\\.org$" . org-mode))
;; The above is the default in recent emacsen

(require 'org-clock)

(defun org-archive-done-tasks-bulk ()
  "Archive all top-level DONE tasks in the current Org file."
  (interactive)
  (require 'org)

  (let* ((archive-file
          (concat (file-name-sans-extension (buffer-file-name)) "_archive.org"))
         (entries '()))

    (save-excursion
      (goto-char (point-min))

      ;; find headings beginning with "* DONE"
      (while (re-search-forward "^\\*+ DONE " nil t)
        (org-back-to-heading t)
        (let ((start (point)))
          (org-end-of-subtree t t)
          (push (buffer-substring start (point)) entries)
          (delete-region start (point))
          (goto-char start))))

    ;; write archive
    (when entries
      (with-current-buffer (find-file-noselect archive-file)
        (goto-char (point-max))
        (unless (bolp) (insert "\n"))
        (insert (mapconcat #'identity (reverse entries) "\n\n"))
        (insert "\n")
        (save-buffer)))

    (message "Archived %d tasks" (length entries))))

(setq org-auto-align-tags t)

(setq org-startup-folded t)

(setq org-hide-emphasis-markers t)

(with-eval-after-load 'org-agenda
  (set-face-attribute 'org-agenda-date nil :height 1.1)
  (set-face-attribute 'org-agenda-date-weekend nil :height 1.0)
  (set-face-attribute 'org-agenda-date-today nil :height 1.0 :weight 'bold))

(defun my-org-align-all-tags ()
  "Realign all Org tags in the current buffer."
  (interactive)
  (org-map-entries
   (lambda ()
     (org-set-tags-command))))

;; Do not dim blocked tasks
(setq org-agenda-dim-blocked-tasks nil)

;; Compact the block agenda view
(setq org-agenda-compact-blocks t)

(setq org-export-with-toc nil)

(setq org-export-with-sub-superscripts nil)

(defun org-insert-custom-timestamp ()  
  (interactive)  
  (insert (format-time-string "%Y%m%d")))  

;; I use C-c t to insert timestamp
(global-set-key (kbd "C-c t") 'org-insert-custom-timestamp)

;; I use C-c c to start capture mode
(global-set-key (kbd "C-c c") 'org-capture)

;; Capture templates for: TODO tasks, Notes, appointments, phone calls, meetings, and org-protocol
(require 'org-capture)
(global-set-key (kbd "C-c c") #'org-capture)

(setq org-capture-templates
      '(("t" "todo" entry (file "/Users/muneer78/Documents/GitHub/emacs-files/todos.org")
         "* TODO %?\n%U\n%a")
        ("l" "Reading list" entry
         (file+headline "/Users/muneer78/Documents/GitHub/emacs-files/reading-list.org" "Reading List")
         "** TODO [[%^{URL}][%^{Link name}]]"
         :prepend t)))

(setq org-refile-targets
      '(("/Users/muneer78/Documents/GitHub/emacs-files/refile.org" :maxlevel . 1)
        ("/Users/muneer78/Documents/GitHub/emacs-files/todos.org" :maxlevel . 2)))

(setq org-blank-before-new-entry
      '((heading . nil)
        (plain-list-item . nil)))

(defun my/org-mode-hook ()
  "Stop the org-level headers from increasing in height relative to the other text."
  (dolist (face '(org-level-1
                  org-level-2
                  org-level-3
                  org-level-4
                  org-level-5))
    (set-face-attribute face nil :weight 'semi-bold :height 1.0)))

(add-hook 'org-mode-hook #'my/org-mode-hook)


(setq org-agenda-skip-scheduled-if-done t)
(setq org-agenda-skip-deadline-if-done t)
(setq org-agenda-skip-timestamp-if-done t)
(setq org-agenda-skip-function-global '(org-agenda-skip-entry-if 'todo 'done))
(setq org-agenda-span 'month)

;; Org SSG
(add-to-list 'load-path "/Users/muneer78/.emacs.d/lisp")
(require 'org-ssg)

(defun xah-reformat-lines (&optional Width)
  "Reformat current block or selection into short lines or 1 long line.
When called for the first time, change to one line. Second call change it to multi-lines. Repeated call toggles.
If `universal-argument' is called first, ask user to type max length of line. By default, it is 80.

Note: this command is different from emacs `fill-region' or `fill-paragraph'.
This command never adds or delete non-whitespace chars. It only exchange whitespace sequence.

URL `http://xahlee.info/emacs/emacs/emacs_reformat_lines.html'
Created: 2016
Version: 2025-08-29"
  (interactive
   (list
    (if current-prefix-arg
        (cond
         ((not (numberp current-prefix-arg)) 80)
         (t (prefix-numeric-value current-prefix-arg)))
      80)))
  ;; This symbol has a property 'is-long-p, the possible values are t and nil. This property is used to easily determine whether to compact or uncompact, when this command is called again
  (let ((xisLong (if (eq last-command this-command) (get this-command 'is-long-p) nil))
        (xwidth (if Width Width 80))
        xbeg xend)
    (seq-setq (xbeg xend) (if (region-active-p) (list (region-beginning) (region-end)) (list (save-excursion (if (re-search-backward "\n[ \t]*\n" nil 1) (match-end 0) (point))) (save-excursion (if (re-search-forward "\n[ \t]*\n" nil 1) (match-beginning 0) (point))))))
    (if xisLong
        (save-excursion
          (save-restriction
            (narrow-to-region xbeg xend)
            (goto-char (point-min))
            (while (re-search-forward " +" nil 1)
              (when (> (- (point) (line-beginning-position)) xwidth)
                (replace-match "\n")))))
      (save-excursion
        (save-restriction
          (narrow-to-region xbeg xend)
          (goto-char (point-min))
          (while (re-search-forward "[ \n\t]+" xend :move) (replace-match " ")))))
    (put this-command 'is-long-p (not xisLong))))

(defun xah-python-format-buffer ()
  "Format the current buffer file.
Calls the external program “black”.
Buffer is saved first.

URL `http://xahlee.info/emacs/emacs/xah_format_python_code.html'
Created: 2022-08-25
Version: 2025-07-08"
  (interactive)
  (when (not (buffer-file-name)) (user-error "buffer %s is not a file." (buffer-name)))
  (when (buffer-modified-p) (save-buffer))
  (let ((xoutbuf (get-buffer-create "*xah-python-format output*"))
        xexitstatus)
    (with-current-buffer xoutbuf (erase-buffer))
    (setq xexitstatus (call-process "black" nil xoutbuf nil buffer-file-name "-q"))
    (if (eq 0 xexitstatus)
        (progn
          (kill-buffer xoutbuf)
          (revert-buffer t t t))
      (progn
        (display-buffer xoutbuf)
        (error "error xah-python-format")))))

					; Tweak the looks of Emacs

;; Those three belong in the early-init.el, but I am putting them here
;; for convenience.  If the early-init.el exists in the same directory
;; as the init.el, then Emacs will read-evaluate it before moving to
;; the init.el.
(menu-bar-mode 0)
(scroll-bar-mode 0)
(tool-bar-mode 0)

(let ((mono-spaced-font "Monospace")
      (proportionately-spaced-font "Sans"))
  (set-face-attribute 'default nil :family mono-spaced-font :height 100)
  (set-face-attribute 'fixed-pitch nil :family mono-spaced-font :height 1.0)
  (set-face-attribute 'variable-pitch nil :family proportionately-spaced-font :height 1.0))

;; Set Ubuntu Nerd Font 14pt as default for all frames/buffers
(set-face-attribute 'default nil :font "Ubuntu Nerd Font-14")

;; Ensure new frames also use it (important for daemon/users of emacsclient)
(add-to-list 'default-frame-alist '(font . "Ubuntu Nerd Font-14"))

;; Remember to do M-x and run `nerd-icons-install-fonts' to get the
;; font files.  Then restart Emacs to see the effect.
(use-package nerd-icons
  :straight t)

(use-package nerd-icons-completion
  :straight t
  :after marginalia
  :config
  (add-hook 'marginalia-mode-hook #'nerd-icons-completion-marginalia-setup))

(use-package nerd-icons-corfu
  :straight t
  :after corfu
  :config
  (add-to-list 'corfu-margin-formatters #'nerd-icons-corfu-formatter))

(use-package nerd-icons-dired
  :straight t
  :hook
  (dired-mode . nerd-icons-dired-mode))

					; Configure the minibuffer and completions

(when (fboundp 'electric-indent-mode)
  (electric-indent-mode -1))

(use-package vertico
  :straight t
  :hook (after-init . vertico-mode))

(use-package marginalia
  :straight t
  :hook (after-init . marginalia-mode))

(use-package orderless
  :straight t
  :config
  (setq completion-styles '(orderless basic))
  (setq completion-category-defaults nil)
  (setq completion-category-overrides nil))

(use-package savehist
  :straight nil ; it is built-in
  :hook (after-init . savehist-mode))

(use-package corfu
  :straight t
  :hook (after-init . global-corfu-mode)
  :bind (:map corfu-map ("<tab>" . corfu-complete))
  :config
  (setq tab-always-indent 'complete)
  (setq corfu-preview-current nil)
  (setq corfu-min-width 20)

  (setq corfu-popupinfo-delay '(1.25 . 0.5))
  (corfu-popupinfo-mode 1) ; shows documentation after `corfu-popupinfo-delay'

  ;; Sort by input history (no need to modify `corfu-sort-function').
  (with-eval-after-load 'savehist
    (corfu-history-mode 1)
    (add-to-list 'savehist-additional-variables 'corfu-history)))

(setq split-height-threshold nil)
(setq split-width-threshold 0)

;; Enable visual-line-mode for all buffers (global setting)
(global-visual-line-mode t)

					; The file manager (Dired)

(use-package dired
  :straight nil
  :commands (dired)
  :hook
  ((dired-mode . dired-hide-details-mode)
   (dired-mode . hl-line-mode))
  :config
  (setq dired-recursive-copies 'always)
  (setq dired-recursive-deletes 'always)
  (setq delete-by-moving-to-trash t)
  (setq dired-dwim-target t))

(use-package dired-subtree
  :straight t
  :after dired
  :bind
  ( :map dired-mode-map
    ("<tab>" . dired-subtree-toggle)
    ("TAB" . dired-subtree-toggle)
    ("<backtab>" . dired-subtree-remove)
    ("S-TAB" . dired-subtree-remove))
  :config
  (setq dired-subtree-use-backgrounds nil))

(when (>= emacs-major-version 28)
  (setq dired-kill-when-opening-new-dired-buffer t))

(when (< emacs-major-version 28)
  (progn
    (define-key dired-mode-map (kbd "RET") 'dired-find-alternate-file) ; was dired-advertised-find-file
    (define-key dired-mode-map (kbd "^") (lambda () (interactive) (find-alternate-file ".."))) ; was dired-up-directory
    ))

(use-package trashed
  :straight t
  :commands (trashed)
  :config
  (setq trashed-action-confirmer 'y-or-n-p)
  (setq trashed-use-header-line t)
  (setq trashed-sort-key '("Date deleted" . t))
  (setq trashed-date-format "%Y-%m-%d %H:%M:%S"))

(defun xah-dired-sort ()
  "Sort dired dir listing in different ways.
Prompt for a choice.
Works in linux, MacOS, Microsoft Windows.

URL `http://xahlee.info/emacs/emacs/dired_sort.html'
Created: 2018-12-23
Version: 2025-01-05"
  (interactive)
  (let ((xmenu '(("date" . "-Al -t")
                 ("size" . "-Al -S")
                 ("name" . "-Al ")
                 ("dir" . "-Al --group-directories-first")))
        xsortBy)
    (setq xsortBy (completing-read "Sort by (default date):" xmenu nil t nil nil (caar xmenu)))
    (dired-sort-other (cdr (assoc xsortBy xmenu)))))

(defvar xah-move-to-target-dirs
  '(
    ;;
    ("Documents" . "~/Documents/")
    ("Pictures" . "~/Pictures/")
    ("Desktop" . "~/Desktop/")
    ("Downloads" . "~/Downloads/"))
  "An alist of dir paths for `xah-move-file-to-dir' to move file to.
Each key is string for prompt, each value is dir path.
Dir path must end in a slash.
Useful is to create a bunch of dir, named family, travel, papers, work, etc, to sort photos into.
URL `http://xahlee.info/emacs/emacs/move_file_to_dir.html'")

(defun arrayify (start end quote)
  "Turn strings on newlines into a QUOTEd, comma-separated one-liner."
  (interactive "r\nMQuote: ")
  (let ((insertion
         (mapconcat
          (lambda (x) (format "%s%s%s" quote x quote))
          (split-string (buffer-substring start end)) ", ")))
    (delete-region start end)
    (insert insertion)))

					; Themes
(add-to-list 'custom-theme-load-path "/Users/muneer78/.emacs.d/themes/")
(load-theme 'synthwave)

(setq org-alphabetical-lists t)

;; Explicitly load required exporters
(require 'ox-html)
(require 'ox-latex)
(require 'ox-ascii)
(require 'ox-md)

;; Epub
(add-to-list 'auto-mode-alist '("\\.epub\\'" . nov-mode))

;;csv-mode

(defun my/csv-mode-setup ()
  "Custom settings for `csv-mode'."
  ;; Enable visual alignment of fields on the fly
  (csv-align-mode t)
  ;; Prevent long lines from wrapping, requiring horizontal scrolling
  (toggle-truncate-lines 1)
  ;; Optionally, enable the header line display
  (csv-header-line t)
  ;; Add automatic separator guessing (useful for tsv, etc.)
  (csv-guess-set-separator)
  )

;; Add the custom setup function to the csv-mode hook
(add-hook 'csv-mode-hook 'my/csv-mode-setup)

(setq csv-separators '(";" "," "\t" "|"))

;;elfeed

(use-package elfeed
  :straight t
  :bind ("C-x w" . elfeed) ; Quick shortcut to open elfeed
  :config
  (setq elfeed-db-directory (expand-file-name "elfeed" user-emacs-directory)))

(use-package elfeed-org
  :straight t
  :config
  (elfeed-org)
  ;; REPLACE the path below with the actual path to your feeds.org file
  (setq rmh-elfeed-org-files (list "/Users/muneer78/.emacs.d/elfeed.org")))

(setq elfeed-show-entry-switch #'elfeed-display-buffer)

(defun elfeed-display-buffer (buf &optional act)
  (pop-to-buffer buf)
  (set-window-text-height (get-buffer-window) (round (* 0.7 (frame-height)))))

(setq elfeed-search-title-max-width 120)  ; <-- add this line

(add-hook 'elfeed-new-entry-hook #'elfeed-declickbait-entry)

(defun elfeed-declickbait-entry (entry)
  (let ((title (elfeed-entry-title entry)))
    (setf (elfeed-meta entry :title)
          (elfeed-title-transform title))))

(defun elfeed-title-transform (title)
  "Declickbait string TITLE."
  (let* ((trim "\\(?:\\(?:\\.\\.\\.\\|[!?]\\)+\\)")
         (arr (split-string title nil t trim))
         (s-table (copy-syntax-table)))
    (modify-syntax-entry ?\' "w" s-table)
    (with-syntax-table s-table
      (mapconcat (lambda (word)
                   (cond
                    ((member word '("AND" "OR" "IF" "ON" "IT" "TO"
                                    "A" "OF" "VS" "IN" "FOR" "WAS"
                                    "IS" "BE"))
                     (downcase word))
                    ((member word '("WE" "DAY" "HOW" "WHY" "NOW" "OLD"
                                    "NEW" "MY" "TOO" "GOT" "GET" "THE"
                                    "ONE" "DO" "YOU"))
                     (capitalize word))
                    ((> (length word) 3) (capitalize word))
                    (t word)))
                 arr " "))))

(defun elfeed-show-eww-open (&optional use-generic-p)
  "open with eww"
  (interactive "P")
  (let ((browse-url-browser-function #'eww-browse-url))
    (elfeed-show-visit use-generic-p)))

(defun elfeed-search-eww-open (&optional use-generic-p)
  "open with eww"
  (interactive "P")
  (let ((browse-url-browser-function #'eww-browse-url))
    (elfeed-search-browse-url use-generic-p)))

(define-key elfeed-show-mode-map (kbd "B") 'elfeed-show-eww-open)
(define-key elfeed-search-mode-map (kbd "S") 'elfeed-search-eww-open)

(defun my-elfeed-search-other-window ()
  "Browse `elfeed' entry in the other window.
Credit: https://protesilaos.com/dotemacs"
  (interactive)
  (let* ((entry (if (eq major-mode 'elfeed-show-mode)
                    elfeed-show-entry
                  (elfeed-search-selected :ignore-region)))
         (link (elfeed-entry-link entry))
         (win (selected-window)))
    (with-current-buffer (get-buffer "*elfeed-search*")
      (unless (one-window-p)              ; experimental
        (delete-other-windows win))
      (split-window-right)
      (other-window 1)
      (evil-window-increase-width 10)
      (elfeed-search-show-entry entry))))

(defun my-elfeed-kill-buffer-and-window ()
  "Do-what-I-mean way to handle `elfeed' windows and buffers.
When in an entry buffer, kill the buffer and return to the Search view.
If the entry is in its own window, delete it as well.
When in the search view, close all other windows, else kill the buffer."
  (interactive)
  (let ((win (selected-window)))
    (cond ((eq major-mode 'elfeed-show-mode)
           (elfeed-kill-buffer)
           (unless (one-window-p) (delete-window win))
           (switch-to-buffer "*elfeed-search*"))
          ((eq major-mode 'elfeed-search-mode)
           (if (one-window-p)
               (progn
                 (elfeed-search-quit-window)
                 (kill-buffer "*elfeed-search*")
                 (kill-buffer "*elfeed-log*")
                 (kill-buffer "elfeed-list.org")
                 (tab-bar-close-tab))
             (delete-other-windows win))))))

;; misc

(defun xah-search-current-word ()
  "Call `isearch' on current word or selection.
“word” here is A to Z, a to z, and hyphen [-] and lowline [_], independent of syntax table.

URL `http://xahlee.info/emacs/emacs/emacs_search_current_word.html'
Created: 2010-05-29
Version: 2025-09-15"
  (interactive)
  (let (xbeg xend)
    (if (region-active-p)
        (setq xbeg (region-beginning) xend (region-end))
      (save-excursion
        (skip-chars-backward "-_A-Za-z0-9")
        (setq xbeg (point))
        (right-char)
        (skip-chars-forward "-_A-Za-z0-9")
        (setq xend (point))))
    (deactivate-mark)
    (when (< xbeg (point)) (goto-char xbeg))
    (isearch-mode t)
    (isearch-yank-string (buffer-substring-no-properties xbeg xend))))

(defun xah-upcase-sentence ()
  "Upcase first letters of sentences of current block or selection.

URL `http://xahlee.info/emacs/emacs/emacs_upcase_sentence.html'
Created: 2020-12-08
Version: 2025-03-25"
  (interactive)
  (let (xbeg xend)
    (seq-setq (xbeg xend) (if (region-active-p) (list (region-beginning) (region-end)) (list (save-excursion (if (re-search-backward "\n[ \t]*\n" nil 1) (match-end 0) (point))) (save-excursion (if (re-search-forward "\n[ \t]*\n" nil 1) (match-beginning 0) (point))))))
    (save-restriction
      (narrow-to-region xbeg xend)
      (let ((case-fold-search nil))
        ;; after period or question mark or exclamation
        (goto-char (point-min))
        (while (re-search-forward "\\(\\.\\|\\?\\|!\\)[ \n]+ *\\([a-z]\\)" nil 1)
          (upcase-region (match-beginning 2) (match-end 2))
          (overlay-put (make-overlay (match-beginning 2) (match-end 2)) 'face 'highlight))
        ;; after a blank line, after a bullet, or beginning of buffer
        (goto-char (point-min))
        (while (re-search-forward "\\(\\`\\|• \\|\n\n\\)\\([a-z]\\)" nil 1)
          (upcase-region (match-beginning 2) (match-end 2))
          (overlay-put (make-overlay (match-beginning 2) (match-end 2)) 'face 'highlight))
        ;; for HTML. first letter after tag
        (when
            (or
             (eq major-mode 'xah-html-mode)
             (eq major-mode 'html-mode)
             (eq major-mode 'sgml-mode)
             (eq major-mode 'nxml-mode)
             (eq major-mode 'xml-mode)
             (eq major-mode 'mhtml-mode))
          (goto-char (point-min))
          (while
              (re-search-forward "\\(<title>[ \n]?\\|<h[1-6]>[ \n]?\\|<p>[ \n]?\\|<li>[ \n]?\\|<dd>[ \n]?\\|<td>[ \n]?\\|<br ?/?>[ \n]?\\|<figcaption>[ \n]?\\)\\([a-z]\\)" nil 1)
            (upcase-region (match-beginning 2) (match-end 2))
            (overlay-put (make-overlay (match-beginning 2) (match-end 2)) 'face 'highlight))))
      (goto-char (point-max)))
    (skip-chars-forward " \n\t")))

;; yasnippet
(use-package yasnippet
  :config
  (yas-global-mode 1)
  (add-hook 'yas-minor-mode-hook
            (lambda ()
              (yas-activate-extra-mode 'text-mode))))

(setq yas-snippet-dirs '("~/.emacs.d/snippets"))

;; --- Python (tree-sitter) ---
(use-package python
  :mode ("\\.py\\'" . python-ts-mode)
  :custom (python-shell-interpreter "python3"))

(setq lsp-python-provider 'pyright)

;; --- pet: auto-detect uv's .venv ---
(use-package pet
  :config
  (add-hook 'python-ts-mode-hook
	    (lambda ()
	      (setq-local python-shell-interpreter
			  (pet-executable-find "python"))
	      (setq-local python-shell-interpreter-args "-i")
	      (setq-local lsp-pyright-python-executable-cmd
			  (pet-executable-find "python")))))

;; --- LSP + Pyright ---
(use-package lsp-mode
  :custom (lsp-keymap-prefix "C-c l"))

(use-package lsp-ui
  :hook (lsp-mode . lsp-ui-mode)
  :custom
  (lsp-ui-doc-show-with-cursor t)
  (lsp-ui-sideline-show-diagnostics t))

(use-package lsp-pyright
  :hook (python-ts-mode . (lambda ()
			    (require 'lsp-pyright) (lsp))))

;; --- Completion ---
(use-package corfu
  :init (global-corfu-mode)
  :custom (corfu-auto t))

;; --- Format on save: ruff via uv run ---
(use-package apheleia
  :config
  (apheleia-global-mode +1)
  (setf (alist-get 'python-ts-mode apheleia-mode-alist)
        '(ruff-format ruff-isort))
  (setf (alist-get 'ruff-format apheleia-formatters)
        '("uv" "run" "ruff" "format" "-"))
  (setf (alist-get 'ruff-isort apheleia-formatters)
        '("uv" "run" "ruff" "check" "--select=I" "--fix" "-")))

;; --- Run file with uv run ---
(defun my/uv-run-file ()
  "Run the current Python file with uv run."
  (interactive)
  (compile (format "uv run python %s"
		   (shell-quote-argument (buffer-file-name)))))
(add-hook 'python-ts-mode-hook
	  (lambda ()
	    (local-set-key (kbd "C-c C-r") #'my/uv-run-file)))

;; --- Debugger (debugpy via uv) ---
(use-package dap-mode
  :after lsp-mode
  :config
  (require 'dap-python)
  (setq dap-python-debugger 'debugpy)
  (setq dap-python-executable
	(lambda () (list "uv" "run" "python")))
  (dap-auto-configure-mode))

;; --- Which-key + Projectile ---
(use-package which-key
  :config (which-key-mode))
(use-package projectile
  :init (projectile-mode +1)
  :bind-keymap ("C-c p" . projectile-command-map))
