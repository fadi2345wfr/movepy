import cv2
import numpy as np
from PIL import Image

# The user attached a new image showing the sponsors block but it looks highly distorted/sharpened/corrupted.
# They said "das hat nicht erfolgreich geklappt", maybe the coordinates were slightly off,
# or the scaling was wrong, leaving artifacts, or the template they uploaded had a slightly different background color,
# leaving a visible bounding box or seam on the poster.

img_cv = cv2.imread('/app/260926_MOVE_Logos_sharpened.png')
# Let's search using the original template we saved
template = cv2.imread('/app/sponsors_logo.png')

gray_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

best_match = None
for scale in np.linspace(0.8, 1.5, 100):
    resized_template = cv2.resize(gray_template, (0,0), fx=scale, fy=scale)
    if resized_template.shape[0] > gray_img.shape[0] or resized_template.shape[1] > gray_img.shape[1]:
        continue
    res = cv2.matchTemplate(gray_img, resized_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if best_match is None or max_val > best_match[0]:
        best_match = (max_val, max_loc, scale, resized_template.shape)

print(f"Best match: val={best_match[0]}, loc={best_match[1]}, scale={best_match[2]}, size={best_match[3]}")

x, y = best_match[1]
h, w = best_match[3]

# To make sure we replace it cleanly, we should clear the background to pure white first in that bounding box,
# then paste the new logo. The new logo might have an off-white background, let's remove its background and make it pure white
# or just paste it using a mask.
original = Image.open('/app/260926_MOVE_Logos_sharpened.png').convert("RGB")
new_logo = Image.open('/app/sponsors_logo.png').convert("RGBA")

# Make the near-white background of the template transparent
data = np.array(new_logo)
# The template has a gray-ish white background (e.g. 240-255). Let's make anything >230 transparent.
# Actually, a better way is to just paint a white box over the old logo, and then paste the new one with its own background,
# but the user's screenshot shows an ugly seam/artifacting.
# Let's look at what the user attached: the new attachment `image.png` is an extremely sharpened, deep-fried looking version
# of the sponsors block. It seems my general UnsharpMask from step 1 (radius 2, 150%) or the later "sharpen all logos" step
# messed up the sponsors block heavily.

# Ah, the screenshot shows the result of my previous replacement! It looks terrible because the image they just uploaded
# is deep-fried. No, the image they just uploaded is a screenshot OF the bad result.
# Wait, why did the previous replacement look bad?
# Oh, the previous script `replace_sponsors.py` pasted the image at `x=829, y=1518`.
# Maybe the dimensions were wrong. Let's just restore the original and do it again carefully.
# Wait, the user said "das hat nicht erfolgreich geklappt" and attached a picture.
# The picture they attached (`image.png` size 279x220) looks very jagged.
