import numpy as np
from PIL import Image
import sys

def img_to_array(img_path):
    img = Image.open(img_path)
    arr = np.array(img)
    print(arr.shape)
    print(np.unique(arr))

if __name__ == "__main__":
    np.set_printoptions(threshold=np.inf)
    IMG_PATH = sys.argv[1]
    img_to_array(IMG_PATH)