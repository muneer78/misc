import os
import sqlite3

conn = sqlite3.connect("file_index.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS files (path TEXT, content TEXT)")
def index_folder(folder):
    for root, _, files in os.walk(folder):
        for name in files:
            if name.endswith((".txt", ".md", ".py")):
                path = os.path.join(root, name)
                try:
                    with open(path, "r", errors="ignore") as f:
                        content = f.read()
                        c.execute("INSERT INTO files VALUES (?, ?)", (path, content))
                except:
                    pass
    conn.commit()
index_folder("documents")