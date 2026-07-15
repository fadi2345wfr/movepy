import cv2
import numpy as np
from PIL import Image, ImageFilter

img_cv = cv2.imread('/app/260926_MOVE_Logos_sharpened.png')
template = cv2.imread('/tmp/file_attachments/image.png')

# The user attached the specific logo. Let's find it more robustly or just sharpen all logos again.
# The user said "hat leider nicht erfolgreich geklappt Berlin-Logo... lokalisiert und einen zusätzlichen..."
# It means my localization was wrong or the sharpening wasn't enough/didn't hit the right spot.
# Let's search the whole image for the template.
# The template is 355x51

# Let's find exactly where the template is using a scale range.
gray_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

best_match = None
for scale in np.linspace(0.5, 1.5, 100):
    resized = cv2.resize(gray_template, (0,0), fx=scale, fy=scale)
    if resized.shape[0] > gray_img.shape[0] or resized.shape[1] > gray_img.shape[1]:
        continue
    res = cv2.matchTemplate(gray_img, resized, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if best_match is None or max_val > best_match[0]:
        best_match = (max_val, max_loc, scale, resized.shape)

print(f"Best match for Berlin logo: val={best_match[0]}, loc={best_match[1]}, scale={best_match[2]}, size={best_match[3]}")

if best_match[0] > 0.5:
    x, y = best_match[1]
    h, w = best_match[3]

    # Let's also do a general sharpening of the entire logo area just in case.
    original = Image.open('/app/260926_MOVE_Logos_sharpened.png').convert("RGB")
    img_w, img_h = original.size

    # Sharpen the specific Berlin logo heavily
    # Add some padding
    pad = 10
    box = (max(0, x-pad), max(0, y-pad), min(img_w, x+w+pad), min(img_h, y+h+pad))
    logo_region = original.crop(box)

    # Apply a very strong sharpen filter
    logo_region = logo_region.filter(ImageFilter.UnsharpMask(radius=4, percent=300, threshold=1))

    # Let's also apply a slight contrast enhancement to make it pop more
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(logo_region)
    logo_region = enhancer.enhance(1.5)

    original.paste(logo_region, box)

    original.save('/tmp/file_attachments/260926_MOVE_Logos_sharpened.png')
    original.save('/app/260926_MOVE_Logos_sharpened.png')
    print("Sharpened the specific logo heavily.")
else:
    print("Could not find the logo with high confidence.")
