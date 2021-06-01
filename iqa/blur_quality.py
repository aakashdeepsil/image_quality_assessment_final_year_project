import tensorflow as tf
import keras
import matplotlib.pyplot as plt
import numpy as np
import cv2

#Total Variation
def totalVariation(content_image):
    image = tf.Variable(content_image)
    total_variation = tf.image.total_variation(image).numpy()
    return total_variation[0]

# Diagonal Modified Laplacian
def digModifiedLaplacian(img):
    M1 = np.array([[-1, 2, -1]])
    M2 = np.array([[0, 0, -1], [0, 2, 0], [-1, 0, 0]])/np.sqrt(2)
    M3 = np.array([[-1, 0, 0], [0, 2, 0], [0, 0, -1]])/np.sqrt(2)
    F1 = np.abs(cv2.filter2D(img, -1, M1))
    F2 = np.abs(cv2.filter2D(img, -1, M2))
    F3 = np.abs(cv2.filter2D(img, -1, M3))
    F4 = np.abs(cv2.filter2D(img, -1, M1.T))
    FM = np.abs(F1) + np.abs(F2) + np.abs(F3) + np.abs(F4)
    return(np.mean(FM))


# Singular Value Decomposition
def svd(img):
    #Takes a lot of time for color image.
    top_sv=0
    total_sv=0
    sv_num=3
    u, s, v = np.linalg.svd(img)
    top_sv = np.sum(s[0:sv_num])
    total_sv = np.sum(s)
    return(top_sv/total_sv)