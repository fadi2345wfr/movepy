from PIL import Image

# Let's open the main image
original = Image.open('/app/260926_MOVE_Logos_sharpened.png').convert("RGB")

# Open the clear template
new_logo = Image.open('/app/sponsors_logo.png').convert("RGB")

# The location is x=828, y=1518, w=259, h=197 based on the match
x, y = 828, 1518
w, h = 259, 197

# Instead of just pasting, the previous paste left artifacts because the new logo might not have covered the old one perfectly,
# or the resize method caused jaggedness. Let's use LANCZOS and make sure to clear the area with white first.
from PIL import ImageDraw
draw = ImageDraw.Draw(original)
# Draw a white rectangle slightly larger than the found match to cover any artifacts
pad = 10
draw.rectangle([(x-pad, y-pad), (x+w+pad, y+h+pad)], fill=(255, 255, 255))

# Resize the new logo cleanly
new_logo = new_logo.resize((w, h), Image.Resampling.LANCZOS)
original.paste(new_logo, (x, y))

original.save('/tmp/file_attachments/260926_MOVE_Logos_sharpened.png')
original.save('/app/260926_MOVE_Logos_sharpened.png')
print("Fixed the sponsors block with a clean wipe and paste.")
