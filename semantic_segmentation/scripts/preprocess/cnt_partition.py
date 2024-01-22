import sys
import json

cnt = {}
train, val, test = [], [], []
with open(sys.argv[1], "r") as f:
    data = f.read()
    for line in data.strip().split("\n"):
        #print (line)
        items = line.strip().split()
        i = int(items[1])
        if i not in cnt:
            cnt[i] = 0
        cnt[i] += 1
        if i == 0:
            train.append(items[0])
        elif i == 1:
            val.append(items[0])
        elif i == 2:
            test.append(items[0])
print (cnt)

output = {
        "train": train,
        "valid": val,
        "test": test
        }

with open(sys.argv[2], "w") as f:
    json.dump(output, f, indent=2)
