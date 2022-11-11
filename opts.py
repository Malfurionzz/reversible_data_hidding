import argparse


def embedingArgumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cover_path', type=str,default='images/pt.jpg',help='image for covering')
    parser.add_argument('--emb_path', type=str, default='images/hid_binary[100, 100].bmp', help='image for embedding')
    return parser.parse_args()


def preprocessingArgumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emb_path', type=str, default='images/hid.jpg', help='image for embedding')
    parser.add_argument('--preprocess', type=str, default='binary', help='Embeded image preprocessing method, default gray level, currently binary and gray supportted')
    parser.add_argument('--size', type=list, default=[50,50], help='define size of embeding img [H,W]')
    return parser.parse_args()


def extractingArgumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', type=str, default='imgs/pt.jpg_embeding.bmp', help='image for embedding')
    parser.add_argument('--pivot', type=int, default=49, help='pp')
    parser.add_argument('--size', type=list, default=[100,100], help='define size of embeding img [H,W]')
    return parser.parse_args()


def testArgumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_path', type=str, default='images/hid_binary[100, 100].bmp',help='path of image for contrast')
    parser.add_argument('--extract_path', type=str, default='imgs/pt.jpg_embeding.bmp',help='embed image path')
    parser.add_argument('--pivot', type=int, default=49, help='pp')
    parser.add_argument('--size', type=list, default=[100,100], help='define size of embeding img [H,W]')
    return parser.parse_args()

