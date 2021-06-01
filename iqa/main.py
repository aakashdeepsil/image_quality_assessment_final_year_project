import tensorflow as tf
import numpy as np
import cv2
import os
import glob
from skimage import feature
from iqa.jpeg_quality import jpegQuality
from iqa.blur_quality import totalVariation,digModifiedLaplacian,svd

def load_img(path_to_img):
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img

'''
DML : blurness inc - value dec 
SVD : blurness inc - value inc
TV  : blurness inc - value dec
jpeg : compression inc - value inc

'''


def main():
	totalVariationThreshold = 18917.27147
	digModifiedLaplacianThreshold = 9.15444907
	svdThreshold = 0.409693234
	jpegThresholdLow  = 3.0190372085866
	jpegThresholdUpper = 7.01
	imageDirectory =r'E:/FinalYearProject/image_quality_assessment_final_year_project/iqa/static/images/*'
	# imageDirectory =r'C:\Users\Jatin\OneDrive\Desktop\NR- IQA\static\images\*'
	totalVariationWeight = 28.5014
	digModifiedLaplacianWeight = 42.3033
	svdWeight = 39.6645
	images = glob.glob(imageDirectory)
	badImages = []
	goodImages = []
	imageSuggestedForDeletion = []
	print(len(images))

	for image in images:
		calculatedWeight = 0
		img =cv2.imread(image,0)
		contentImage = load_img(image)
		totalVariationResult = totalVariation(contentImage)
		digModifiedLaplacianResult = digModifiedLaplacian(img)
		svdResult = svd(img)
		jpegResult = jpegQuality(img)
		imageName = image.split('\\')[-1]

		if totalVariationResult < totalVariationThreshold:
			calculatedWeight += totalVariationWeight
		else:
			calculatedWeight -= totalVariationWeight

		if digModifiedLaplacianResult < digModifiedLaplacianThreshold:
			calculatedWeight += digModifiedLaplacianWeight
		else:
			calculatedWeight -= digModifiedLaplacianWeight
		
		if svdResult < svdThreshold:
			calculatedWeight -= svdWeight
		else:
			calculatedWeight += svdWeight


		if calculatedWeight < 0 and jpegResult < jpegThresholdLow:
			goodImages.append(imageName)
		elif calculatedWeight < 0 and jpegResult > jpegThresholdLow and jpegResult < jpegThresholdUpper:
			imageSuggestedForDeletion.append(imageName) 
		else:
			badImages.append(imageName)

		print(image,calculatedWeight,jpegResult)
	
	print(goodImages)
	print(badImages)
	print(imageSuggestedForDeletion)
	
	return goodImages, badImages, imageSuggestedForDeletion
