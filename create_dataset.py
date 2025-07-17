import argparse
import os
import shutil
import json
from pathlib import Path
from tqdm import tqdm
from settings import SETTING_BASE_DIR

BASE_DIR = Path(SETTING_BASE_DIR)

def validate_original_datasets():
    empty_dirs = set()
    file_mapping = {}

    for split in SPLITS:
        print(f"Validating split: {split}")

        with open(split, 'r') as f:
            data = json.load(f)

        for item in tqdm(data['images']):
            dir_name = item['file_name'].split('/')[0]
            file_name = item['file_name'].split('/')[-1]
            assert dir_name in dir_mapping, f"Directory {dir_name} not found in mapping."
            if len(dir_mapping[dir_name]) == 0:
                empty_dirs.add(dir_name)
                continue
            found = 0
            found_in_dirs = []
            for dir_path in dir_mapping[dir_name]:
                assert (BASE_DIR / dir_path).exists(), f"Directory {dir_path} does not exist."
                if (BASE_DIR / dir_path / file_name).exists():
                    found += 1
                    found_in_dirs.append(dir_path)
                    break
            assert found > 0, f"File {file_name} not found in any of the mapped directories for {dir_name}."
            assert found == 1, f"File {file_name} found in multiple directories: {found_in_dirs}."

            if str(BASE_DIR / found_in_dirs[0] / file_name) not in file_mapping:
                file_mapping[str(BASE_DIR / found_in_dirs[0] / file_name)] = set()
            file_mapping[str(BASE_DIR / found_in_dirs[0] / file_name)].add(str(IMG_DIR / item['file_name']))

    # assert len(empty_dirs) == 0, f"Some directories are empty: {empty_dirs}"

    print("Validation completed successfully.")
    print(f"Empty directories: {empty_dirs}")

    return file_mapping

def create_dataset(file_mapping):
    print("Creating dataset...")

    for src, dsts in tqdm(file_mapping.items()):
        for dst in dsts:
            dst_dir = os.path.dirname(dst)
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copyfile(src, dst)

    print("Dataset created successfully.")

def validate_created_dataset():
    total_images = {}
    count_images = {}

    file_names = {}

    for split in SPLITS:
        print(f"Validating created split: {split}")

        with open(split, 'r') as f:
            data = json.load(f)

        for item in tqdm(data['images']):
            # assert item['file_name'] not in file_names, f"Duplicate file name found: {item['file_name']}"
            file_names[item['file_name']] = item['id']
            dir_name = item['file_name'].split('/')[0]
            file_name = item['file_name'].split('/')[-1]
            if dir_name not in total_images:
                total_images[dir_name] = 0
                count_images[dir_name] = 0

            total_images[dir_name] += 1
            if (IMG_DIR / item['file_name']).exists():
                count_images[dir_name] += 1
            # else:
            #     print(IMG_DIR / item['file_name'], "does not exist.")

    print("Validation of created dataset completed successfully.")
    for dir_name, total in total_images.items():
        count = count_images.get(dir_name, 0)
        if count != total:
            print(f"Directory {dir_name}: Total images = {total}, Counted images = {count}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create dataset from MP100 splits')
    parser.add_argument('--output_dir', type=str, default=str(BASE_DIR/'mp100'), help='Output directory for processed dataset')
    parser.add_argument('--mode', type=str, choices=['valid_org', 'create', 'valid'], help='Mode for processing dataset', required=True)
    args = parser.parse_args()

    DATASET_DIR = Path(args.output_dir)
    IMG_DIR = DATASET_DIR / 'images'
    SPLITS = DATASET_DIR.glob('annotations/*.json')

    with open(BASE_DIR / 'dir_mapping.json', 'r') as f:
        dir_mapping = json.load(f)

    if args.mode == 'valid_org':
        validate_original_datasets()
    elif args.mode == 'create':
        try:
            file_mapping = validate_original_datasets()
        except AssertionError as e:
            print(f"Validation failed: {e}")
            exit(1)
        create_dataset(file_mapping)
    elif args.mode == 'valid':
        validate_created_dataset()
    else:
        raise ValueError("Invalid mode.")