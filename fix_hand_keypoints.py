from pathlib import Path
import cv2
from matplotlib import pyplot as plt
import json
from tqdm import tqdm

onehand10k_dir = Path("OneHand10K")
image_dir = onehand10k_dir / "Train/source"
mask_dir = onehand10k_dir / "Train/mask"

dataset_dir = Path("mp100")
annotations_dir = dataset_dir / "annotations"

output_dir = dataset_dir / "annotations_fixed"

output_dir.mkdir(parents=True, exist_ok=True)

with open(onehand10k_dir / "Train/label_joint.txt", "r") as f:
    data = f.read().strip().split("\n")
    data = [line.split(',') for line in data]

onehand10k_annotations = {
    d[0]: {
        "image_path" : str(image_dir / d[0]),
        "mask_path" : str(mask_dir / d[0].replace('.jpg', '.png')),
        "width": int(d[1]),
        "height": int(d[2]),
        "hand_number": int(d[3]),
        "keypoints": [[int(d[i]), int(d[i + 1])] for i in range(4, len(d), 2)],
    } for d in data
}

def find_bbox(image_name):
    anno = onehand10k_annotations[image_name]
    mask = cv2.imread(anno["mask_path"], cv2.IMREAD_GRAYSCALE)
    if mask is None:
        print(f"Error loading mask for {image_name}")
        return None
    
    mask[mask < mask.mean()] = 0
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print(f"No contours found for {image_name}")
        return None
    
    # Get bounding boxes for all contours
    bboxes = [cv2.boundingRect(cnt) for cnt in contours]
    if not bboxes:
        return None
    x_min = min([x for x, y, w, h in bboxes])
    y_min = min([y for x, y, w, h in bboxes])
    x_max = max([x + w for x, y, w, h in bboxes])
    y_max = max([y + h for x, y, w, h in bboxes])

    bbox_width = x_max - x_min
    bbox_height = y_max - y_min

    scale = 0.1
    padd_width = int(scale * bbox_width)
    padd_height = int(scale * bbox_height)

    x_min = max(0, x_min - padd_width)
    y_min = max(0, y_min - padd_height)
    x_max = min(anno["width"] - 1, x_max + padd_width)
    y_max = min(anno["height"] - 1, y_max + padd_height)

    # Return as (x, y, w, h)
    return (x_min, y_min, x_max - x_min, y_max - y_min)

anno_list = sorted(list(annotations_dir.glob("*.json")))
for anno_file in anno_list:
    print(f"Processing {anno_file.name}...")
    with open(anno_file, "r") as f:
        anno = json.load(f)

    image_map = {}

    print(anno.keys())

    for image in anno["images"]:
        if "human_hand" not in image["file_name"]:
            continue

        image_id = image["id"]
        image_name = image["file_name"].split("/")[-1]

        image_map[image_id] = image_name

        image["width"] = onehand10k_annotations[image_name]["width"]
        image["height"] = onehand10k_annotations[image_name]["height"]

    for annotation in tqdm(anno["annotations"]):
        if annotation["image_id"] not in image_map:
            continue

        image_name = image_map[annotation["image_id"]]

        keypoints = []
        for point in onehand10k_annotations[image_name]['keypoints']:
            if point[0] == -1:
                keypoints.extend([0, 0, 0])
            else:
                keypoints.extend([point[0], point[1], 1])

        bbox = find_bbox(image_name)
        annotation["bbox"] = bbox
        annotation["area"] = bbox[2] * bbox[3] if bbox else 0
        annotation["keypoints"] = keypoints
        # ignore segmentation
        annotation.pop("segmentation")

    with open(output_dir / anno_file.name, "w") as f:
        json.dump(anno, f)

