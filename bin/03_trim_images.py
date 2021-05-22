import sys
from pathlib import Path
from PIL import Image
import cv2

file_path   = sys.argv[1]  #'./booster'
trim_top    = int(sys.argv[2])
trim_bottom = int(sys.argv[3])
trim_left   = int(sys.argv[4])
trim_right  = int(sys.argv[5])

file_list = sorted(Path(file_path).glob('*.png')) 
for file in file_list:

    img = cv2.imread(str(file))
    img.shape
    # img[top : bottom, left : right]
    #img1 = img[20 : 240, 10: 230]
    img1 = img[trim_top : trim_bottom, trim_left: trim_right]
    cv2.imwrite(str(file), img1)

exit()

