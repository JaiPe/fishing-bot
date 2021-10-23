import win32gui

def find_window(window_title, window_class = 'GxWindowClass'):
    return win32gui.FindWindow(window_class, window_title)
