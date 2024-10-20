import cv2
import numpy as np
import json
import re
import os
from process import process_images


def images_to_vox_json(images, output_file="voxel_data.json"):
    voxels = []
    for z, image in enumerate(images):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        non_zero_indices = np.where(gray != 0)
        x_indices, y_indices = non_zero_indices

        for i in range(len(x_indices)):
            x = int(x_indices[i])
            y = int(y_indices[i])
            if 0 <= x < image.shape[1]:
                r, g, b = map(int, image[y, x])
                voxels.append([x, y, z, [r, g, b]])

    voxel_data = {
        "voxels": voxels,
        "data": {}
    }

    with open(output_file, "w") as f:
        json.dump(voxel_data, f)