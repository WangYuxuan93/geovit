import sys
import json

celeba_split = "/home/mrch/data/celeba_split.json"
with open(celeba_split, "r") as f:
    spl = json.load(f)

map_file = "/home/mrch/data/CelebAMask-HQ/CelebA-HQ-to-CelebA-mapping.txt"
mask_split = {
        "train": [],
        "valid": [],
        "test": []
        }
with open(map_file, "r") as f:
    data = f.read().strip().split("\n")
    for line in data[1:]:
        items = line.strip().split()
        orig_file = items[2]
        #print (items)
        flag = False
        for type in spl:
            if orig_file in spl[type]:
                mask_split[type].append(int(items[0]))
                flag = True
                break
        if not flag:
            print ("Invalid file: {}".format(orig_file))
            exit()

print ("train/valid/test={}/{}/{}".format(len(mask_split["train"]), len(mask_split["valid"]), len(mask_split["test"])))
output_file = "celeba_mask_split.json"
with open(output_file, "w") as f:
    json.dump(mask_split, f, indent=2)
