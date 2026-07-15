import cv2
import numpy as np
from PIL import Image

img_cv = cv2.imread('/app/260926_MOVE_Logos_sharpened.png')
template = cv2.imread('/app/sponsors_logo.png')

gray_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# The user said "unten rechts zwei logos so". We need to find the "SPONSOREN:" block on the right.
# Let's search for this block.
best_match = None
for scale in np.linspace(0.5, 2.5, 100):
    resized_template = cv2.resize(gray_template, (0,0), fx=scale, fy=scale)
    if resized_template.shape[0] > gray_img.shape[0] or resized_template.shape[1] > gray_img.shape[1]:
        continue
    res = cv2.matchTemplate(gray_img, resized_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if best_match is None or max_val > best_match[0]:
        best_match = (max_val, max_loc, scale, resized_template.shape)

print(f"Best match for Sponsors block: val={best_match[0]}, loc={best_match[1]}, scale={best_match[2]}, size={best_match[3]}")

if best_match[0] > 0.4:
    x, y = best_match[1]
    h, w = best_match[3]

    # We will paste the new clearer version over the old one.
    original = Image.open('/app/260926_MOVE_Logos_sharpened.png').convert("RGB")
    new_logo = Image.open('/app/sponsors_logo.png').convert("RGB")

    # To avoid background mismatch (if template has slight gray background), let's make its white transparent or just paste it
    # Actually, the poster has a white background. Let's just resize and paste.
    new_logo = new_logo.resize((w, h), Image.Resampling.LANCZOS)

    original.paste(new_logo, (x, y))

    original.save('/tmp/file_attachments/260926_MOVE_Logos_sharpened.png')
    original.save('/app/260926_MOVE_Logos_sharpened.png')
    print("Replaced the Sponsors block on the right.")
else:
    print("Could not find the Sponsors block.")
