import cv2
import numpy as np

def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def to_gray_from_hsv(img):
    return to_gray(cv2.cvtColor(img, cv2.COLOR_HSV2BGR))

def get_threshold(image):
    return cv2.minMaxLoc(to_gray(image))[1]

def to_hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def to_bgr_from_hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

def num_pixels_in_range(img, from_thresh, to_thresh):
    return __in_range(img, from_thresh, to_thresh).sum()

def no_alpha(img):
    if img.shape[2] == 4:
        trans_mask = img[:,:,3] == 0

        img[trans_mask] = [255, 255, 255, 255]
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img

def in_range(img, from_thresh, to_thresh):
    return __in_range(img, from_thresh, to_thresh)

def to_bgr_from_rgb(rgb):
    return (rgb[2], rgb[1], rgb[0])

def __in_range(img, from_thresh, to_thresh):
    return cv2.inRange(img, to_bgr_from_rgb(from_thresh), to_bgr_from_rgb(to_thresh))

def increase_brightness(img, value = 4):
    img = to_hsv(img)
    img[:,:,2] += min(255, value)
    return to_bgr_from_hsv(img)

def count_pixels_mte_threshold(img, threshold):
    return np.sum(img >= threshold)