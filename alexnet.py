import argparse
import numpy as np

import chainer
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer.training import extensions


class Alex(chainer.Chain):
    """Single-GPU AlexNet without partition toward the channel axis."""

    insize = 227

    def __init__(self, arg):
        super(Alex, self).__init__(
            conv1=L.convolution2D(3, 96, 11, stride=4)
            conv2=L.convolution2D(96, 256, 5, pad=2)
            conv3=L.convolution2D(256, 384, 3, pad=1)
            conv4=L.convolution2D(384, 384, 3, pad=1)
            conv5=L.convolution2D(384, 256, 3, pad=1)
            fc6=L.Linear(9216,4096)
            fc7=L.Linear(4096,4096)
            fc8=L.Linear(4096,1000)
        )
        self.train = True

    def __call__(self, x):
        h = F.max_pooling_2d(F.local_response_normalization(
            F.relu(self.conv1(x))), 3, stride=2)
        h = F.max_pooling_2d(F.local_response_normalization(
            F.relu(self.conv2(h))), 3, stride=2)
        h = F.relu(self.conv3(h))
        h = F.relu(self.conv4(h))
        h = F.max_pooling_2d(F.relu(self.conv5(h)), 3, stride=2)
        h = F.dropout(F.relu(self.fc6(h)), train=self.train)
        h = F.dropout(F.relu(self.fc6(h)), train=self.train)
        h = self.fc8(h)

        return h

    def main():
        parser = argparse.ArgumentParser(description='fruit classifier')
        parser.add_argument('--batchsize','-b',type=int,default=100)
        parser.add_argument('--epoch','-e',type=int,default=20)
        parser.add_argument('--gpu','-g',type=int,default=-1)
        parser.add_argument('--out','-o',default='result')

        args = parser.parse_args()

        print('GPU: {}'.format(args.gpu))
        print('# unit: {}'.format(args.unit))
        print('# Minbatch-size: {}'.format(args.batchsize))
        print('# epoch: {}'.format(args.epoch))
        print('')

        model = L.Classifier(Alex(args.channnel, len(detasets)))
        if args.gpu >= 0:
            chainer.cuda.get_device(args.gpu).use()
            model.to_gpu()

        # setup the optimizer
        optimizer = chainer.optimizer.Adam()
        optimizer.setup(model)

        if args.model != '' and args.optimizer != '':
            chainer.serializers.load_npz(args.model, model)
            chainer.serializers.load_npz(args.optimizer, optimizer)

        train_iter = chainer.iterators.SerialIterator(train, args.batchsize)
        test_iter = chainer.iterators.SerialIterator(test, args.batchsize, repeat=False, shuffle=False)

        #setup the trainer
        updater = training.StandardUpdater()
        trainer = training.Trainer(updater, (args.epoch, 'epoch'), put=args.out)

        trainer.extend(extensions.Evaluator(test_iter, model, device=args.gpu))
        trainer.extend(extensions.LogReport())
        trainer.extend(extensions.PrintReport(
            ['epoch', 'main/loss', 'validation/main/loss', 'main/accuracy', 'validation/main/accuracy']
        ))

        trainer.run()

        #save models

        #send to browser


if __name__ == '__main__':
    main()
