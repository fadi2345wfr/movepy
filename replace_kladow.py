import cv2
import numpy as np
from PIL import Image

img_cv = cv2.imread('/app/260926_MOVE_Logos_sharpened.png')
template = cv2.imread('/app/kladow_logo.png')

# Convert to grayscale for matching
gray_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

best_match = None
# Look for "KLADOW" logo in the main image to replace it with the new template
# The template is 207x145, it might be roughly the same size in the poster
for scale in np.linspace(0.5, 2.0, 100):
    resized_template = cv2.resize(gray_template, (0,0), fx=scale, fy=scale)
    if resized_template.shape[0] > gray_img.shape[0] or resized_template.shape[1] > gray_img.shape[1]:
        continue
    res = cv2.matchTemplate(gray_img, resized_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if best_match is None or max_val > best_match[0]:
        best_match = (max_val, max_loc, scale, resized_template.shape)

print(f"Best match for KLADOW logo: val={best_match[0]}, loc={best_match[1]}, scale={best_match[2]}, size={best_match[3]}")

if best_match[0] > 0.4:  # Threshold can be a bit lower since the user wants to *replace* it, meaning it might look slightly different now
    x, y = best_match[1]
    h, w = best_match[3]

    # Let's replace the found region with the provided template, scaled to match the found size
    original = Image.open('/app/260926_MOVE_Logos_sharpened.png').convert("RGB")
    new_logo = Image.open('/app/kladow_logo.png').convert("RGB")
    new_logo = new_logo.resize((w, h), Image.Resampling.LANCZOS)

    # The logo might have a white background. Let's just paste it directly over.
    # To be safe, we might want to clear the old area first if the new one is slightly transparent,
    # but the template provided seems opaque (JPEG-like).

    original.paste(new_logo, (x, y))

    original.save('/tmp/file_attachments/260926_MOVE_Logos_sharpened.png')
    original.save('/app/260926_MOVE_Logos_sharpened.png')
    print("Replaced the KLADOW logo.")
else:
    print("Could not find the KLADOW logo in the main image.")
