import cv2
import numpy as np
import math
import sys
# from Font.funcs import putTTFText

SPECTRUM = " .:-=+*#%@"
# SPECTRUM = " .:*-=+%@#"
IMG_SPECTRUM = [cv2.cvtColor(cv2.imread(f"util/font{i}.png"), cv2.COLOR_RGB2RGBA) for i in range(0, 10)]

def main():
    filename = sys.argv[1]
    img = cv2.imread(f"in/{filename}", 0)
    # img2 = cv2.imread(f"in/{filename}")

    h, w = img.shape
    pix = int(sys.argv[2])
    small = cv2.resize(img, (w // pix, h // pix))
    # img2_fix = cv2.cvtColor(cv2.resize(img2, ((w // pix) * 5, (h // pix) * 5)), cv2.COLOR_RGB2RGBA)
    # print(h, w)

    white = input("black bg? (Y/n) ") == "n"
    invert = input("invert? (Y/n) ") != "n"

    new_h = (h // pix) * 5
    new_w = (w // pix) * 5

    text = np.zeros((new_h, new_w, 4), np.uint8)
    for i in range(0, new_h):
        for j in range(0, new_w):
            text[i][j] = [0, 0, 0, 255]

    with open("test.txt", "w") as f:
        for i in range(0, h // pix):
            line = ""
            for j in range(0, w // pix):
                # text = putTTFText(text, SPECTRUM[int((small[i][j] / 256) * 10)], (j*5, i*5), "quinquefive/Quinquefive.ttf", 5)
                for k in range(0, 5):
                    for l in range(0, 5):
                        if(IMG_SPECTRUM[int((small[i][j] / 256) * 10)][k][l][3] != 0):
                            text[i*5 + k][j*5 + l] = IMG_SPECTRUM[int((small[i][j] / 256) * 10)][k][l]
                # text[(i*5):(i*5 + 5)][(j*5):(j*5 + 5)] = IMG_SPECTRUM[int((small[i][j] / 256) * 10)]
                line += SPECTRUM[int((small[i][j] / 256) * 10)]
            f.write(line + "\n")

    colors_rgb = cv2.imread("util/colors.png")
    colors = cv2.cvtColor(colors_rgb, cv2.COLOR_RGB2RGBA)
    for i in range(0, new_h):
        for j in range(0, new_w):
            if not invert:
                if not (text[i][j] == [0, 0, 0, 255]).all():
                    # text[i][j] = img2_fix[i][j]
                    text[i][j] = colors[math.floor((i / new_h) * 256)][math.floor((j / new_w) * 256)]
                elif white:
                    text[i][j] = [255, 255, 255, 255]
            else:
                if (text[i][j] == [0, 0, 0, 255]).all():
                    # text[i][j] = img2_fix[i][j]
                    text[i][j] = colors[math.floor((i / new_h) * 256)][math.floor((j / new_w) * 256)]
                elif not white:
                    text[i][j] = [0, 0, 0, 255]

    cv2.imwrite(f"out/ac_{filename}", text)

    # cap = cv2.VideoCapture(0)
    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    
    # cap.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()