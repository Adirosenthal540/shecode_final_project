import cv2 as cv
import pytesseract
from matplotlib import pyplot as plt
import numpy as np

def ShowImage(image, image_title):
    cv.imshow(image_title, image)
    cv.waitKey(0)

def RotateImage():
    pass

def FindLines(img):
    edges = cv.Canny(img, 50, 150, apertureSize=3)
    #edges = cv.Canny(gray, 50, 150, apertureSize=3)
    cv.imshow("edges",edges)
    cv.waitKey(0)
    lines = cv.HoughLinesP(edges,1,np.pi/180, 100, minLineLength=300, maxLineGap=20)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(img, (x1, y1), (x2, y2), (0,255, 0), 2)

    cv.imshow("image", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

img = cv.imread(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\test_images\test_tesseract.png", 0)

cv.imshow("image",img)
cv.waitKey(0)
FindLines(img)