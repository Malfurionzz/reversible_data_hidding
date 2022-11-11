import random
import numpy as np
import copy
def sp_noise(img, proportion):
    '''
    添加椒盐噪声
    proportion的值表示加入噪声的量，可根据需要自行调整
    return: img_noise
    '''
    height, width = img.shape[0], img.shape[1]#获取高度宽度像素值
    num = int(height * width * proportion) #一个准备加入多少噪声小点
    noise_img=copy.deepcopy(img)
    for i in range(num):
        w = random.randint(0, width - 1)
        h = random.randint(0, height - 1)
        if random.randint(0, 1) == 0:
            noise_img[h, w] = 0
        else:
            noise_img[h, w] = 255
    return noise_img

def gaussian_noise(img_raw, mean, sigma):
    '''
        此函数用将产生的高斯噪声加到图片上
        传入:
            img   :  原图
            mean  :  均值
            sigma :  标准差
        返回:
            gaussian_out : 噪声处理后的图片
        '''
    img=copy.deepcopy(img_raw)
    # 将图片灰度标准化
    img = img / 255
    # 产生高斯 noise
    noise = np.random.normal(mean, sigma, img.shape)
    # 将噪声和图片叠加
    gaussian_out = img + noise
    # 将超过 1 的置 1，低于 0 的置 0
    gaussian_out = np.clip(gaussian_out, 0, 1)
    # 将图片灰度范围的恢复为 0-255
    gaussian_out = np.uint8(gaussian_out*255)
    # 将噪声范围搞为 0-255
    # noise = np.uint8(noise*255)
    return gaussian_out# 这里也会返回噪声，注意返回值

def random_noise(image,noise_num):
    '''
    添加随机噪点（实际上就是随机在图像上将像素点的灰度值变为255即白色）
    param image: 需要加噪的图片
    param noise_num: 添加的噪音点数目
    return: img_noise
    '''
    # 参数image：，noise_num：
    img_noise = copy.deepcopy(image)
    # cv2.imshow("src", img)
    rows, cols, chn = img_noise.shape
    # 加噪声
    for i in range(noise_num):
        x = np.random.randint(0, rows)#随机生成指定范围的整数
        y = np.random.randint(0, cols)
        img_noise[x, y, :] = 255
    return img_noise
