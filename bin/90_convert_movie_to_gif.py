import math
import sys
import cv2
from PIL import Image


def get_fps_n_count(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return (None, None)

    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = round(cap.get(cv2.CAP_PROP_FPS))

    cap.release()
    cv2.destroyAllWindows()
    return (fps, count)


def aspect_ratio(width, height):
    gcd = math.gcd(width, height)
    ratio_w = width // gcd
    ratio_h = height // gcd
    return (ratio_w, ratio_h)


def resize_based_on_aspect_ratio(aspect_ratio, base_width, max_width=400):
    if base_width < max_width:
        return None

    base = max_width / aspect_ratio[0]
    new_w = int(base * aspect_ratio[0])
    new_h = int(base * aspect_ratio[1])
    return (new_w, new_h)


def get_frame_range(video_path, start_frame, stop_frame, step_frame):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    asp = aspect_ratio(width, height)
    width_height = resize_based_on_aspect_ratio(asp, width, max_width=400)

    im_list = []
    for n in range(start_frame, stop_frame, step_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        if ret:
            if width_height is not None:
                frame = cv2.resize(frame, dsize=width_height)
            img_array = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(img_array)
            im_list.append(im)

    cap.release()
    cv2.destroyAllWindows()
    return im_list


def make_gif(filename, im_list):
    im_list[0].save(filename, save_all=True, append_images=im_list[1:], loop=0)


def main(target_file):
    video_file = target_file

    fps, count = get_fps_n_count(video_file)
    if fps is None:
        print("Cannot open the video file.")
        return

    start_sec = 0
    stop_sec = 8

    start_frame = int(start_sec * fps)
    stop_frame = int(stop_sec * fps)
    step_frame = 3

    print("Convert Start")
    im_list = get_frame_range(video_file, start_frame, stop_frame, step_frame)
    if im_list is None:
        print("Cannot open the video file.")
        return

    make_gif('test.gif', im_list)
    print("end")


if __name__ == "__main__":
    main(sys.argv[1])


