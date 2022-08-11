import os
import random
import textwrap

from PIL import Image, ImageFont, ImageDraw


def get_img(name):
    return Image.open(f'quoteBgs/{name}')


def get_random_img():
    return get_img(random.choice(os.listdir("quoteBgs")))


def write_to_pic(text, tagged):
    image = get_random_img()
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("font.ttf", size=34)
    para = textwrap.wrap(text, width=30)

    S, W = 80, 640

    draw.rectangle((S, S, W, W))

    current_h, pad = S + 10, 10

    current_h += current_h * (11 - len(para)) / 3

    for line in para:
        w, h = draw.textlength(line, font=font)
        draw.text(((W - w + S) / 2, current_h + S / 2), line, font=font)
        current_h += h + pad

    w, h = draw.textsize(tagged, font=font)
    draw.text(((W - w + S) / 2, current_h + h + S / 2), tagged, font=font)
    image.save("quoteBgs/test.png")


img = get_random_img()
write_to_pic(
    "If you're visiting this page, you're likely here because you're searching for a random sentence. Sometimes a random word just isn't enough, and that is where the random sentence generator comes into play. By inputting the desir ",
    "@ravenFTX")

# resize
exit(0)
for image_path in os.listdir("bgs"):
    print(image_path)
    img = Image.open(f'bgs/{image_path}')
    wsize = 1280
    hsize = 720
    img = img.resize((wsize, hsize), Image.LANCZOS)
    img.save(f'quoteBgs/{image_path}')
