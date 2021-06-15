import cv2
import pytesseract
from matplotlib import pyplot as plt

if __name__ == '__main__':
    img = cv2.imread('test-bg/handc.jpeg')
    img = cv2.medianBlur(img, 5)

    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th3 = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(th3, cv2.MORPH_OPEN, kernel)

    result = 255 - opening
    print(pytesseract.image_to_string(result))
    titles = ['Original Image', 'Adaptive Gaussian Thresholding', 'Final After Morph']
    images = [img, th3, result]
    cv2.imwrite('result/threshold.png', th3)
    cv2.imwrite('result/thresholdmorph.png', result)
    xrange = range
    for i in xrange(3):
        plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.savefig("mygraph.png")
    cv2.imshow('opening', opening)
    cv2.waitKey()