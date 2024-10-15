import os
import re
import cv2
import numpy as np
import voxypy
from voxypy.models import Vox, Color, VoxWriter


def images_to_vox(directory_path, output_file_path, regex_pattern):
    filenames = [f for f in os.listdir(directory_path) if re.match(regex_pattern, f)]
    filenames.sort()

    images = []

    for filename in filenames:
        image_path = os.path.join(directory_path, filename)
        image = cv2.imread(image_path)
        images.append(image)

    image_stack = np.stack(images, axis=-1, dtype=int)

    # vox = Vox.from_dense(image_stack, [])
    # model = VoxWriter(output_file_path, vox)
    # model.write()