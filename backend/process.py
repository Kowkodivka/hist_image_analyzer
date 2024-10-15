import cv2
import numpy as np


def resize_image(image, max_width, max_height):
    return cv2.resize(image, (max_width, max_height), interpolation=cv2.INTER_AREA)


def remove_background(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    contours = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if not contours:
        return None
    
    contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(contour)
    result = image[y:y+h, x:x+w]

    b_channel, g_channel, r_channel = cv2.split(result)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    alpha_channel[morphed[y:y+h, x:x+w] == 0] = 0

    result = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    return result


def process_images(images):
    max_width = 0
    max_height = 0
    cropped_images = []
    result = []

    for image in images:
        image_bg_rmd = remove_background(image)
        
        if image_bg_rmd is not None:
            h, w = image_bg_rmd.shape[:2]
            max_width = max(max_width, w)
            max_height = max(max_height, h)
            cropped_images.append(image_bg_rmd)
    
    for image_bg_rmd in cropped_images:
        resized_image = resize_image(image_bg_rmd, max_width, max_height)
        result.append(resized_image)

    return result