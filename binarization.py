import cv2
import numpy as np
import matplotlib.pyplot as plt

from binarization_lib import histogram, get_optimal_threshold, binarize_image, change_image_intensity

def load_image(filename):
    try:
        image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        image = image.astype(np.float32)
        return image
    except:
        print('Image not found')
        raise Exception('Image not found')

def build_histogram(histogram: dict, min_val: int, max_val: int):
    x = sorted(list(histogram.keys()))
    x.pop(0)
    y = [histogram[valKey] for valKey in x]
    plt.bar(x, height=y)
    plt.show()
    return

def main():
    image = load_image('./penguin.jpg')
    mean = cv2.mean(image)
    
    intensities = [
        [0.5, 50],
        [1.0, 100],
        [1.5, 50],
        [2.0, 0]
    ]

    counter = 0

    for intensity in intensities:
        res_image = cv2.convertScaleAbs(image, alpha=intensity[0], beta=intensity[1])
        cv2.imshow('t', res_image)
    #     print(f'Processing image {counter}...')
        hist, min_val, max_val = histogram(res_image)

        threshold = get_optimal_threshold(res_image)
        print(threshold)
        res_image = binarize_image(image, threshold)
        cv2.imshow('res', res_image)
        cv2.waitKey(0)
        cv2.imwrite(str(counter)+'_res.png', res_image)
        counter += 1

main()