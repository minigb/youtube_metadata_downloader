import json
import os


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
    

def save_json(data, file_path):
    parent_dir = os.path.dirname(file_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
        print(f"Created {parent_dir}")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)