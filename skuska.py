import json
import os

jsonBuffer = "./probabilityBuffer.data"
if os.path.isfile(jsonBuffer):
    with open(jsonBuffer, 'r') as f:
        probabilityBuffer = json.load(f)
else:
    probabilityBuffer = dict = {"aaa":0, "b":10}

with open(jsonBuffer, 'w') as f:
    json.dump(probabilityBuffer, f)
print(probabilityBuffer)