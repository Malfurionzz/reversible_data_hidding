import os
import numpy as np
# from multiprocessing import shared_memory
from multiprocessing import Process
# from multiprocessing.managers import SharedMemoryManager
from multiprocessing import Queue
import cv2
import numpy as np
import socket
import time
import sys
def capture(q,h,w):
    # q: 用于缓存frame的队列
    # h: 窗口的height
    # w: 窗口的width
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    out_win='raw'
    cv2.namedWindow(out_win, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(out_win, w, h)
    cv2.moveWindow(out_win,400,200)
    while True:
        # 逐帧捕获
        ret, frame = cap.read()
        q.put(cv2.resize(frame, (256, 256)))
        # q.put(frame)
        # frame is a ndarray with shape (H,W,C)
        # 如果正确读取帧，ret为True
        if not ret:
            break
        cv2.imshow(out_win, frame)
        cv2.waitKey(100)
        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyWindow(out_win)
            break
# 完成所有操作后，释放捕获器
    

def process(q,h,w):
    # q: 用于缓存frame的队列
    # h: 窗口的height
    # w: 窗口的width

    out_win='processed'
    cv2.namedWindow(out_win, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(out_win, w, h)
    cv2.moveWindow(out_win,800,200)
    cnt = 1
    start = time.time()
    while True:
        # 从队列中取帧
        # frame = []
        # for i in range(1):
        #     frame.append(q.get()
        frame = q.get()
        # TODO: more detailed process e.g. predicting?
        data = np.frombuffer(frame, np.uint8)
        # image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        image = data.reshape(256,256,3)
        cv2.imshow(out_win,image)
        cnt += 1
        if cnt % 11 == 0:
            end = time.time()
            print("fps=",str(int(10/(end-start))))
            start = time.time()

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyWindow(out_win)


def recvall(sock, count):
    buf = b''  # buf是一个byte类型
    while count:
        buf += sock.recv(1024) if count > 1024 else sock.recv(count)
        count = 256*256*3 - len(buf)
    return buf



def SendVideo(q):
    # 建立sock连接
    # address要连接的服务器IP地址和端口号
    address = ('121.248.48.131', 23556)
    try:
        # 建立socket对象，参数意义见https://blog.csdn.net/rebelqsp/article/details/22109925
        # socket.AF_INET：服务器之间网络通信
        # socket.SOCK_STREAM：流式socket , for TCP
        sock = socket.socket()
        # 开启连接
        sock.connect(address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    #
    # ret, frame = capture.read()
    # # 压缩参数，后面cv2.imencode将会用到，对于jpeg来说，15代表图像质量，越高代表图像质量越好为 0-100，默认95
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]

    frame = q.get()
    cnt = 0
    while True:
        # 停止0.1S 防止发送过快服务的处理不过来，如果服务端的处理很多，那么应该加大这个值
        # time.sleep(0.1)
        # cv2.imencode将图片格式转换(编码)成流数据，赋值到内存缓存中;主要用于图像数据格式的压缩，方便网络传输
        # '.jpg'表示将图片按照jpg格式编码。
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        # 建立矩阵
        data = np.array(imgencode)
        # 将numpy矩阵转换成字符形式，以便在网络中传输

        stringData = data.tostring()
        # data = np.frombuffer(stringData, np.uint8)
        # decimg = cv2.imdecode(data, cv2.IMREAD_COLOR)

        # 先发送要发送的数据的长度
        # ljust() 方法返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串
        sock.send(str.encode(str(len(stringData)).ljust(16)))
        # 发送数据
        sock.send(stringData)
        # cnt += 1
        # if cnt % 10 == 0:
        #     print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),'客户端发送了',str(cnt),'帧')

        frame = q.get()
        if cv2.waitKey(10) == 27:
            break
    sock.close()

import matplotlib.pyplot as plt
def ReceiveVideo(q):
    # 建立sock连接
    # address要连接的服务器IP地址和端口号
    address = ('121.248.48.131', 23557)
    try:
        # 建立socket对象，参数意义见https://blog.csdn.net/rebelqsp/article/details/22109925
        # socket.AF_INET：服务器之间网络通信
        # socket.SOCK_STREAM：流式socket , for TCP
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock = socket.socket()
        # 开启连接
        sock.connect(address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    #
    # ret, frame = capture.read()
    # # 压缩参数，后面cv2.imencode将会用到，对于jpeg来说，15代表图像质量，越高代表图像质量越好为 0-100，默认95
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
    cnt = 0
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1572864)
    # print('缓冲区大小',str(sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)))
    while True:
        # receive = sock.recv(16)
        # sock.send(str.encode(str(len('ack')).ljust(16)))
        # if len(receive):
        # stringData = recvall(sock.recv(int(receive)), int(receive))
        stringData = recvall(sock,256*256*3)
        q.put(stringData)
        cnt += 1
        if cnt % 1 == 0:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '客户端接收了', str(cnt), '帧')


        if cv2.waitKey(10) == 27:
            break
    sock.close()


if __name__ == '__main__':
    qin = Queue()
    qout = Queue()
    # capture(q)
    capturer=Process(target=capture, args=(qin,400,400))
    sendVideo=Process(target=SendVideo, kwargs={'q': qin})
    receiveVideo = Process(target=ReceiveVideo, kwargs={'q':qout})
    processor=Process(target=process, args=(qout,400,400))
    capturer.start()
    sendVideo.start()
    receiveVideo.start()
    processor.start()
    capturer.join()
    sendVideo.join()
    receiveVideo.join()
    processor.join()


