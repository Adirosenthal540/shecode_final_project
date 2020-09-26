from ImageProcessing import ImageProcessing
from handwriteDoc import Check_image_page
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
            if image.isHandwrite:
                imageNumPage = Check_image_page(image.imagePath)
        return newImagesForTrain


    def PrintExtractText(self):
        for text in self.text_in_images:
            print (text)


    def main(self):
        if self.isTrain:
            if self.isScanned:
                self.processScannedImages()
        for image in self.images:
            #letterBounds = image.GetLetterBoundsInLine(image.imageArrays["original"])
