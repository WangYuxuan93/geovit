import json
from datasets import Dataset, DatasetDict, Image
from tqdm import tqdm
import os

def create_dataset(img_ids, spl_name):
    print ("Creating {} set ...".format(spl_name))
    image_paths = []
    label_paths = []
    for img_id in tqdm(img_ids):
        img_path = os.path.join(img_dir, "{}.jpg".format(img_id))
        if not os.path.exists(img_path):
            print ("Image file {} doesn't exist".format(img_path))
            exit()
        padded_id = str(100000 + img_id)[1:]
        label_path = os.path.join(label_dir, "{}_mask.png".format(padded_id))
        if not os.path.exists(label_path):
            print ("Label file {} doesn't exist".format(label_path))
            exit()
        image_paths.append(img_path)
        label_paths.append(label_path)
    dataset = Dataset.from_dict({"image": sorted(image_paths),
                                "label": sorted(label_paths)})
    dataset = dataset.cast_column("image", Image())
    dataset = dataset.cast_column("label", Image())
    return dataset

img_dir = "/home/mrch/data/CelebAMask-HQ/CelebA-HQ-img"
label_dir = "/home/mrch/data/CelebAMask-HQ/labels"
split_file = "/home/mrch/data/CelebAMask-HQ/celeba_mask_split.json"
dataset_file = "/home/mrch/data/CelebAMask-HQ/celeba_mask"

with open(split_file, "r") as f:
    splits = json.load(f)

# step 1: create Dataset objects
train_dataset = create_dataset(splits["train"], "train")
validation_dataset = create_dataset(splits["valid"], "valid")
test_dataset = create_dataset(splits["test"], "test")

# step 2: create DatasetDict
dataset = DatasetDict({"train": train_dataset,
                       "validation": validation_dataset,
                       "test": test_dataset
                    })

dataset.save_to_disk(dataset_file)
