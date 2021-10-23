import cv2
from os import remove
import glob

def write_tmp(img, name = 'temp.png'):
    cv2.imwrite(f'./.tmp/{name}', img)

def empty(dir):
    for f in glob.glob(dir):
        remove(f)