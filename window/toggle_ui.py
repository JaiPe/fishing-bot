import time
from common.color import num_pixels_in_range
from common.screenshot import crop_region, screenshot
from common.mouse_keyboard import key_down, key_up, press_key

def close_ui(hwnd, screen = []):
    if __is_ui_open(hwnd, screen):
        __toggle_ui(hwnd)
        time.sleep(2.5)
        return True

def open_ui(hwnd, screen = []):
    if not __is_ui_open(hwnd, screen):
        __toggle_ui(hwnd)
        time.sleep(0.001)
        return True

def __is_ui_open(hwnd, screen = []):
    region = (-50, 0, 50, 50)
    screen = crop_region(screen, region) if len(screen) > 0 else screenshot(hwnd, region)

    return num_pixels_in_range(
        screen,
        (199, 170, 8),
        (200, 171, 9)
    ) > 1

def __toggle_ui(hwnd):
    key_down(hwnd, 18)
    press_key(hwnd, 90)
    key_up(hwnd, 18)