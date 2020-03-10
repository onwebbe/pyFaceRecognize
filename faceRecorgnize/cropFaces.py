import cv2 as cv
import numpy as np
import utils.ImageUtils as ImageUtils
import utils.Constants as Constants
import dlib
import utils.Constants as Constants
from skimage import io


def cropFaces(imagePath):
  #Loading the image to be tested
  image_raw = ImageUtils.createImageFromPath(imagePath)

  #Converting to grayscale
  image_gray = cv.cvtColor(image_raw, cv.COLOR_BGR2GRAY)

  haar_cascade_face = cv.CascadeClassifier(Constants.DATA_ROOT_PATH + '/' + Constants.PROGRAM_DATA_PATH + '/' + 'haarcascade_frontalface_default.xml')

  faces_rects = haar_cascade_face.detectMultiScale(image_gray, scaleFactor = 1.2, minNeighbors = 5)

  # Let us print the no. of faces found
  print('Faces found: ', len(faces_rects))

  croppedImage_list = []
  for (x,y,w,h) in faces_rects:
    croppedImage = image_raw[y:(y+h), x:(x+w)]
    croppedImage_list.append(croppedImage)
    cv.rectangle(image_raw, (x, y), (x+w, y+h), (0, 255, 0), 2)
  
  result_data = {}
  result_data['croppedImageList'] = croppedImage_list
  result_data['imageHighlighed'] = image_raw
  return result_data

def cropFaces2(imagePath):
  #Loading the image to be tested
  result_data = None
  image_raw = ImageUtils.createImageFromPath(imagePath)
  
  if (image_raw is not None):
    cloned_image = ImageUtils.cloneImage(image_raw)
    predictor_path = Constants.DATA_ROOT_PATH + '/' + Constants.PROGRAM_DATA_PATH + '/' + 'shape_predictor_68_face_landmarks.dat'
    face_rec_model_path = Constants.DATA_ROOT_PATH + '/' + Constants.PROGRAM_DATA_PATH + '/' + 'dlib_face_recognition_resnet_model_v1.dat'
    # prepare predict 
    sp = dlib.shape_predictor(predictor_path)
    facerec = dlib.face_recognition_model_v1(face_rec_model_path)
    detector = dlib.get_frontal_face_detector()

    croppedImage_list = []
    feature_list = []
    dets = detector(image_raw, 1)
    for k, d in enumerate(dets):
      x, y, w, h = d.left(), d.top(), d.width(), d.height()
      croppedImage = image_raw[y:(y+h), x:(x+w)]
      croppedImage_list.append(croppedImage)
      cv.rectangle(cloned_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

      shape = sp(cloned_image, d)
      face_descriptor = facerec.compute_face_descriptor(image_raw, shape)
      v = np.array(face_descriptor)
      print('--------------------------')
      print(str(imagePath) + ':' + str(k))
      print (v)
      print('--------------------------')
      feature_list.append(v)

    result_data = {}
    result_data['croppedImageList'] = croppedImage_list
    result_data['croppedFeatureList'] = feature_list
    result_data['imageHighlighed'] = cloned_image
  return result_data