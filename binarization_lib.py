import cv2 as cv
import numpy as np
from math import floor

def histogram(image: np.array) -> [dict, int, int]:
    brightness = {}
    minB = 256
    maxB = -1
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pb = image[i][j]
            if pb > maxB:
                maxB = pb
            if pb < minB:
                minB = pb
            
            if pb in brightness.keys():
                brightness[pb] += 1
            else:
                brightness[pb] = 1
    return [brightness, minB, maxB]

def calculate_mean(hist:dict, min_val: int, max_val: int) -> [float, int]:
    m = 0
    count = 0
    i = min_val
    for key in hist.keys():
        m += (key)*hist[key]
        count += hist[key]
        i += 1
    m /= count
    return m, count

def calculate_dispersion(hist:dict, min_val: int, max_val: int) -> float:
    mean, count = calculate_mean(hist, min_val, max_val)
    disp = 0
    i = min_val
    while i < max_val:
        for _ in range(hist[i]):
            disp += (i - mean)**2
        i += 1
    
    disp /= (count-1)
    return disp

def get_optimal_threshold(image: np.array):
    hist, min_val, max_val = histogram(image)
    deltaBright = floor((max_val-min_val)/20)

    max_disp = calculate_dispersion(hist, min_val, max_val)/(256.0**2)

    currentB = min_val + deltaBright

    k = []

    while (currentB < max_val):
        a = calculate_dispersion(hist, min_val, currentB)
        b = calculate_dispersion(hist, currentB, max_val)
        k.append(1. - (a+b)/max_disp)
        currentB += deltaBright

    optimal_threshold = max(k)
    return optimal_threshold

def binarize_image(image: np.array, threshold: int) -> np.array:
    res_image = np.zeros(image.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (image[i][j] > threshold):
                res_image[i][j] = 255

    return res_image

def change_image_intensity(image: np.array, in_param: list, out_param: list) -> np.array:
    res_image = np.zeros(image.shape)
    in_param_len = in_param[1] - in_param[0]
    out_param_len = out_param[1] - out_param[0]
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            res_image[i][j] = np.clip(in_param[0]*res_image[i][j]+in_param[1],0,255)
            # pv = image[i][j]
            # if (pv >= in_param[0]) and (pv <= in_param[1]):
            #     res_image[i][j] = (((pv - in_param[0])/float(in_param_len)*float(out_param_len))+out_param[0])/255.0
            # elif (pv > in_param[1]):
            #     res_image[i,j] = out_param[1]
    return res_image