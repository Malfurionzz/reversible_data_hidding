import cv2
import numpy as np
import copy

from opts import extractingArgumentParser

def extracting(imgPath,pivot,imgEmbedSize):

	embed = cv2.imread(imgPath,cv2.IMREAD_GRAYSCALE)

	pivot=pivot
	extract=copy.deepcopy(embed)
	binStreamList=[]
	value=[]
	embedList=[]
	for i in range(embed.shape[0]):
		for j in range(embed.shape[1]):
			if extract[i][j]==pivot:
				value.append((i,j,extract[i][j]))
				binStreamList.append(0)
			if extract[i][j]==pivot+1:
				value.append((i,j,extract[i][j]))
				binStreamList.append(1)
				extract[i][j]=extract[i][j]-1

	for i in range(embed.shape[0]):
		for j in range(embed.shape[1]):
			if extract[i][j]> pivot and extract[i][j]<255:
				extract[i,j] = extract[i][j]-1
	for b in binStreamList:
		if b == 1:
			embedList.append(255)
		else:
			embedList.append(0)

	imgEmbedMatrix = [ embedList[i*imgEmbedSize[0]:(i+1)*imgEmbedSize[0]] for i in range(imgEmbedSize[1]) ]
	imgEmbed = np.array(imgEmbedMatrix,dtype=np.uint8)
	cv2.imwrite('./imgs/{}_extract.bmp'.format(imgPath.split('/')[-1].split('.')[0]),imgEmbed)
	cv2.imwrite('./imgs/{}_cover.bmp'.format(imgPath.split('/')[-1].split('.')[0]),extract)
	print('Extracting done!')


if __name__ == '__main__':
	opt=extractingArgumentParser()
	extracting(opt.img_path,opt.pivot,opt.size)
