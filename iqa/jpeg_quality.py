import numpy as np
from scipy.signal import convolve2d
from statistics import mean

def jpegQuality(image):
    m,n = image.shape
    f1 = np.array([[1,-1]])
    f2 = f1.transpose()
    h = abs(convolve2d(image,f1,'valid'))
    v = abs(convolve2d(image,f1.transpose(),'valid'))
    m1 = m//8
    n1 = n//8
    map1=[]
    map2=[]
    len=4
    for i in range(1,m1-1):
        for j in range(1,n1-1):
            
            value = sum(h[i*8:i*8+8,j*8-len-1:j*8+8+len])/8
            L_h = sum(value[len+1:len+8])/7
            P_h = sum(value[0:len]+value[len+1:len+1+len]+value[8:len+8]+value[len+9:len+9+len])/4/len
            B_h = value[len]+value[8+len]
            
            value = np.sum(v[i*8-len-1:i*8+8+len,j*8:j*8+8],axis=1)/8
            L_v = sum(value[len+1:len+8])/7
            P_v = sum(value[0:len]+value[len+1:len+1+len]+value[8:len+8]+value[len+9:len+9+len])/4/len
            B_v = value[len]+value[8+len]
            
            B = ((B_h+B_v)/2)-(P_h+P_v)
            L = L_v+L_h
            lab = abs(B)+abs(L)
            
            if lab>0:
                map1.append(B)
                map2.append(L)
    
    B = mean(map1)
    L = mean(map2)
    IQA = B/(L**(0.215))
    
    return IQA          