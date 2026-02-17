(setq custom-file (locate-user-emacs-file "custom.el"))
(load custom-file :no-error-if-file-is-missing)

; Set up the package manager

(require 'package)
(package-initialize)

(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/"))

(when (< emacs-major-version 29)
  (unless (package-installed-p 'use-package)
    (unless package-archive-contents
      (package-refresh-contents))
    (package-install 'use-package)))

; Basic behaviour

(setq inhibit-splash-screen t)
(setq inhibit-startup-message t)

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

(setq org-auto-align-tags t)

(setq org-startup-folded t)

(setq org-hide-emphasis-markers t)


 '(org-agenda-date ((t (:height 1.1))))
 '(org-agenda-date-weekend ((t (:height 1.0))))
 '(org-agenda-date-today ((t (:height 1.0 :weight bold))))

(defun my-org-align-all-tags ()
  "Realign all Org tags in the current buffer."
  (interactive)
  (org-map-entries
   (lambda ()
     (org-set-tags-command))))

;; Define home and work org settings
(defvar org-home-directory "/Users/muneer78/files/emacs/"
  "Directory for personal org files.")

(defvar org-home-default-notes-file "/Users/muneer78/files/emacs/todos.org"
  "Default notes file for home context.")

(defvar org-work-directory "/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Documents/GitHub/localwork/org"
  "Directory for work org files.")

(defvar org-work-default-notes-file "/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Documents/GitHub/localwork/notes.org"
  "Default notes file for work context.")

(defvar current-org-context 'home
  "Current org context: 'home or 'work.")

;; Function to set org agenda files based on context
(defun set-org-context (context)
  "Set org-agenda-files to CONTEXT (either 'home or 'work)."
  (interactive (list (intern (completing-read "Select context: " '("home" "work")))))
  (setq current-org-context context)
  (cond
   ((eq context 'home)
    (setq org-directory org-home-directory)
    (setq org-agenda-files (list org-home-directory))
    (setq org-default-notes-file org-home-default-notes-file))
   ((eq context 'work)
    (setq org-directory org-work-directory)
    (setq org-agenda-files (list org-work-directory))
    (setq org-default-notes-file org-work-default-notes-file))
   (t (error "Unknown context: %s" context)))
  (message "Switched to %s org context: %s"
           context
           org-directory))

;; Convenience functions
(defun org-context-home ()
  "Switch to home org context."
  (interactive)
  (set-org-context 'home))

(defun org-context-work ()
  "Switch to work org context."
  (interactive)
  (set-org-context 'work))

;; Keybindings
(global-set-key (kbd "C-c o h") #'org-context-home)
(global-set-key (kbd "C-c o w") #'org-context-work)

;; Initialize with work context on startup (since you had work paths configured)
(set-org-context 'home)

;; Do not dim blocked tasks
(setq org-agenda-dim-blocked-tasks nil)

;; Compact the block agenda view
(setq org-agenda-compact-blocks t)

(setq org-export-with-toc nil)

(setq org-export-with-sub-superscripts nil)

(defun org-insert-custom-timestamp ()  
  (interactive)  
  (insert (format-time-string "%Y%m%d")))  

;; I use C-c t to start capture mode
(global-set-key (kbd "C-c t") 'org-insert-custom-timestamp)


;; I use C-c c to start capture mode
(global-set-key (kbd "C-c c") 'org-capture)

;; Capture templates for: TODO tasks, Notes, appointments, phone calls, meetings, and org-protocol
(setq org-capture-templates
      (quote (("t" "todo" entry (file "/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Documents/GitHub/localwork/org/todo.org")
               "* TODO %?\n%U\n%a\n" :clock-in t :clock-resume t)
              ("r" "respond" entry (file "/Users/.../refile.org")
               "* NEXT Respond to %:from on %:subject\nSCHEDULED: %t\n%U\n%a\n" :clock-in t :clock-resume t :immediate-finish t)
              ("n" "note" entry (file "/Users/.../refile.org")
               "* %? :NOTE:\n%U\n%a\n" :clock-in t :clock-resume t))))

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

(defun my/org-copy-subtrees-containing-dtd ()
  "Copy all Org subtrees containing the string 'dtd' into a new buffer."
  (interactive)
  (let ((outbuf (generate-new-buffer "*org-dtd-matches*"))
        (matches '()))
    (org-map-entries
     (lambda ()
       (let* ((beg (org-entry-beginning-position))
              (end (org-entry-end-position))
              (text (buffer-substring-no-properties beg end)))
         (when (string-match-p "dtd" text)
           (push text matches))))
     nil 'file)

    (with-current-buffer outbuf
      (org-mode)
      (insert (string-join (nreverse matches) "\n\n"))
      (goto-char (point-min)))

    (switch-to-buffer outbuf)))

;; org babel

;; active Babel languages
(org-babel-do-load-languages
 'org-babel-load-languages
 '((R . t)
   (python . t)))

(defun org-sort-on-save ()
  "Sort org entries by scheduled date when saving."
  (when (and (eq major-mode 'org-mode)
             (buffer-file-name))
    (org-sort-entries-by-scheduled)))

;; Add to save hook
(add-hook 'before-save-hook #'org-sort-on-save)

(setq org-agenda-skip-scheduled-if-done t)
(setq org-agenda-skip-deadline-if-done t)
(setq org-agenda-skip-timestamp-if-done t)
(setq org-agenda-skip-function-global '(org-agenda-skip-entry-if 'todo 'done))
(setq org-agenda-span 'month)

;; Python dev
(add-hook 'after-init-hook #'global-flycheck-mode)

(use-package reformatter
  :ensure t
  :config
  (reformatter-define dd/ruff-format
    :program "uvx"
    :args `("ruff" "format" "--stdin-filename" ,buffer-file-name "-"))
  (reformatter-define dd/ruff-sort
    :program "uvx"
    :args `("ruff" "check" "--select" "I" "--fix" "--stdin-filename" ,buffer-file-name "-")))

(defun dd/python-init ()
  (let* ((project (project-current))
         (project-root (when project (project-root project)))
         (venv-path (when project-root
                      (expand-file-name ".venv" project-root))))
    (when (and venv-path (file-directory-p venv-path))
      (make-local-variable 'pyvenv-virtual-env)
      (pyvenv-activate venv-path))
    (dd/ruff-format-on-save-mode +1)
    (dd/ruff-sort-on-save-mode +1)))

(add-hook 'python-base-mode-hook #'dd/python-init)

(use-package pet
  :config
  (add-hook 'python-base-mode-hook 'pet-mode -10))

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
  :ensure t)

(use-package nerd-icons-completion
  :ensure t
  :after marginalia
  :config
  (add-hook 'marginalia-mode-hook #'nerd-icons-completion-marginalia-setup))

(use-package nerd-icons-corfu
  :ensure t
  :after corfu
  :config
  (add-to-list 'corfu-margin-formatters #'nerd-icons-corfu-formatter))

(use-package nerd-icons-dired
  :ensure t
  :hook
  (dired-mode . nerd-icons-dired-mode))

; Configure the minibuffer and completions

(when (fboundp 'electric-indent-mode)
  (electric-indent-mode -1))

(use-package vertico
  :ensure t
  :hook (after-init . vertico-mode))

(use-package marginalia
  :ensure t
  :hook (after-init . marginalia-mode))

(use-package orderless
  :ensure t
  :config
  (setq completion-styles '(orderless basic))
  (setq completion-category-defaults nil)
  (setq completion-category-overrides nil))

(use-package savehist
  :ensure nil ; it is built-in
  :hook (after-init . savehist-mode))

(use-package corfu
  :ensure t
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
  :ensure nil
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
  :ensure t
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
  :ensure t
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

(add-to-list 'custom-theme-load-path "/Users/mahmad/.emacs.d/themes/")
(add-to-list 'custom-theme-load-path "/Users/muneer78/.emacs.d/themes/")


(load-theme 'synthwave)

(add-hook 'org-mode-hook #'my/org-mode-hook)

(setq org-alphabetical-lists t)

;; Explicitly load required exporters
(require 'ox-html)
(require 'ox-latex)
(require 'ox-ascii)
(require 'ox-md)

(with-eval-after-load 'ox-md
  (defun my-org-md-link (link desc info)
    "Format LINK with optional DESC for Markdown export without <> around URLs."
    (let* ((raw (org-element-property :raw-link link))
           (url (org-export-data (org-element-property :raw-link link) info)))
      (cond
       ;; Link with description → [desc](url)
       (desc
        (format "[%s](%s)" desc url))
       ;; Plain URL → just the URL
       (t url))))

  (advice-add 'org-md-link :override #'my-org-md-link))

(require 'ox-md)

(defun my-jira-item (item contents info)
  "Render list ITEM as Jira-style nested asterisks (Jira format)."
  (let* ((level 1)
         (parent (org-export-get-parent item)))
    ;; count list nesting
    (while parent
      (when (eq (org-element-type parent) 'plain-list)
        (setq level (1+ level)))
      (setq parent (org-export-get-parent parent)))
    (concat (make-string level ?*)
            " "
            (org-trim contents)
            "\n")))

(org-export-define-derived-backend 'jira-md 'md
  :translate-alist
  '((item . my-jira-item)
    (plain-list . (lambda (_ c _) c))))

(defun org-export-to-jira-markdown ()
  "Export region if active, otherwise whole buffer, to Jira-flavored Markdown.
Result is copied to clipboard."
  (interactive)
  (let* ((text (if (use-region-p)
                   (buffer-substring-no-properties
                    (region-beginning)
                    (region-end))
                 (buffer-substring-no-properties
                  (point-min)
                  (point-max))))
         (output (org-export-string-as text 'jira-md t)))
    (kill-new output)
    (message "Jira markdown copied to clipboard")))

(with-eval-after-load 'org
  (define-key org-mode-map (kbd "C-c j") #'org-export-to-jira-markdown))

;; NEW: Abbrev mode configuration
;; Enable abbrev-mode globally
(setq-default abbrev-mode t)

(defun my-insert-timestamp ()
  (interactive)
  (insert (format-time-string "%Y%m%d")))

;; Define abbreviations
(define-abbrev global-abbrev-table "timestamp" "" 'my-insert-timestamp)

;; Save abbrevs when Emacs exits
(setq save-abbrevs 'silently)

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
  :ensure t
  :bind ("C-x w" . elfeed) ; Quick shortcut to open elfeed
  :config
  (setq elfeed-db-directory (expand-file-name "elfeed" user-emacs-directory)))

(use-package elfeed-org
  :ensure t
  :config
  (elfeed-org)
  ;; REPLACE the path below with the actual path to your feeds.org file
  (setq rmh-elfeed-org-files (list "/Users/muneer78/.emacs.d/elfeed.org")))

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

;;org-ssg-generator

;;; org-ssg.el --- Static Site Generator for Org-mode files -*- lexical-binding: t; -*-

;; Author: Your Name
;; Version: 1.0
;; Package-Requires: ((emacs "27.1"))

;;; Commentary:
;; This package converts Org-mode files to HTML for a static site using org-publish.
;; It splits multi-heading org files and generates a complete static site.

;;; Code:

(require 'org)
(require 'ox-html)
(require 'ox-publish)
(require 'seq)
(require 'subr-x)

;;; Configuration Variables

(defvar org-ssg-content-dir "~/files/emacs/content/"
  "Directory containing org-mode content files.")

(defvar org-ssg-output-dir "~/Documents/GitHub/mun-ssg/site-2"
  "Directory for generated HTML files.")

(defvar org-ssg-split-dir nil
  "Directory for split org files. Automatically set to content-dir/split/")

(defvar org-ssg-site-config
  '((name . "Encyclopedia Muneerica")
    (description . "A YungMun Joint")
    (baseurl . "")
    (url . "")
    (github . "muneer78")
    (twitter . "reenum"))
  "Site configuration alist.")

;;; Utility Functions

(defun org-ssg-slugify (text)
  "Convert TEXT to URL-safe slug."
  (let ((slug (downcase text)))
    (setq slug (replace-regexp-in-string "[^a-z0-9-]" "-" slug))
    (setq slug (replace-regexp-in-string "-+" "-" slug))
    (string-trim slug "-")))

(defun org-ssg-extract-date-from-heading (heading)
  "Extract date from HEADING text in format YYYY-MM-DD."
  (when (string-match "\\([0-9]\\{4\\}\\)-\\([0-9]\\{2\\}\\)-\\([0-9]\\{2\\}\\)" heading)
    (concat (match-string 1 heading)
            (match-string 2 heading)
            (match-string 3 heading))))

;;; Publishing Functions

(defun org-ssg-split-headings (plist filename pub-dir)
  "Split an Org file into separate files, each corresponding to a top-level heading.

Each file name is based on the heading title. PLIST is the property list for the
publishing process, FILENAME is the input Org file, and PUB-DIR is the publishing
directory."
  (let ((heading-level 1)
        (file-count 0)
        sections
        heading-positions)
    
    ;; First pass: collect heading positions and metadata
    (with-temp-buffer
      (insert-file-contents filename)
      (goto-char (point-min))
      
      ;; Collect all heading positions first
      (while (re-search-forward (format "^\\*\\{%d\\} \\(.*\\)" heading-level) nil t)
        (let* ((heading-line (match-string 1))
               (heading-start (match-beginning 0))
               ;; Split heading into title and tags
               (heading-parts (if (string-match "\\(.*?\\)[ \t]+\\(:[[:alnum:]_@#%:]+:\\)[ \t]*$" heading-line)
                                  (list (match-string 1 heading-line)
                                        (match-string 2 heading-line))
                                (list heading-line nil)))
               (heading-title (string-trim (car heading-parts))))
          (push (list heading-start heading-title) heading-positions)))
      
      ;; Reverse to get chronological order
      (setq heading-positions (nreverse heading-positions))
      
      ;; Second pass: extract content for each heading
      (dotimes (i (length heading-positions))
        (let* ((current-heading (nth i heading-positions))
               (next-heading (nth (1+ i) heading-positions))
               (heading-start (car current-heading))
               (heading-title (cadr current-heading))
               (section-end (if next-heading
                                (car next-heading)
                              (point-max)))
               ;; Extract the content as a string
               (content (buffer-substring-no-properties heading-start section-end))
               ;; Sanitize title for filename
               (sanitized-title (replace-regexp-in-string "[^a-zA-Z0-9_-]" "-" heading-title))
               ;; Extract date from heading for filename prefix
               (date-prefix (org-ssg-extract-date-from-heading heading-title)))
          
          ;; Only proceed if sanitized title exists and is valid
          (when (and sanitized-title (not (string-empty-p sanitized-title)))
            (let ((output-file (if date-prefix
                                   (format "%s-%s.org" date-prefix sanitized-title)
                                 (format "%s.org" sanitized-title))))
              (push (cons output-file content) sections))))))
    
    ;; Third pass: write all sections to files
    (dolist (section (nreverse sections))
      (let ((output-file (expand-file-name (car section) pub-dir))
            (content (cdr section)))
        (with-temp-file output-file
          (insert content))
        (setq file-count (1+ file-count))
        (message "Wrote %s" output-file)))
    
    (message "Split %s into %d files" filename file-count)
    ;; Return nil to indicate successful processing
    nil))

;;; Sitemap Functions

(defun org-ssg-sitemap-format-entry (entry style project)
  "Format sitemap ENTRY for PROJECT with STYLE."
  (let* ((file (org-publish-find-title entry project))
         (date (org-publish-find-date entry project)))
    (format "[[file:%s][%s]] - %s"
            entry
            file
            (format-time-string "%Y-%m-%d" date))))

(defun org-ssg-sitemap-function (title list)
  "Generate sitemap with TITLE and LIST of entries."
  (concat "#+TITLE: " title "\n\n"
          (org-list-to-org list)))

;;; Publishing Configuration

;;;###autoload
(defun org-ssg-setup-publish ()
  "Setup org-publish-project-alist for org-ssg."
  (interactive)
  (setq org-ssg-split-dir (expand-file-name "split" org-ssg-content-dir))
  
  ;; Ensure directories exist
  (make-directory org-ssg-split-dir t)
  (make-directory org-ssg-output-dir t)
  
  (setq org-publish-project-alist
        `(("split-posts"
           :base-directory ,org-ssg-content-dir
           :base-extension "org"
           :publishing-directory ,org-ssg-split-dir
           :exclude ".*"
           :include ("posts.org" "all.org" "index.org")
           :publishing-function org-ssg-split-headings
           :recursive nil)
          
          ("blog-posts"
           :base-directory ,org-ssg-split-dir
           :base-extension "org"
           :publishing-directory ,(expand-file-name "posts" org-ssg-output-dir)
           :publishing-function org-html-publish-to-html
           :recursive t
           :section-numbers nil
           :with-toc nil
           :html-preamble t
           :html-postamble t
           :auto-sitemap t
           :sitemap-filename "index.org"
           :sitemap-title ,(alist-get 'name org-ssg-site-config)
           :sitemap-style list
           :sitemap-sort-files anti-chronologically
           :sitemap-format-entry org-ssg-sitemap-format-entry
           :sitemap-function org-ssg-sitemap-function
           :html-head-include-default-style nil
           :html-head-include-scripts nil
           :html-head "<link rel=\"stylesheet\" href=\"/static/css/style.css\" type=\"text/css\"/>")
          
          ("static-files"
           :base-directory ,(expand-file-name "static" default-directory)
           :base-extension "css\\|js\\|jpg\\|gif\\|png\\|jpeg\\|svg\\|webp"
           :recursive t
           :publishing-directory ,(expand-file-name "static" org-ssg-output-dir)
           :publishing-function org-publish-attachment)
          
          ("org-ssg"
           :components ("split-posts" "blog-posts" "static-files"))))
  
  (message "org-publish configuration set up successfully"))

;;;###autoload
(defun org-ssg-publish ()
  "Publish the site using org-publish."
  (interactive)
  (org-ssg-setup-publish)
  (message "Publishing org-ssg project...")
  (org-publish "org-ssg" nil)
  (message "Site published successfully!")
  (message "Output directory: %s" org-ssg-output-dir))

;;;###autoload
(defun org-ssg-publish-force ()
  "Force publish the site, regenerating all files."
  (interactive)
  (org-ssg-setup-publish)
  (message "Force publishing org-ssg project...")
  (org-publish "org-ssg" t)
  (message "Site force published successfully!")
  (message "Output directory: %s" org-ssg-output-dir))

;;;###autoload
(defun org-ssg-clean ()
  "Clean the split directory and output directory."
  (interactive)
  (when org-ssg-split-dir
    (when (file-directory-p org-ssg-split-dir)
      (delete-directory org-ssg-split-dir t)
      (message "Cleaned split directory: %s" org-ssg-split-dir)))
  (when (file-directory-p org-ssg-output-dir)
    (delete-directory org-ssg-output-dir t)
    (message "Cleaned output directory: %s" org-ssg-output-dir)))

;;;###autoload
(defun org-ssg-preview ()
  "Preview the generated site in browser."
  (interactive)
  (let ((index-file (expand-file-name "posts/index.html" org-ssg-output-dir)))
    (if (file-exists-p index-file)
        (browse-url-of-file index-file)
      (message "No site to preview. Run org-ssg-publish first."))))

(provide 'org-ssg)
;;; org-ssg.el ends here
