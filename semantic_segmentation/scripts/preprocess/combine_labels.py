from PIL import Image
import json
import sys
import os
import numpy as np
from tqdm import tqdm

idfile = "id2label.json"
with open(idfile, "r") as f:
    id2label = json.load(f)
    id2label = {int(k): v for k, v in id2label.items()}
    label2id = {v: k for k, v in id2label.items()}
print (id2label)

def combine(files):
    label_dict = {x:None for x in id2label.keys()}
    for file in files:
        im = Image.open(file)
        lab_type = '_'.join(os.path.basename(file).split(".")[0].split('_')[1:])
        lab_id = label2id[lab_type]
        #print (file, lab_type, lab_id)
        #exit()
        labels = np.array(im)
        # replace 255 with label id
        labels[labels==255] = lab_id
        label_dict[lab_id] = labels
    lab_tensor = np.zeros_like(labels)

    #print (label_dict)
    for k in id2label.keys():
        if label_dict[k] is not None:
            #print ("copying label:", id2label[k])
            # only copy values where the current label tensor is 0
            empty_mask = (lab_tensor == 0)
            lab_tensor[empty_mask] = label_dict[k][empty_mask]
    #np.set_printoptions(threshold = np.inf)
    out_img = Image.fromarray(lab_tensor)
    #print (lab_tensor)
    #exit()
    return out_img


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
            data[img_id] = []
        data[img_id].append(os.path.join(cur_dir, file))
        if label not in labels:
            labels.append(label)
print ("Total img", len(data))

#print (list(data.items())[0])

output_dir = "/home/mrch/data/CelebAMask-HQ/labels"
for img_id in tqdm(data):
    ann_files = data[img_id]
    out_img = combine(ann_files)
    output_file = os.path.join(output_dir, img_id+"_mask.png")
    out_img.save(output_file)
    #exit()
