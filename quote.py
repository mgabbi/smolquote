import os
import random
import textwrap

from PIL import Image, ImageFont, ImageDraw


def get_img(name):
    return Image.open(f'quoteBgs/{name}')


def get_random_img():
    return get_img(random.choice(os.listdir("quoteBgs")))


def write_to_pic(img, text):
    font = ImageFont.truetype("font.ttf", size=48)
    editable = ImageDraw.Draw(img)
    W, H = 1280, 720

    box = editable.textbbox((W / 2, H / 2), text, font=font, align="center")

    editable.rectangle((128, 128, 720, 592))

    len = editable.textlength(text, font=font, )

    start = offset = 128
    for line in textwrap.wrap(text, width=20):
        editable.text((start, offset), line, font=font, fill="#FFF", align="center")
        offset += font.getsize(line)[1] + 10

    # editable.text()
    img.save("quoteBgs/test.png")


img = get_random_img()
write_to_pic(img,
             "WASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUPWASSUP")
# resize
exit(0)
for image_path in os.listdir("bgs"):
    print(image_path)
    img = Image.open(f'bgs/{image_path}')
    wsize = 1280
    hsize = 720
    img = img.resize((wsize, hsize), Image.LANCZOS)
    img.save(f'quoteBgs/{image_path}')
