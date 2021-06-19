from PIL import Image, ImageOps
import pytesseract

def add_border(input_image, output_image, border, color):
    img = Image.open(input_image)

    if isinstance(border, int) or isinstance(border, tuple):
        bimg = ImageOps.expand(img, border=100, fill='white')
    else:
        raise runtimeerror('border is not an integer or tuple!')

    bimg.save(output_image)


if __name__ == '__main__':

    in_img = 'invoice/cmpname.png'
    add_border(in_img, output_image='test/cmp2.png', border=100, color='white')
    img = 'test/cmp2.png'
    data = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
    print(data)