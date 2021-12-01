import torch
from torchvision import transforms
import sys
from PIL import Image
import tensorflow as tf
import numpy as np

if len(sys.argv) != 3:
    print("USAGE: python3 visualize-output-tensor.py input-predictions.pt path/to/output-dir/")
    exit(1)

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

t = torch.load(sys.argv[1], map_location=torch.device('cpu'))
#im = transforms.ToPILImage()(t).convert("RGB")

np.set_printoptions(threshold=np.inf)
arr = t.numpy().astype(np.uint8)
print("Unique classes in all masks:")
print(np.unique(arr))

for i in range(arr.shape[0]):
    img = Image.fromarray(arr[i], 'P')
    img.putpalette(PALETTE)

    out_dir = sys.argv[2]
    img.save(f"{out_dir}/{i}.png")

