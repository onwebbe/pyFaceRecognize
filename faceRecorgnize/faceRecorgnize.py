import cv2 as cv
import numpy as np
import dlib
import utils.Constants as Constants
from skimage import io

def getFaceFeature(imagePath, rawImagePath):
  image = io.imread(imagePath)
  predictor_path = Constants.DATA_ROOT_PATH + '/' + Constants.PROGRAM_DATA_PATH + '/' + 'shape_predictor_68_face_landmarks.dat'
  face_rec_model_path = Constants.DATA_ROOT_PATH + '/' + Constants.PROGRAM_DATA_PATH + '/' + 'dlib_face_recognition_resnet_model_v1.dat'
  # prepare predict 
  sp = dlib.shape_predictor(predictor_path)
  facerec = dlib.face_recognition_model_v1(face_rec_model_path)
  detector = dlib.get_frontal_face_detector()
  
  dets = detector(image, 0)
  for k, d in enumerate(dets): 
    shape = sp(image, d)
    # 提取特征
    face_descriptor = facerec.compute_face_descriptor(image, shape)
    v = np.array(face_descriptor)

    return v