from PIL import Image

def convert_image_format(image_path):
    im = Image.open(image_path)
    format = im.format
    sizeFormat = len(format)
    if format!="TIFF":
        im.save(image_path[:(-1*sizeFormat)]+".tiff", 'TIFF')

