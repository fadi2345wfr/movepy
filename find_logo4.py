import cv2
import numpy as np

img = cv2.imread('/app/260926_MOVE_Logos_sharpened.png', cv2.IMREAD_GRAYSCALE)
template = cv2.imread('/tmp/file_attachments/image.png', cv2.IMREAD_GRAYSCALE)

best_match = None
for scale in np.linspace(0.1, 1.5, 100):
    resized = cv2.resize(template, (0,0), fx=scale, fy=scale)
    if resized.shape[0] > img.shape[0] or resized.shape[1] > img.shape[1]:
        continue
    res = cv2.matchTemplate(img, resized, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if best_match is None or max_val > best_match[0]:
        best_match = (max_val, max_loc, scale, resized.shape)

print(f"Best Match: val={best_match[0]}, loc={best_match[1]}, scale={best_match[2]}, size={best_match[3]}")
