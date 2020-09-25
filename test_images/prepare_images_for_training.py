from PIL import Image
import os
def convert_image_format(image_path):
    im = Image.open(image_path)
    format = im.format
    sizeFormat = len(format)
    if format!="TIF":
        im.save(image_path[:(-1*sizeFormat)]+".tif", 'TIF')
    os.remove(image_path)

for i in range(1, 12):
    path = "C:\\Users\\Adi Rosental\\Documents\\she_code\\shecode_final_project\\handwriteDoc\\test_train_hebrew\\rows\\" + str(i)+".tiff"
    path2 = "C:\\Users\\Adi Rosental\\Documents\\she_code\\shecode_final_project\\handwriteDoc\\test_train_hebrew\\rows\\" + str(i)+".tif"
    os.rename(path, path2)