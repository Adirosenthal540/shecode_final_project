import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
# img = cv2.imread(r"test_images\lena_learn_opencv.jpg", -1)

# img = np.zeros([512, 512], np.uint8)
# font = cv2.FONT_HERSHEY_SIMPLEX
# img = cv2.putText(img, "opencv", (10,500), font, 4 , (255,255,255), 10, cv2.LINE_AA)
#
# img = cv.imread("test_images\gradient.png", 0)
# _, th1 = cv.threshold(img, 127, 255)
# cv.imshow("image", img)
#
# cv.waitKey(0)
# cv.destroyAllWindows()

#cv2.imwrite("lena_copy.png", img)
# font = cv2.FONT_HERSHEY_SIMPLEX
# img = cv2.putText(img, "opencv", (10,500), font, 4 , (255,25,255), 10, cv2.LINE_AA)

# img = cv.imread("test_images\gradient.png", 0)
# _, th1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
# # _, th2 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
# # _, th3 = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)
#
# cv.imshow("image", img)
# cv.imshow("th1", th1)
# cv.imshow("th2", th2)
# cv.imshow("th3", th3)
# cv.imshow("th4", th4)
#
# img = cv.imread("test_images\sudoku.png", 0)
# th2 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2 )
# th3 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2 )
#
# cv.imshow("image", img)
# cv.imshow("th2", th2)
# cv.imshow("th3", th3)

img = cv.imread("test_images\smarties.png", cv.IMREAD_GRAYSCALE)
_, mask = cv.threshold(img, 220, 225, cv.THRESH_BINARY_INV)

kernal = np.ones((2,2), np.uint8)
dilation = cv.dilate(mask, kernal , iterations=3)
erosion = cv.erode(mask, kernal, iterations=2)
opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernal)
closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernal)
mg = cv.morphologyEx(mask, cv.MORPH_GRADIENT, kernal)
th = cv.morphologyEx(mask, cv.MORPH_TOPHAT, kernal)

titles = ["image", "mask", "dilation","erosion", "opening", "closing", "mg", "th"]
images = [img, mask, dilation, erosion,opening,closing,mg, th]

for i in range(8):
    plt.subplot(2,4,i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()


cv.waitKey(0)
cv.destroyAllWindows()