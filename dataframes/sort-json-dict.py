import json

with open("/Users/muneer78/Documents/GitHub/automated-reading-list/keyword-candidates.json", "r") as f:
    data = json.load(f)

# Sort by value, then by key for ties
sorted_data = dict(
    sorted(data.items(), key=lambda x: (-x[1], x[0]))
)

with open("/Users/muneer78/Documents/GitHub/automated-reading-list/keyword-candidates-sorted.json", "w") as f:
    json.dump(sorted_data, f, indent=2)