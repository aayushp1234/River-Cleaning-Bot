from ultralytics import YOLO
import cv2
import numpy as np
import argparse
import os

BASE = os.path.dirname(__file__)
MODEL = os.path.join(BASE, '../best_model/best.pt')
TRACKER = os.path.join(BASE, '../data/bytetrack.yaml')


def parse_args():
	parser = argparse.ArgumentParser(description='Live prediction')
	parser.add_argument('--webcam-resolution', default=None, nargs=2, type=int)
	parser.add_argument('--model', default=[MODEL], nargs=1)
	parser.add_argument('--capture-device', default=[0], nargs=1, type=int)
	parser.add_argument('--confidence', default=[0.5], nargs=1, type=float)
	parser.add_argument('--tracker', default=[TRACKER], nargs=1)
	parser.add_argument('--iou-threshold', default=[0.5], nargs=1, type=float)

	return parser.parse_args()


def track(frame, model, tracker, roi_hori = (0., 1.), iou = 0.5, conf = 0.5):
	roi_hori = map(int, (frame.shape[0] * y for y in roi_hori))
	frame = frame[next(roi_hori):next(roi_hori), ...]

	return frame, model.track(frame, tracker=tracker, iou=iou, conf=conf)[0].boxes


def get_deviation(boxes):
	devs = {}

	if boxes.is_track:
		for id, box in zip(boxes.id, boxes.xywhn):
			devs[id] = box[0] - 0.5

	return devs


def live_inference(args):
	model = YOLO(args.model[0])
	cap = cv2.VideoCapture(args.capture_device[0])
	if args.webcam_resolution is not None:
		cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.webcam_resolution[0])
		cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.webcam_resolution[1])

	while True:
		_, frame = cap.read()
		if not _:
			os.sys.exit('Camera not working')

		frame, result = track(frame, model, args.tracker[0], iou=args.iou_threshold[0], conf=args.confidence[0])
		devs = None

		if result.is_track:
			for id, xyxy in zip(result.id, result.xyxy):
				xyxy = tuple(np.int16(np.asarray(xyxy.cpu())))
				cv2.rectangle(frame, xyxy[:2], xyxy[2:], (0, 255, 0), 2)
				cv2.putText(frame, f'trash:{int(id)}', (xyxy[0], xyxy[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
			devs = get_deviation(result)

		cv2.imshow('Feed', frame)

		print(devs)
		print(result.id)
		print()

		if cv2.waitKey(10) == 27:
			break

	cv2.destroyAllWindows()


if __name__ == '__main__':
	args = parse_args()
	live_inference(args)
