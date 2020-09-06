import numpy as np
import cv2 as cv
from Image import Image

PAGE1NUMLINE = 14
PAGE2NUMLINE = 14
PAGE3NUMLINE = 14
PAGE4NUMLINE = 8

class HandwrittenDoc():
    def __init__(self, p1, p2, p3=None, p4=None):
        self.page1 = p1
        self.page2 = p2
        self.page3 = p3
        self.page4 = p4
        self.dicPageLineLable = self.createLableForPageAndLine()

    def createLableForPageAndLine(self):
        dic = {}
        for page in range(4):
            if page == 1:
                line = 0
                while line <10:
                    dic[(page, line)] = chr(1488 + line) # א - י
                    line += 1
                dic[(page, 10)] = 1499 # כ
                dic[(page, 11)] = 1500 # ל
                dic[(page, 12)] = 1502 # מ
                dic[(page, 13)] = 1504 # נ
            elif page == 2:
                dic[(page, 0)] = 1505 # ס
                dic[(page, 1)] = 1506 # ע
                dic[(page, 2)] = 1508 # פ
                dic[(page, 3)] = 1510 # צ
                dic[(page, 4)] = 1511 # ק
                dic[(page, 5)] = 1512 # ר
                dic[(page, 6)] = 1513 # ש
                dic[(page, 7)] = 1514 # ת
                dic[(page, 8)] = 1498 # ך
                dic[(page, 9)] = 1501 # ם
                dic[(page, 10)] = 1503 # ן
                dic[(page, 11)] = 1507 # ף
                dic[(page, 12)] = 1509 # ץ
                dic[(page, 13)] = 49 # 1
            elif page == 3:
                line = 0
                for i in range(8):
                    dic[(page, line)] = chr(50 + line)  # 2-9
                    line += 1
                dic[(page, 8)] = 48  # 0
                dic[(page, 9)] = 37  # %
                dic[(page, 10)] = 64  # @
                dic[(page, 11)] = 33  # !
                dic[(page, 12)] = 93  # ]
                dic[(page, 13)] = 91  # [
            elif page == 4:
                dic[(page, 0)] = 125  # }
                dic[(page, 1)] = 123  # {
                dic[(page, 2)] = 58  # :
                dic[(page, 3)] = 63  # ?
                dic[(page, 4)] = 34  # "
                dic[(page, 5)] = 59  # ;
                dic[(page, 6)] = 92  # \
                dic[(page, 7)] = 45  # -
        return dic

    def FindLableForLine(self, page, lineNum):
        if page == 1:
            for i in range(1488, 1498):
                print(chr(i))
        elif page == 2:
            pass
        elif page == 3:
            pass
        elif page ==4:
            pass
