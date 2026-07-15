import cv2
import numpy as np

img = cv2.imread('/app/260926_MOVE_Logos_sharpened.png', cv2.IMREAD_GRAYSCALE)
template = cv2.imread('/tmp/file_attachments/image.png', cv2.IMREAD_GRAYSCALE)

# We want to find the logo without scaling if possible, or maybe it is scaled.
# The user might have just cropped it from the image.
res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(res)
print(f"Direct match confidence: {max_val} at {max_loc}")
