import numpy as np
import cv2 as cv
import os
from ImageProcessing import ImageProcessing
from PIL import Image

THRESHOLDTIGHT = 110
MINPIXELLETTER = 10 # MIN PIXEL NUM FOR LETTER \ LINE
MAXNUMLINES = 9
NUMPAGES = 4

def check_PDF_name(namefile):
    order_list = []
    namefile = namefile[:-4]
    orderPages = namefile.split("_")[-1]
    for num in orderPages:
        min_page_ord = 49
        max_page_ord = min_page_ord + NUMPAGES
        if ord(num) < min_page_ord or ord(num) >= max_page_ord:
            print ("ERROR - Wrong name for the PDF")
            return -1
        else:
            order_list.append(int(num))
    print("The order of the pages in your pdf - " + os.path.basename(namefile) + " are: " +orderPages)
    return order_list

def Check_image_page(namefile):
    num_page = namefile[-5]
    min_page_ord = 49
    max_page_ord = min_page_ord + NUMPAGES
    if ord(num_page) < min_page_ord or ord(num_page) >= max_page_ord:
        print("ERROR - Wrong name for the image")
    return (int(num_page))

# def FindLabelForBound(self, yMin, yMax, bound, page):
#     image = self.pages[page]
#     heightLine = int((yMax - yMin) / MAXNUMLINES)
#     yMiddleBorder = bound[1] + bound[3] * 0.5
#     for line in range(MAXNUMLINES+1):
#         if (yMin + heightLine * line) <= yMiddleBorder and (yMin + heightLine * (line+1) > yMiddleBorder):
#             return self.FindLabelForLine(page, line)
#             #cv.line(image, (0, yMin + heightLine * i), (image.shape[1], yMin + heightLine * i), (0, 0, 255), 5)
#     return -1

def FindSquaresHandwriteDoc(image):
    thresh = cv.threshold(image, 160, 255, cv.THRESH_BINARY_INV)[1]
    #thresh = cv.threshold(gray, 255 - mean + std, 255, cv.THRESH_BINARY_INV)[1]
    cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # min and max area for square, given the fact that there are 10 square in row
    min_area = (image.shape[0] / 30) * image.shape[1] * 0.75
    max_area = (image.shape[0] / 15) * image.shape[1]

    boundries = []
    for c in cnts:
        area = cv.contourArea(c)

        if area > min_area and area < max_area:
            x, y, w, h = cv.boundingRect(c)

            fix = int(h * 0.2)
            x = x + fix
            y = y + fix
            w = w - fix*2
            h = h - fix*2
            boundries.append((x,y,w,h))
            # cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
            #cv.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
    # boundries = np.array(boundries)
    #cv.imshow("image", image)
    #cv.waitKey(0)
    if len(boundries) < MAXNUMLINES:
        print("ERROR - did'nt recognize all the sqares need to take a picture again or to wrap it")
        return -1
    elif len(boundries) > MAXNUMLINES:
        print("ERROR - there are noises, need to take a picture again or to wrap it")
        return -1
    return boundries

def reorderBoundries(boundries):
    reorderBoundries = []
    lenList = len(boundries)
    for i in range(lenList):
        reorderBoundries.append(boundries[lenList - 1 - i])
    return reorderBoundries


def ExportHandriteLinesFromScannedDoc(image, pageNum):
    handwrittenDic = HandwrittenDic()
    newImagesForTrain = []
    boundries = FindSquaresHandwriteDoc(image.imageArray) # The boundries are order from the bottom of the page up.
    boundries = reorderBoundries(boundries)

    for i in range(len(boundries)):
        x, y, w, h =  boundries[i]
        cutImage = image.cutImage(image.imageArray, x, y, x + w, y + h)
        Label = handwrittenDic.FindLabelForLine(page = pageNum, lineNum = i+1)
        newImagesForTrain.append(ImageProcessing(cutImage, imagePath = None, Label = Label, writerID = image.writerID))

    return newImagesForTrain

# def GetLineBounds(imageArray):
#     lineBounds = []
#     minValImage = np.amin(imageArray, axis=1)
#     height = imageArray.shape[0]
#     width = imageArray.shape[1]
#     smallThanTHRESHOLDTIGHT = minValImage < THRESHOLDTIGHT
#     row = 1
#     startL = 0
#     endL = 0
#     imgCopy = imageArray.copy()
#     while row < height:
#         while smallThanTHRESHOLDTIGHT[row]:
#             if smallThanTHRESHOLDTIGHT[row - 1] == False:
#                 startL = row
#             if smallThanTHRESHOLDTIGHT[row + 1] == False:
#                 endL = row
#             row += 1
#         if (smallThanTHRESHOLDTIGHT[row - 1] == True):
#             if endL - startL <= MINPIXELLETTER:
#                 row += 1
#                 continue
#             else:
#                 lineBounds.append((startL, endL))
#                 cv.line(imgCopy, (0,startL), (0,endL), 0, 5)
#                 cv.line(imgCopy, (0,startL), (width,startL), 0, 5)
#                 cv.line(imgCopy, (0,endL), (width,endL), 0, 5)
#         row += 1
#     cv.imshow("line bounds image", imgCopy)
#     cv.waitKey(0)
#
#     return lineBounds

