import json
from datetime import datetime

def log_contact(name, note):
    with open("contacts.json", "a") as f:
        f.write(json.dumps({
            "name": name,
            "note": note,
            "time": datetime.now().isoformat()
        }) + "\n")