import cv2
import numpy as np
import math
import sys

DIRS = {
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
}

# widen each pixel to 3x3
def widen(img):
    h, w = img.shape
    arr = np.zeros((h, w, 3), np.uint8)
    for i in range(0, h):
        for j in range(0, w):
            if (img[i][j] != [0, 0, 0]).all():
                arr[i][j] = [255, 255, 255]
                for dir in DIRS:
                    if (i + dir[0]) >= 0 and (i + dir[0]) < h and (j + dir[1]) >= 0 and (j + dir[1]) < w:
                        arr[i + dir[0]][j + dir[1]] = [255, 255, 255]
    
    return arr

def main():
    filename = sys.argv[1]
    img = cv2.imread(f"in/{filename}")
    low = int(sys.argv[2])
    high = int(sys.argv[3])

    white = input("black bg? (Y/n) ") == "n"
    invert = input("invert? (Y/n) ") != "n"

    edge = cv2.Canny(img, low, high)

    h, w, _ = img.shape
    # print(h, w)

    colors = cv2.imread("in/colors.png")
    edge_color = widen(edge)

    for i in range(0, h):
        for j in range(0, w):
            if not invert:
                if not (edge_color[i][j] == [0, 0, 0]).all():
                    edge_color[i][j] = colors[math.floor((i / h) * 256)][math.floor((j / w) * 256)]
                elif white:
                    edge_color[i][j] = [255, 255, 255]
            else:
                if (edge_color[i][j] == [0, 0, 0]).all():
                    edge_color[i][j] = colors[math.floor((i / h) * 256)][math.floor((j / w) * 256)]
                elif not white:
                    edge_color[i][j] = [0, 0, 0]

    # cv2.imshow("rainbow", edge_color)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    cv2.imwrite(f"out/ec_{filename}", edge_color)

if __name__ == "__main__":
    main()