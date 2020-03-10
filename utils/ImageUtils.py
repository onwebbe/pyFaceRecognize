import numpy as np
import cv2
import db.FaceData as FaceData

def createImageFromPath(imagePath):
  return cv2.imread(imagePath)

def getImageSize(inputImage):
  image_shapre = inputImage.shape
  h, w, c = image_shapre
  image_size = {}
  image_size['width'] = w
  image_size['height'] = h
  image_size['channel'] = c
  return image_size

def cloneImage(inputImage):
  clone_img = inputImage.copy()
  return clone_img

def displayImage(image):
  cv2.namedWindow('display_image')
  cv2.imshow('display_image', image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def displayImages(imageList):
  i = 0
  for image in imageList:
    windowName = 'display_image' + str(i)
    cv2.namedWindow(windowName)
    cv2.moveWindow(windowName, 200 + 40 * i, 200 + 30 * i)
    cv2.imshow(windowName, image)
    i = i + 1
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def getFaceInDBByRawImage(rawImageName):
  faceDB = FaceData.getFaceData()
  return faceDB.searchFaceByRawImageFileName(rawImageName)