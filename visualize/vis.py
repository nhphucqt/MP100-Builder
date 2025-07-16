import argparse
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Path
import uvicorn
import os

app = FastAPI()

templates = Jinja2Templates(directory="./visualize/templates")

def safe_join(base, *paths):
    # Prevent directory traversal
    final_path = os.path.abspath(os.path.join(base, *paths))
    if not final_path.startswith(os.path.abspath(base)):
        raise ValueError("Unsafe path")
    return final_path

@app.get("/", response_class=HTMLResponse)
@app.get("/browse/{subpath:path}", response_class=HTMLResponse)
def browse(request: Request, subpath: str = ""):
    abs_path = safe_join(DATASET_DIR, subpath)
    items = []
    for name in os.listdir(abs_path):
        full_path = os.path.join(abs_path, name)
        rel_path = os.path.relpath(full_path, DATASET_DIR)
        items.append({
            "name": name,
            "is_dir": os.path.isdir(full_path),
            "rel_path": rel_path
        })
    parent = os.path.dirname(subpath) if subpath else None
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

    DATASET_DIR = args.dataset_dir

    print(f"Starting server with dataset directory: {DATASET_DIR}")

    app.mount("/images", StaticFiles(directory=DATASET_DIR), name="images")

    uvicorn.run("__main__:app", host=args.host, port=args.port, log_level="info")