# -*- coding:utf-8 -*-

import argparse
import numpy as np
import cv2
import time
import threading
import os
import os.path
import re
from datetime import datetime

camera = 1
cameraNum = [0, 1, 2, 3]
x = []
y = []
width = []
height = []


def faceDetect(frame, cameraNum, save_file):

	cascade_path = "./lib/haarcascade_frontalface_default.xml"

	global timeCount
	global count
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	cascade = cv2.CascadeClassifier(cascade_path)
	facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))
	print facerect

	if len(facerect) > 0:
		print 'Face has been detected'
		color = (255)
		now = datetime.now().strftime('%Y%m%d%H%M%S')
		image_path = "./datasets/" + save_file
		if os.path.isdir(imagePath) == False:
			os.mkdir(imagePath)
			print 'make image path'
		else:
			print 'path already exists'
	else:
		print 'where is the face?'

	i = 0
	for rect in facerect:
		print rect[0]
		timeCount += 1
		x.append(rect[0] - 50)
		y.append(rect[1] - 50)
		width.append(rect[2] + 100)
		height.append(rect[3] + 100)
		for n in range(len(x)):
			dst = frame[y[n]:y[n] + 10 + 3 * height[n], x[n]:x[n] + 30 + width[n]]
			newImage_path = image_path + "/" + now + "_" + str(i) + '.jpg'
			cv2.imwrite(newImage_path, dst)
			i += 1

		time.sleep(3)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='face detect')
	parser.add_argument('--data', '-d', type=str, default='others')
	args = parser.parse_args()

	cap = cv2.VideoCapture(0)
	print cap

	while True:
		ret, frame = cap.read()
		cv2.imshow('camera0 capture', frame)
        # ret, frame1 = cap[1].read()

		th0 = faceDetect(frame, cameraNum[0], 'me')
		#print th0
        # th1 = FaceThread(frameresize1, cameraNum[1])

		#th0.start()
        # th1.start()

        # cv2.imshow('camera1 capture', frameresize1)

	cap.release()
    # cap[1].release()

	cv2.destroyAllWindows()
