from window.position import bring_to_front
from common.screenshot import screenshot

import time
import cv2

def request_fish_bounds(hwnd, screen = []):
    bring_to_front(hwnd)

    screen = screen if len(screen) > 0 else screenshot(hwnd)

    roi = cv2.selectROI(screenshot(hwnd))
    cv2.destroyAllWindows()

    return None if len(list(filter(lambda value: value == 0, roi))) == 4 else roi