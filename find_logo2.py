import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('/app/260926_MOVE_Logos_sharpened.png', cv2.IMREAD_GRAYSCALE)
template = cv2.imread('/tmp/file_attachments/image.png', cv2.IMREAD_GRAYSCALE)

res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.5
loc = np.where( res >= threshold)

for pt in zip(*loc[::-1]):
    print("Found potential match at:", pt)
