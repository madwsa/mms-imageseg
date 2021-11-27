import numpy as np
from PIL import Image
import sys
from os import listdir
from os.path import isfile, join
from datetime import datetime

from numpy.core.numeric import zeros_like
from numpy.lib.twodim_base import mask_indices

from tqdm import tqdm

LABEL_COLORS = np.array([
    [0,0,0], #Black
    [255,0,0], #Solar Panels
    [0,255,0], #Drive Shaft
    [0,0,255], #Parabolic Antenna
    [255,255,0], #Satellite Dish
    [255,0,255], #Main Module
    [0,255,255], #Telescope
    [255,128,128], #Main Thrusters
    [255,204,77], #Rotational Thrusters
    [128,255,255], #Sensors
    [64,128,192] #Launch Vehicle Adapter
])

NEW_LABELS = [
    (13,13,13),
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (255,255,0),
    (255,0,255),
    (0,255,255),
    (255,128,128),
    (255,204,77),
    (128,255,255),
    (64,128,191)
]

PALETTE = [
    0,0,0, #Black
    255,0,0, #Solar Panels
    0,255,0, #Drive Shaft
    0,0,255, #Parabolic Antenna
    255,255,0, #Satellite Dish
    255,0,255, #Main Module
    0,255,255, #Telescope
    255,128,128, #Main Thrusters
    255,204,77, #Rotational Thrusters
    128,255,255, #Sensors
    64,128,192 
]
# Pad with zeroes to 768 values, i.e. 256 RGB colours
PALETTE = PALETTE + [0]*(768-len(PALETTE))

def closest(color, label_colors):
    """Find the closest color.
    
    color : np.array of shape (3)
        color in question to be matched
    label_colors : np.array of shape (n, 3) 
        n is the number of colors to choose from.

    Returns an np.array of shape (3) with the closest color, and an index into the label_colors array (used for classing)

    Source: https://stackoverflow.com/questions/54242194/python-find-the-closest-color-to-a-color-from-giving-list-of-colors
    """

    distances = np.sqrt(np.sum((label_colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = label_colors[index_of_smallest]
    return smallest_distance[0], index_of_smallest[0]

def process_image(img_path, output_dir, labels):
    """Standardize colors in images and make all nearly-black into black.

    img_path : path to the img in question
    label_colors : np.array of shape (n, 3) 
        n is the number of colors to choose from.
    epsilon : float
        the percent "error" representing how far away from black a given RGB value can be. 

    Sources: 
    - https://stackoverflow.com/questions/138250/how-to-read-the-rgb-value-of-a-given-pixel-in-python
    - https://scikit-image.org/docs/dev/user_guide/numpy_images.html
    """

    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)


    # TEST CODE
    # img = np.full((6, 8, 3), np.array((2,5,7)))
    # arr = np.array(img)

    # arr[2,2] = np.array((208,0,0))

    # arr[4,4] = np.array((0,208,208))

    # END TEST CODE

    i = 0
    grayscale_array = np.zeros((600, 800), dtype=np.uint8)

    for color in labels:
        mask = arr[:, :, :] == np.array(color)
        grayscale_array[np.all(mask, axis=-1)] = i
        i += 1

    grayscale_img = Image.fromarray(grayscale_array, 'L')

    file_part = img_path.split("/")[-1]
    new_filename = f"{output_dir}/no_palette_{file_part}"
    grayscale_img.save(new_filename)

def enumerate_images(input_dir):
    """Get a path to all files in the specified dir.

    input_dir : string
        input path to the directory with the image files
    """
    return [join(input_dir, f) for f in listdir(input_dir) if isfile(join(input_dir, f))]

def get_new_labels(in_file):
    colors = []
    with open(in_file, "r") as color_file:
        for line in color_file:
            s = line.strip().split(",")
            colors.append((int(s[0]), int(s[1]), int(s[2])))

    return colors


if __name__ == "__main__":
    IMG_DIR = sys.argv[1]
    OUTPUT_DIR = sys.argv[2]
    input_imgs = enumerate_images(IMG_DIR)
    labels = NEW_LABELS
    if len(sys.argv) == 4:
        labels = get_new_labels(sys.argv[3])
    print(labels)
    for img in tqdm(input_imgs):
        process_image(img, OUTPUT_DIR, labels)