import numpy as np
from PIL import Image
import sys

if __name__ == "__main__":
    np.set_printoptions(threshold=np.inf)
    IMG_PATH = sys.argv[1]
    img = Image.open(IMG_PATH)
    arr = np.array(img)
    print(np.unique(arr))
    