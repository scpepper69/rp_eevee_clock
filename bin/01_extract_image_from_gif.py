import sys
from pathlib import Path
from PIL import Image, ImageSequence

IMAGE_PATH  = sys.argv[1]  #'./booster.gif'
DESTINATION = sys.argv[2]  #'./'

DEBUG_MODE = True

def get_frames(path):
    im = Image.open(path)
    return (frame.copy() for frame in ImageSequence.Iterator(im))

def write_frames(frames, name_original, destination):
    path = Path(name_original)

    stem = path.stem
    #extension = path.suffix
    extension = '.png'
    destination = destination + stem

    dir_dest = Path(destination)
    if not dir_dest.is_dir():
        dir_dest.mkdir(0o700)
        if DEBUG_MODE:
            print('Destionation directory is created: "{}".'.format(destination))

    for i, f in enumerate(frames):
        name = '{}/{}-{}{}'.format(destination, stem, str(i + 1).zfill(2), extension)
        f.save(name)
        if DEBUG_MODE:
            print('A frame is saved as "{}".'.format(name))


frames = get_frames(IMAGE_PATH)
write_frames(frames, IMAGE_PATH, DESTINATION)

exit()
