import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys

PIXEL_REMOVE = 20
THRESHOLDTIGHT = 0.75
MINHIGHTLETTER = 20 # MIN PIXEL NUM FOR LETTER \ LINE

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

class Image():

    def __init__(self, imageArray, isTrain = False, isHandwrite = False, label = -1):
        self.imageArrays = {"original":imageArray}
        self.processes = ["original"] # List with the names of all the actions that made on the image
        self.isTrain = isTrain
        self.isHandwrite = isHandwrite
        self.label = label


    def ImageWidth(self, imageArray):
        return imageArray.shape[1]

    def ImageHeight(self, imageArray):
        return imageArray.shape[0]

    def cutImage(self,imageArray, x1, y1, x2, y2):
        img_cut = imageArray[min(y1,y2):max(y1,y2), min(x1,x2):max(x1,x2)]
        self.imageArrays["cutImage"] = img_cut
        self.processes.append("cutImage")
        return img_cut

    def ShowImage(self, imageArray, description, time = 0):
        cv.imshow(description, imageArray)
        cv.waitKey(time)

    # def CopyImageArray(self, imageArray):
    #     return imageArray.copy()

    def resizeImage(self, imageArray, width, height):
        resizeImg = cv.resize(imageArray, (width, height))
        self.imageArrays["resizeImage"] = resizeImg
        self.processes.append("resizeImage")
        return resizeImg

    def RotateImage(self):
        pass

    def removePixelsEdge(self, img, numPixel):
        widthImg = img.shape[1]
        heightImg = img.shape[0]
        imgRemovePixels = img[numPixel:heightImg - numPixel, numPixel:widthImg - numPixel]
        imgResize = cv.resize(imgRemovePixels, (widthImg, heightImg))
        self.imageArrays["removePixelsEdge"] = imgResize
        self.processes.append("removePixelsEdge")
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
        self.imageArrays["wropImage"] = imgWarp
        self.processes.append("wropImage")
        return imgWarp

    def GetLineBounds(self, img):
        lineBounds = []
        maxValImage = np.amax(img, axis=1)
        smallThanTHRESHOLDTIGHT = maxValImage < THRESHOLDTIGHT
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

            if endL - startL <= MINHIGHTLETTER:
                row += 1
                continue
            else:
                lineBounds.append((startL, endL))
            row += 1
        cv.line(imgeSelectEdge, points[-1], points[-2], (255, 0, 0), 5)
        return lineBounds



"""
        def LetterNumbers(pagenumber = 0):
            letter = []
            if pagenumber == 0:
                j = 0;
                for i in range(52, 68):
                    letter[j] = i
                    j++
            elif pagenumber == 1:
                j = 0;
                for (int i = 68; i <= 78; i++)
                {
                    letter[j] = i;
                j + +;

                }
                for (int i = 25; i >= 21; i--)
                    {

                        letter[j] = i;
                    j + +;
                    }
                    break;
                }
                case
                2:
                {
                int
                j = 0;
                for (int i = 20; i >= 5; i--)
                    {
                        letter[j] = i;
                    j + +;

                    }
                    break;
                }
                case
                3:
                {
                int
                j = 0;
                for (int i = 4; i >= 0; i--)
                    {

                        letter[j] = i;
                    j + +;
                    }
                    for (int i = 51; i >= 41; i--)
                        {

                            letter[j] = i;
                        j + +;
                        }
                        break;
                        }
                        case
                        4:
                        {
                        int
                        j = 0;
                        for (int i = 40; i >= 26; i--)
                            {

                                letter[j] = i;
                            j + +;
                            }
                            for (int i = 79; i <= 79; i++)
                                {

                                    letter[j] = i;
                                j + +;
                                }
                                break;
                                }
                                case
                                5:
                                {
                                int
                                j = 0;
                                for (int i = 80; i <= 95; i++)
                                    {

                                        letter[j] = i;
                                    j + +;
                                    }
                                    break;
                                    }

                                    }
                                    ret

"""


