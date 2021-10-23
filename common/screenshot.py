import time
import win32gui
import pyautogui
import numpy as np
import win32ui
import cv2
import mss
import mss.tools

def __screenshot(hwnd, region):
    with mss.mss() as sct:
        x, y = win32gui.ClientToScreen(hwnd, (region[0], region[1]))
        # The screen part to capture
        region = {'top': y, 'left': x, 'width': region[2], 'height': region[3]}

        # Grab the data
        sct_img = np.array(sct.grab(region))
        return sct_img[:, :, :3]

# Save to the picture file
#mss.tools.to_png(img.rgb, img.size, output='dummy.png')


#return pyautogui.screenshot(region=(x, y, region[2], region[3]))

def screenshot(hwnd, region = None):
    x1, y1, x2, y2 = win32gui.GetClientRect(hwnd)

    if region == None:
        w = x2 - x1
        h =  y2 - y1
        region = (x1, y1, w, h)
    else:
        # Allow for - values coming from the right
        if region[0] < 0:
            region = (x2 + region[0], y1, region[2], region[3])
        if region[1] < 0:
            region = (x1, y2 + region[1], region[2], region[3])

    return __screenshot(hwnd, region)

def screen_sample(hwnd, pos):
    return __screenshot(hwnd, (pos[0], pos[1], 1, 1)).getpixel((0, 0))

def screenshot_sequence(hwnd, **options):
    region = options['region'] if 'region' in options else None
    frame_rate = options['frame_rate'] if 'frame_rate' in options else 1/12
    num_captures = options['num_captures'] if 'num_captures' in options else 10

    screens = []

    for i in range(num_captures):
        screens.append(screenshot(hwnd, region))
        time.sleep(frame_rate)
    
    return screens

def crop_region(img_or_imgs, region):
    if type(img_or_imgs) == list:
        return list(map(lambda img: __crop_region(img, region), img_or_imgs))
    return __crop_region(img_or_imgs, region)

def __crop_region(img, region):
    (x, y, w, h) = region
    return img[y: y+h, x: x+w]
