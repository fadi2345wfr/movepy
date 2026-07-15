import cv2
import numpy as np

img = cv2.imread('/app/260926_MOVE_Logos_sharpened.png')
# Convert to grayscale for better matching
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread('/tmp/file_attachments/image.png', cv2.IMREAD_GRAYSCALE)

# Try different scales of the template
found = None
for scale in np.linspace(0.2, 3.0, 50)[::-1]:
    resized = cv2.resize(template, (int(template.shape[1] * scale), int(template.shape[0] * scale)))
    if resized.shape[0] > img_gray.shape[0] or resized.shape[1] > img_gray.shape[1]:
        continue

    res = cv2.matchTemplate(img_gray, resized, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if found is None or max_val > found[0]:
        found = (max_val, max_loc, scale)

print(f"Best match: {found[0]} at scale {found[2]}")
if found[0] > 0.6:
    print(f"Location: {found[1]}")
    scale = found[2]
    print(f"Size: {int(template.shape[1]*scale)}x{int(template.shape[0]*scale)}")
