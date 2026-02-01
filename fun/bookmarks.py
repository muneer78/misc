import sqlite3

conn = sqlite3.connect("links.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS links (url TEXT, tags TEXT)")
c.execute("INSERT INTO links VALUES (?, ?)", ("https://example.com", "python,tools"))
conn.commit()