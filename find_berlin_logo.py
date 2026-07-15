import cv2
import numpy as np

img = cv2.imread('/app/260926_MOVE_Logos_sharpened.png')
# Red mask
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(img_hsv, np.array([0,150,150]), np.array([10,255,255])) + \
       cv2.inRange(img_hsv, np.array([170,150,150]), np.array([180,255,255]))

# Find contours
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 10 and h > 10:
        print(f"Red component found at: x={x}, y={y}, w={w}, h={h}")
