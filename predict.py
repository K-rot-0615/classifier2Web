import argparse
from image import faceRead
from labeling import getPredictData

import chainer
import chainer.functions as F


def predict_image(model, data):
    x = Valiable(data)
    y = F.softmax(model.predictor(x.data[0]))
    return y


def main():
    parser = argparse.ArgumentParser(description='face prediction')
    parser.add_argument('--data', '-d', type=str, default='./datasets/ryota' )
    parser.add_argument('--model', '-m', type=str)

    images = faceRead(args.data)
    for image in images:
        test_data = getPredictData(image)
        result = predict_image(args.model, args.data)
        print result


if __name__ == '__main__':
    main()
