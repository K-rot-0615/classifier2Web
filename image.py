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

camera = 2
x = []
y = []
width = []
height = []
cap = []


class FaceThread(threading.Thread):

	def __init__(self, frame, cameraNum, save_file):
		super(FaceThread, self).__init__()
		self._cascade_path = "./lib/haarcascade_frontalface_default.xml"
		self._frame = frame
		self._cameraNum = cameraNum
		self.save_file = save_file

	def run(self):
		global timeCount
		global count
		self._frame_gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
		self._cascade = cv2.CascadeClassifier(self._cascade_path)
		self._facerect = self._cascade.detectMultiScale(
		    self._frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(40, 40))

		if len(self._facerect) > 0:
			print 'Face has been detected'
			self._color = (255)
			self._now = datetime.now().strftime('%Y%m%d%H%M%S')
			self._image_path = "./datasets/" + self._save_file
			if os.path.isdir(self._imagePath) == False:
				os.mkdir(self._imagePath)
				print 'make image path'

		i = 0
		for rect in self._facerect:
			print rect[0]
			timeCount += 1
			x.append(rect[0] - 50)
			y.append(rect[1] - 50)
			width.append(rect[2] + 100)
			height.append(rect[3] + 100)
			for n in range(len(x)):
				self._dst = self._frame[y[n]:y[n] + 10 +
				    3 * height[n], x[n]:x[n] + 30 + width[n]]
				self._newImage_path = self._image_path + \
				    "/" + self._now + "_" + str(i) + '.jpg'
				frame_height = self._frame.shape[0]
				frame_width = self._frame.shape[1]
				cv2.imwrite(self._newImage_path, self._dst)
				i += 1

			time.sleep(3)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='face detect')
	parser.add_argument('--data', '-d', type=str, default='')
	args = parser.parse_args()

	for i in range(camera+1):
		cap.append(cv2.VideoCapture(i))

	while True:
		ret, frame0 = cap[0].read()
        # ret, frame1 = cap[1].read()

        if(threading.activeCount() == 1):
            th0 = FaceThread(frame0, cameraNum[0], args.data)
            # th1 = FaceThread(frameresize1, cameraNum[1])

            th0.start()
            # th1.start()

        cv2.imshow('camera0 capture', frame0)
        # cv2.imshow('camera1 capture', frameresize1)

	cap[0].release()
    # cap[1].release()

	cv2.destroyAllWindows()
