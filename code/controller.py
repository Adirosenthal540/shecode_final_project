import cv2 as cv
import sys
import numpy as np
from matplotlib import pyplot as plt
import os

INPUT_NUM_TRYS = 2

# the func get the "text" request for an input and the possibles values. It ask from the user an input and check if it is right.
def get_input(text, posible_values):
    input = input(text).lower()
    if (not input in posible_values):
        i = 1
        print("wrong input. try again..")
        new_input = input(text)
        while (not input in posible_values):
            if i >= INPUT_NUM_TRYS:
                sys.exit()
            new_input = input(text)
            i += 1
        return new_input
    else:
        return input

# func check if the file is an image file:
def CheckImage(file):
    valid_images = [".jpg", ".gif", ".png"]
    ext = os.path.splitext(file)[1]
    if ext.lower() not in valid_images:
        return False
    else:
        return True


# the func save all the paths of the images and text files(optional)
# input: path of a folder,  is_txtFiles = true if want to find also text files
# output: list of all the images ans text files (if is_txtFiles is true)
def Extract_files_from_folder(folder,  is_txtFiles=0):
    images = []
    txtFiles=[]
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
        images.append(os.path.join(folder, file))

    if (is_txtFiles):
        return images, txtFiles
    return images

class Controller():

    def __init__(self):
        self.isTrain = get_input("Is this a train or test? (train / test)" , ["train","test"]) == "train"
        self.images = []
        self.text_in_images = []
        self.processedImage = None
        if (self.isTrain):
            self.is_handwritePage = get_input("Do you want to train the network with your handwrite by using the sccaned pages? (yes/no)", ["yes", "no"]) == "yes"
            if (self.is_handwritePage):
                self.AskImagesOfHandwriteTrain()
            else:
                self.AskLabeledImagesAndTextFiles()
        else:
            self.AskImagesForTest()

    def AskImagesOfHandwriteTrain(self):
        folder = input("Enter the folder's path with all the images : ")
        images = Extract_files_from_folder(folder)
        for image in images:
            self.images.append(cv.imread(image, 1))

    def AskLabeledImagesAndTextFiles(self):
        folder = input("Enter the folder's path with all the images \
              and there labels (text files) with the same names (like: 'image1.png', 'image1.txt'): ")
        images, text_files = Extract_files_from_folder(folder, True)
        for i in range(len(images)):
            self.images.append(cv.imread(images[i], 1))
            txt_file = open(text_files[i], "r")
            self.text_in_images.append(txt_file.read())
            txt_file.close()

    def AskImagesForTest(self):
        print("Enter all the paths of the images you want to extract text from (when finish insert 'END') : ")
        i = 1
        pathImage = input("image " + str(i) + " :")
        while pathImage != 'END':
            if (CheckImage(pathImage)):
                self.images.append(cv.imread(pathImage, 1))
                i += 1
            pathImage = input("image " + str(i) + " :")

    def ImageProcessingBeforeTesseract(self):
        for image in self.images:
            pass #call processing funcs from "image processing"
            # save in

    def ExtractTextFromImage(self):
        for image in self.images:
            pass #call testing funcs from "modelTesseract"

    def PrintExtractText(self):
        for text in self.text_in_images:
            print (text)