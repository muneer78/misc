# Create a DataFrame from a JSON file
import json
import pandas as pd

with open("data.json") as f:
    data = json.load(f)

data
# output
{
    "data": [
        {
            "id": 101,
            "category": {"level_1": "code design", "level_2": "method design"},
            "priority": 9,
        },
        {
            "id": 102,
            "category": {"level_1": "error handling", "level_2": "exception logging"},
            "priority": 8,
        },
    ]
}

df = pd.json_normalize(data, "data")
