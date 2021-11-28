import numpy as np
from PIL import Image
import sys
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

PIXELS_PER_IMAGE = 600*800

def count_image_pixels(img_path, counts, total_pixels):
    img = Image.open(img_path)
    arr = np.array(img)

    #Uses int64 by default - no worries about int overflows.
    count_arr = np.bincount(arr.ravel(), minlength=11)
    total_pixels += PIXELS_PER_IMAGE
    out = np.add(count_arr, counts)
    return out, total_pixels

def enumerate_images(input_dir):
    """Get a path to all files in the specified dir.

    input_dir : string
        input path to the directory with the image files
    """
    return [join(input_dir, f) for f in listdir(input_dir) if isfile(join(input_dir, f))]

if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    IMG_DIRS = sys.argv[1:]
    TOTAL_PIXELS = 0
    COUNTS = np.bincount([], minlength=11)

    input_imgs = []

    for dir in IMG_DIRS:
        input_imgs += enumerate_images(dir)

    for img_path in tqdm(input_imgs):
        COUNTS, TOTAL_PIXELS = count_image_pixels(img_path, COUNTS, TOTAL_PIXELS)
        COUNTS, TOTAL_PIXELS = count_image_pixels(img_path, COUNTS, TOTAL_PIXELS)
    
    out = np.multiply(np.divide(COUNTS, np.full((11), TOTAL_PIXELS)), 100)
    print(out)