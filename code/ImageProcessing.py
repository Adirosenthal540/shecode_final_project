import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys

PIXEL_REMOVE = 20
THRESHOLDTIGHT = 110
MINPIXELLETTER = 10 # MIN PIXEL NUM FOR LETTER \ LINE

def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew

class ImageProcessing():

    def __init__(self, imageArray, imagePath, isTrain = False, isHandwrite = False, label = -1):
        self.imageArray = imageArray
        self.label = label
        self.imagePath = imagePath


    def ImageWidth(self, imageArray):
        return imageArray.shape[1]

    def ImageHeight(self, imageArray):
        return imageArray.shape[0]

    def cutImage(self,imageArray, x1, y1, x2, y2):
        img_cut = imageArray[min(y1,y2):max(y1,y2), min(x1,x2):max(x1,x2)]
        return img_cut

    def ShowImage(self, imageArray, description, time = 0):
        cv.imshow(description, imageArray)
        cv.waitKey(time)

    # def CopyImageArray(self, imageArray):
    #     return imageArray.copy()

    def resizeImage(self, imageArray, width, height):
        resizeImg = cv.resize(imageArray, (width, height))
        return resizeImg

    def RotateImage(self):
        pass

    def removePixelsEdge(self, img, numPixel):
        widthImg = img.shape[1]
        heightImg = img.shape[0]
        imgRemovePixels = img[numPixel:heightImg - numPixel, numPixel:widthImg - numPixel]
        imgResize = cv.resize(imgRemovePixels, (widthImg, heightImg))
        return imgResize

    def FindLines(self, img):
        edges = cv.Canny(img, 50, 150, apertureSize=3)
        cv.imshow("edges", edges)
        cv.waitKey(0)
        lines = cv.HoughLinesP(edges,1,np.pi/180, 100, minLineLength=300, maxLineGap=20)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(img, (x1, y1), (x2, y2), (0,255, 0), 2)

        cv.imshow("image", img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def WropImage(self, img, points):
        imgContour = img.copy()
        points = reorder(points)
        width = img.shape[1]
        height = img.shape[0]
        pts1 = np.float32(points)  # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])  # PREPARE POINTS FOR WARP
        matrix = cv.getPerspectiveTransform(pts1, pts2)
        imgWarp = cv.warpPerspective(img, matrix, (width, height))
        imgWarp = self.removePixelsEdge(imgWarp, PIXEL_REMOVE)
        cv.imshow("wrop Image", imgWarp)
        cv.waitKey(5)
        return imgWarp

    def GetLineBounds(self, img):
        lineBounds = []
        minValImage = np.amin(img, axis=1)
        smallThanTHRESHOLDTIGHT = minValImage < THRESHOLDTIGHT
        row = 1
        startL = 0
        endL = 0
        imgCopy = img.copy()
        while row < self.ImageHeight(img):
            while smallThanTHRESHOLDTIGHT[row]:
                if smallThanTHRESHOLDTIGHT[row - 1] == False:
                    startL = row
                if smallThanTHRESHOLDTIGHT[row + 1] == False:
                    endL = row
                row += 1
            if (smallThanTHRESHOLDTIGHT[row - 1] == True):
                if endL - startL <= MINPIXELLETTER:
                    row += 1
                    continue
                else:
                    lineBounds.append((startL, endL))
                    cv.line(imgCopy, (0,startL), (0,endL), 0, 5)
                    cv.line(imgCopy, (0,startL), (self.ImageWidth(img),startL), 0, 5)
                    cv.line(imgCopy, (0,endL), (self.ImageWidth(img),endL), 0, 5)
            row += 1
        cv.imshow("line bounds image", imgCopy)
        cv.waitKey(0)

        return lineBounds

    def FindLetterBoundsInLine(self,img, startLine, endLine):
        letterBounds = []
        img_cut = img[startLine : endLine, 0 : img.width]
        minValImage = np.amin(img_cut, axis=0)
        smallThanTHRESHOLDTIGHT = minValImage < THRESHOLDTIGHT
        column = 1
        startLetter = 0
        endLetter = 0
        imgCopy = img.copy()
        while column < self.ImageWidth(img):
            while smallThanTHRESHOLDTIGHT[column]:
                if smallThanTHRESHOLDTIGHT[column - 1] == False:
                    startLetter = column
                if smallThanTHRESHOLDTIGHT[column + 1] == False:
                    endLetter = column
                    column += 1
            if (smallThanTHRESHOLDTIGHT[column - 1] == True):
                if endLetter - startLetter <= MINPIXELLETTER:
                    column += 1
                    continue
                else:
                    letterBounds.append([(startLetter, startLine), (endLetter,endLine)])
                    cv.line(imgCopy, (startLetter, startLine), (startLetter, endLine), 0, 5)
                    cv.line(imgCopy, (endLetter, startLine), (endLetter, endLine), 0, 5)
                    cv.line(imgCopy, (startLetter, startLine), (endLetter, startLine), 0, 5)
                    cv.line(imgCopy, (startLetter, endLine), (endLetter, endLine), 0, 5)
            column += 1
        cv.imshow("line bounds image", imgCopy)
        cv.waitKey(0)
        return letterBounds

    def GetLetterBoundsInLine(self, img):
        lineBounds = self.GetLineBounds(img)
        letterBounds = []
        for lineBound in lineBounds:
            currentLineLetterBounds = self.FindLetterBoundsInLine(img, lineBound[[0]], lineBound[1])
            letterBounds. append(currentLineLetterBounds)
        return letterBounds


