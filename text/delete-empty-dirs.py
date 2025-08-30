import os
import shutil

while True:
    to_delete = []
    for root, dirs, _ in os.walk("."):
        for d in dirs:
            full_path = os.path.join(root, d)
            if all(s.startswith(".") for s in os.listdir(full_path)):
                to_delete.append(full_path)

    if to_delete:
        for p in to_delete:
            print(p)
            shutil.rmtree(p)
    else:
        break
