import os
from PIL import Image
import numpy as np

GRAYSHADE =150
MINPERCENT = 25
# *** The data is combination of TIF image (tif) of one line of text and txt Image (gt.txt) which is the lable of the image
# *** The name of the tif and the matching txt file should be the same - becouse there are lot of diffrent handwrite
# *** the user will insert his own ID and the name of each image will be calculate from uniqe ID of the image (integer)
# *** and the user ID - like: 1-316550797.tif, 1-316550797.gt.txt, 2-316550797.tif, 2-316550797.gt.txt etc.
DataFolder = r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\DataBase"
infoFile = r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\DataBase\info.txt"



def Insert_to_database(images_processed):
    f = open(infoFile, "r")
    list_of_lines = f.readlines()
    numImage = list_of_lines[0].split(" ")[-1]
    numStart = int(numImage)
    list_of_lines[0] = list_of_lines[0][:-(len(numImage))]
    numImage = int(numImage)
    for imageP in images_processed:
        if Check_data(imageP):
            nameImage = imageP.writerID +"_"+ str(numImage)
            pathNewImage = os.path.join(DataFolder, nameImage+".tif")
            im = Image.fromarray(imageP.imageArray)
            im.save(pathNewImage, 'TIFF')
            f = open(os.path.join(DataFolder, nameImage+".gt.txt"), "w+", encoding="utf-8")
            f.write(imageP.Label)
            f.close()
            numImage += 1

    list_of_lines[0] = list_of_lines[0] + str(numImage)
    a_file = open(infoFile, "w", encoding="utf-8")
    a_file.writelines(list_of_lines)
    a_file.close()
    return (numStart, numImage)

def delete_from_database(lineID_start, lineID_stop = None):
    if lineID_stop == None:
        lineID_stop = lineID_start
    pass

def Check_data(imageP):
    imageArray = imageP.imageArray
    numDarkPixels = np.sum(imageArray < GRAYSHADE)
    numPixelsInImage = imageArray.size
    percent = (numDarkPixels / numPixelsInImage) * 100
    if percent > MINPERCENT:
        return False
    else:
        return True

