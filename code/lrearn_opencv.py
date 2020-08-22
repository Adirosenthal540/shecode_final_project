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

# # ~learn how to clean noises in image~
# img = cv.imread("test_images\smarties.png", cv.IMREAD_GRAYSCALE)
# _, mask = cv.threshold(img, 220, 225, cv.THRESH_BINARY_INV)
#
# kernal = np.ones((2,2), np.uint8)
# dilation = cv.dilate(mask, kernal , iterations=3)
# erosion = cv.erode(mask, kernal, iterations=2)
# opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernal)
# closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernal)
# mg = cv.morphologyEx(mask, cv.MORPH_GRADIENT, kernal)
# th = cv.morphologyEx(mask, cv.MORPH_TOPHAT, kernal)
#
# titles = ["image", "mask", "dilation","erosion", "opening", "closing", "mg", "th"]
# images = [img, mask, dilation, erosion,opening,closing,mg, th]
#
# for i in range(8):
#     plt.subplot(2,4,i+1), plt.imshow(images[i], 'gray')
#     plt.title(titles[i])
#     plt.xticks([]), plt.yticks([])
# plt.show()
#
#
# cv.waitKey(0)
# cv.destroyAllWindows()

# # 3:40
# # ~learn how to clean noises in image~
# img = cv.imread("test_images\\pic2.png")
# img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#
# # with this kernel we decide to bring equal wieght to each pixel
# kernal = np.ones((9,9), np.float32)/81
#
# dst = cv.filter2D(img, -1, kernal)
# blur = cv.blur(img, (9,9));
# gblue = cv.GaussianBlur(img, (9,9), 0)
# # use the next filter for salt and paper noise
# median = cv.medianBlur(img, 9)
# # use the next filter for remove noises and keep the edge sharp
# bilateralFilter = cv.bilateralFilter(img, 9, 75,75)
#
# titles = ["image", "2D Convolution", "blur", "Gaussianblue", "median", "bilateralFilter"]
# images = [img, dst, blur, gblue, median, bilateralFilter]
#
# for i in range(6):
#     plt.subplot(2,3,i+1), plt.imshow(images[i], 'gray')
#     plt.title(titles[i])
#     plt.xticks([]), plt.yticks([])
# plt.show()

# # 4:11 - image gradient
#
# # img = cv.imread("test_images\\sudoku.png", cv.IMREAD_GRAYSCALE)
# img = cv.imread("test_images\\messi5.jpg", cv.IMREAD_GRAYSCALE)
# # we cam add ksize(=3)
# lap = cv.Laplacian(img, cv.CV_64F)
# lap = np.uint8(np.absolute(lap))
# sobelX = cv.Sobel(img, cv.CV_64F, 1, 0)
# sobelY = cv.Sobel(img, cv.CV_64F, 0, 1)
# # Canny edge detector
# edges = cv.Canny(img, 100, 200)
#
# sobelX= np.uint8(np.absolute(sobelX))
# sobelY= np.uint8(np.absolute(sobelY))
#
# # combain sobelX and sobelY
# sobelCombain = cv.bitwise_or(sobelX, sobelY)
#
# titles = ["image", "Laplacian", "sobelX", "sobelY", "sobelCombain", "edges"]
# images = [img, lap, sobelX, sobelY, sobelCombain, edges]
#
# for i in range(6):
#     plt.subplot(2,3,i+1), plt.imshow(images[i], 'gray')
#     plt.title(titles[i])
#     plt.xticks([]), plt.yticks([])
# plt.show()

# # 4:32 - image pyramids
#
# img = cv.imread("test_images\\lena_learn_opencv.jpg")
# lr = cv.pyrDown(img)
# hr = cv.pyrUp(img)
# hr2 = cv.pyrUp(lr)
#
# cv.imshow("original image", img)
# cv.imshow("pytdown 1 image", lr)
# cv.imshow("pyrUp 1 image", hr)
# cv.imshow("pyrUp 1 image", hr2)
#
# cv.waitKey(0)
# cv.destroyAllWindows()

#
# # 5:15 find and drow contours
#
# img = cv.imread("test_images\\opencv-logo.png")
# imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# ret, thresh = cv.threshold(imgray, 127, 255, 0)
# contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
# print("number of contuers:"+str(len(contours)))
#
# cv.drawContours(img, contours, -1, (0,255,0), 3)
# cv.imshow("Image", img)
# cv.imshow("Image GRAY", imgray)
#
# cv.waitKey(0)
# cv.destroyAllWindows()

