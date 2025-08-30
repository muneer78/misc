import json

path_json_file = "/Volumes/solutions_architect_sandbox/rneis_output/misc/model.bim"
# Open and read the JSON file
print("Reading JSON file...")
with open(path_json_file, "r") as file:
    json = json.load(file)

sqls = []
for a in json["model"]["tables"]:
    print(a["name"])
    table = a["name"]
    for b in a["partitions"]:
        for c in b["source"]["expression"]:
            # print(c[0:13])
            if c[0:13] == "    Source = ":
                # print("sdgffds")
                cs = c.split(",")
                for d in cs:
                    print("**", d)
                    ...
                # sqls.append(dict(table=table,sql=d))
