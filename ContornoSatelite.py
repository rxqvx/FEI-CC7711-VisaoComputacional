#pip install opencv-python

import math

import numpy as np
import cv2
import matplotlib.pyplot as plt

#Importa e converta para RGB
img = cv2.imread('./Satelite.jpeg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img_blur = cv2.blur(img,(25,25))

#Convertendo para preto e branco (RGB -> Gray Scale -> BW)
img_gray = cv2.cvtColor(img_blur, cv2.COLOR_RGB2GRAY)
a = img_gray.max()
_, thresh = cv2.threshold(img_gray, a/4.5, a,cv2.THRESH_BINARY_INV)


tamanhoKernel = 25
kernel = np.ones((tamanhoKernel,tamanhoKernel), np.uint8)


#Filtro de ruído (bluring)
#img_blur = cv2.blur(img_gray, ksize=(tamanhoKernel,tamanhoKernel))

# Detecção borda com Canny (sem blurry)
edges_gray = cv2.Canny(image=img_gray, threshold1=a/1, threshold2=a/1)
# Detecção borda com Canny (com blurry)
edges_blur = cv2.Canny(image=img_blur, threshold1=a/10, threshold2=a/10)

thresh_open = cv2.dilate(thresh,kernel,iterations = 1)

img_grad = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)



# contorno
contours, hierarchy = cv2.findContours(
                                   image = edges_blur,
                                   mode = cv2.RETR_TREE,
                                   method = cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea, reverse = True)
img_copy = img.copy()
final = cv2.drawContours(img_copy, contours, contourIdx = -1,
                         color = (255, 0, 0), thickness = 2)


#plot imagens
#imagens = [img,img_gray,img_blur,edges_gray,edges_blur,thresh,thresh_open,img_grad,final]
imagens = [final]

formatoX = math.ceil(len(imagens)**.5)
if (formatoX**2-len(imagens))>formatoX:
    formatoY = formatoX-1
else:
    formatoY = formatoX
for i in range(len(imagens)):
    plt.subplot(formatoY, formatoX, i + 1)
    plt.imshow(imagens[i],'gray')
    plt.xticks([]),plt.yticks([])
plt.show()
