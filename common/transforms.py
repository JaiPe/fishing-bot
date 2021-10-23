import cv2
import numpy as np
from skimage.metrics import structural_similarity
from common.color import to_gray

def similarity(img1, img2):
    return (structural_similarity(img1, img2, full=True)[1] * 255).astype("uint8")

def adjust_brightness(image, clip_hist_percent=25):
    gray = to_gray(image) if image.shape and len(image.shape) > 2 and image.shape[2] > 1 else image
    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return auto_result

def remove_isolated_pixels(image):
    connectivity = 8

    output = cv2.connectedComponentsWithStats(image, connectivity, cv2.CV_32S)

    num_stats = output[0]
    labels = output[1]
    stats = output[2]

    new_image = image.copy()

    for label in range(num_stats):
        if stats[label,cv2.CC_STAT_AREA] == 1:
            new_image[labels == label] = 0

    return new_image

def sobel(img, amount = 3):
    return cv2.Sobel(img, cv2.CV_8UC1, 0, 1, ksize=amount)

def adaptive_threshold(img, color_to = 255):
    return cv2.adaptiveThreshold(img, color_to, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)

def threshold(img, color_from, color_to = 255):
    return cv2.threshold(img, color_from, color_to, cv2.THRESH_BINARY)[1]

def morph_close(img, amount = 10):
    kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (amount, amount))
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

def morph_open(img, amount = 4):
    kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (amount, amount))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def blur(img, amount = 3):
    return cv2.medianBlur(img, amount)

def gaussian_blur(img, amount = 7):
    return cv2.GaussianBlur(img, (amount, amount), 2)

def dilate(img, amount = 11):
    kernel = np.ones((amount, amount), np.uint8)
    return cv2.dilate(img, kernel)

def erode(img, amount = 18):
    kernel = np.ones((amount, amount), np.uint8)
    return cv2.erode(img, kernel)

def merge(imgs):
    final = imgs[0]
    for i, img in enumerate(imgs):
        if i == 0:
            continue
        final = cv2.addWeighted(final, 1, img, 1, 0.9)

    return final
