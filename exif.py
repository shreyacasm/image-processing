from PIL import Image, ExifTags


image = Image.open('result/2-rot.png')
for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation]=='Orientation':
            break
info = image._getexif()
print(info[orientation])