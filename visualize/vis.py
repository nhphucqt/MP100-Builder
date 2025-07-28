import argparse
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Path
import pathlib
import numpy as np
import uvicorn
import os
from xtcocotools.coco import COCO

app = FastAPI()

templates = Jinja2Templates(directory="./visualize/templates")

def load_annotations(annotations_dir: pathlib.Path):
    anno = {}

    for annotation_file in annotations_dir.glob("*.json"):
        coco = COCO(annotation_file)
        for img_id in coco.getImgIds():
            img_anno = coco.loadImgs(img_id)[0]
            file_name = img_anno['file_name']
            if file_name not in anno:
                anno[file_name] = []

            anno[file_name].append({
                'img_id': img_id,
                'ann_id': img_anno['id'],
                'annotation_filename': str(annotation_file),
                'annotation_name': str(annotation_file.name).split('.')[0].split('_', 1)[-1],
                'width': img_anno['width'],
                'height': img_anno['height'],
                'objs': [],
            })
            ann_ids = coco.getAnnIds(imgIds=img_id)
            objs = coco.loadAnns(ann_ids)

            for obj in objs:
                x, y, width, height = obj['bbox']
                anno[file_name][-1]['objs'].append({
                    'id': obj['id'],
                    'bbox': [x, y, width, height],
                    'keypoints': np.array(obj['keypoints']).reshape(-1, 3).tolist(), # (x, y, visibility)
                    'skeleton': coco.cats[obj['category_id']]['skeleton']
                })
    
    return anno

def safe_join(base, *paths):
    # Prevent directory traversal
    final_path = os.path.abspath(os.path.join(base, *paths))
    if not final_path.startswith(os.path.abspath(base)):
        raise ValueError("Unsafe path")
    return final_path

@app.get("/annotations/{subpath:path}")
def get_annotations(subpath: str = Path(..., description="Path to the annotation file")):
    print(subpath)
    return annotation.get(subpath, {"error": "File not found"})

@app.get("/", response_class=HTMLResponse)
@app.get("/browse/{subpath:path}", response_class=HTMLResponse)
def browse(request: Request, subpath: str = ""):
    abs_path = safe_join(IMG_DIR, subpath)
    items = []
    for name in sorted(os.listdir(abs_path)):
        full_path = os.path.join(abs_path, name)
        rel_path = os.path.relpath(full_path, IMG_DIR)
        items.append({
            "name": name,
            "is_dir": os.path.isdir(full_path),
            "rel_path": rel_path
        })
    parent = os.path.dirname(subpath) if subpath else None

    print(items)

    return templates.TemplateResponse(
        "file_browser.html",
        {"request": request, "items": items, "parent": parent, "subpath": subpath}
    )

print("__name__:", __name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-dir', type=str, help='Path to the dataset directory.')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the server on.')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on.')
    args = parser.parse_args()

    DATASET_DIR = pathlib.Path(args.dataset_dir)
    ANN_DIR = DATASET_DIR / 'annotations_fixed'
    IMG_DIR = DATASET_DIR / 'images'

    if not DATASET_DIR.exists():
        raise ValueError(f"Dataset directory {DATASET_DIR} does not exist.")

    print(f"Starting server with dataset directory: {DATASET_DIR}")

    annotation = load_annotations(ANN_DIR)

    for file_name, anns in annotation.items():
        print(f"File: {file_name}, Annotations: {anns}")
        break


    app.mount("/images", StaticFiles(directory=IMG_DIR), name="images")

    uvicorn.run("__main__:app", host=args.host, port=args.port)