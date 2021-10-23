from common.mouse_keyboard import press_key, type_message
import time

def apply_lure(hwnd):
    press_key(hwnd, 13)
    time.sleep(0.01)
    type_message('/use Bright Baubles')
    press_key(hwnd, 13)
    time.sleep(0.01)
    press_key(hwnd, 13)
    type_message('/use 16')
    time.sleep(0.01)
    press_key(hwnd, 13)
    time.sleep(7)
