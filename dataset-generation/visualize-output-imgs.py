import torch
from torchvision import transforms
import sys
from PIL import Image
import tensorflow as tf
import numpy as np
from torchvision import transforms

if len(sys.argv) != 4:
    print("USAGE: python3 visualize-output-tensor.py tensor-imgs.pt path/to/img/outputs path/to/mask/outputs")
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

imgs, masks = torch.load(sys.argv[1], map_location=torch.device('cpu'))

np_masks = []

i = 0

for item in imgs:
    print(item.shape)
    img = transforms.ToPILImage()(item).convert("RGB")

    out_dir = sys.argv[2]
    img.save(f"{out_dir}/{i}.png")
    i += 1

for mask in masks:
    mask_arr = mask.numpy().astype(np.uint8)
    np_masks.append(mask_arr)

i = 0

for mask in np_masks:
    img = transforms.ToPILImage(mode="L")(mask)
    img.putpalette(PALETTE)

    out_dir = sys.argv[3]
    img.save(f"{out_dir}/{i}.png")
    i += 1
