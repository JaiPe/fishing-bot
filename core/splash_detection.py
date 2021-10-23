from common.color import to_gray, count_pixels_mte_threshold, get_threshold
from common.screenshot import screenshot
from common.crop import crop_bounds

def is_splash_detected(hwnd, bobber_bounds, **options):
    min_white_count = options['min_white_count']
    min_white_threshold = options['min_white_threshold']
    img = screenshot(hwnd, bobber_bounds)
    current_white_count = count_pixels_mte_threshold(img, min_white_threshold)
    return current_white_count >= min_white_count, current_white_count  - min_white_count, current_white_count

def get_white_threshold(cropped_screens):
    return max(list(map(lambda img: get_threshold(img), cropped_screens)))
