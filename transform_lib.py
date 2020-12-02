import cv2
import numpy as np
from math import sin,cos,ceil

def create_black_image(w, h):
    return np.zeros((h,w), np.uint8)

def create_white_image(h,w):
    return np.ones((h,w),np.uint8)*255

def calc_point_position(point_coordinates, k, omega, c, f):
    x = point_coordinates[0]
    y = -point_coordinates[1]

    u = ceil( x*k*cos(omega) + k*y*sin(omega) + c)
    v = ceil( -k*x*sin(omega) + k*y*cos(omega) + f)

    return [u,v]

def transform_image(image, result_image, k=0, omega=0, c=0, f=0):
    image_size = list(image.shape)
    image_size.reverse()
    edge_points = [[0,0], [image_size[0]-1,0], [0, image_size[1]-1], [image_size[0]-1, image_size[1]-1]]
    edges = [calc_point_position(point, k, omega, c, f) for point in edge_points]

    first = lambda x: x[0]
    second = lambda x: x[1]
    new_image_x = (max(edges, key=first)[0] - min(edges, key=first)[0])
    new_image_y = (max(edges, key=second)[1] - min(edges, key=second)[1])
    delta_min_x = min(edges, key=first)[0]
    delta_min_y = min(edges, key=second)[1]

    # result_image = create_white_image((new_image_x+abs(c)+1)*2, (new_image_y+abs(f)+1)*2)

    for i in range(0, image_size[0]):
        for j in range(0, image_size[1]):
            new_coords = calc_point_position([i, j], k, omega, c, f)
            new_coords[0] -= delta_min_x; new_coords[0] += c
            new_coords[1] -= delta_min_y; new_coords[1] += f
            result_image[new_coords[0]][new_coords[1]] = 0

    return result_image