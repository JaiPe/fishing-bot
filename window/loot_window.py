import cv2
from common.screenshot import screenshot
from common.color import num_pixels_in_range
from common.crop import crop_bounds

def is_loot_window_open(hwnd, image = None):
    return num_pixels_in_range(
        crop_bounds(image, (184, 133, 21, 21)) if len(image) > 0 else screenshot(hwnd, (184, 133, 21, 21)),
        (199, 170, 8),
        (200, 171, 9)
    ) > 1