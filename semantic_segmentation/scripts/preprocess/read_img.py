import sys
import os
import json

input_dir = sys.argv[1]
dirs = os.listdir(input_dir)
data = {}
labels = []
for cur_dir in dirs:
    #print (cur_dir)
    cur_dir = os.path.join(input_dir, cur_dir)
    if not os.path.isdir(cur_dir): continue
    files = os.listdir(cur_dir)    
    for file in files:
        if not file.endswith("png"): continue
        items = file.split(".")[0].split("_")
        img_id = items[0]
        label = "_".join(items[1:])
        if len(img_id) == 0:
            print (file, items)
            exit()
        if img_id not in data:
            data[img_id] = set()
        data[img_id].add(label)
        if label not in labels:
            labels.append(label)
print ("Total img", len(data))

keys = sorted(data.keys())[:100]
print (keys)

first_id = list(data.keys())[0]
first_num_label = len(data[first_id])
print (first_id, data[first_id])

labels = sorted(labels)
print (labels)

labels = ["unlabeled"] + labels

id2label = {i: labels[i] for i in range(len(labels))}
with open('id2label.json', 'w') as fp:
    json.dump(id2label, fp, indent=2)

#for id in data:
#    num_label = len(data[id])
#    if num_label != first_num_label:
#        print ("uneq:", id, data[id])
