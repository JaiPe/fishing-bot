from os import listdir
from os.path import join
from common.color import no_alpha
import cv2
import numpy as np

def read_imgs_from_path(path):
    return map(
            lambda p: (map(int, p.split('.')[0].split('-')), no_alpha(cv2.imread(join(path, p)))),
            list(filter(lambda image_path: '-base-' not in image_path, listdir(path)))
        )
        
def get_samples(root = 'new_samples'):
    samples = []
    base_image_samples = {}

    for (filename_parts, image) in read_imgs_from_path(root):
        (id, x, y, w, h) = filename_parts

        if not id in base_image_samples:
            base_1 = no_alpha(cv2.imread(join(root, f'{id}-base-1.png')))
            base_2 = no_alpha(cv2.imread(join(root, f'{id}-base-2.png')))
            base_3 = no_alpha(cv2.imread(join(root, f'{id}-base-3.png')))

            base_image_samples[id] = (base_1, base_2, base_3)

        samples.append({ 'filename': f'{id}-{x}-{y}-{w}-{h}', 'bounds': (x, y, w, h), 'image': image, 'base_images': base_image_samples[id] })
    return samples
