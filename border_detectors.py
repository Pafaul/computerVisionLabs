import numpy as np

class BorderDetector:
    u_mask = None
    v_mask = None
    threshold = None

    def detectBorders(self, img_part):
        u = self.getSum(img_part, self.u_mask)
        v = self.getSum(img_part, self.v_mask)
        totalDiff = (u**2 + v**2)**0.5
        if (totalDiff > self.threshold):
            return 255
        else:
            return 0

    def getSum(self, img, mask):
        return sum(sum(np.multiply(img, mask)))

class RobertsCross(BorderDetector):
    u_mask = np.array([[1,0], [0,-1]])
    v_mask = np.array([[0,1], [-1,0]])
    def __init__(self, threshold = 0):
        self.threshold = threshold
        self.x_diffs = [0,1]
        self.y_diffs = [0,1]

class PrewittOperator(BorderDetector):
    u_mask = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    v_mask = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    def __init__(self, threshold = 0):
        self.threshold = threshold
        self.x_diffs = [-1,1]
        self.y_diffs = [-1,1]
        

class KirschOperator(BorderDetector):
    u_mask = np.array([[5,-3,-3],[5,0,-3],[5,-3,-3]])
    v_mask = np.array([[5,5,5],[-3,0,-3],[-3,-3,-3]])
    def __init__(self, threshold = 0):
        self.threshold = threshold
        self.x_diffs = [-1,1]
        self.y_diffs = [-1,1]


def detectBordersOnImage(image, bd: BorderDetector):
    def getImagePart(image, shape, borders):
        img_part = np.zeros(shape)
        for i in range(borders[0][0], borders[0][1]+1):
            for j in range(borders[1][0], borders[1][1]+1):
                img_part[i-borders[0][0]][j-borders[1][0]] = image[i][j]
        return img_part


    res_image = np.zeros(image.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (i + bd.x_diffs[0] >= 0) and \
               (i + bd.x_diffs[1] < image.shape[0]) and \
               (j + bd.y_diffs[0] >= 0) and \
               (j + bd.y_diffs[1] < image.shape[1]):

                res_image[i][j] = bd.detectBorders(
                    getImagePart(
                        image,
                        (bd.x_diffs[1]-bd.x_diffs[0]+1, bd.y_diffs[1]-bd.y_diffs[0]+1),
                        [
                            [i+bd.x_diffs[0],i+bd.x_diffs[1]],
                            [j+bd.y_diffs[0],j+bd.y_diffs[1]]
                        ]
                ))
    return res_image