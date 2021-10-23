import time
import win32api
import win32con
import pyautogui

def type_message(message):
    pyautogui.typewrite(message)

def right_click(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,int(x), int(y), 0, 0)
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,int(x), int(y), 0, 0)
    time.sleep(0.02)

def move_mouse(x, y):
    win32api.SetCursorPos((x, y))

def left_click(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,int(x), int(y), 0, 0)
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,int(x), int(y), 0, 0)
    time.sleep(0.01)

def key_up(hwnd, code):
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, code, 0)

def key_down(hwnd, code):
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, code, 0)

def press_key(hwnd, code):
    key_down(hwnd, code)
    time.sleep(0.01)
    key_up(hwnd, code)