import cv2 as cv
import sys
from opts import preprocessingArgumentParser

def genNeedImg(imgPath,size=None,flag='binary'):
    '''
    用于生成指定大小的灰度图或二值图, imgPath为图像路径
    size为lst类型，用于指定生成图像的尺寸, 如：(512,512)，默认为None表示输出原图像尺寸
    flag为标志转换类型，默认为binary，可选的值为binary或gray
    '''
    imgRaw = cv.imread(imgPath)
   
    if size != None: # 调整图像尺寸
        imgRaw= cv.resize(imgRaw,size)
    else:
        size=[imgRaw.shape[0],imgRaw.shape[1]]
    imgGray = cv.cvtColor(imgRaw,cv.COLOR_RGB2GRAY) # 转换颜色空间为灰度
    # print(imgPath)
    imgName = imgPath.split('/')[-1].split('.')[0] # 获取图像原始名称
    if flag == 'gray': # 生成灰度图
        cv.imwrite('./images/{}_gray.bmp'.format(imgName),imgGray)
        print('Gray image generated!')
        return './images/{}_gray.bmp'.format(imgName)
    else: # 生成二值图
        ret, imgBinary = cv.threshold(imgGray,127,255,cv.THRESH_BINARY)
        cv.imwrite('./images/{}_binary{}.bmp'.format(imgName,size),imgBinary) 
        print('Binary image generated!')
        print('threshold:{}'.format(ret)) # 输出转换阈值
        return imgBinary




if __name__ == "__main__":
    opt=preprocessingArgumentParser()
    rawimgName = opt.emb_path
    imgEmbedPath=genNeedImg(rawimgName,opt.size,flag=opt.preprocess)