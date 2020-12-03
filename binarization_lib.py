from cv2 import cv2
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

def calculate_dispersion(image, hist:dict, min_val: int, max_val: int) -> float:
    mean = 0
    disp = 0
    i = min_val
    count = 0
    while i < max_val:
        if i not in hist.keys():
            continue
        count += hist[i]
        mean += (i/256.0)*hist[i]
        i += 1
    mean /= count

    i = min_val
    while i < max_val:
        if i not in hist.keys():
            continue
        for _ in range(hist[i]):
            disp += (float(i)/256.0 - mean)**2
        i += 1
    
    disp /= (count-1)
    return disp

def get_optimal_threshold(image: np.array):
    hist, min_val, max_val = histogram(image)
    deltaBright = floor(abs(max_val-min_val)/20)

    max_disp = calculate_dispersion(image, hist, min_val, max_val)
    print('max:', max_disp)

    currentB = min_val + deltaBright

    k = []

    while (currentB < max_val):
        a = calculate_dispersion(image, hist, min_val, currentB)
        b = calculate_dispersion(image, hist, currentB, max_val)
        print(a, b)
        k.append(1. - (a+b)/max_disp)
        currentB += deltaBright

    print(k)
    optimal_threshold = max(k)
    return optimal_threshold

def binarize_image(image: np.array, threshold: int) -> np.array:
    res_image = np.zeros(image.shape, dtype=float)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (float(image[i][j])/256.0 > threshold):
                res_image[i][j] = 1.0

    return res_image
