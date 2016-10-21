# -*- coding:utf-8 -*-

import argparse
import numpy as np
import glob
from PIL import image
from chainer.datasets import tuple_dataset


def labeling():
    imageData = []
    labelData = []

    # path and label
    for n in data:
        path = n[0]
        label = n[1]
        imgList = glob.glob(path + '*')
        for imgName in imgList:
            img = Image.open(imgName)
            r,g,b = img.split()
            imgData_R = np.asarray([np.float32(r)/255.0])
            imgData_G = np.asarray([np.float32(g)/255.0])
            imgData_B = np.asarray([np.float32(b)/255.0])

            imgData = np.asarray([np.float32(imgData_R,imgData_G,imgData_B)
            lblData = np.int32(label)

            imageData.append(imgData)
            labelData.append(lblData)

    threshold = np.int32(len(imageData)/10*8)
    train = tuple_dataset.TupleDataset(imageData[0:threshold], labelData[0:threshold])
    test = tuple_dataset.TupleDataset(imageData[threshold:], labelData[threshold:])

return train, test


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='labeling images')
    parser.add_argument('--data_dir','-d',type=str,default='others')
    parser.add_argument('--label','-l',type=int,default=0)

    args = parser.parse_args()

    data = []
    data.append(np.asarray(['./datasets/others', 0]))
    data.append(np.asarray(['./datasets/myself', 1]))
    train, test = labeling(data)
