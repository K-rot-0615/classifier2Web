import argparse
from image import faceDetect
from image import dataRead
from labeling import getPredictData
from alexnet import Alex

import cv2
import chainer
import chainer.functions as F
import chainer.links as L
from chainer import Variable


def predict_image(model, data):
    x = Variable(data)
    y = F.softmax(model.predictor(x.data[0]))
    return y.data[0]


def main():
    parser = argparse.ArgumentParser(description='face prediction')
    parser.add_argument('--testPath', '-t', type=str, default='./datasets/test/')
    parser.add_argument('--detect', '-d', type=str, default='')
    parser.add_argument('--output', '-o', type=str, default='')
    parser.add_argument('--size', '-s', type=int, default=128)
    parser.add_argument('--model', '-m', type=str, default='output2.model')
    parser.add_argument('--channel', '-c', type=int, default=3)

    args = parser.parse_args()

    #load model and translate it from gpu model to cpu model
    model = L.Classifier(Alex())
    chainer.serializers.load_npz(args.model, model)
    model.to_cpu()

    #save file as predicted data
    #cap = cv2.VideoCapture(0)
    #while True:
        #ret,frame = cap.read()
        #cv2.imshow('predicted data', frame)
        #predicted_data = faceDetect(frame, 0, args.detect, args.output, args.size)

        # predict
        #images = dataRead(args.testPath)
        #print images
        #for image in images:
            #print image
            #test_data = getPredictData(image, args.channel)
            #result = predict_image(model, test_data)
            #print result

        # escape from the roop
        #k = cv2.waitKey(10)
        #if k == 27:
            #break

    #cap.release()
    #cv2.destroyAllWindows()

    images = dataRead(args.testPath)
    for image in images:
        test_data = getPredictData(image, args.channel)
        result = predict_image(model, test_data)
        print result


if __name__ == '__main__':
    main()
