import numpy as np
import cv2 as cv
from PIL import Image

THRESHOLDTIGHT = 110
MINPIXELLETTER = 10 # MIN PIXEL NUM FOR LETTER \ LINE
MAXNUMLINES = 14

class HandwrittenDoc():
    def __init__(self, p1, p2, p3=None, p4=None):
        self.pages = {1:p1, 2:p2, 3:p3, 4:p4}
        self.dicPageLineLable = self.createLableForPageAndLine()

    # The function given a line it's label bt the character ASCII value
    def createLableForPageAndLine(self):
        dic = {}
        for page in range(1, 5):
            if page == 1:
                line = 0
                while line < 10:
                    dic[(page, line)] = chr(1488 + line)  # א - י
                    line += 1
                dic[(page, 10)] = chr(1499)  # כ
                dic[(page, 11)] = chr(1500)  # ל
                dic[(page, 12)] = chr(1502)  # מ
                dic[(page, 13)] = chr(1504)  # נ
            elif page == 2:
                dic[(page, 0)] = chr(1505)  # ס
                dic[(page, 1)] = chr(1506)  # ע
                dic[(page, 2)] = chr(1508)  # פ
                dic[(page, 3)] = chr(1510)  # צ
                dic[(page, 4)] = chr(1511)  # ק
                dic[(page, 5)] = chr(1512)  # ר
                dic[(page, 6)] = chr(1513)  # ש
                dic[(page, 7)] = chr(1514)  # ת
                dic[(page, 8)] = chr(1498)  # ך
                dic[(page, 9)] = chr(1501)  # ם
                dic[(page, 10)] = chr(1503)  # ן
                dic[(page, 11)] = chr(1507)  # ף
                dic[(page, 12)] = chr(1509)  # ץ
                dic[(page, 13)] = chr(49)  # 1
            elif page == 3:
                line = 0
                for i in range(8):
                    dic[(page, line)] = chr(50 + line)  # 2-9
                    line += 1
                dic[(page, 8)] = chr(48)  # 0
                dic[(page, 9)] = chr(37)  # %
                dic[(page, 10)] = chr(64)  # @
                dic[(page, 11)] = chr(33)  # !
                dic[(page, 12)] = chr(93)  # ]
                dic[(page, 13)] = chr(91)  # [
            elif page == 4:
                dic[(page, 0)] = chr(125)  # }
                dic[(page, 1)] = chr(123)  # {
                dic[(page, 2)] = chr(58)  # :
                dic[(page, 3)] = chr(63)  # ?
                dic[(page, 4)] = chr(34)  # "
                dic[(page, 5)] = chr(59)  # ;
                dic[(page, 6)] = chr(92)  # \
                dic[(page, 7)] = chr(45)  # -
        return dic

    def FindLableForLine(self, page, lineNum):
        label = self.dicPageLineLable[(page, lineNum)]
        return label

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

    def FindLabelForBound(self, yMin, yMax, bound, page):
        image = self.pages[page]
        heightLine = int((yMax - yMin) / MAXNUMLINES)
        yMiddleBorder = bound[1] + bound[3] * 0.5
        for line in range(MAXNUMLINES+1):
            if (yMin + heightLine * line) <= yMiddleBorder and (yMin + heightLine * (line+1) > yMiddleBorder):
                return self.FindLableForLine(page, line)
                #cv.line(image, (0, yMin + heightLine * i), (image.shape[1], yMin + heightLine * i), (0, 0, 255), 5)
        return -1

    def FindSquaresHandwriteDoc(self, image):

        image = cv.resize(image, (600, 800))
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        mean = gray.mean()
        std = gray.std()
        #thresh = cv.threshold(gray, 160, 255, cv.THRESH_BINARY_INV)[1]
        thresh = cv.threshold(gray, 255 - mean + std, 255, cv.THRESH_BINARY_INV)[1]
        cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        # min and max area for square, given the fact that there are 10 square in row
        min_area = (image.shape[1] / 18) * image.shape[1] / 18
        max_area = (image.shape[1] / 9) * image.shape[1] / 9

        boundries = []
        for c in cnts:
            area = cv.contourArea(c)

            if area > min_area and area < max_area:
                x, y, w, h = cv.boundingRect(c)

                fixW = int(w * 0.15)
                fixh = int(h * 0.15)
                x = x + fixW
                y = y + fixh
                w = w - fixW*2
                h = h - fixh*2
                boundries.append((x,y,w,h))
                # cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
                cv.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
        boundries = np.array(boundries)

        if len(boundries) < 80:
            print("ERROR - did'nt recognize all the sqares need to take a picture again or to wrap it")
        elif len(boundries) > 80:
            print("ERROR - there are noises, need to take a picture again or to wrap it")
        return boundries

    def ExportHandriteImageFromDoc(self, page):
        image = self.pages[page]
        boundries = self.FindSquaresHandwriteDoc(image)
        dicLetters = {}

        yMin = min(boundries[:, 1])
        yMax = max(boundries[:, 1] + boundries[:, 3])

        for bound in boundries:
            label = self.FindLineOfPoint(yMin, yMax, bound, page)

