from PIL import Image
import subprocess
import numpy as np
import cv2


def image_pretreat(img):
    grey = img.convert('L')
    binary = grey.point(lambda x: 0 if x > 170 else 255)
    binary.show()


if __name__ == '__main__':
    img = cv2.imread('plate2.jpg')
    print(img)
    img[:, :, 1] = 0
    cv2.imshow('test', img)
    cv2.waitKey()