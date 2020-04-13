from django.shortcuts import render
from django.http import HttpResponse
import json
import utils.FaceUtils as FaceUtils
import utils.ImageUtils as ImageUtils

from .MyEncoder import MyEncoder


from db.FaceData import FaceDB
import db.FaceData as FaceData

import utils.FaceUtils as FaceUtils

import utils.Constants as Constants

import mimetypes
import os

from wsgiref.util import FileWrapper

import django.core.servers.basehttp

# Create your views here.
def getFaces(request):
  faceDB = FaceDB(Constants.FACE_DB)
  faceDB.startDatabase()
  faceDataList = faceDB.getAllFaces()
  faceDB.stopDatabase()
  allFaceList = {}
  for faceData in faceDataList:
    faceId = faceData['faceId']
    allFaceList[faceId] = faceData
  return HttpResponse(json.dumps(allFaceList, cls=MyEncoder, indent=2))

def getImage(request):
  image_path = request.GET.get('path')
  print(image_path)
  fileWrapper = FileWrapper(open(image_path, 'rb'))
  content_type = mimetypes.guess_type(image_path)[0]
  contentLength = os.path.getsize(image_path)
  response = HttpResponse(fileWrapper, content_type = content_type)
  response['Content-Length']      = contentLength
  response['Content-Disposition'] = "attachment; filename=%s" %  image_path
  return response

def getPersons(request):
  faceDB = FaceDB(Constants.FACE_DB)
  faceDB.startDatabase()
  personDataList = faceDB.getAllPersons()
  faceDB.stopDatabase()
  allPersonList = {}
  for faceData in personDataList:
    personId = faceData['personId']
    allPersonList[personId] = faceData
  return HttpResponse(json.dumps(allPersonList, cls=MyEncoder, indent=2))

def getFacesWithName(request):
  faceDB = FaceDB(Constants.FACE_DB)
  faceDB.startDatabase()
  faceDataList = faceDB.getAllFacesWithName()
  faceDB.stopDatabase()
  allFaceList = {}
  for faceData in faceDataList:
    faceId = faceData['faceId']
    allFaceList[faceId] = faceData
  return HttpResponse(json.dumps(allFaceList, cls=MyEncoder, indent=2))


def changeFacePerson(request):
  faceId = request.GET.get('faceId')
  personId = request.GET.get('personId')
  faceDB = FaceDB(Constants.FACE_DB)
  faceDB.startDatabase()
  faceDB.changeFacePerson(faceId, personId, 'M')
  faceDB.stopDatabase()

  _updateMostSimilarPerson(faceId)
  responseJSON = {}
  responseJSON["success"] = True
  return HttpResponse(json.dumps(responseJSON, cls=MyEncoder, indent=2))


def _updateMostSimilarPerson(faceId):
  faceDB = FaceData.getNewFaceData()
  sourcePersonId = faceDB.findFaceById(faceId)['personId']
  compareFace = FaceUtils.compareFaceByOthers(faceId)
  for valueObj in compareFace:
    compareFaceId = valueObj[0]
    similarValue = valueObj[1]
    compareFaceObj = faceDB.findFaceById(compareFaceId)
    compareFaceAssignStatus = compareFaceObj['assignedStatus']
    if (compareFaceAssignStatus == 'U' or compareFaceAssignStatus == 'A'):
      if (similarValue <= 0.35):
        # compareFaceData = faceDB.findFaceById(compareFaceId)
        # targetFaceId = compareFaceData['faceId']
        faceDB.changeFacePerson(compareFaceId, sourcePersonId, 'M')
        print('找到相似的脸，改变脸：' + str(compareFaceId) + ' 到人物：' + str(sourcePersonId) + ' 相似值：' + str(similarValue))
      else:
        print('没有相似的脸了')
        break
    else:
      print('这张脸手动改过')


def changePersonName(request):
  personName = request.GET.get('personName')
  personId = request.GET.get('personId')
  faceDB = FaceDB(Constants.FACE_DB)
  faceDB.startDatabase()
  faceDB.changePersonName(personId, personName)
  faceDB.stopDatabase()
  responseJSON = {}
  responseJSON["success"] = True
  return HttpResponse(json.dumps(responseJSON, cls=MyEncoder, indent=2))

def getPersonById(request):
  personId = request.GET.get('personId')
  faceDB = FaceDB(Constants.FACE_DB)
  faceDB.startDatabase()
  personData = faceDB.getPersonById(personId)
  faceDB.stopDatabase()
  if (personData is not None):
    return HttpResponse(json.dumps(personData, cls=MyEncoder, indent=2))
  else:
    return HttpResponse(json.dumps({}, cls=MyEncoder, indent=2))

def addNewPersonFace(request):
  faceId = request.GET.get('faceId')
  personName = request.GET.get('personName')
  faceDB = FaceDB(Constants.FACE_DB)
  faceDB.startDatabase()
  personId = faceDB.newPerson(personName)
  faceDB.changeFacePerson(faceId, personId, 'M')
  faceDB.stopDatabase()
  _updateMostSimilarPerson(faceId)
  return HttpResponse(json.dumps({'success': True, 'data': {'personId': personId}}, cls=MyEncoder, indent=2))

def getFaceByPersonId(request):
  personId = request.GET.get('personId')
  faceDB = FaceDB(Constants.FACE_DB)
  faceDB.startDatabase()
  faceItem = None
  faceList = faceDB.getFacesByPersonId(personId)
  if (len(faceList) > 0):
    faceItem = faceList[0]

  return HttpResponse(json.dumps({'success': True, 'data': faceItem}, cls=MyEncoder, indent=2))

def _getPersonDetailById(personId):
  faceDB = FaceDB(Constants.FACE_DB)
  faceDB.startDatabase()
  personData = faceDB.getPersonById(personId)
  faceItem = None
  faceList = faceDB.getFacesByPersonId(personId)
  faceCount = len(faceList)
  if (len(faceList) > 0):
    faceItem = faceList[0]
  faceDB.stopDatabase()

  personDetail = {}
  if ((faceItem is not None) and (personData is not None)):
    personDetail['personId'] = personData['personId']
    personDetail['personName'] = personData['personName']
    personDetail['faceId'] = faceItem['faceId']
    personDetail['imagePath'] = faceItem['imagePath']
    personDetail['rawImagePath'] = faceItem['rawImagePath']
    personDetail['featurePath'] = faceItem['featurePath']
    personDetail['faceCount'] = faceCount
  
  return personDetail

def getPersonDetailById(request):
  personId = request.GET.get('personId')
  personDetail = _getPersonDetailById(personId)
  
  return HttpResponse(json.dumps({'success': True, 'data': personDetail}, cls=MyEncoder, indent=2))

def getPersonDetailList(request):
  faceDB = FaceDB(Constants.FACE_DB)
  faceDB.startDatabase()
  personDataList = faceDB.getAllPersons()
  faceDB.stopDatabase()

  allPersonDetailList = []
  for faceData in personDataList:
    personId = faceData['personId']
    personDetail = _getPersonDetailById(personId)
    allPersonDetailList.append(personDetail)
  return HttpResponse(json.dumps({'success': True, 'data': allPersonDetailList}, cls=MyEncoder, indent=2))