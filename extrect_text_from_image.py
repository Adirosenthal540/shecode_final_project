import cv2
import pytesseract
import matplotlib.pyplot as plt
import numpy as np
pytesseract.pytesseract.tesseract_cmd =  r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = cv2.imread(r"C:\Users\Adi Rosental\Desktop\Capture3.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#print(pytesseract.image_to_string(img))
_, binary_thresh = cv2.threshold(img, 125,255, cv2.THRESH_BINARY_INV)
fig = plt.figure(figsize = (12,12))
fig.add_subplot(1,2,1)
plt.imshow(img)
fig.add_subplot(1,2,2)
plt.imshow(binary_thresh)
plt.show()
# lines = cv2.HoughLinesP(binary_thresh,1,np.pi/180, 100, minLineLength=300, maxLineGap=20)
# print(lines)
# angle = 0
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     r = np.arctan2(y1-y2, x2-x1)
#     angle += np.arctan2(y2-y1,x2-x1)
# avg_radian = angle / len(lines)
# avg_angle = avg_radian * 180 / np.pi
# hImg, wImg,_= img.shape
# boxes = pytesseract.image_to_data((img))
# print (boxes)
# str= pytesseract.image_to_string(binary_thresh)
# print (str)
# boxes= pytesseract.image_to_boxes(img)
# for b in boxes.splitlines():
#     print(b)
#     b=b.split(" ")
#     x,y,w,h = int(b[1]),int(b[2]), int(b[3]),int(b[4])
#     cv2.rectangle(img, (x,hImg-y), (w,hImg -h), (0,0,255), 1)
# cv2.imshow('Result', img)
# cv2.waitKey(0)
