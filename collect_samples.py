from debug.collect_single_sample import collect_single_sample
import time
from window.toggle_ui import open_ui
from common.mouse_keyboard import press_key
from common.screenshot import screenshot
from window.position import bring_to_front, move_window
from window.find import find_window

def collect():
    hwnd = find_window('World of Warcraft')
    if not hwnd:
        raise ValueError("Could not find window")
    
    bring_to_front(hwnd)
    open_ui(hwnd)
    move_window(hwnd, (0, 0, 1626, 919))

    screen_original = None
    is_casting = False

    sample_1 = screenshot(hwnd)
    time.sleep(0.05)
    sample_2 = screenshot(hwnd)
    time.sleep(0.05)
    sample_3 = screenshot(hwnd)

    def cast():
        press_key(hwnd, 49)
        time.sleep(3)
        return screenshot(hwnd)

    count = 1
    while count < 3:
        if is_casting == False:
            screen_original = cast()
            is_casting = True
        
        if collect_single_sample(hwnd, screen_original, (sample_1, sample_2, sample_3)) == True:
            count += 1
        else:
            raise Exception('Cancelled')
