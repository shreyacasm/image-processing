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
    cv2.imwrite("line_detected.png", morphed)

    ## (2) Invert the morphed image, and add to the source image:
    dst = cv2.add(gray, (255 - morphed))

    ## extra steps to filter
    imagec = dst.copy()
    imagec = cv2.medianBlur(imagec, 5)
    imagec = cv2.adaptiveThreshold(imagec, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    opening = cv2.morphologyEx(imagec, cv2.MORPH_OPEN, kernel)

    imagec = 255 - opening

    cv2.imshow('img_wanted', dst)
    cv2.imwrite("line_removed.png", dst)
    cv2.imshow("after_edit", imagec)

    # result[dst == 0] = (255, 255, 255)
    # retouch_mask = (result <= [250., 250., 250.]).all(axis=2)
    # result[retouch_mask] = [0, 0, 0]
    # cv2.imshow('darken', dst)

    data = pytesseract.image_to_string(dst)
    print("through dir:", data)

    data = pytesseract.image_to_string(imagec)
    print("through add", imagec)
    cv2.waitKey()