import time
import win32gui

def move_window(hwnd, position = (0, 0, 1604, 863)):
    if position != win32gui.GetClientRect(hwnd):
        win32gui.SetWindowPos(hwnd, hwnd, *position, 0x0004)
        # Give time for window resize transition
        time.sleep(2)
    else:
        print("Window already correct size")

def bring_to_front(hwnd):
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.02)
