import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

img_path = '/app/260926_MOVE_Logos_sharpened.png'
original = Image.open(img_path).convert("RGB")
w, h = original.size

# The specific logo was found at x=537, y=1651, size w=276, h=40
# We will heavily sharpen this specific region.
# We'll expand the box a bit just to be sure we cover it entirely.
box = (525, 1640, 525+300, 1640+60)

logo_region = original.crop(box)
# Apply a stronger unsharp mask for this specific logo
logo_region = logo_region.filter(ImageFilter.UnsharpMask(radius=3, percent=250, threshold=2))
original.paste(logo_region, box)

original.save('/tmp/file_attachments/260926_MOVE_Logos_sharpened.png')
original.save('/app/260926_MOVE_Logos_sharpened.png')
print("Successfully sharpened the specific Berlin logo.")
