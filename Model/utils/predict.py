from ultralytics import YOLO
import os
import argparse
import cv2

BASE = os.path.dirname(__file__)
MODEL = os.path.join(BASE, '../best_model/best.pt')


def parse_args():
	parser = argparse.ArgumentParser(description='Predictions on pre-recorded images and videos')
	parser.add_argument('--model', default=[MODEL], nargs=1)
	parser.add_argument('--confidence', default=[0.5], nargs=1, type=float)
	parser.add_argument('-k', '--keep', action='store_true')
	parser.add_argument('source')
	parser.add_argument('--iou-threshold', default=[0.5], nargs=1, type=float)
	parser.add_argument('-s', '--show', action='store_true')

	return parser.parse_args()


def inference(args):
	model = YOLO(args.model[0])
	if not os.path.exists(args.source[0]):
		os.sys.exit('Source does not exist')

	results = model(source=args.source, conf=args.confidence[0], save=args.keep, iou=args.iou_threshold[0], show=args.show, stream=True)
	cv2.destroyAllWindows()

	for result in results:
		enc = result.boxes.xywhn
		print(f'\nDeviations:')
		for box in enc:
			print('\t', box[0] - 0.5)


if __name__ == '__main__':
	args = parse_args()
	inference(args)
