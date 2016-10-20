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
timeCount = 0
cameraNum = [0,1,2,3]
x=[]
y=[]
width=[]
height=[]
count = 0
color=(255,255,255)

class FaceThread(threading.Thread):

	def __init__(self, frame, cameraNum):
		super(FaceThread, self).__init__()
		self._cascade_path = "./lib/haarcascade_frontalface_default.xml"
		self._frame = frame
		self._cameraNum = cameraNum

	def run(self):
		global timeCount
		global count
		self._frame_gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
		self._cascade = cv2.CascadeClassifier(self._cascade_path)
		self._facerect = self._cascade.detectMultiScale(self._frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(40, 40))

		if len(self._facerect) > 0:
			print 'Face has been detected'
			self._color = (255, 255, 255)
			self._now = datetime.now().strftime('%Y%m%d%H%M%S')
			self._image_path = "./datasets/" + str(timeCount/10)
			if os.path.isdir(self._imagePath) == False:
				os.mkdir(self._imagePath)
				print 'make image path'

		i=0
		f=True
		for rect in self._facerect:
			print rect[0]
			timeCount+=1
			if count ==0:
				x.append(rect[0]-50)
				y.append(rect[1]-50)
				width.append(rect[2]+100)
				height.append(rect[3]+100)
				count=1
			elif count==1:
				for n in range(len(x)):
					if x[n]<rect[0] and x[n]+width[n]>rect[0]+rect[2] and y[n]<rect[1] and y[n]+height[n]>rect[1]+rect[3]:
						f=False
						print 'false'
				if f==True:
					print'True'
					x.append(rect[0]-50)
					y.append(rect[1]-50)
					width.append(rect[2]+100)
					height.append(rect[3]+100)
				for n in range(len(x)):
					self._dst = self._frame[y[n]:y[n]+10+3*height[n], x[n]:x[n]+30+width[n]]
					self._newImage_path = self._image_path + "/" + self._now + "_" + str(i) + '.jpg'
					frame_height=self._frame.shape[0]
					frame_width=self._frame.shape[1]
					imageResize=cv2.resize(self._dst,(400,600))
					cv2.imwrite(self._newImage_path,imageResize )
					i += 1
				f=True
				time.sleep(3)


if __name__ == '__main__':

    cap = []
    for i in range(camera+1):
    	cap.append(cv2.VideoCapture(i))

    while True:
        ret, frame0 = cap[0].read()
        #ret, frame1 = cap[1].read()
        #ret, frame2 = cap[2].read()
        frameresize0=cv2.resize(frame0,(1500,1500))
        #frameresize1=cv2.resize(frame1,(1600,1600))
        #frameresize2=cv2.resize(frame2,(1600,1600))
        if(threading.activeCount() == 1):
            th0 = FaceThread(frameresize0, cameraNum[0])
            #th1 = FaceThread(frameresize1, cameraNum[1])
            #th2 = FaceThread(frameresize2, cameraNum[2])
            th0.start()
            #th1.start()
            #th2.start()
        cv2.imshow('camera0 capture', frameresize0)
        #cv2.imshow('camera1 capture', frameresize1)
        #cv2.imshow('camera2 capture', frameresize2)
        k = cv2.waitKey(10)
        if k == 27:
            break

    cap[0].release()
    #cap[1].release()
    #cap[2].release()
    cv2.destroyAllWindows()
