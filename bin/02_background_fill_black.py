import sys
import cv2
import numpy as np
from IPython.display import Image, display
from matplotlib import pyplot as plt
from pathlib import Path

file_path = sys.argv[1]  #'./booster'
file_list = sorted(Path(file_path).glob('*.png')) 

for file in file_list:
    print(file)
    img = cv2.imread(str(file))

    h, w = img.shape[:2]
    mask = np.zeros((h + 2, w + 2), dtype=np.uint8)

    # Fill Black
    retval, img, mask, rect = cv2.floodFill(
        img,
        mask,
        seedPoint=(0, 0),
        newVal=(0, 0, 0),
        loDiff=(20, 20, 20),
        upDiff=(20, 20, 20),
        flags=4 | 255 << 8,
    )
    #print("retval", retval)  # retval 6339
    #print("rect", rect)  # rect (49, 42, 90, 90)
    #plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #plt.show()

    cv2.imwrite(str(file), img)

exit()

