import sys
import os
import difflib
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSplitter, QListWidget,
    QPushButton, QFileDialog, QVBoxLayout, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.Qsci import QsciScintilla, QsciLexerMarkdown

# Zeilen-Diff als Farbhintergrund (grün=insert, rot=delete, gelb=replace)
DIFF_COLORS = {
    'insert': (217,91,38),
    'delete': (0,163,224),
    'replace': (242,169,0),
}

def pad_and_merge(base_lines, conf_lines):
    sm = difflib.SequenceMatcher(None, base_lines, conf_lines)
    left, right, opmap = [], [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                left.append(base_lines[i1 + k])
                right.append(conf_lines[j1 + k])
                opmap.append('equal')
        elif tag == 'replace':
            maxlen = max(i2 - i1, j2 - j1)
            for k in range(maxlen):
                l = base_lines[i1 + k] if i1 + k < i2 else ''
                r = conf_lines[j1 + k] if j1 + k < j2 else ''
                left.append(l)
                right.append(r)
                opmap.append('replace')
        elif tag == 'insert':
            for k in range(j2 - j1):
                left.append('')
                right.append(conf_lines[j1 + k])
                opmap.append('insert')
        elif tag == 'delete':
            for k in range(i2 - i1):
                left.append(base_lines[i1 + k])
                right.append('')
                opmap.append('delete')
    return left, right, opmap

class DiffScintilla(QsciScintilla):
    def __init__(self, lines, opmap, which, editable=True):
        super().__init__()
        self.setUtf8(True)
        self.setReadOnly(not editable)
        self.setLexer(QsciLexerMarkdown(self))
        self.setText('\n'.join(lines))
        self.lines = lines
        self.opmap = opmap
        self.which = which
        self.markerDefine(QsciScintilla.MarkerSymbol.Background, 1)
        self.markerDefine(QsciScintilla.MarkerSymbol.Background, 2)
        self.markerDefine(QsciScintilla.MarkerSymbol.Background, 3)
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "00000")
        self.setAutoIndent(True)
        self.setWrapMode(QsciScintilla.WrapMode.WrapNone)
        self.apply_diff_markers()
    def apply_diff_markers(self):
        self.markerDeleteAll()
        # Dark mode friendly colors:
        # Marker 1 = insert (muted green)
        # Marker 2 = delete (muted red)
        # Marker 3 = replace (muted orange/yellow)
        self.setMarkerBackgroundColor(QColor(45, 85, 45), 1)    # dark green
        self.setMarkerBackgroundColor(QColor(85, 45, 45), 2)    # dark red
        self.setMarkerBackgroundColor(QColor(85, 70, 35), 3)    # dark orange/yellow
        for idx, tag in enumerate(self.opmap):
            if tag == 'equal':
                continue
            if tag == 'insert' and self.which == 'conflict':
                self.markerAdd(idx, 1)
            elif tag == 'delete' and self.which == 'base':
                self.markerAdd(idx, 2)
            elif tag == 'replace':
                self.markerAdd(idx, 3)

