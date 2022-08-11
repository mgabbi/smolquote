import io
import os
import random
import textwrap

from PIL import Image, ImageFont, ImageDraw


def get_img(name):
    return Image.open(f'quoteBgs/{name}')


def get_random_img():
    return get_img(random.choice(os.listdir("quoteBgs")))


def convert_pil_image_to_byte_array(img):
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()
    return img_byte_array


def get_printed_quote(text, tagged):
    image = get_random_img()
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("font.ttf", size=34)
    para = textwrap.wrap(text, width=30)

    S, W = 80, 640

    current_h, pad = S, 10

    w, h = draw.textsize(para[0], font=font)

    current_h += h * ((12 - len(para)) / 2)

    draw.text(((W - w + S) / 2, current_h + S / 2), para[0], font=font)
    current_h += h + pad

    for line in para[1:]:
        w, h = draw.textsize(line, font=font)
        draw.text(((W - w + S) / 2, current_h + S / 2), line, font=font)
        current_h += h + pad

    w, h = draw.textsize(tagged, font=font)
    draw.text(((W - w + S) / 2, current_h + 1.5 * h + S / 2), tagged, font=font)
    # image.save("quoteBgs/test.png")
    return convert_pil_image_to_byte_array(image)

# resize
# exit(0)
# for image_path in os.listdir("bgs"):
#     print(image_path)
#     img = Image.open(f'bgs/{image_path}')
#     wsize = 1280
#     hsize = 720
#     img = img.resize((wsize, hsize), Image.LANCZOS)
#     img.save(f'quoteBgs/{image_path}')
