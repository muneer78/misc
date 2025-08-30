import json
import pprint

json_data = None
with open("fuel_details_20240522210404437203.json", "r") as f:
    # Skip the first two lines
    lines = f.readlines()[2:]
    # Join the remaining lines into a single string
    data = "".join(lines).strip()

    try:
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        print("Attempting to parse line-by-line")
        json_data = []
        for line in lines:
            line = line.strip()
            if line:  # Avoid empty lines
                try:
                    json_obj = json.loads(line)
                    json_data.append(json_obj)
                except json.JSONDecodeError as e:
                    print(f"Skipping line due to JSON decode error: {e}")
                    continue

# print json to screen with human-friendly formatting
pprint.pprint(json_data, compact=True)
