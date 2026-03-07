import os, hashlib
from collections import defaultdict
def hash_partial(f, n=4096):
    with open(f,'rb') as fh:
        return hashlib.md5(fh.read(n)).hexdigest()
by_size = defaultdict(list)
for root,_,files in os.walk("/path/to/scan"):
    for f in files:
        p = os.path.join(root,f); s = os.path.getsize(p)
        by_size[s].append(p)
for size, files in by_size.items():
    if len(files) < 2: continue
    hashes = {}
    for p in files:
        h = hash_partial(p)
        if h in hashes: print("Partial dup:", p, "==", hashes[h])
        else: hashes[h]=p