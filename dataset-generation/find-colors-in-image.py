import numpy as np
from PIL import Image
import sys

def find_colors(img_path):
    s = set()
    img = Image.open(img_path)
    arr = np.array(img)
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            s.add((arr[x,y][0], arr[x,y][1], arr[x,y][2]))
    print(s)

if __name__ == "__main__":
    np.set_printoptions(threshold=np.inf)
    IMG_PATH = sys.argv[1]
    find_colors(IMG_PATH)