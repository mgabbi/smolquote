import os
import random
import textwrap

from PIL import Image, ImageFont, ImageDraw


def get_img(name):
    return Image.open(f'quoteBgs/{name}')


def get_random_img():
    return get_img(random.choice(os.listdir("quoteBgs")))


def write_to_pic(img, text):
    font = ImageFont.truetype("font.ttf", size=36)
    editable = ImageDraw.Draw(img)
    W, H = 1280, 720

    box = editable.textbbox((W / 2, H / 2), text, font=font, align="center")

    editable.rectangle((128, 128, 720, 592))

    len = editable.textlength(text, font=font, )

    start = offset = 128
    for line in textwrap.wrap(text, width=30):
        editable.text((start, offset), line, font=font, fill="#FFF", align="right")
        offset += font.getsize(line)[1] + 10

    # editable.text()
    img.save("quoteBgs/test.png")


img = get_random_img()
write_to_pic(img,
             "If you're visiting this page, you're likely here because you're searching for a random sentence. Sometimes a random word just isn't enough, and that is where the random sentence generator comes into play. By inputting the desired number, you can make a list of as many random sentences as you want or need")

# resize
exit(0)
for image_path in os.listdir("bgs"):
    print(image_path)
    img = Image.open(f'bgs/{image_path}')
    wsize = 1280
    hsize = 720
    img = img.resize((wsize, hsize), Image.LANCZOS)
    img.save(f'quoteBgs/{image_path}')
