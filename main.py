import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

img_path = '/tmp/file_attachments/260926_MOVE_Logos_sharpened.png'
original = Image.open(img_path).convert("RGB")
w, h = original.size

# 1. Sharpen Logos (from y=1154 to y=1654)
sharpened_region = original.crop((0, h-800, w, h-300))
sharpened_region = sharpened_region.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
original.paste(sharpened_region, (0, h-800, w, h-300))

# 2. Draw Bottom Line and Ticket Number
draw = ImageDraw.Draw(original)
# Clear the bottom region below y=h-220
draw.rectangle([(0, h-220), (w, h)], fill=(255, 255, 255))

# Draw dashed line around y=h-200 with dots at the ends
line_y = h - 200
line_color = (115, 115, 115)
dash_length = 20
space_length = 15

start_x = 20
end_x = w - 20

# Draw left dot
draw.ellipse([(start_x-5, line_y-5), (start_x+5, line_y+5)], fill=line_color)
# Draw right dot
draw.ellipse([(end_x-5, line_y-5), (end_x+5, line_y+5)], fill=line_color)

for x in range(start_x + 15, end_x - 15, dash_length + space_length):
    draw.line([(x, line_y), (min(x + dash_length, end_x - 15), line_y)], fill=line_color, width=4)

# Generate a 9-digit number with spaces
raw_number = str(random.randint(100000000, 999999999))
ticket_number = f"{raw_number[:3]} {raw_number[3:6]} {raw_number[6:]}"

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 55)
except Exception:
    font = ImageFont.load_default()

text1 = "TICKET-NR. "
text2 = ticket_number
color1 = (107, 28, 158)
color2 = (0, 0, 0)

# Calculate widths
bbox1 = font.getbbox(text1)
w1 = bbox1[2] - bbox1[0]
h1 = bbox1[3] - bbox1[1]

bbox2 = font.getbbox(text2)
w2 = bbox2[2] - bbox2[0]

total_w = w1 + w2
text_start_x = (w - total_w) // 2
text_start_y = h - 120

draw.text((text_start_x, text_start_y), text1, fill=color1, font=font)
draw.text((text_start_x + w1, text_start_y), text2, fill=color2, font=font)

# Save back to the original attachment
original.save('/tmp/file_attachments/260926_MOVE_Logos_sharpened.png')
print("Successfully sharpened logos and added a random ticket number:", ticket_number)
