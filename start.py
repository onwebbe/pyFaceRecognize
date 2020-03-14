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

def updateMostSimilarPerson(faceId):
  faceDB = FaceData.getFaceData()
  compareFace = FaceUtils.compareFaceByOthers(faceId)


  for valueObj in compareFace:
    compareFaceId = valueObj[0]
    similarValue = valueObj[1]
    if (similarValue <= 0.4):
      compareFaceData = faceDB.findFaceById(compareFaceId)
      comparePersonId = compareFaceData['personId']
      faceDB.changeFacePerson(faceId, comparePersonId)
      print('找到相似的脸' + str(comparePersonId))
    else:
      faceDB.changeFacePerson(faceId, Constants.PERSON_ID_UNNAMED)
      print('没有相似的脸, 更新为 匿名')
    break

def displayFaceCompareResult(sourceFaceId):
  faceDB = FaceData.getFaceData()
  compareFace = FaceUtils.compareFaceByOthers(sourceFaceId)
  faceData = faceDB.findFaceById(sourceFaceId)
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




def processAllFiles(path):
  allfile=[]
  for dirpath,dirnames,filenames in os.walk(path):
    for name in filenames:
      processFile(os.path.join(dirpath, name))
    for dir in dirnames:
      processAllFiles(os.path.join(path, dir))
  return allfile
  
def processFile(filePath):
  rawFilePath = filePath
  print("---------开始处理: " + rawFilePath + " ---------")
  existingRawFileInDB = ImageUtils.getFaceInDBByRawImage(rawFilePath)
  if (len(existingRawFileInDB) == 0):
    resultData = cropFaces.cropFaces2(rawFilePath)
    if (resultData is not None):
      faceList = resultData['croppedImageList']
      featureList = resultData['croppedFeatureList']
      faceIndex = 0
      if (len(faceList) == 0):
        faceId = FaceUtils.createNewFaceForPerson('', rawFilePath, Constants.PERSON_ID_UNNAMED)
        FaceUtils.updateFaceFeatureFile(faceId, '')
      else:
        for index in range(0, len(faceList)):
          faceImage = faceList[index]
          featureData = featureList[index]

          faceFileName = os.path.join(Constants.DATA_ROOT_PATH, Constants.FACE_IMG_FILE_PATH, "face_" + filename + "_" + str(faceIndex) + ".bmp")
          cv.imwrite(faceFileName, faceImage)
          
          faceIndex = faceIndex + 1

          faceId = FaceUtils.createNewFaceForPerson(faceFileName, rawFilePath, Constants.PERSON_ID_UNNAMED)
          faceFeaturePath = os.path.join(Constants.DATA_ROOT_PATH, Constants.FEATURE_FILE_PATH, 'faceFeature_' + str(faceId) + '.npy')
          print ("开始保存feature:" + faceFeaturePath)
          saveFeatureData = np.array(featureData)
          np.save(faceFeaturePath, saveFeatureData)
          FaceUtils.updateFaceFeatureFile(faceId, faceFeaturePath)

          updateMostSimilarPerson(faceId)
  else:
    print("     " + rawFilePath + " 已处理过了")
  
  print("---------结束处理: " + rawFilePath + " ---------")

processAllFiles(rawImageRootPath)