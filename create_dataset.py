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

    print("Validation completed successfully.")
    print(f"Empty directories: {empty_dirs}")

def create_dataset():
    print("Creating dataset...")

    empty_dirs = set()

    for split in SPLITS:
        print(f"Creating split: {split}")

        with open(split, 'r') as f:
            data = json.load(f)

        for item in tqdm(data['images']):
            # print(item['file_name'])
            dir_name = item['file_name'].split('/')[0]
            # print(dir_path)
            file_name = item['file_name'].split('/')[-1]
            assert dir_name in dir_mapping, f"Directory {dir_name} not found in mapping."

            if len(dir_mapping[dir_name]) == 0:
                # print(f"Directory {dir_name} has no paths in mapping.")
                empty_dirs.add(dir_name)
                continue
            found = 0
            found_in_dirs = []
            for dir_p in dir_mapping[dir_name]:
                assert (BASE_DIR / dir_p).exists(), f"Directory {dir_p} does not exist."
                if (BASE_DIR / dir_p / file_name).exists():
                    found += 1
                    found_in_dirs.append(dir_p)
                    break
            assert found > 0, f"File {file_name} not found in any of the mapped directories for {dir_name}."
            assert found == 1, f"File {file_name} found in multiple directories: {found_in_dirs}."

            os.makedirs(OUTPUT_DIR / item['file_name'], exist_ok=True)
            shutil.copy(BASE_DIR / found_in_dirs[0] / file_name, OUTPUT_DIR / item['file_name'])

    print("Dataset created successfully.")
    print(f"Empty directories: {empty_dirs}")

def validate_created_dataset():
    total_images = {}
    count_images = {}

    for split in SPLITS:
        print(f"Validating created split: {split}")

        with open(split, 'r') as f:
            data = json.load(f)

        for item in tqdm(data['images']):
            dir_name = item['file_name'].split('/')[0]
            file_name = item['file_name'].split('/')[-1]
            if dir_name not in total_images:
                total_images[dir_name] = 0
                count_images[dir_name] = 0

            total_images[dir_name] += 1
            if (OUTPUT_DIR / item['file_name']).exists():
                count_images[dir_name] += 1

    print("Validation of created dataset completed successfully.")
    for dir_name, total in total_images.items():
        count = count_images.get(dir_name, 0)
        if count != total:
            print(f"Directory {dir_name}: Total images = {total}, Counted images = {count}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create dataset from MP100 splits')
    # parser.add_argument('--base_dir', type=str, default=str(BASE_DIR), help='Base directory for dataset')
    parser.add_argument('--output_dir', type=str, default=str(BASE_DIR/'mp100'), help='Output directory for processed dataset')
    parser.add_argument('--mode', type=str, choices=['valid_org', 'create', 'valid'], help='Mode for processing dataset', required=True)
    args = parser.parse_args()

    BASE_DIR = Path(args.base_dir)
    OUTPUT_DIR = Path(args.output_dir)

    SPLITS = [
        OUTPUT_DIR / 'annotations/mp100_split1_test.json', 
        OUTPUT_DIR / 'annotations/mp100_split1_train.json', 
        OUTPUT_DIR / 'annotations/mp100_split1_val.json', 
        OUTPUT_DIR / 'annotations/mp100_split2_test.json',
        OUTPUT_DIR / 'annotations/mp100_split2_train.json',
        OUTPUT_DIR / 'annotations/mp100_split2_val.json',
        OUTPUT_DIR / 'annotations/mp100_split3_test.json',
        OUTPUT_DIR / 'annotations/mp100_split3_train.json',
        OUTPUT_DIR / 'annotations/mp100_split3_val.json',
        OUTPUT_DIR / 'annotations/mp100_split4_test.json',
        OUTPUT_DIR / 'annotations/mp100_split4_train.json',
        OUTPUT_DIR / 'annotations/mp100_split4_val.json',
        OUTPUT_DIR / 'annotations/mp100_split5_test.json',
        OUTPUT_DIR / 'annotations/mp100_split5_train.json',
        OUTPUT_DIR / 'annotations/mp100_split5_val.json',
    ]

    with open(BASE_DIR / 'dir_mapping.json', 'r') as f:
        dir_mapping = json.load(f)

    if args.mode == 'valid_org':
        validate_original_datasets()
    elif args.mode == 'create':
        create_dataset()
    elif args.mode == 'valid':
        validate_created_dataset()
    else:
        raise ValueError("Invalid mode.")