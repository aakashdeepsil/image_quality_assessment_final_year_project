import tensorflow as tf
import numpy as np
import cv2
import os
import glob
import shutil
from skimage import feature
from jpeg_quality import jpegQuality
from blur_quality import totalVariation,digModifiedLaplacian,svd


def check_directory_exists(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def saveImagesToDirectory(currentDirectoryPath, targetDirectoryPath, images):
	os.chdir(targetDirectoryPath)
	for imageName in images:
		imagePath = currentDirectoryPath[:len(currentDirectoryPath)] + imageName
		image = cv2.imread(imagePath)
		cv2.imwrite(imageName,image)
	

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


def classifyImages(imageDirectory):
	totalVariationThreshold = 18917.27147
	digModifiedLaplacianThreshold = 9.15444907
	svdThreshold = 0.409693234
	jpegThresholdLow  = 3.0190372085866
	jpegThresholdUpper = 7.01
	totalVariationWeight = 28.5014
	digModifiedLaplacianWeight = 42.3033
	svdWeight = 39.6645
	images = glob.glob(imageDirectory)
	badImages = []
	goodImages = []
	imageSuggestedForDeletion = []

	print("Total Images : ",len(images))

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

		print("----------------------------------------------")
		print("Image : ", imageName)
		print("Blur Weight : ", calculatedWeight)
		print("Jpeg Quality : ", jpegResult)
		print("----------------------------------------------")
	
	return goodImages, badImages, imageSuggestedForDeletion

def main():
	# YOU NEED TO CHANGE THESE PATHS ACCORDING TO YOUR SYSTEM
	GOOD_IMAGES_PATH = r'E:\Images\Results\goodImages'
	BAD_IMAGES_PATH = r'E:\Images\Results\badImages'
	IMAGE_SUGGESTED_FOR_DELETION_PATH = r'E:\Images\Results\imageSuggestedForDeletion'
	imageDirectory =r'E:\Images\imagesToClassify\*'

	goodImages, badImages, imageSuggestedForDelettion = classifyImages(imageDirectory)

	check_directory_exists(GOOD_IMAGES_PATH)
	check_directory_exists(BAD_IMAGES_PATH)
	check_directory_exists(IMAGE_SUGGESTED_FOR_DELETION_PATH)

	os.mkdir(GOOD_IMAGES_PATH)
	os.mkdir(BAD_IMAGES_PATH)
	os.mkdir(IMAGE_SUGGESTED_FOR_DELETION_PATH)

	saveImagesToDirectory(imageDirectory,GOOD_IMAGES_PATH,goodImages)
	saveImagesToDirectory(imageDirectory,BAD_IMAGES_PATH,badImages)
	saveImagesToDirectory(imageDirectory,IMAGE_SUGGESTED_FOR_DELETION_PATH,imageSuggestedForDelettion)


main()


