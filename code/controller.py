import cv2 as cv
import sys
import numpy as np
from matplotlib import pyplot as plt
import os

class Controller():

    def __init__(self, isTrain, images):
        self.isTrain = isTrain
        self.images = images
        self.text_in_images = []
        self.processedImage = []


    def ImageProcessingBeforeTesseract(self):
        for image in self.images:
            pass


    def ExtractTextFromImage(self):
        for image in self.images:
            pass #call testing funcs from "modelTesseract"


    def processScannedImages(self):
        for image in self.images:
            if image.isHandwrite:
                pass


    def PrintExtractText(self):
        for text in self.text_in_images:
            print (text)


    def main(self):
        for image in self.images:
            image.GetLineBounds(image.imageArrays["original"])