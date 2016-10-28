from alexnet import Alex
from labeling import labeling

import numpy as np
import argparse

import chainer
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer.training import extensions


def main():
    parser = argparse.ArgumentParser(description='training')
    parser.add_argument('--batchsize', '-b', type=int, default=20)
    parser.add_argument('--epoch', '-e', type=int, default=20)
    parser.add_argument('--gpu', '-g', type=int, default=-1)
    parser.add_argument('--out', '-o', default='result')

    args = parser.parse_args()

    print('GPU: {}'.format(args.gpu))
    #print('# unit: {}'.format(args.unit))
    #print('# Minbatch-size: {}'.format(args.batchsize))
    #print('# epoch: {}'.format(args.epoch))
    #print('')

    # prepare datasets
    data = []
    data.append(np.asarray(['./datasets/ryota/', 0]))
    data.append(np.asarray(['./datasets/masakatsu/', 1]))
    data.append(np.asarray(['./datasets/sakamoto/', 2]))
    train, test = labeling(data)

    model = L.Classifier(Alex())
    if args.gpu >= 0:
        chainer.cuda.get_device(args.gpu).use()
        model.to_gpu()

    # setup the optimizer
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)

    #if args.model != '' and args.optimizer != '':
        #chainer.serializers.load_npz(args.model, model)
        #chainer.serializers.load_npz(args.optimizer, optimizer)

    train_iter = chainer.iterators.SerialIterator(train, args.batchsize)
    test_iter = chainer.iterators.SerialIterator(
        test, args.batchsize, repeat=False, shuffle=False)

    # setup the trainer
    updater = training.StandardUpdater(train_iter, optimizer, device=args.gpu)
    trainer = training.Trainer(
        updater, (args.epoch, 'epoch'), out=args.out)

    trainer.extend(extensions.Evaluator(test_iter, model, device=args.gpu))
    trainer.extend(extensions.LogReport())
    trainer.extend(extensions.PrintReport(
        ['epoch', 'main/loss', 'validation/main/loss',
            'main/accuracy', 'validation/main/accuracy']
    ))

    trainer.run()

    # save models
    output = "output" + str(len(data))
    modelName = output + '.model'
    optimizerName = output + '.state'

    chainer.serializers.save_npz(modelName, model)
    chainer.serializers.save_npz(optimizerName, optimizer)


if __name__ == '__main__':
    main()
