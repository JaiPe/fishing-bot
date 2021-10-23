
from window.user_input import request_fish_bounds
import cv2
from os import listdir

def __get_available_sample_prefix(path):
    names = sorted(set(map(lambda p: int(p.split('-')[0]), listdir(path))))
    i = 1
    while i < names[-1]:
        if i != names[i - 1]:
            return i
        i += 1

    return names[-1] + 1

def collect_single_sample(hwnd, image, *base_images):
    prefix = __get_available_sample_prefix('./new_samples')

    print('Crop bobber in image')

    target_bobber_rect = request_fish_bounds(hwnd, image)

    if target_bobber_rect is None:
        print('Skipping save')
        return False
        
    cv2.imwrite(f'./new_samples/{prefix}-{"-".join(map(str, target_bobber_rect))}.png', image)
    cv2.imwrite(f'./new_samples/{prefix}-base-1.png', base_images[0])
    cv2.imwrite(f'./new_samples/{prefix}-base-2.png', base_images[1])
    cv2.imwrite(f'./new_samples/{prefix}-base-3.png', base_images[2])
    return True
