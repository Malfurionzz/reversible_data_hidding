import os
import cv2
from skimage.metrics import mean_squared_error as mse
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

import numpy as np
import pandas as pd
from opts import testArgumentParser
from utils import sp_noise,gaussian_noise,random_noise
from extraction import extracting

fileList=[]
pivotList=[]
spaceList=[]
for root, dirs, files in os.walk("./n07717556/", topdown=False):
    fileList=files
    for f in files:
        coverImg=cv2.imread(root+f,cv2.IMREAD_GRAYSCALE)
        hist,_ = np.histogram(coverImg.ravel(),256,[0,256])
        spaceList.append(max(hist))
        pivotList.append(np.argmax(hist))

coverList=[f for f,space in zip(fileList,spaceList) if space>2500]
df=pd.DataFrame(data=coverList)
df.to_csv('filelist.csv')

# print(pivotList)
print(spaceList)
# rawCover = cv2.imread('images/pt.jpg',cv2.IMREAD_GRAYSCALE)
# rawHid = cv2.imread('images/hid_binary[100, 100].bmp',cv2.IMREAD_GRAYSCALE)
# embed = cv2.imread('imgs/pt.jpg_embeding.bmp',cv2.IMREAD_GRAYSCALE)
# extractedCover = cv2.imread('imgs/pt_cover.bmp',cv2.IMREAD_GRAYSCALE)
# extractedHid = cv2.imread('imgs/pt_extract.bmp',cv2.IMREAD_GRAYSCALE)

# print('ssim-->',ssim(rawCover,embed))
# print('mse-->',mse(rawCover,embed))
# print('psnr-->',psnr(rawCover,embed))

# print('ssim-->',ssim(rawCover,extractedCover))
# print('mse-->',mse(rawCover,extractedCover))
# print('psnr-->',psnr(rawCover,extractedCover))

# print('ssim-->',ssim(rawHid,extractedHid))
# print('mse-->',mse(rawHid,extractedHid))
# print('psnr-->',psnr(rawHid,extractedHid))