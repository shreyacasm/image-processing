import cv2
import numpy as np
import pytesseract
from PIL import ImageEnhance, ImageOps
from matplotlib import pyplot as plt

if __name__ == '__main__':
    ## Read
    img = cv2.imread("test-bg/shadow.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # result = img.copy()
    ## (1) Create long line kernel, and do morph-close-op
    kernel = np.ones((1, 40), np.uint8)
    morphed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite("result/line_detected.png", morphed)

    ## (2) Invert the morphed image, and add to the source image:
    dst = cv2.add(gray, (255 - morphed))

    ## extra steps to filter
    dst_n = dst
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilation = cv2.dilate(dst_n, kernel, iterations=2)
    dilation = cv2.morphologyEx(dst_n, cv2.MORPH_CLOSE, kernel)
    #dilation = 255 - dilation

    cv2.imshow('img_wanted', dst)
    cv2.imwrite("result/line_removed.png", dst)
    cv2.imwrite("result/dilated.png", dilation)
    cv2.imshow("after_edit", dilation)

    data = pytesseract.image_to_string(dst)
    print("through dir:", data)

    data = pytesseract.image_to_string(dilation)
    print("through add", data)
    cv2.waitKey()