class ConflictResolver(QMainWindow):
    def __init__(self, base_folder=None):
        super().__init__()
        self.setWindowTitle("Syncthing Conflict Resolver (QScintilla)")
        self.resize(1350,850)
        self.root_dir = base_folder
        self.conflict_map = {}

        main_split = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(main_split)

        # Left: folder + file list
        left = QWidget(); lout = QVBoxLayout(left)
        btn = QPushButton("Select Folder..."); btn.clicked.connect(self.select_folder)
        self.list_widget = QListWidget(); lout.addWidget(btn); lout.addWidget(self.list_widget)
        left.setLayout(lout)
        main_split.addWidget(left); main_split.setStretchFactor(0,1)

        # Right: dynamic panes
        self.viewer = QSplitter(Qt.Orientation.Horizontal)
        main_split.addWidget(self.viewer); main_split.setStretchFactor(1,4)
        self.list_widget.currentItemChanged.connect(self.load_views)

        self.base_editor = None
        self.conf_editor = None

        if self.root_dir:
            self.scan_conflicts()

    def select_folder(self):
        d = QFileDialog.getExistingDirectory(self, "Select Folder")
        if d:
            self.root_dir=d; self.scan_conflicts()

    def scan_conflicts(self):
        self.conflict_map.clear()
        if not self.root_dir: return
        for dp,ds,fs in os.walk(self.root_dir):
            for f in fs:
                if '.sync-conflict-' in f:
                    idx=f.find('.sync-conflict-')
                    base=f[:idx]+os.path.splitext(f)[1]
                    bp=os.path.join(dp,base); cp=os.path.join(dp,f)
                    if os.path.exists(bp): self.conflict_map.setdefault(bp,[]).append(cp)
        self.list_widget.clear()
        for bp in sorted(self.conflict_map): self.list_widget.addItem(bp)

    def clear_views(self):
        for i in reversed(range(self.viewer.count())):
            w=self.viewer.widget(i); w.setParent(None)

    def load_views(self, cur, prev):
        if not cur: return
        bp=cur.text(); cps=sorted(self.conflict_map.get(bp,[]))
        self.clear_views()
        # load base
        try: base_text=open(bp,encoding='utf-8',errors='replace').read()
        except: base_text=''
        base_lines=base_text.splitlines()
        if not cps: return
        try: conf_text=open(cps[0],encoding='utf-8',errors='replace').read()
        except: conf_text=''
        conf_lines=conf_text.splitlines()
        left, right, opmap = pad_and_merge(base_lines, conf_lines)

        # --- Layout with QScintilla editors ---
        pane = QWidget(); lo = QHBoxLayout(pane); lo.setContentsMargins(0,0,0,0)

        # Base Editor
        vbox0 = QVBoxLayout(); vbox0.setContentsMargins(0,0,0,0)
        lbl = QPushButton(os.path.basename(bp)); lbl.setEnabled(False); vbox0.addWidget(lbl)
        self.base_editor = DiffScintilla(left, opmap, 'base', editable=True); vbox0.addWidget(self.base_editor)
        btn_accept = QPushButton("Accept base & delete conflicts"); btn_accept.clicked.connect(lambda:self.accept_and_cleanup(bp))
        vbox0.addWidget(btn_accept)
        w0 = QWidget(); w0.setLayout(vbox0); lo.addWidget(w0)

        # Conflict Editor
        vbox1 = QVBoxLayout(); vbox1.setContentsMargins(0,0,0,0)
        lbl2 = QPushButton(os.path.basename(cps[0])); lbl2.setEnabled(False); vbox1.addWidget(lbl2)
        self.conf_editor = DiffScintilla(right, opmap, 'conflict', editable=True); vbox1.addWidget(self.conf_editor)
        btn_accept_conf = QPushButton("Accept this conflict"); btn_accept_conf.clicked.connect(lambda:self.accept_version(cps[0],bp))
        btn_copy = QPushButton("Copy selection to base")
        btn_copy.clicked.connect(self.copy_to_base)
        vbox1.addWidget(btn_accept_conf); vbox1.addWidget(btn_copy)
        w1 = QWidget(); w1.setLayout(vbox1); lo.addWidget(w1)

        # Add older conflicts as additional (read-only) editors
        for cp in cps[1:]:
            try: ctext = open(cp, encoding='utf-8', errors='replace').read()
            except: ctext = ''
            q = DiffScintilla(ctext.splitlines(), [], '', editable=False)
            lo.addWidget(q)

        pane.setLayout(lo)
        self.viewer.addWidget(pane)

    def accept_and_cleanup(self, bp):
        # Save any edits to base
        if self.base_editor:
            open(bp,'w',encoding='utf-8').write(self.base_editor.text())
        # Remove conflict files
        for cp in self.conflict_map.get(bp, []):
            try: os.remove(cp)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not delete {cp}:\n{e}")
        # Update list & views, select next
        row = self.list_widget.currentRow()
        self.scan_conflicts()
        self.clear_views()
        if self.list_widget.count() > 0:
            next_row = min(row, self.list_widget.count() - 1)
            self.list_widget.setCurrentRow(next_row)

    def copy_to_base(self):
        # Copy selection from conf_editor to base_editor
        selected = self.conf_editor.selectedText()
        if selected:
            self.base_editor.replaceSelectedText(selected)

    def accept_version(self, src, dst):
        open(dst,'wb').write(open(src,'rb').read())
        QMessageBox.information(self,"Accepted",f"{dst} <- {src}")
        self.scan_conflicts(); self.clear_views()

def parse_base_flag():
    # Usage: script.py --base /folder/path
    base = None
    args = sys.argv[1:]
    if "--base" in args:
        idx = args.index("--base")
        if idx+1 < len(args): base = args[idx+1]
    elif "-b" in args:
        idx = args.index("-b")
        if idx+1 < len(args): base = args[idx+1]
    elif args and not args[0].startswith('-'):
        base = args[0]
    return base

if __name__=='__main__':
    app=QApplication(sys.argv)
    base_folder = parse_base_flag()
    win=ConflictResolver(base_folder)
    win.show(); sys.exit(app.exec())
