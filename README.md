# MP100 dataset builder

## Preparation

Create a `.env` file in the repo directory, using the provided `.example.env` as a template:

```bash
cp dataset/.example.env dataset/.env
```

## Download COCO 2017 dataset

Link: https://cocodataset.org/#download

```bash
wget http://images.cocodataset.org/zips/train2017.zip
unzip train2017.zip
```

## Download 300W dataset

Link: https://ibug.doc.ic.ac.uk/resources/300-W/

```bash
python download_300w.py
```

## Download AFLW dataset

Link: https://www.tugraz.at/institute/icg/research/team-bischof/learning-recognition-surveillance/downloads/aflw

Fill out the form to get the download link, then download the dataset:

```bash

```

## Download OneHand10K dataset

```bash
```

## Download DeepFashion2 dataset

Link: https://github.com/switchablenorms/DeepFashion2

Fill the form to get the unzip password

```bash
mkdir DeepFashion2
cd DeepFashion2
gdown --fuzzy 12DmrxXNtl0U9hnN1bzue4XX7nw1fSMZ5 # Download json_for_validation.zip
gdown --fuzzy 1hsa-UE-LX8sks8eAcGLL-9QDNyNt6VgP # Download test.zip
gdown --fuzzy 1lQZOIkO-9L0QJuk_w1K8-tRuyno-KvLK # Download train.zip
gdown --fuzzy 1O45YqhREBOoLudjA06HcTehcEebR0o9y # Download validation.zip
unzip -P [password] json_for_validation.zip
unzip -P [password] test.zip
unzip -P [password] train.zip
unzip -P [password] validation.zip
cd ..
```

## Download AP-10K dataset

```bash
```

## Download MacaquePose dataset

```bash
```

Vinegar Fly, Desert Locust, CUB-200, CarFusion, AnimalWeb, Keypoint-5

## Download Vinegar Fly and Desert Locust datasets

Link: https://github.com/jgraving/DeepPoseKit-Data

```bash
git clone git+https://www.github.com/jgraving/deepposekit-data
python deepposekit_loader.py
``` 

## Download CUB-200 dataset

```bash
wget https://data.caltech.edu/records/65de6-vp158/files/CUB_200_2011.tgz
tar -xvzf CUB_200_2011.tgz
```

## Download CarFusion dataset

Link: http://www.cs.cmu.edu/~ILIM/projects/IM/CarFusion/cvpr2018/index.html

Fill out the form to get the google drive link, download all zip files in drive to the 'carfusion_dataset' directory, and unzip them:

```bash
mkdir carfusion_dataset
cd carfusion_dataset
gdown --fuzzy [google_drive_link_1]
gdown --fuzzy [google_drive_link_2]
...
unzip *.zip
cd ..
```

## Download AnimalWeb dataset

Link: https://fdmaproject.wordpress.com/author/fdmaproject/

```bash
gdown --fuzzy 13PbHxUofhdJLZzql3TyqL22bQJ3HwDK4
7z x animal_dataset_v1_c.rar # Extract the dataset
```

## Download Keypoint-5 dataset

Link: https://github.com/jiajunwu/3dinn

```bash
wget http://3dinterpreter.csail.mit.edu/data/keypoint-5.zip
unzip keypoint-5.zip
```

