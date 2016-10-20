import os
import argparse

def main():
    parser = argparse.ArgumentParsers(description='gather image dataset')

    parser.add_argument('-path',type=str,help='path to data folder',default='')
    parser.add_argument('-parallel',type=int,help='number of process to download',default=-1)
    parser.add_argument('-limit',type=int,help='upper limit of image count',default=-1)

    parser.add_argument('-imagenet',action='store_true',help='gather imagenet dataset')
    parser.add_argument('--wnid',type=str,help='target wnid')
    parser.add_argument('--subset',action='store_true',help='download child subset')
    args = parser.parse_args()

    current = os.getcwd()
    path = args.path if agrs.path else os.path.join(current, 'data/')

    api = None
    if args.imagenet:
        from mlimages.gather.imagenet import ImagenetAPI
        api = ImagenetAPI(path,parallel=args.parallel,limit=args.limit)
        api.logger.info('start to gather the imagenet images')
        api.gather(wnid=args.wnid,include_subset=args.subset)

if __name__ == '__main__':
    main()
