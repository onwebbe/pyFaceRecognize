import db.FaceData as FaceData
import numpy as np
def loadAllFaceFeatures():
  faceDB = FaceData.getNewFaceData()
  faceDataList = faceDB.getAllFaces()
  allFaceList = {}
  for faceData in faceDataList:
    featurePath = faceData['featurePath']
    faceId = faceData['faceId']
    if (len(featurePath) > 0):
      face_array = np.load(featurePath)
      allFaceList[faceId] = face_array
  return allFaceList

def createNewPersonFace(facePath, rawImagePath):
  faceDB = FaceData.getFaceData()
  personId = faceDB.newPerson(None)
  return faceDB.newFace(rawImagePath, facePath, personId)

def createNewFaceForPerson(facePath, rawImagePath, personId):
  faceDB = FaceData.getFaceData()
  return faceDB.newFace(rawImagePath, facePath, personId)

def updateFaceFeatureFile(faceId, featurePath):
  faceDB = FaceData.getFaceData()
  return faceDB.updateFaceFeature(faceId, featurePath)

def compareFaceByOthers(faceId):
  faceDB = FaceData.getNewFaceData()
  faceData = faceDB.findFaceById(faceId)
  if (faceData != None):
    featureFilePath = faceData['featurePath']
    print("开始load feature:" + featureFilePath)
    currentFeature = np.load(featureFilePath)

    faceCompareResult = {}
    allFaceFeature = loadAllFaceFeatures()
    for key, otherFaceFeature in allFaceFeature.items():
      if (key != faceId):
        distance = (np.linalg.norm(currentFeature - otherFaceFeature))
        faceCompareResult[key] = distance
    sortedFaces = sorted(faceCompareResult.items(), key=lambda d:d[1])
    print (sortedFaces)
    return sortedFaces
