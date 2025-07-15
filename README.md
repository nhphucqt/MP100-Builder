# MP100 dataset builder

## Preparation

Create a `.env` file in the repo directory, using the provided `.example.env` as a template:

```bash
cp dataset/.example.env dataset/.env
```

## Download COCO 2017 dataset

```bash
wget http://images.cocodataset.org/zips/train2017.zip
unzip train2017.zip
```

## Download 300W dataset

```bash
python download_300w.py
```