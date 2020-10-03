from ImageProcessing import ImageProcessing
from HandwrittenDoc import Check_image_page, ExportHandriteLinesFromScannedDoc
import DataManager
import ModelTesseract
import cv2 as cv
import sys
import numpy as np
from matplotlib import pyplot as plt
import os

class Controller():

    def __init__(self, isTrain, images, root, isScanned = False):
        self.isTrain = isTrain
        self.isScanned = isScanned
        self.image_processing_list = images
        self.root = root


    def ImageProcessingBeforeTesseract(self):
        for image in self.images:
            pass


    def ExtractTextFromImage(self):
        for image in self.images:
            pass #call testing funcs from "modelTesseract"


    def processScannedImages(self):
        newImagesForTrain =[]
        for image in self.image_processing_list:
            pageNum = Check_image_page(image.imagePath)
            newImagesForTrain= newImagesForTrain + ExportHandriteLinesFromScannedDoc(image, pageNum)
        numS, numE = DataManager.Insert_to_database(newImagesForTrain, self.root)
        return (numS, numE)

    def processLabeledImages(self):
        pass

    def processExportFromImage(self):
        tesseract = ModelTesseract.ModelTesseract()
        text = tesseract.ExportTextTesseract(self.image_processing_list[0].imageArray)
        return text

    def main(self):
        for image in self.image_processing_list:
            print(image.imagePath)
            cv.imshow("image", image.imageArray)
            cv.waitKey(0)
            print(image.Label)
            print(image.handwrite_ID)

        if self.isTrain:
            if self.isScanned:
                numS, numE = self.processScannedImages()
                return ("Sucsses - insert " +str(numE - numS)+ " lines for training, images - " + str(numS) + " to "+str(numE))
            else:
                numS, numE = self.processLabeledImages()
        else:
            text = self.processExportFromImage()
            return text
        # for image in self.images:
        #     letterBounds = image.GetLetterBoundsInLine(image.imageArrays["original"])
