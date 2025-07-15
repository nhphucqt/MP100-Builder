import h5py
import numpy as np
from pathlib import Path
# import cv2
from PIL import Image

BASE_DIR = Path('/home/dtle/camouflage/dataset/deepposekit-data/datasets/')

dirs = [
    BASE_DIR / 'fly',
    BASE_DIR / 'locust',
]

for dir in dirs:
    if not dir.exists():
        print(f"Directory {dir} does not exist.")
        continue

    print(f"Processing directory: {dir}")

    with h5py.File(dir / 'annotation_data_release.h5', 'r') as f:
        images = np.array(f['images'])
        print(images.shape)
        # shape [num_images, height, width, 1]

        # save image as [id].jpg to images/ dir

        if not (dir / 'images').exists():
            (dir / 'images').mkdir(parents=True)

        for i, image in enumerate(images):
            image = Image.fromarray(image.squeeze(), mode='L')
            image.save(dir / 'images' / f"{i}.jpg")