class HandwrittenDic():
    def __init__(self):
        self.dicPageLineLabel = self.createLabelForPageAndLine()

    # The function given a line it's Label im hebrew
    def createLabelForPageAndLine(self):
        dic = {}
        for page in range(1, 5):
            if page == 1:
                dic[(page, 1)] = "בשמלה אדומה ושתי צמות,"
                dic[(page, 2)] = "ילדה קטנה, יחידה ותמה"
                dic[(page, 3)] = "עמדה ושאלה – למה?"
                dic[(page, 4)] = "וכל הרי הגעש וכל הסערות"
                dic[(page, 5)] = "עמדו מזעפם ולא מצאו תשובה."
                dic[(page, 6)] = "יונתן הקטן רץ בבוקר אל הגן"
                dic[(page, 7)] = "הוא טיפס על העץ אפרוחים חיפש"
                dic[(page, 8)] = "אוי ואבוי לו לשובב, חור גדול במכנסיו"
                dic[(page, 9)] = "מן העץ התגלגל ועונשו קיבל"
            elif page == 2:
                dic[(page, 1)] = "אני אוהב שוקולד ועוגות גבינה"
                dic[(page, 2)] = "וארטיק וסוכריות ותות גינה"
                dic[(page, 3)] = "אני אוהב ימי הולדת ושקיות עם דברים טובים"
                dic[(page, 4)] = "ואת השמש ואת הירח וגם כמה כוכבים."
                dic[(page, 5)] = "אפונה וגזר ישבו במקרר "
                dic[(page, 6)] = "ויחד עם בטטה התחילו לקטר:"
                dic[(page, 7)] = "\"קר לי ברגליים, תדליק ת'מנורה בקיר,"
                dic[(page, 8)] = "כי חושך מצרים, אז בואו נשיר\"."
                dic[(page, 9)] = "תנו לגדול בשקט בערוגה בכפר."
            elif page == 3:
                dic[(page, 1)] = "שם תזרח השמש גם מחר"
                dic[(page, 2)] = "תנו לגדול בשקט בלי לקפוא מקור"
                dic[(page, 3)] = "רק קצת זבל, מים וגם אור."
                dic[(page, 4)] = "אפונה וגזר, ישבו בתוך מחבט."
                dic[(page, 5)] = "ויחד עם בטטה רצו להיות לבד"
                dic[(page, 6)] = "אך שוד ושבר, מישהו גפרור מדליק"
                dic[(page, 7)] = "ושמן מכל עבר, זה לא מצחיק!"
                dic[(page, 8)] = "כי חושך מצרים, אז בואו נשיר\"."
                dic[(page, 9)] = "רוץ בן סוסי, רוץ ודהר! רוץ בביקעה, טוס בהר!"
            elif page == 4:
                dic[(page, 1)] = "רוצה, טוסה, יום וליל – פרש אני ובן חיל!"
                dic[(page, 2)] = "אני רץ. אני חייב להספיק כל מה שהעולם מציע"
                dic[(page, 3)] = "כל זמן שהאוויר מגיע וזה לא מפריע ומלטף אותי."
                dic[(page, 4)] = "ויש אצלך אור, למה לי לעצור."
                dic[(page, 5)] = "אני יודע אני זז וזה פוגע, בלב שלי יש חור"
                dic[(page, 6)] = "שאי אפשר לסגור ואני רץ..."
                dic[(page, 7)] = "בים הרוגע השמש שוקע למי מתגעגע"
                dic[(page, 8)] = "לי ולך, לי ולך, לי ולך."
                dic[(page, 9)] = "בהצלחה באימון!"
        return dic

    def FindLabelForLine(self, page, lineNum):
        Label = self.dicPageLineLabel[(page, lineNum)]
        return Label


    # def createLabelForPageAndLine_not_used(self):
    #     dic = {}
    #     for page in range(1, NUMPAGES):
    #         if page == 1:
    #             line = 0
    #             while line < 10:
    #                 dic[(page, line)] = chr(1488 + line)  # א - י
    #                 line += 1
    #             dic[(page, 10)] = chr(1499)  # כ
    #             dic[(page, 11)] = chr(1500)  # ל
    #             dic[(page, 12)] = chr(1502)  # מ
    #             dic[(page, 13)] = chr(1504)  # נ
    #         elif page == 2:
    #             dic[(page, 0)] = chr(1505)  # ס
    #             dic[(page, 1)] = chr(1506)  # ע
    #             dic[(page, 2)] = chr(1508)  # פ
    #             dic[(page, 3)] = chr(1510)  # צ
    #             dic[(page, 4)] = chr(1511)  # ק
    #             dic[(page, 5)] = chr(1512)  # ר
    #             dic[(page, 6)] = chr(1513)  # ש
    #             dic[(page, 7)] = chr(1514)  # ת
    #             dic[(page, 8)] = chr(1498)  # ך
    #             dic[(page, 9)] = chr(1501)  # ם
    #             dic[(page, 10)] = chr(1503)  # ן
    #             dic[(page, 11)] = chr(1507)  # ף
    #             dic[(page, 12)] = chr(1509)  # ץ
    #             dic[(page, 13)] = chr(49)  # 1
    #         elif page == 3:
    #             line = 0
    #             for i in range(8):
    #                 dic[(page, line)] = chr(50 + line)  # 2-9
    #                 line += 1
    #             dic[(page, 8)] = chr(48)  # 0
    #             dic[(page, 9)] = chr(37)  # %
    #             dic[(page, 10)] = chr(64)  # @
    #             dic[(page, 11)] = chr(33)  # !
    #             dic[(page, 12)] = chr(93)  # ]
    #             dic[(page, 13)] = chr(91)  # [
    #         elif page == 4:
    #             dic[(page, 0)] = chr(125)  # }
    #             dic[(page, 1)] = chr(123)  # {
    #             dic[(page, 2)] = chr(58)  # :
    #             dic[(page, 3)] = chr(63)  # ?
    #             dic[(page, 4)] = chr(34)  # "
    #             dic[(page, 5)] = chr(59)  # ;
    #             dic[(page, 6)] = chr(92)  # \
    #             dic[(page, 7)] = chr(45)  # -
    #     return dic







