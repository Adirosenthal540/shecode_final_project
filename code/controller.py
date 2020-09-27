from ImageProcessing import ImageProcessing
from HandwrittenDoc import Check_image_page, ExportHandriteLinesFromScannedDoc
from DataManager import Insert_to_database
import cv2 as cv
import sys
import numpy as np
from matplotlib import pyplot as plt
import os

class Controller():

    def __init__(self, isTrain, images, isScanned = False):
        self.isTrain = isTrain
        self.isScanned = isScanned
        self.image_processing_list = images
        self.text_in_images = []
        self.processedImage = []


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
            newImagesForTrain= newImagesForTrain +ExportHandriteLinesFromScannedDoc(image, pageNum)
        numS, numE = Insert_to_database(newImagesForTrain)
        return (numS, numE)


    def main(self):
        if self.isTrain:
            if self.isScanned:
                numS, numE = self.processScannedImages()
                return ("Sucsses - insert " +str(numE - numS)+ " lines for training, images - " + str(numS) + " to "+str(numE))
        # for image in self.images:
        #     letterBounds = image.GetLetterBoundsInLine(image.imageArrays["original"])
