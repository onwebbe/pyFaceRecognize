import db.sqlLite3DB as sqlLiteDB
import utils.Constants as Constants
class FaceDB():
  def __init__(self, db):
    if (db == None):
      self.db = sqlLiteDB
    else:
      self.db = db

  def startDatabase(self):
    self.conn = self.db.startDatabase()
    pass

  def stopDatabase(self):
    self.db.stopDatabase(self.conn)
    pass

  def newFace(self, rawImagePath, facePath, personId):
    data = {}
    data['facepath'] = facePath
    data['personId'] = personId
    data['imagepath'] = rawImagePath
    return self.db.newFace(self.conn, data)

  def newPerson(self, name):
    return self.db.newPerson(self.conn, name)

  def getAllFaces(self):
    return self.db.getAllFaces(self.conn)

  def updateFaceFeature(self, faceId, faceFeaturePath):
    return self.db.updateFaceFeature(self.conn, faceId, faceFeaturePath)

  def searchFaceByRawImageFileName(self, rawImageFileName):
    return self.db.searchFaceByRawImageFileName(self.conn, rawImageFileName)
  
  def findFaceById(self, faceId):
    return self.db.findFaceById(self.conn, faceId)

faceDB = FaceDB(Constants.FACE_DB)
faceDB.startDatabase()

def getFaceData():
  return faceDB