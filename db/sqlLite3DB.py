import sqlite3

def initDatabase(conn):
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS FACES(
    FACE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    FACE_IMAGE_PATH TEXT,
    PERSON_ID INTEGER,
    RAW_IMAGE_FILE_PATH TEXT,
    FEATURE_FILE_PATH TEXT
  );''')
  c.execute('''CREATE TABLE IF NOT EXISTS PERSON(
    PERSON_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PERSON_NAME TEXT DEFAULT '匿名'
  );''')
  conn.commit()


def startDatabase():
  conn = sqlite3.connect('test.db')
  initDatabase(conn)
  return conn

def stopDatabase(conn):
  conn.close()

def createNewFace(conn):
  pass

def newPerson(conn, personName):
  if (personName != None):
    sql = "INSERT INTO PERSON (PERSON_NAME) VALUES ('" + personName + "')"
    c = conn.cursor()
    c.execute(sql)
  else:
    sql = "INSERT INTO PERSON (PERSON_NAME) VALUES ('匿名')"
    c = conn.cursor()
    c.execute(sql)
    cursor = c.execute("select last_insert_rowid();")

  conn.commit()
  personId = None
  for row in cursor:
    personId = row[0]
  
  return personId
    

def newFace(conn, data):
  c = conn.cursor()
  face_path = data['facepath']
  person_id = data['personId']
  image_path = data['imagepath']
  sql = "INSERT INTO FACES (FACE_IMAGE_PATH, PERSON_ID, RAW_IMAGE_FILE_PATH) \
          VALUES ('" + face_path + "'," + str(person_id) + ",'" + image_path + "')"
  c.execute(sql)
  cursor = c.execute("select last_insert_rowid();")
  conn.commit()
  faceId = None
  for row in cursor:
    faceId = row[0]

  return faceId

def updateFaceFeature(conn, faceId, faceFeaturePath):
  sql = "UPDATE FACES SET FEATURE_FILE_PATH = '" + faceFeaturePath + "' WHERE FACE_ID=" + str(faceId)
  c = conn.cursor()
  c.execute(sql)
  conn.commit()

def getAllFaces(conn):
  sql = "SELECT FACE_ID, FACE_IMAGE_PATH, PERSON_ID, RAW_IMAGE_FILE_PATH, FEATURE_FILE_PATH FROM FACES"
  c = conn.cursor()
  cursor = c.execute(sql)
  facesData = []
  for row in cursor:
    faceData = {}
    faceData['faceId'] = row[0]
    faceData['imagePath'] = row[1]
    faceData['personId'] = row[2]
    faceData['rawImagePath'] = row[3]
    faceData['featurePath'] = row[4]
    facesData.append(faceData)
  return facesData
    
def searchFaceByRawImageFileName(conn, rawImageFileName):
  sql = "SELECT FACE_ID, FACE_IMAGE_PATH, PERSON_ID, RAW_IMAGE_FILE_PATH, FEATURE_FILE_PATH FROM FACES WHERE RAW_IMAGE_FILE_PATH = '" + rawImageFileName + "'"
  c = conn.cursor()
  cursor = c.execute(sql)
  facesData = []
  for row in cursor:
    faceData = {}
    faceData['faceId'] = row[0]
    faceData['imagePath'] = row[1]
    faceData['personId'] = row[2]
    faceData['rawImagePath'] = row[3]
    faceData['featurePath'] = row[4]
    facesData.append(faceData)
  return facesData

def findFaceById(conn, faceId):
  sql = "SELECT FACE_ID, FACE_IMAGE_PATH, PERSON_ID, RAW_IMAGE_FILE_PATH, FEATURE_FILE_PATH FROM FACES WHERE FACE_ID = " + str(faceId)
  c = conn.cursor()
  cursor = c.execute(sql)
  for row in cursor:
    faceData = {}
    faceData['faceId'] = row[0]
    faceData['imagePath'] = row[1]
    faceData['personId'] = row[2]
    faceData['rawImagePath'] = row[3]
    faceData['featurePath'] = row[4]
    return faceData
  return None

# connect = startDatabase()
# print(newPerson(connect, None))
# stopDatabase(connect)