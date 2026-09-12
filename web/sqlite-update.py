import sqlite3
import re
import shutil

db = "/Users/muneer78/.local/share/buku/bookmarks.db"

# Make a backup before modifying anything
shutil.copy2(db, db + ".bak")

conn = sqlite3.connect(db)
cur = conn.cursor()

cur.execute("""
    SELECT id, URL, desc
    FROM bookmarks
    WHERE metadata = 'Medium'
""")

rows = cur.fetchall()

print(f"Found {len(rows)} Medium bookmarks to update.")

for bookmark_id, url, description in rows:
    if description:
        # Normalize whitespace and take the first 10 words
        words = re.findall(r'\S+', description)
        new_name = " ".join(words[:10])
    else:
        # Fall back to the Medium URL slug when no description is available.
        # Example:
        #   10-python-shortcuts-so-clever-i-stopped-writing-boilerplate-0f5a810c273f
        # becomes:
        #   10 Python Shortcuts So Clever I Stopped Writing Boilerplate
        slug = url.rstrip("/").split("/")[-1]
        slug = re.sub(r"-[0-9a-f]{8,}$", "", slug, flags=re.IGNORECASE)
        new_name = slug.replace("-", " ").title()

    cur.execute("""
        UPDATE bookmarks
        SET metadata = ?
        WHERE id = ?
    """, (new_name, bookmark_id))

    print(f"{bookmark_id}: {new_name}")

conn.commit()
conn.close()

print(f"\nDone. Backup saved as {db}.bak")