import ast
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict

# -------- CONFIG --------
INPUT_DIR = Path("/Users/muneer78/Downloads/convert")   # <-- change this
OUTPUT_FILE = Path("/Users/muneer78/Downloads/similar_scripts.txt")
SIMILARITY_THRESHOLD = 0.90
# ------------------------

class NormalizeNames(ast.NodeTransformer):
    def visit_Name(self, node):
        return ast.copy_location(ast.Name(id="_VAR", ctx=node.ctx), node)

    def visit_FunctionDef(self, node):
        node.name = "_FUNC"
        self.generic_visit(node)
        return node

def ast_dump(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    tree = NormalizeNames().visit(tree)
    ast.fix_missing_locations(tree)
    return ast.dump(tree)

# Collect Python files
files = sorted(INPUT_DIR.glob("*.py"))

# Build normalized AST dumps
trees = {}
for f in files:
    try:
        trees[f] = ast_dump(f)
    except SyntaxError:
        # Skip files with syntax errors
        continue

# Compare and group similarities
similar = defaultdict(list)
seen_pairs = set()

for i, f1 in enumerate(files):
    if f1 not in trees:
        continue
    for f2 in files[i + 1:]:
        if f2 not in trees:
            continue

        pair = tuple(sorted((f1, f2)))
        if pair in seen_pairs:
            continue

        score = SequenceMatcher(None, trees[f1], trees[f2]).ratio()
        if score >= SIMILARITY_THRESHOLD:
            similar[f1].append((f2, score))
            similar[f2].append((f1, score))
            seen_pairs.add(pair)

# Write report
with OUTPUT_FILE.open("w", encoding="utf-8") as out:
    for script in sorted(similar):
        out.write(f"{script.name}\n")
        for other, score in sorted(similar[script], key=lambda x: -x[1]):
            out.write(f"  - {other.name} ({score:.2f})\n")
        out.write("\n")

print(f"Similarity report written to {OUTPUT_FILE}")
