import cv2
import numpy as np
import copy

from opts import embedingArgumentParser


def genEmbedBinStream(imgEmbed):
    '''将嵌入图像抽取成比特流'''
    rowScale = imgEmbed.shape[0]
    columnScale = imgEmbed.shape[1]
    binStreamList = []
    for i in range(rowScale):
        for j in range(columnScale):
            if imgEmbed.item(i,j) != 0:
                imgEmbed.itemset((i,j),1)
            binStreamList.append(imgEmbed.item(i,j))
    return binStreamList


def embedding(coverPath,embedingPath):
	coverImg = cv2.imread(coverPath,cv2.IMREAD_GRAYSCALE)
	embedingImg = cv2.imread(embedingPath,cv2.IMREAD_GRAYSCALE)
	binStreamList=genEmbedBinStream(embedingImg)
	hist,_ = np.histogram(coverImg.ravel(),256,[0,256])
	maxEmbedingSpace=max(hist)
	print(maxEmbedingSpace)
	if len(binStreamList)>maxEmbedingSpace:
		raise RuntimeError('Embeding space overloading!')

	maxDistributionPixelValue=np.argmax(hist)
	print(maxDistributionPixelValue)
	embed=copy.deepcopy(coverImg)

	for i in range(coverImg.shape[0]):
		for j in range(coverImg.shape[1]):
			if embed[i][j]> maxDistributionPixelValue and embed[i][j]<255:
				embed[i,j] = embed[i][j]+1
				
	# m =''.join(format(ord(x),'08b') for x in strp)
	embedingSapceList=np.argwhere(embed==maxDistributionPixelValue)
	embedZone=[embedingSapceList[i] for i in range(min(len(binStreamList),len(embedingSapceList)))]
	for bin,ind in zip(binStreamList,embedZone):
		embed[ind[0]][ind[1]]=embed[ind[0]][ind[1]]+int(bin)
	cv2.imwrite('imgs/{}_embeding.bmp'.format(coverPath.split('/')[-1]),embed)
	return embed

if __name__ == '__main__':
	opt=embedingArgumentParser()
	embedding(opt.cover_path,opt.emb_path)














