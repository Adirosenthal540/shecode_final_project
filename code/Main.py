from Controller import Controller
from ImageProcessing import ImageProcessing
from HandwrittenDoc import check_PDF_name
import cv2 as cv
from PIL import Image
import sys
import numpy as np
from matplotlib import pyplot as plt
import os
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError

INPUT_NUM_TRYS = 2
POPPLER_PATH = "C:\\poppler-20.09.0\\bin"


def click_event(event, x, y, flags, param):
    global points
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(imgeSelectEdge, (x, y), 3, (0, 0, 255), -1)
        points.append((x, y))
        if len(points) >= 2:
            cv.line(imgeSelectEdge, points[-1], points[-2], (255, 0, 0), 5)
        cv.imshow("Select_area_of_text-need_to_be_a_square", imgeSelectEdge)


def selectTextArea(img):
    global imgeSelectEdge, points
    imgeSelectEdge = img
    cv.imshow("Select_area_of_text-need_to_be_a_square", imgeSelectEdge)
    cv.setMouseCallback("Select_area_of_text-need_to_be_a_square", click_event)
    cv.imshow("Select_area_of_text-need_to_be_a_square", imgeSelectEdge)
    cv.waitKey()
    cv.destroyAllWindows()
    if len(points) < 4:
        print("ERROR - YOU NEED TO DROW SQUARE")
        sys.exit()
    points = np.array(points[0:4])
    return points


def setBorderOfText(image):
    global points
    points= []
    print("Select the edegs of the scanned documents (with 4 points) and close the image's frame ")
    points = selectTextArea(image.imageArray)
    image.WropImage(image.imageArray, points)

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
    valid_images = [".jpg", ".gif", ".png", "tif", "tiff"]
    ext = os.path.splitext(file)[1]
    if ext.lower() not in valid_images:
        return False
    else:
        return True

def CheckPDF(file):
    ext = os.path.splitext(file)[1]
    if ext.lower() =='pdf':
        return True
    else:
        return False

# The Image of the training will be extract to same path where it save
def ExtractImagesFromPDF(file, files):
    order = check_PDF_name(file)
    images = convert_from_path(file, fmt="jpeg", poppler_path =POPPLER_PATH)
    outputpath, namefile = os.path.split(file)
    i = 0
    for image in images:
        # image = Image.open(im)
        new_path_image = os.path.join(outputpath, namefile +"_"+ order[i] + ".tif")
        i += 1
        image.save(new_path_image, 'TIFF')
        files.append(new_path_image)
    return files

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
            if (CheckPDF(file) == True):
                files = ExtractImagesFromPDF(file, files)
        if is_txtFiles:
            nameImage = os.path.splitext(file)[0]
            if nameImage+".txt" in files :
                txtFiles.append(os.path.join(folder, nameImage+".txt"))
            elif nameImage+".gt.txt" in files:
                txtFiles.append(os.path.join(folder, nameImage + ".gt.txt"))
            else:
                print ("the image '" + file + "' has no .txt file")
                continue
        imagesInFolder.append(os.path.join(folder, file))
    if (is_txtFiles):
        return imagesInFolder, txtFiles
    return imagesInFolder


def AskScannedImages():
    global images, points
    folder = input("Enter the folder's path with all the images \ PDF : \n /"
                   "***paid attention*** \n/"
                   "Images - the image's names should be with the num of the page at the end (like: adi1.png, adi2.png...)/"
                   " PDF - should write at the end the order of the pages number after bottom line (like: adi_312.pdf, adi_1234.pdf, adi_442311.pdf \n").strip('"')
    markTextArea = get_input("Do you wont to mark the area of the text on the documents? (yes/no) ", ["yes", "no"]) == "yes"
    imagesInFolder = Extract_files_from_folder(folder)
    for imageInFolder in imagesInFolder:
        image = ImageProcessing(cv.imread(imageInFolder, 0), imagePath = imageInFolder)
        if (markTextArea):
            setBorderOfText(image)
        images.append(image)
        return folder


def AskLabeledImagesAndTextFiles():
    global images, txtFiles, points
    folder = input("Enter the folder's path with all the images "\
                   "and there labels (text files) with the same names (like: 'image1.png', 'image1.txt'): \n")
    markTextArea = get_input("Do you wont to mark the area of the text on the documents? (yes/no) ", ["yes", "no"]) == "yes"
    imagesInFolder, text_in_images = Extract_files_from_folder(folder, True)
    for i in range(len(imagesInFolder)):
        txt_file = open(text_in_images[i], "r", encoding="utf-8")
        text= txt_file.read()
        txtFiles.append(text)
        txt_file.close()
        #print(txtFiles)
        image = ImageProcessing(cv.imread(imagesInFolder[i], 0), label = txtFiles[i], imagePath = imagesInFolder[i])
        if markTextArea:
            setBorderOfText(image)
        images.append(image)
    return folder

def AskImagesAsInput_tesseract():
    global images, points
    print("Enter all the paths of the images you want to extract text from (when finish insert 'END') :\n ")
    i = 1
    pathImage = input("image " + str(i) + " :").strip('"')
    markTextArea = get_input("Do you wont to mark the area of the text on the documents? (yes/no) ", ["yes", "no"]) == "yes"
    while pathImage != 'END':
        if (CheckImage(pathImage)):
            image = ImageProcessing(cv.imread(pathImage, 0), imagePath = pathImage)
            if markTextArea:
                setBorderOfText(image)
            images.append(image)
            i += 1
        else:
            print("File: "+str(pathImage)+" is not an image file")
        pathImage = input("image " + str(i) + " :").strip('"')


def main():
    global images, txtFiles, points
    images = []
    txtFiles = []
    points = []
    isTrain = get_input("Is this a train or test? (train / test)" , ["train","test"]) == "train"
    if (isTrain):
        isScanned = get_input("Do you want to use scanned documents (with the rectangles) or you want to use prepare " \
                                     "data (images and text files)?  (scanned / prepared)",["yes", "no"]) == "yes"
        if (isScanned):
            AskScannedImages()
        else:
            AskLabeledImagesAndTextFiles()
    else:
        AskImagesAsInput_tesseract()

    controller = Controller(isTrain, images, isScanned = isScanned)
    controller.main()

if __name__ == "__main__":
    main()

