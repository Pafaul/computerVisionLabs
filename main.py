import cv2
import numpy as np
from border_detectors import detectBordersOnImage,RobertsCross,PrewittOperator,KirschOperator

def readImageGrayscale(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img.transpose()

def main():
    img = readImageGrayscale('2.jpg')
    bordersRC = detectBordersOnImage(img, RobertsCross(50)).transpose()
    bordersPO = detectBordersOnImage(img, PrewittOperator(100)).transpose()
    bordersKO = detectBordersOnImage(img, KirschOperator(200)).transpose()
    img = img.transpose()
    cv2.imwrite('grayscale.png', img)
    cv2.imwrite('RC.png', bordersRC)
    cv2.imwrite('PO.png', bordersPO)
    cv2.imwrite('KO.png', bordersKO)

    cv2.imshow('Original image', img)
    cv2.imshow('RC', bordersRC)
    cv2.imshow('PO', bordersPO)
    cv2.imshow('KO', bordersKO)

    cv2.waitKey(0)

if __name__ == '__main__':
    main()