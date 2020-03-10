import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import dlib
import utils.Constants as Constants
from skimage import io
import utils.FaceUtils as FaceUtils

def getFaceFeature(imagePath, rawImagePath):
  image = io.imread(imagePath)
  predictor_path = Constants.DATA_ROOT_PATH + '/' + Constants.PROGRAM_DATA_PATH + '/' + 'shape_predictor_68_face_landmarks.dat'
  face_rec_model_path = Constants.DATA_ROOT_PATH + '/' + Constants.PROGRAM_DATA_PATH + '/' + 'dlib_face_recognition_resnet_model_v1.dat'
  # prepare predict 
  sp = dlib.shape_predictor(predictor_path)
  facerec = dlib.face_recognition_model_v1(face_rec_model_path)
  detector = dlib.get_frontal_face_detector()
  
  dets = detector(image, 1)
  for k, d in enumerate(dets): 
    shape = sp(image, d)
    # 提取特征
    face_descriptor = facerec.compute_face_descriptor(image, shape)
    v = np.array(face_descriptor)

    return v
    # faceId = FaceUtils.createNewPersonFace(imagePath, rawImagePath)
    # faceFeaturePath = Constants.DATA_ROOT_PATH + '/' + Constants.FEATURE_FILE_PATH + '/faceFeature_' + str(faceId) + '.feature.npy'
    # numpy_array = np.array(v)
    # np.save(faceFeaturePath, numpy_array )
    # FaceUtils.updateFaceFeatureFile(faceId, faceFeaturePath)

def convertToRGB(image):
    return cv.cvtColor(image, cv.COLOR_BGR2RGB)

def faceDetect():
  #Loading the image to be tested
  test_image = cv.imread('/Users/i326432/Downloads/face2.jpg')
  #Converting to grayscale
  test_image_gray = cv.cvtColor(test_image, cv.COLOR_BGR2GRAY)
  plt.imshow(test_image_gray, cmap='gray')




  haar_cascade_face = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

  faces_rects = haar_cascade_face.detectMultiScale(test_image_gray, scaleFactor = 1.2, minNeighbors = 5)

  # Let us print the no. of faces found
  print('Faces found: ', len(faces_rects))
  i = 0
  for (x,y,w,h) in faces_rects:
      croppedImage = test_image[y:(y+h), x:(x+w)]
      cv.imwrite(str(i)+".bmp", croppedImage)
      i = i + 1
      cv.rectangle(test_image, (x, y), (x+w, y+h), (0, 255, 0), 2)


  #convert image to RGB and show image
  cv.namedWindow('test')
  cv.imshow('test', test_image)

  cv.waitKey(0)
  cv.destroyAllWindows()


# feature1 = getFaceFeature('1.bmp', '/Users/i326432/Downloads/face2.jpg')
# feature2 = getFaceFeature('1.bmp', '/Users/i326432/Downloads/face2.jpg')
# print (np.linalg.norm(feature1 - feature2))


# print (FaceUtils.loadAllFaces())

# feature1 = getFaceFeature('1.bmp', '/Users/i326432/Downloads/face2.jpg')
# faceFeaturePath = Constants.DATA_ROOT_PATH + '/' + Constants.FEATURE_FILE_PATH + '/xxxfaceFeature_0.feature.npy'
# numpy_array = np.array(feature1)
# np.save(faceFeaturePath, numpy_array )
# print (np.load(Constants.DATA_ROOT_PATH + '/' + Constants.FEATURE_FILE_PATH + '/faceFeature_1.npy'))
