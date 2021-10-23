import numpy as np
import cv2
from common.transforms import merge, similarity, morph_close, blur, gaussian_blur, erode, to_gray, adaptive_threshold, dilate
from common.crop import crop_bounds

def process(img, screen_bounds, *base_images):
    bounds_mask = np.zeros(img.shape[:2], dtype=np.uint8)
    base_images_merged = base_images[0]#merge(
    #    base_images
    #)
    img = crop_bounds(img, screen_bounds)
    diff = similarity((to_gray(erode(blur(base_images_merged)))), (to_gray(erode(blur(img)))))
    diff = adaptive_threshold(dilate(gaussian_blur(diff)))
    (x, y, w, h) = screen_bounds
    bounds_mask[y: y+h, x: x+w] = diff

    return (bounds_mask, base_images_merged)
