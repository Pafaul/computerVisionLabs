import cv2
import numpy as np
from math import pi

from transform_lib import *

def main():
    image = create_black_image(150, 125)
    res_image = create_white_image(500,700)
    cv2.imwrite('original_image.png', image)
    cv2.imshow('test', image)
    cv2.waitKey(0)

    res_image = transform_image(image, res_image, k=0.5, omega=pi/4, c=20, f=20)
    cv2.imwrite('1.png', res_image)
    res_image = transform_image(image, res_image, k=1.3, omega=pi/2, c=250, f=20)
    cv2.imwrite('2.png', res_image)
    res_image = transform_image(image, res_image, k=2, omega=pi*2/3, c=20, f=300)
    cv2.imwrite('3.png', res_image)
    print(res_image.shape)
    cv2.imshow('res', res_image)
    cv2.waitKey(0)

main()