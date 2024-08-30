import xml.etree.ElementTree as ET
import os

BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datasets/FloW_IMG')
DIRS = [('./test/annotations', './test/labels'), ('./training/annotations', './training/labels')]
DIRS = [(os.path.join(BASE, x), os.path.join(BASE, y)) for x, y in DIRS]


def makelabels(file, dir, svdir, classes, next_index):
	tree = ET.parse(os.path.join(dir, file))
	objects = tree.findall('object')
	imgsz = tree.find('size')
	imgsz = tuple(int(imgsz.find(x).text) for x in ('width', 'height', 'depth'))

	entries = []
	for obj in objects:
		name = obj.find('name').text
		if classes.get(name) is None:
			classes[name] = next_index
			next_index += 1
		box = obj.find('bndbox')
		xyxy = tuple(int(box.find(x).text) for x in ('xmin', 'ymin', 'xmax', 'ymax'))
		xywh = (xyxy[0] + xyxy[2])/2, (xyxy[1] + xyxy[3])/2, xyxy[2] - xyxy[0], xyxy[3] - xyxy[1]
		xywhn = (xywh[i]/imgsz[i%2] for i in range(4))

		entries.append(map(str, (classes.get(name), *xywhn)))

	with open(os.path.join(svdir, os.path.splitext(file)[0] + '.txt'), 'w') as label:
		for entry in entries:
			label.write(' '.join(entry) + '\n')

	return next_index


if __name__ == '__main__':
	classes = {}
	next_index = 0

	for dir, svdir in DIRS:
		for file in os.listdir(dir):
			next_index = makelabels(file, dir, svdir, classes, next_index)

	print(classes)
