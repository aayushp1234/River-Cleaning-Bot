# Dataset downloading

## Make a `Model/datasets` directory 
> Execute this while in **project root**
>
>       mkdir ./Model/datasets

## TACO dataset
> The TACO dataset can be downloaded in a yolov8 format [here](https://universe.roboflow.com/taco-t7kkz/taco-dataset-ql1ng/dataset/15)
> - Click on YOLOv8 download format and the link to download the `.zip` file would be generated.
> - Move the downloaded file to `Model/datasets` directory. Execute this while in **project root**
>
>       mv /path/to/the/zip/file ./Model/datasets/TACO.dataset.v15i.yolov8.zip

## FloW-IMG dataset
> The FloW-IMG dataset can be downloaded via a request to the ORCAUBOAT company [here](https://orca-tech.cn/en/datasets/FloW/FloW-Img)
> - Click on ***Click here to download the FloW-Img. \[Download\]*** and fill in the details
> - You will recieve the download links within 1-2 days. Within the email you get links to download data which would be valid for 24 hours.
> - Download *FloW-Img Image Dataset-FloW_IMG* via url in the mail and store the `.zip` file in `Model/datasets`. Execute this while in **project root**
>
>       mv /path/to/the/zip/file ./Model/datasets/FloW_IMG.zip
> - Download the other bot pov video sequences via the other links and extract them all in `Model/testing/Video_Sequences`. Execute this while in **project root** (unzip one by one below)
>
>       mkdir -p ./Model/testing/Video_Sequences
>       unzip /path/to/each/of/the/zip/files -d ./Model/testing/Video_Sequences


### Now you are all set to refer to RUNME.sh