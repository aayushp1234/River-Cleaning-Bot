# This is full workflow of model training and testing that was used for computer vision model training
# First the required downloads are done as given in README.md

# We have 2 datasets:-
#	Trash Annotations in Context (TACO) dataset
#		This dataset includes annotated images of transh in different environments like concrete floor, shrubsm, earthy land, etc.
#	FloW IMG dataset
#		This dataset is provided by ORCAUBOAT(orca-tech.cn) company which targets similar unmanned water surface cleaning bots.
#		The dataset contains annotated images of the lake surface in the point of view of a water surface traversel bot. The images have floating trash annotated in xml label format which can be converted to yolov8 supported format using the converter file we made.

# Activating the python virtual environment and installing the requirements
python3 -m venv ./.venv
. ./.venv/bin/activate
pip install -r ./requirements.txt

# First we unzip the databases we collected using the README.md setup
mkdir -p ./datasets/TACO.dataset.v15i.yolov8   # As the zip file probably won't contain the outer directory
unzip ./datasets/TACO.dataset.v15i.yolov8.zip -d ./datasets/TACO.dataset.v15i.yolov8
unzip ./datasets/FloW_IMG.zip -d ./datasets
python3 ./utils/xml_to_labels.py    # This converts xml labels to yolov8 model training compatible labels

# Next we want to train the yolo model as follows using ultralytics api:-
# We use yolov8 nano architecture pre-trained model as our base model
# Now, we use transfer learning to fine-tune our model for TACO dataset which makes the model better at detecting trash in general environments
yolo task=detect mode=train model=yolov8n.pt data=./data/base.yaml epochs=70 imgsz=640
# Next, we again fine-tune the best.pt model that we get from the previous fine-tuning on the FloW dataset to make it better specifically for detecting trash on water surface in pov of the bot
yolo task=detect mode=train model=./runs/detect/train/weights/best.pt data=./data/floated.yaml epochs=50 imgsz=640

# The model has now been trained and is located in runs/detect/train2/weights/best.pt
# We followed the same process and The best model was copied to best_model/ under the name best.pt
# Now, yolov8 best.pt model is heavy for Raspberry Pi5. So, we chose to export the model in a lighter format like tflite
cd ./best_model
yolo export model=./best.pt format=tflite
cd -

# Testing of the model performance could be done as follows
# First we test on the images provided by the dataset
yolo task=detect mode=val model=./best_model/best.pt data=./data/floated.yaml
# Testing on some freely available random floating trash video image
yolo task=detect mode=predict model=./best_model/best.pt source=./testing/sample.jpg
# Now, to do it on some real video clips provided by ORCAUBOAT and some recorded by us
#	First we unzip the compressed folders with the clips. ORCAUBOAT video sequences would've been unzipped while setup using README.md
unzip ./testing/RealVids.zip -d ./testing
#   Now, we make the predictions
yolo task=detect mode=predict model=./best_model/best.pt source=./Video_Sequences/Sequence_27.avi
yolo task=detect mode=predict model=./best_model/best.pt source=./RealVids
# All the inference results can be viewed in runs/detect directory

# The bot control is primarily influenced by the deviation of the detected trash from the central vertical of the image
# utils/ contain python files that display deviations from the central vertical in each frame.
# For the pre-recorded videos and normal prediction
python3 ./utils/predict.py -s ./testing/RealVids --iou-threshold 0.3 --confidence 0.6
python3 ./utils/predict.py -s ./testing/Video_Sequences_23.avi --iou-threshold 0.4 --confidence 0.7
# For video-camera feeds and bytetrack trash tracking
python3 ./utils/track.py --iou-threshold 0.45 --confidence 0.65

# We may have used object tracking but it was computationally expensive though it would've saved any false trash detections hindering the bot in some frames to follow trash rather than anything else
# Thus, we resorted to trust the model (after many tests) and always follow the trash with least deviation in any frame
