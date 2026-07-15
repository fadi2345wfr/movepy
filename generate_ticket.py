import random
import os
from PIL import Image, ImageEnhance, ImageDraw, ImageFont

def process_image(input_img_path, insert_img_path, output_path):
    img = Image.open(input_img_path).convert('RGB')

    # 1. Sharpen the image
    enhancer = ImageEnhance.Sharpness(img)
    img_sharpened = enhancer.enhance(2.0)

    # 2. Expand canvas height by 400 pixels to ensure no overlap
    width, height = img_sharpened.size
    new_height = height + 400
    new_img = Image.new('RGB', (width, new_height), color='white')
    new_img.paste(img_sharpened, (0, 0))

    draw = ImageDraw.Draw(new_img)

    # 3. Draw dashed line
    line_y = height + 30
    dash_length = 20
    space_length = 15
    for x in range(0, width, dash_length + space_length):
        draw.line([(x, line_y), (min(x + dash_length, width), line_y)], fill='black', width=3)

    # 4. Paste image.png
    insert_img = Image.open(insert_img_path).convert('RGBA')
    # Resize insert_img to fit nicely
    insert_img.thumbnail((width - 40, 200))

    insert_x = (width - insert_img.width) // 2
    insert_y = line_y + 30
    new_img.paste(insert_img, (insert_x, insert_y), insert_img)

    # 5. Generate 9-digit ticket number
    ticket_number = f"{random.randint(100000000, 999999999)}"

    # 6. Draw text
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 40)
    except IOError:
        try:
             font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        except IOError:
             font = ImageFont.load_default()

    # Calculate text bounding box
    text_bbox = draw.textbbox((0, 0), f"TICKET-NR.: {ticket_number}", font=font)
    text_width = text_bbox[2] - text_bbox[0]

    text_x = (width - text_width) // 2
    # Ensure text is below the inserted image
    text_y = insert_y + insert_img.height + 40

    draw.text((text_x, text_y), f"TICKET-NR.: {ticket_number}", fill='black', font=font)

    # Save the result
    new_img.save(output_path)

if __name__ == "__main__":
    process_image("original.png", "image.png", "260926_MOVE_Logos_sharpened.png")
