import cv2
import numpy as np

img = cv2.imread('/app/260926_MOVE_Logos_sharpened.png')
# The logo has the text "BERLIN" in red. Let's look for red text.
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# lower mask (0-10)
lower_red = np.array([0,50,50])
upper_red = np.array([10,255,255])
mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

# upper mask (170-180)
lower_red = np.array([170,50,50])
upper_red = np.array([180,255,255])
mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

# join my masks
mask = mask0 + mask1

coords = np.where(mask > 0)
if len(coords[0]) > 0:
    min_y, max_y = np.min(coords[0]), np.max(coords[0])
    min_x, max_x = np.min(coords[1]), np.max(coords[1])
    print(f"Found red pixels at Y: {min_y} to {max_y}, X: {min_x} to {max_x}")
else:
    print("No red pixels found")
