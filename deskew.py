# import the necessary packages
import numpy as np
import cv2
import pytesseract
from PIL import Image, ImageOps


def deskew(cvImage):
    newImage = cvImage.copy()
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('states/1-grayscale.png', gray)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    cv2.imwrite('states/2-blur.png', blur)

    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cv2.imwrite('states/3-threshold.png', thresh)

    constant = cv2.copyMakeBorder(thresh, 100, 100, 100, 100, cv2.BORDER_CONSTANT)
    cv2.imwrite('states/output.png', constant)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(constant, kernel, iterations=5)
    cv2.imwrite('states/4-dilate.png', dilate)
    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates

    coords = np.column_stack(np.where(dilate > 0))
    angle = cv2.minAreaRect(coords)[-1]
    print("[after coords INFO] angle: {:.2f}".format(angle))

    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle > 45:
        angle = -(-90 + angle)
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle

    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # draw the correction angle on the image so we can validate it
    # cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
    #     (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # show the output image
    cv2.imwrite('result/2-rot.png', rotated)
    print("[INFO] angle: {:.3f}".format(angle))
    cv2.imshow("Input", image)
    cv2.imshow("Rotated", rotated)
    # print(pytesseract.image_to_osd(cv2.imread('result/2-rot.png')))
    print(pytesseract.image_to_string(rotated))
    cv2.waitKey(0)


if __name__ == '__main__':
    image = cv2.imread('line_removed.png')
    deskew(image)
