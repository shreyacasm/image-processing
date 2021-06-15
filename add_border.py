from PIL import Image, ImageOps
import cv2

def add_border(input_image, output_image, border, color):
    img = Image.open(input_image)

    if isinstance(border, int) or isinstance(border, tuple):
        bimg = ImageOps.expand(img, border=100, fill='red')
    else:
        raise runtimeerror('border is not an integer or tuple!')

    bimg.save(output_image)


if __name__ == '__main__':

    in_img = 'test/real_case.jpeg'
    add_border(in_img, output_image='test/real_caseborder.jpeg', border=100, color='white')