from core.image_processor import process
import cv2
import time
from core.find_contours import find_contours
from window.position import bring_to_front
from common.mouse_keyboard import left_click, press_key
from common.screenshot import screenshot
from common.crop import crop_bounds

def cast(hwnd, *pre_cast_screens, **options):
    max_match_contours = options['max_match_contours']
    max_match_radius = options['max_match_radius']
    screen_bounds = options['screen_bounds']
    min_match_radius = options['min_match_radius']
    bring_to_front(hwnd)
    press_key(hwnd, 49)
    time.sleep(2)
    image = screenshot(hwnd)
    pre_cast_screens = list(map(lambda img: crop_bounds(img, screen_bounds), pre_cast_screens))

    accepted_contours, _ = find_contours(process(image, screen_bounds, *pre_cast_screens)[0], screen_bounds, max_match_radius=max_match_radius,
                             min_match_radius=min_match_radius)
    num_accepted_contours = len(accepted_contours)

    if num_accepted_contours == 0 or num_accepted_contours > max_match_contours:
        print(f'{num_accepted_contours} contours found (max {max_match_contours})')
        return image, []

    return image, accepted_contours
