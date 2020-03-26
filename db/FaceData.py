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

  def getAllFacesWithName(self):
    return self.db.getAllFacesWithName(self.conn)

  def getAllPersons(self):
    return self.db.getAllPersons(self.conn)

  def getPersonById(self, personId):
    return self.db.getPersonById(self.conn, personId)

  def updateFaceFeature(self, faceId, faceFeaturePath):
    return self.db.updateFaceFeature(self.conn, faceId, faceFeaturePath)

  def searchFaceByRawImageFileName(self, rawImageFileName):
    return self.db.searchFaceByRawImageFileName(self.conn, rawImageFileName)
  
  def findFaceById(self, faceId):
    return self.db.findFaceById(self.conn, faceId)

  def changeFacePerson(self, faceId, personId):
    return self.db.changeFacePerson(self.conn, faceId, personId)
  
  def changePersonName(self, personId, personName):
    return self.db.changePersonName(self.conn, personId, personName)
    
  def getFacesByPersonId(self, personId):
    return self.db.getFacesByPersonId(self.conn, personId)

faceDB = FaceDB(Constants.FACE_DB)
faceDB.startDatabase()

def getFaceData():
  return faceDB