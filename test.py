import cv2 as cv
img = cv.imread('/Users/i326432/Desktop/Screen Shot 2020-02-08 at 12.47.04 AM.png')
cv.namedWindow('test')
cv.imshow('test', img)
cv.waitKey(0)