import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import cv2

file_path   = sys.argv[1]  #'./booster'

if len(sys.argv) < 6:
    en_color     = 1.0
    en_contrast  = 1.0
    en_sharpness = 1.0
    en_dilation  = 0
else:
    en_color     = float(sys.argv[2])
    en_contrast  = float(sys.argv[3])
    en_sharpness = float(sys.argv[4])
    en_dilation  = int(sys.argv[5])

file_list = sorted(Path(file_path).glob('*.png')) 
for file in file_list:
    im = Image.open(str(file))

    # Enhance Color
    enhancer = ImageEnhance.Color(im)  
    im = enhancer.enhance(en_color)

    # Contrast
    enhancer = ImageEnhance.Contrast(im)  
    im = enhancer.enhance(en_contrast)

    # Sharpness
    enhancer = ImageEnhance.Sharpness(im)  
    im = enhancer.enhance(en_sharpness)

    # Dilation / Erosion
    if en_dilation == 1:
        im = im.filter(ImageFilter.MinFilter())
    elif en_dilation == 2:
        im = im.filter(ImageFilter.MaxFilter())

    raw_img = im.resize((16, 16), Image.LANCZOS)
    raw_img.save(str(file))

exit()

