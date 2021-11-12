import numpy as np
from PIL import Image
import sys
from os import listdir
from os.path import isfile, join

LABEL_COLORS = np.array([
    [255,0,0], #Solar Panels
    [0,255,0], #Drive Shaft
    [0,0,255], #Parabolic Antenna
    [255,255,0], #Satellite Dish
    [255,0,255], #Main Module
    [0,255,255], #Telescope
    [255,128,128], #Main Thrusters
    [255,204,77], #Rotational Thrusters
    [128,255,255], #Sensors
    [64,128,192], #Launch Vehicle Adapter
    [0,0,0] #Black
])

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

def filter_black(pixel, epsilon):
    """Convert an almost black pixel to black.

    pixel : np.array of shape (3)
    epsilon : float
        the percent "error" representing how far away from black a given RGB value can be.

    Returns the (pixel, True) if the pixel is now true black, (pixel, False) otherwise

    This operates on each channel separately.

    """

    comp = pixel - epsilon

    if comp[0] > 0 or comp[1] > 0 or comp[2] > 0:
        return (pixel, False)
    else:
        return (np.array([0,0,0]), True)

def process_image(img_path, output_dir, label_colors, epsilon = np.array([25,25,25])):
    """Standardize colors in images and make all nearly-black into black.

    img_path : path to the img in question
    label_colors : np.array of shape (n, 3) 
        n is the number of colors to choose from.
    epsilon : float
        the percent "error" representing how far away from black a given RGB value can be. 

    Source: https://stackoverflow.com/questions/138250/how-to-read-the-rgb-value-of-a-given-pixel-in-python

    """

    new_image = Image.new('RGB', (800, 600))

    with Image.open(img_path) as img:
        pix = img.load()
        if img.mode != 'RGB':
            print("Image Mode not RGB.")
            sys.exit(1)
        width, height = img.size
        if width != 800 or height != 600:
            print(f"Image Dimensions incorrect. Width was {width} and Height was {height}.")
        grayscale_array = np.zeros((height, width), dtype=np.uint8)
        for x in range(0,width):
            for y in range(0,height):
                pixel = np.array(pix[x,y])
                closest_color,label_color_index = closest(pixel, label_colors)
                grayscale_array[y,x] = label_color_index

    grayscale_img = Image.fromarray(grayscale_array)

    file_part = img_path.split("/")[-1]
    new_filename = f"{output_dir}/{file_part}"
    grayscale_img.save(new_filename)

def enumerate_images(input_dir):
    """Get a path to all files in the specified dir.

    input_dir : string
        input path to the directory with the image files
    """
    return [join(input_dir, f) for f in listdir(input_dir) if isfile(join(input_dir, f))]


if __name__ == "__main__":
    IMG_DIR = sys.argv[1]
    OUTPUT_DIR = sys.argv[2]
    input_imgs = enumerate_images(IMG_DIR)
    epsilon_float_val = float(sys.argv[3])

    EPSILON = np.array([epsilon_float_val, epsilon_float_val, epsilon_float_val])
    for img in input_imgs:
        process_image(img, OUTPUT_DIR, LABEL_COLORS, EPSILON)