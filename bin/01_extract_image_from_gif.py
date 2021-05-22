import sys
from pathlib import Path
from PIL import Image, ImageSequence

gif_path  = sys.argv[1]  #'./booster.gif'
dest_path = sys.argv[2]  #'./'

DEBUG_MODE = True

def get_frames(path):
    im = Image.open(path)
    return (frame.copy() for frame in ImageSequence.Iterator(im))

def write_frames(frames, name_original, dest_path):
    path = Path(name_original)

    stem = path.stem
    #extension = path.suffix
    extension = '.png'
    dest_path = dest_path + stem

    dir_dest = Path(dest_path)
    if not dir_dest.is_dir():
        dir_dest.mkdir(0o700)
        if DEBUG_MODE:
            print('Destionation directory is created: "{}".'.format(dest_path))

    for i, f in enumerate(frames):
        name = '{}/{}-{}{}'.format(dest_path, stem, str(i + 1).zfill(2), extension)
        f.save(name)
        if DEBUG_MODE:
            print('A frame is saved as "{}".'.format(name))


frames = get_frames(gif_path)
write_frames(frames, gif_path, dest_path)

exit()
