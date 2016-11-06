# -*- coding:utf-8 -*-

import argparse
import cv2
import time
import os
import os.path
import glob
from PIL import Image

camera = 1
cameraNum = [0, 1, 2, 3]
x = []
y = []
width = []
height = []
global count


def faceDetect(frame, cameraNum, save_file, resize):

	cascade_path = "./lib/haarcascade_frontalface_default.xml"
	cascade = cv2.CascadeClassifier(cascade_path)
	#frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))
	facerect = cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))
	print facerect

	if len(facerect) > 0:
		print 'Face has been detected'
		color = (255)
		image_path = "./datasets/" + save_file
		if os.path.isdir(image_path) == False:
			os.mkdir(image_path)
			print 'make image path'
		else:
			print 'path already exists'
	else:
		print 'where is the face?'

	i = 0
	for rect in facerect:
		print rect[0]
		x.append(rect[0] - 50)
		y.append(rect[1] - 50)
		width.append(rect[2] + 100)
		height.append(rect[3] + 100)
		for n in range(len(x)):
			dst = frame[y[n]:y[n] + 10 + 3 * height[n], x[n]:x[n] + 30 + width[n]]
			#imgResize = cv2.resize(dst,None,fx=dst.shape[0]/resize,fy=dst.shape[1]/resize)
			imgResize = cv2.resize(dst,(resize,resize))
			newImage_path = image_path + "/" + str(i) + '.png'
			#while True:
			    #if os.path.isfile(newImage_path):
				    #i += 1
                #else:
				    #cv2.imwrite(newImage_path, imgResize)
				    #break
			if os.path.isfile(newImage_path):
				i+=1
			else:
				cv2.imwrite(newImage_path, imgResize)

		time.sleep(3)


def faceRead(path):
	data = []
	for n in path:
		imgList = glob.glob(path + '*.png')
		for imgName in imgList:
			data.append(imgName)
	return data


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='face detect')
	parser.add_argument('--data', '-d', type=str, default='others')
	parser.add_argument('--size', '-s', type=int, default=128)
	args = parser.parse_args()

	cap = cv2.VideoCapture(0)
	while True:
		ret, frame = cap.read()
		cv2.imshow('camera capture', frame)
		th0 = faceDetect(frame, cameraNum[0], args.data, args.size)

		k = cv2.waitKey(10)
		if k == 27:
			break

	cap.release()
	cv2.destroyAllWindows()
