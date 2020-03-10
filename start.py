import faceRecorgnize.cropFaces as cropFaces
import faceRecorgnize.faceRecorgnize as faceRecorgnize
import utils.ImageUtils as ImageUtils
import utils.Constants as Constants
import utils.FaceUtils as FaceUtils
import cv2 as cv
import os
import numpy as np
import db.FaceData as FaceData

rawImageRootPath = "/Users/i326432/Documents/kimiface/"

for filename in os.listdir(rawImageRootPath):
  rawFilePath = os.path.join(rawImageRootPath, filename)
  print("---------开始处理: " + rawFilePath + " ---------")
  existingRawFileInDB = ImageUtils.getFaceInDBByRawImage(rawFilePath)
  if (len(existingRawFileInDB) == 0):
    resultData = cropFaces.cropFaces2(rawFilePath)
    if (resultData is not None):
      faceList = resultData['croppedImageList']
      featureList = resultData['croppedFeatureList']
      faceIndex = 0
      if (len(faceList) == 0):
        faceId = FaceUtils.createNewPersonFace('', rawFilePath)
        FaceUtils.updateFaceFeatureFile(faceId, '')
      else:
        for index in range(0, len(faceList)):
          faceImage = faceList[index]
          featureData = featureList[index]

          faceFileName = os.path.join(Constants.DATA_ROOT_PATH, Constants.FACE_IMG_FILE_PATH, "face_" + filename + "_" + str(faceIndex) + ".bmp")
          cv.imwrite(faceFileName, faceImage)
          
          faceIndex = faceIndex + 1

          faceId = FaceUtils.createNewPersonFace(faceFileName, rawFilePath)
          faceFeaturePath = os.path.join(Constants.DATA_ROOT_PATH, Constants.FEATURE_FILE_PATH, 'faceFeature_' + str(faceId) + '.npy')
          print ("开始保存feature:" + faceFeaturePath)
          saveFeatureData = np.array(featureData)
          np.save(faceFeaturePath, saveFeatureData)
          FaceUtils.updateFaceFeatureFile(faceId, faceFeaturePath)
  else:
    print("     " + rawFilePath + " 已处理过了")
  
  print("---------结束处理: " + rawFilePath + " ---------")

faceDB = FaceData.getFaceData()
compareFace = FaceUtils.compareFaceByOthers(4)
faceData = faceDB.findFaceById(4)
faceFilePath = faceData['imagePath']
faceId = faceData['faceId']
faceImage = cv.imread(faceFilePath)

namedWindowName = 'test_' + str(faceId)
cv.namedWindow(namedWindowName)
cv.imshow(namedWindowName, faceImage)


for valueObj in compareFace:
  faceId = valueObj[0]
  similarValue = valueObj[1]
  if (similarValue <= 0.42):
    faceData = faceDB.findFaceById(faceId)
    faceFilePath = faceData['imagePath']
    faceId = faceData['faceId']
    faceImage = cv.imread(faceFilePath)

    namedWindowName = 'test_' + str(faceId)
    cv.namedWindow(namedWindowName)
    cv.imshow(namedWindowName, faceImage)
  else:
    break

cv.waitKey(0)
cv.destroyAllWindows()