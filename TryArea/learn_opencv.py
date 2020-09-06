import cv2
import pytesseract
import numpy as np
# img = cv2.imread(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\test_images\Capture2.PNG")
#
# h, w, c = img.shape
# boxes = pytesseract.image_to_boxes(img, lang="heb")
# print(boxes)
# for b in boxes.splitlines():
#     b = b.split(' ')
#     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
#
# cv2.imshow('img', img)
# cv2.waitKey(0)
# #import cv2 as cv
# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
#
# # Load image as grayscale and crop ROI
# large = cv2.imread(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\test_images\Capture15.PNG")
#
#
# #large = cv2.imread('1.jpg')
# rgb = cv2.pyrDown(large)
# small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
#
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
# grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)
#
# _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# cv2.imshow('th1', bw)
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
# connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
# # using RETR_EXTERNAL instead of RETR_CCOMP
# contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# #For opencv 3+ comment the previous line and uncomment the following line
# #_, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#
# mask = np.zeros(bw.shape, dtype=np.uint8)
#
# for idx in range(len(contours)):
#     x, y, w, h = cv2.boundingRect(contours[idx])
#     mask[y:y+h, x:x+w] = 0
#     cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
#     r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)
#
#     if r > 0.45 and w > 8 and h > 8:
#         cv2.rectangle(rgb, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2)
# cv2.imshow('mask', mask)
# cv2.imshow('rects', rgb)
# cv2.waitKey()
# x, y, w, h = 364, 633, 791, 273
# ROI = image[y:y+h, x:x+w]

# Calculate mean and STD
#mean, STD  = cv.meanStdDev(image)

# Clip frame to lower and upper STD
# offset = 0.2
# clipped = np.clip(image, mean - offset*STD, mean + offset*STD).astype(np.uint8)

# Normalize to range
# result = cv.normalize(clipped, clipped, 0, 255, norm_type=cv.NORM_MINMAX)
#
# cv.imshow('image', image)
# cv.imshow('result', result)
# cv.waitKey()
# def click_event(event, x, y, flags, param):
#     if event ==cv.EVENT_LBUTTONDOWN:
#         cv.circle(img, (x,y), 3, (0,0,255), -1)
#         points.append((x,y))
#         if len(points) >= 2:
#             cv.line(img, points[-1], points[-2], (255,0,0), 5)
#         cv.imshow("Image", img)
# img = cv.imread(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\test_images\lena_learn_opencv.jpg", -1)
# #img = np.zeros((512,512,3), np.uint8)
# # print(img)
# # print(img.shape)
# # print(img.shape[0])
# cv.imshow("Image", img)
# points = []
# cv.setMouseCallback("Image", click_event)
# cv.waitKey()
# cv.destroyAllWindows()
# print(points)
#

# img = np.zeros([512, 512], np.uint8)
# font = cv.FONT_HERSHEY_SIMPLEX
# img = cv.putText(img, "opencv", (10,500), font, 4 , (255,255,255), 10, cv.LINE_AA)
# crop_img = img[400:500, 300:350]
# cv.imshow("cropped", crop_img)
# cv.waitKey(0)
# #img = cv.imread("test_images\gradient.png", 0)
# #_, th1 = cv.threshold(img, 127, 255)
# cv.imshow("image", img)
#
# cv.waitKey(0)
# cv.destroyAllWindows()

#cv2.imwrite("lena_copy.png", img)
# font = cv2.FONT_HERSHEY_SIMPLEX
# img = cv2.putText(img, "opencv", (10,500), font, 4 , (255,25,255), 10, cv2.LINE_AA)

# img = cv.imread("test_images\gradient.png", 0)
# _, th1 = cv.threshold(image, 100, 255, cv.THRESH_BINARY)
# _, th2 = cv.threshold(image, 100, 255, cv.THRESH_BINARY_INV)
# _, th3 = cv.threshold(image, 100, 255, cv.THRESH_TRUNC)
#
# cv.imshow("image", image)
# cv.imshow("th1", th1)
# cv.imshow("th2", th2)
# cv.imshow("th3", th3)
#cv.imshow("th4", th4)
# cv.waitKey()
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
# img = cv2.imread(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\test_images\Capture15.PNG")
# imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(imgray, 127, 255, 0)
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# print("number of contuers:"+str(len(contours)))
# print(contours)
# cv2.drawContours(img, contours, -1, (0,255,0), 3)
#
# cv2.imshow("Image", img)
# cv2.imshow("Image GRAY", imgray)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#
#
# # 5:24 - basic motion detection
#
# 5:44 - shape detection
def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1,2), dtype=np.int32)
    add = myPoints.sum(1)
    a = myPoints[np.argmin(add)]
    myPointsNew[0] = a
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew

img = cv2.imread(r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\test_images\Capture22.PNG")
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY)
squareBounds = []
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print(len(contours))
imgcopy = img.copy()
for contuor in contours:
  # algorithem to reduce number of vertexes
    approx = cv2.approxPolyDP(contuor, 0.01*cv2.arcLength(contuor, True), True)
  #remove duplicate and the image's frame sqare
    if len(approx) == 4:
    # if len(approx) == 4 and abs(approx[2][0][0]-approx[1][0][0])<imgray.shape[0]-10 and abs(approx[0][0][0]-approx[1][0][0])<10:
        #bound = np.array([(list(approx[0][0]), list(approx[1][0])), (list(approx[2][0]), list(approx[3][0]))])
        #
        bound =reorder(approx)
        myPoints = bound.reshape((4, 2))
        diff = myPoints[3]-myPoints[0]
        if diff [0] < imgcopy.shape[1]/2 and diff[0]>2 and diff [1] < imgcopy.shape[0]/2 and diff[1]>2:
            cv2.drawContours(imgcopy, [approx], -1, (0, 0,255), 2)
            squareBounds.append(bound)

cv2.imshow("shapes", imgcopy)
cv2.waitKey(0)
print(len(squareBounds))
print(squareBounds)
for squareBound in squareBounds:
    img_cut = imgray[min(squareBound[0][0][1], squareBound[1][0][1]):max(squareBound[2][0][1], squareBound[3][0][1]), min(squareBound[0][0][0],squareBound[2][0][0]):max(squareBound[1][0][0],squareBound[3][0][0])]
    #resizeImg = cv2.resize(img_cut, (imgray.shape[1], imgray.shape[0]))
    if pytesseract.image_to_string(img_cut, lang="heb")!="":
        cv2.imshow("shapes", img_cut)
        cv2.waitKey(0)
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

