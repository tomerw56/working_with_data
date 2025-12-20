import json

with open("drone.json") as f:
    d = json.load(f)

print(d)