#
#
# # 5:24 - basic motion detection
#
# # 5:44 - shape detection
# img = cv.imread("test_images\\detect_blob.png")
# imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# _, thresh = cv.threshold(imgray, 0, 255, cv.THRESH_BINARY)
#
# contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
# print(len(contours))
# for contuor in contours:
#   # algorithem to reduce number of vertexes
#     approx = cv.approxPolyDP(contuor, 0.01*cv.arcLength(contuor, True), True)
#     cv.drawContours(img, [approx], -1, (0,0,255), 5)
#     x = approx.ravel()[0]
#     y = approx.ravel()[1]
#     if len(approx) == 4:
#         cv.putText(img, "square", (x,y-10), cv.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255,))
#
# cv.imshow("shapes", img)
# cv.waitKey(0)
#
# # 6:01 - histogram
#
# # 6:18 tamplate matchine - search for elements
#
# img = cv.imread("test_images\\messi5.jpg")
# imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# template = cv.imread("test_images\\messi_face.jpg", 0)
# w, h = template.shape[::-1]
#
# res = cv.matchTemplate(imgray, template, cv.TM_CCOEFF_NORMED)
#
# threshold = 0.95;
# loc = np.where(res >= threshold)
# print(loc)
# for pt in zip(*loc[::-1]):
#     cv.rectangle(img, pt, (pt[0]+w, pt[1] +h), (0,0,255), 2)
#
# cv.imshow("image", img)
# cv.waitKey(0)
# cv.destroyAllWindows()

# # probabilistic hough line transform
# img = cv.imread("test_images\\test_tesseract.png", 0)
# #gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow("image",img)
# cv.waitKey(0)
# edges = cv.Canny(img, 50, 150, apertureSize=3)
# #edges = cv.Canny(gray, 50, 150, apertureSize=3)
# cv.imshow("edges",edges)
# cv.waitKey(0)
# lines = cv.HoughLinesP(edges,1,np.pi/180, 100, minLineLength=300, maxLineGap=20)
#
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     cv.line(img, (x1, y1), (x2, y2), (0,255, 0), 2)
#
# cv.imshow("image", img)
# cv.waitKey(0)
# cv.destroyAllWindows()

# # probabilistic hough circle transform
# img = cv.imread("test_images\\smarties.png")
# output = img.copy()
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# gray = cv.medianBlur(gray, 5)
# circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
# print (circles)
# detected_c = np.uint16(np.around(circles))
# print (detected_c)
# for (x, y, r) in detected_c[0, :]:
#     cv.circle(output, (x,y), r, (0,255,0), 3)
#     cv.circle(output, (x,y), 2, (0,255,255), 3)
#
# cv.imshow("output", output)
# cv.waitKey(0)
# cv.destroyAllWindows()

# # 8:00 - how to detect faces
# face_cascade = cv.CascadeClassifier(r"C:\Users\Adi Rosental\Documents\she_code\opencv\opencv\data\haarcascades\haarcascade_frontalface_default.xml")
# img = cv.imread("test_images\\messi5.jpg")
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# faces = face_cascade.detectMultiScale(gray, 1.1, 4)
#
# for (x, y, w, h) in faces:
#     cv.rectangle(img, (x,y), (x+w,y+h), (255, 0, 0), 3)
# cv.imshow("image", img)
# cv.waitKey()

# # 8:30 - corner detector
#
# img = cv.imread("test_images\\chessboard.png")
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#
# gray = np.float32(gray)
# dst = cv.cornerHarris(gray, 2, 3, 0.04)
#
# dst = cv.dilate(dst, None)
# img[dst > 0.01 * dst.max()] = [0,0,255]
#
# cv.imshow("image", img)
#
# if cv.waitKey(0) & 0Xff == 27:
#     cv.destroyAllWindows()

# # 8:40 - Tomasi corner detection (with max vertexs
# img = cv.imread("test_images\\templ.png")
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#
# corners = cv.goodFeaturesToTrack(gray, 10, 0.01, 10)
# corners = np.int0(corners)
#
# for i in corners:
#     x,y = i.ravel()
#     cv.circle(img, (x,y), 3, 255, -1)
#
# cv.imshow("dst", img)
#
# if cv.waitKey(0) & 0Xff == 27:
#     cv.destroyAllWindows()

