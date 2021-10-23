import win32gui
import numpy as np
import cv2
import win32ui
from common.color import get_threshold

def find_cursor(**options):
    dtype = options['dtype'] if 'dtype' in options else None

    info = win32gui.GetCursorInfo()

    if info[1] == 0:
        return None

    gdc = win32gui.GetDC(0)
    bm = win32gui.GetObject(win32gui.GetIconInfo(info[1])[3])
    hdc = win32ui.CreateDCFromHandle(gdc)
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, bm.bmWidth, bm.bmHeight)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), info[1])
    img_ascii = hbmp.GetBitmapBits(True)
    img = None
    if dtype != 'string':
        img = np.fromstring(img_ascii, dtype='uint8')
        img.shape = (bm.bmWidth, bm.bmHeight, 4)
        img = img[:31, :31]
        img.shape = (31, 31, 4)

    win32gui.DeleteObject(hbmp.GetHandle())
    win32gui.ReleaseDC(0, gdc)
    hdc.DeleteDC()

    if dtype == 'threshold':
            return get_threshold(img)
    if dtype == 'string':
        return img_ascii

    return img