from common.mouse_keyboard import press_key
import time
from common.mouse_keyboard import left_click, move_mouse, key_down, key_up

def logout(hwnd):
    press_key(hwnd, 27)
    time.sleep(0.01)
    left_click(360, 360)
