#!/usr/bin/env python3

import os
import io
import tempfile
import requests
import colorsys
import json
import time
import random
import datetime
import yaml
import sys
from pathlib import Path
from sys import exit

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

import unicornhathd

if len(sys.argv) == 3:
    poke_debug = int(sys.argv[1])
    poke_class = str(sys.argv[2])

FONT = ('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 12)
#FONT = ('/usr/share/fonts/truetype/freefont/PixelMplus12-Bold.ttf', 12)

# sudo apt install fonts-droid
# FONT = ('/usr/share/fonts/truetype/droid/DroidSans.ttf', 12)

# sudo apt install fonts-roboto
# FONT = ('/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf', 10)

unicornhathd.rotation(0)
unicornhathd.brightness(0.4)

width, height = unicornhathd.get_shape()

text_x = width
text_y = 2

font_file, font_size = FONT
font = ImageFont.truetype(font_file, font_size)
text_width, text_height = width, 0

# open weather map
base_path = os.path.dirname(os.path.abspath(__file__))
with open(base_path + '/../lib/api_info.yml','r') as yml:
    api_info = yaml.safe_load(yml)

apikey = api_info['weather']['key']
city = api_info['weather']['city']
api = api_info['weather']['api']
k2c =lambda k: k - 273.15
url = api.format(city=city, key=apikey)

# pokemon image
pokemon_path_org = api_info['pokemon']['path']

def imread_web(url):
    res = requests.get(url)
    img = None
    with tempfile.NamedTemporaryFile(dir='/tmp/') as fp:
        fp.write(res.content)
        fp.file.seek(0)
        img = Image.open(fp.name)
    return img

try:
    while True:

        dt_mm  = str(datetime.datetime.now().strftime('%M'))

        if 'poke_class' in locals():
            pokemon_path = pokemon_path_org + '/' + poke_class
        else:
            if dt_mm == '00' or dt_mm == '30':
                pokemon_path = pokemon_path_org + '/legend'
            else:
                pokemon_path = pokemon_path_org + '/normal'

        # Running Eevee
        poke_list = sorted(Path(pokemon_path).glob('*')) 
        if 'poke_debug' in locals():
            poke_num = poke_debug
        else:
            poke_num = random.randint(0,len(poke_list)-1)
        poke_image = sorted(Path(poke_list[poke_num]).glob('*.*'))
        poke_range = 64 // len(poke_image)
        if poke_range == 0:
            poke_range = 1

        unicornhathd.rotation(90)
        for i in range(poke_range):
            for path in poke_image:
                img = Image.open(path)

                for o_x in range(int(img.size[0] / 16)):
                    for o_y in range(int(img.size[1] / 16)):

                        valid = False
                        for x in range(16):
                            for y in range(16):
                                pixel = img.getpixel(((o_x * 16) + y, (o_y * 16) + x))
                                r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                                if r or g or b:
                                    valid = True
                                unicornhathd.set_pixel(x, y, r, g, b)

                        if valid:
                            unicornhathd.show()
                            if len(poke_image) > 200:
                                time.sleep(0.025)
                            elif len(poke_image) > 100:
                                time.sleep(0.05)
                            else:
                                time.sleep(0.1)

        # Show Datatime
        unicornhathd.rotation(0)
        text_width = 0
        dt_now = datetime.datetime.now()
        dt_fmt = dt_now.strftime('%m/%d(%a) %H:%M')

        lines = [dt_fmt]
        colours = [(255,200,200)] 

        for line in lines:
            w, h = font.getsize(line)
            text_width += w + width
            text_height = max(text_height, h)

        text_width += width + text_x + 1

        image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        offset_left = 0

        for index, line in enumerate(lines):
            draw.text((text_x + offset_left, text_y), line, colours[index], font=font)

            offset_left += font.getsize(line)[0] + width


        for scroll in range(text_width - width):
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel((x + scroll, y))
                    r, g, b = [int(n) for n in pixel]
                    unicornhathd.set_pixel(width - 1 - x, y, r, g, b)

            unicornhathd.show()
            time.sleep(0.01)

        # Weather Information
        r = requests.get(url)
        wdata = json.loads(r.text)
        weather=wdata["weather"][0]["icon"]
        weather_icon="http://openweathermap.org/img/wn/" + weather + ".png"

        temp_now=str(round(k2c(wdata["main"]["temp"])))
        temp_min=str(round(k2c(wdata["main"]["temp_min"])))
        temp_max=str(round(k2c(wdata["main"]["temp_max"])))
        humidity=str(round(wdata["main"]["humidity"]))
        temperture="T:" + temp_now + "°C RH:" + humidity + "%"

        raw_img = imread_web(weather_icon)
        raw_img = raw_img.resize((16, 16), Image.LANCZOS)
        unicornhathd.rotation(90)

        # Show Weather Icon
        for i in range(4):

            valid = False
            for x in range(16):
                for y in range(16):
                    pixel = raw_img.getpixel(((o_x * 16) + y, (o_y * 16) + x))
                    r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                    if r or g or b:
                        valid = True
                    unicornhathd.set_pixel(x, y, r, g, b)

            if valid:
                unicornhathd.show()
                time.sleep(0.6)
                unicornhathd.off()
                time.sleep(0.4)

        # Show Temperture and Humidity
        unicornhathd.rotation(0)
        lines = [temperture]
        colours = [(255,200,200)]
        text_width = 0

        for line in lines:
            w, h = font.getsize(line)
            text_width += w + width
            text_height = max(text_height, h)

        text_width += width + text_x + 1

        image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        offset_left = 0

        for index, line in enumerate(lines):
            draw.text((text_x + offset_left, text_y), line, colours[index], font=font)

            offset_left += font.getsize(line)[0] + width

        for scroll in range(text_width - width):
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel((x + scroll, y))
                    r, g, b = [int(n) for n in pixel]
                    unicornhathd.set_pixel(width - 1 - x, y, r, g, b)

            unicornhathd.show()
            time.sleep(0.01)

except KeyboardInterrupt:
    unicornhathd.off()

finally:
    unicornhathd.off()
