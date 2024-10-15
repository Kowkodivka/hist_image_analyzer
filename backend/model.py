import cv2
import numpy as np


def images_to_vox(images):
    image_stack = np.stack(images, axis=-1, dtype=int)
    return image_stack