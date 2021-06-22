import cv2
import pytesseract
import pkg_resources


if __name__ == '__main__':
    image = cv2.imread('invoice/test5.jpg')
    result = image.copy()
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    print("tesseract version :", pytesseract.get_tesseract_version())
    print("pytesseract version :",pkg_resources.working_set.by_key['pytesseract'].version)

    data = pytesseract.image_to_string(image)
    print("original :\n", data)

    # Remove horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
    remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(result, [c], -1, (255,255,255), 5)

    # Remove vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
    remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(result, [c], -1, (255,255,255), 5)

    cv2.imshow('thresh', thresh)
    cv2.imshow('result', result)
    cv2.imwrite('result/invoice/thresh.png', thresh)
    cv2.imwrite('result/invoice/result.png', result)
    # value = [0, 0, 0]
    # result = cv2.copyMakeBorder(result, 100, 100, 100, 100, cv2.BORDER_CONSTANT, None, value)
    # cv2.imshow('final-result', result)
    # cv2.imwrite('result/invoice/result-fin.png', result)
    data = pytesseract.image_to_string(result, lang='eng', config='--psm 6')
    print("*"*100)
    print("After:\n", data)
    cv2.waitKey()