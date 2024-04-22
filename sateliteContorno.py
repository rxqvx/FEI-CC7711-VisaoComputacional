

import math
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Importa e converte para RGB
img = cv2.imread('./Satelite.jpeg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Convertendo para preto e branco (RGB -> Gray Scale -> BW)
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
a = img_gray.max()
_, thresh = cv2.threshold(img_gray, a/3, a, cv2.THRESH_BINARY_INV)

# Aplicação de abertura para remover pequenos ruídos
tamanhoKernel = 3
kernel = np.ones((tamanhoKernel, tamanhoKernel), np.uint8)
thresh_open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# Aplicação de fechamento para suavizar os contornos
thresh_close = cv2.morphologyEx(thresh_open, cv2.MORPH_CLOSE, kernel)

# Filtro de ruído (blurring)
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

# Detecção de bordas com Canny (sem blur)
edges_gray = cv2.Canny(image=img_gray, threshold1=a/2, threshold2=a)

# Detecção de bordas com Canny (com blur)
edges_blur = cv2.Canny(image=img_blur, threshold1=a/2, threshold2=a)

# Encontrar contornos
contours, hierarchy = cv2.findContours(
                                   image=thresh_close,
                                   mode=cv2.RETR_TREE,
                                   method=cv2.CHAIN_APPROX_SIMPLE)

contours = sorted(contours, key=cv2.contourArea, reverse=True)
img_copy = img.copy()
final = cv2.drawContours(img_copy, contours, contourIdx=-1,
                         color=(255, 0, 0), thickness=2)

# Plot imagens
imagens = [img, img_blur, img_gray, edges_gray, edges_blur, thresh, thresh_open, thresh_close, final]

formatoX = math.ceil(len(imagens) ** 0.5)
if (formatoX ** 2 - len(imagens)) > formatoX:
    formatoY = formatoX - 1
else:
    formatoY = formatoX
for i in range(len(imagens)):
    plt.subplot(formatoY, formatoX, i + 1)
    plt.imshow(imagens[i], 'gray')
    plt.xticks([]), plt.yticks([])
plt.show()