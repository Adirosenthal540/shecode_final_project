from Controller import Controller
from Image import Image
import cv2 as cv
import sys
import numpy as np
from matplotlib import pyplot as plt
import os
#!/usr/bin/env python
# -*- coding: utf-8 -*-
INPUT_NUM_TRYS = 2

# the func get the "text" request for an input and the possibles values. It ask from the user an input and check if it is right.
def get_input(text, posible_values):
    input1 = input(str(text)+"\n")
    input1 = input1.lower()
    if (not input1 in posible_values):
        i = 1
        print("wrong input. try again..")
        new_input = input(str(text)+"\n")
        while (not new_input in posible_values):
            print("wrong input. try again..")
            if i >= INPUT_NUM_TRYS:
                sys.exit()
            new_input = input(str(text)+"\n")
            i += 1
        return new_input
    else:
        return input1

# func check if the file is an image file:
def CheckImage(file):
    valid_images = [".jpg", ".gif", ".png"]
    ext = os.path.splitext(file)[1]
    if ext.lower() not in valid_images:
        print("That is not an image file")
        return False
    else:
        return True


# the func save all the paths of the images and text files(optional)
# input: path of a folder,  is_txtFiles = true if want to find also text files
# output: list of all the images ans text files (if is_txtFiles is true)
def Extract_files_from_folder(folder,  is_txtFiles=0):
    imagesInFolder = []
    txtFiles = []
    files = os.listdir(folder)
    flag = 0
    for file in files:
        if (CheckImage(file) == False):
            continue
        if is_txtFiles:
            nameImage = os.path.splitext(file)[0]
            if nameImage+".txt" in files:
                txtFiles.append(os.path.join(folder, nameImage+".txt"))
            else:
                print ("the image '" + file + "' has no .txt file")
                continue
        imagesInFolder.append(os.path.join(folder, file))

    if (is_txtFiles):
        return imagesInFolder, txtFiles
    return imagesInFolder

def AskImagesOfHandwriteTrain():
    global images
    folder = input("Enter the folder's path with all the images : \n").strip('"')
    imagesInFolder = Extract_files_from_folder(folder)
    for image in imagesInFolder:
        images.append(Image(cv.imread(image, 1), isTrain = True, isHandwrite = True))

def AskLabeledImagesAndTextFiles():
    global images, txtFiles
    folder = input("Enter the folder's path with all the images "\
                   "and there labels (text files) with the same names (like: 'image1.png', 'image1.txt'): \n")
    imagesInFolder, text_in_images = Extract_files_from_folder(folder, True)
    for i in range(len(imagesInFolder)):
        print(text_in_images[i])
        txt_file = open(text_in_images[i], "r", encoding="utf-8")
        text= txt_file.read()
        txtFiles.append(text)
        txt_file.close()
        images.append(Image(cv.imread(imagesInFolder[i], 1), isTrain = True, label = txtFiles[i]))
    return folder

def AskImagesAsInput_tesseract():
    global images
    print("Enter all the paths of the images you want to extract text from (when finish insert 'END') :\n ")
    i = 1
    pathImage = input("image " + str(i) + " :").strip('"')
    while pathImage != 'END':
        if (CheckImage(pathImage)):
            images.append(Image(cv.imread(pathImage, 1), isTrain = False))
            i += 1
        pathImage = input("image " + str(i) + " :").strip('"')


def main():
    global images, txtFiles
    images = []
    txtFiles=[]
    isTrain = get_input("Is this a train or test? (train / test)" , ["train","test"]) == "train"
    if (isTrain):
        is_handwritePage = get_input("Do you want to train the network with your handwrite by using the sccaned pages? (yes/no)",\
            ["yes", "no"]) == "yes"
        if (is_handwritePage):
            AskImagesOfHandwriteTrain()
        else:
            AskLabeledImagesAndTextFiles()
    else:
        AskImagesAsInput_tesseract()
    #img = r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\test_images\unnamed1.jpg"
    for image in images:

    controller = Controller(isTrain, images)

if __name__ == "__main__":
    main()

