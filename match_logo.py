import cv2
import numpy as np

# Load the main image and the template
img = cv2.imread('/app/260926_MOVE_Logos_sharpened.png')
template = cv2.imread('/tmp/file_attachments/image.png')

if template is None:
    print("Could not load template")
    exit()

if img is None:
    print("Could not load image")
    exit()

h, w = template.shape[:2]

# The template might not be the exact same size, but let's try template matching at different scales
# Actually, the user attached the image they probably cropped from the big image or something.
# Let's try direct template matching first
res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    print("Found exact match at:", pt)
    break
else:
    print("No exact match found.")
