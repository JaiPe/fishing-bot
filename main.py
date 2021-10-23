from collect_samples import collect_single_sample
from window.toggle_ui import close_ui, open_ui
import cv2
import time

from core.cast import cast
from core.apply_lure import apply_lure
from common.crop import crop_bounds
from window.loot_window import is_loot_window_open
from common.draw import annotate_contours_circle
from common.color import count_pixels_mte_threshold, get_threshold
from common.mouse_keyboard import right_click, move_mouse, key_down, key_up
from common.screenshot import screenshot, screenshot_sequence
from common.find_cursor import find_cursor
from window.position import bring_to_front, move_window
from window.find import find_window
from core.splash_detection import is_splash_detected, get_white_threshold
from core.logout import logout
from common.fs import empty, write_tmp
from window.user_input import request_fish_bounds
import schedule

empty(f'./.tmp/*.png')
empty(f'./.tmp/**/*.png')

# Threshold for the bobber cursor
bobber_cursor_threshold = 247


class SplashError(Exception):
    pass


def cursor_found(initial_cursor_threshold, pos, expected_cursor_threshold):
    (x, y) = pos

    move_mouse(int(x) + 10, int(y) + 44 + 10)
    time.sleep(0.2)

    new_cursor_thresh = find_cursor(dtype='threshold')

    return initial_cursor_threshold != new_cursor_thresh and new_cursor_thresh == expected_cursor_threshold


def start(hwnd, **options):
    use_lure = options['use_lure']
    runtime_mins = options['runtime_mins']
    bounds = options['bounds']

    if use_lure == True:
        apply_lure(hwnd)
        schedule.every(10).minutes.do(lambda: apply_lure(hwnd))

    time.sleep(0.2)
    move_mouse(100, 100)
    time.sleep(0.1)
    move_mouse(50, 50)
    time.sleep(0.1)

    initial_cursor_threshold = find_cursor(dtype='threshold')

    if not initial_cursor_threshold:
        raise Exception("Could not resolve initial cursor")

    pre_cast_screens = screenshot_sequence(
        hwnd, frame_rate=1/8, num_captures=5)

    cast_count = 0
    misses_count = 0
    faults_count = 0
    timeout_count = 0

    start_time = time.time()

    while start_time + 60 * runtime_mins > time.time():
        cast_count += 1

        post_cast_image, contours = cast(hwnd, *pre_cast_screens, screen_bounds=bounds,
                                         max_match_radius=45, min_match_radius=10, max_match_contours=8, initial_cursor_threshold=initial_cursor_threshold)

        bobber_bounds, center_bobber_bounds = find_bobber(
            contours, initial_cursor_threshold)

        if len(bobber_bounds) == 0:
            print('No bobbers found')
            # collect_single_sample(hwnd, post_cast_image, *pre_cast_screens[:3])
            faults_count += 1
            continue

        extended_bobber_bounds = (max(0, bobber_bounds[0] - 25), max(0, bobber_bounds[1] - 25), post_cast_image.shape[1] - bobber_bounds[0] if bobber_bounds[0] + 100 > post_cast_image.shape[1] else 100,
                                  post_cast_image.shape[0] - bobber_bounds[1] if bobber_bounds[1] + 100 > post_cast_image.shape[0] else 100)
        mixed_screens = (crop_bounds(post_cast_image, extended_bobber_bounds), *screenshot_sequence(hwnd,
                         frame_rate=1/14, num_captures=17, region=extended_bobber_bounds))
        try:
            if wait_for_splash(hwnd, mixed_screens, extended_bobber_bounds, timeout=16) == True:
                print('Bite found!')

                if reel(hwnd, center_bobber_bounds):
                    print('CAUGHT!')
                else:
                    print('MISSED!')
                    misses_count += 1
            else:
                print('Timeout! No bites found')
                timeout_count += 1
        except SplashError:
            print('Offset too high')
            faults_count += 1

        if faults_count > 10:
            raise RuntimeError('Too many faults')
        time.sleep(1)

    # Cancel lure applications
    schedule.clear()

    return (misses_count, timeout_count, cast_count - misses_count - faults_count - timeout_count, faults_count)


def wait_for_splash(hwnd, screens, extended_bobber_bounds, **options):
    cast_time = time.time()
    current_white_threshold = get_white_threshold(screens)
    all_white_counts = list(map(lambda img: count_pixels_mte_threshold(img, current_white_threshold), screens))
    while True:
        avg_white_count = sum(all_white_counts) / len(all_white_counts)
        min_change = avg_white_count * 0.012
        splash_detected, diff, next_white_count = is_splash_detected(hwnd, extended_bobber_bounds, min_white_count=avg_white_count, min_white_threshold=current_white_threshold)

        if splash_detected == True and diff > min_change / 3:
            time.sleep(1 / 11)
            # Double check
            splash_detected, next_diff, next_next_white_count = is_splash_detected(hwnd, extended_bobber_bounds, min_white_count=avg_white_count, min_white_threshold=current_white_threshold)
            if splash_detected == True and diff > min_change / 3 and (next_diff > min_change or diff > min_change):
                return True
            all_white_counts.append(next_next_white_count)
            
        if cast_time + options['timeout'] < time.time():
            return False
        all_white_counts.append(next_white_count)
        time.sleep(1 / 12)


def reel(hwnd, center_bobber_bounds):
    right_click(*center_bobber_bounds)
    time.sleep(0.2)
    loot_screens = screenshot_sequence(hwnd, frame_rate=1/8, num_captures=6)

    return len(list(filter(lambda img: is_loot_window_open(hwnd, img), loot_screens))) > 0


def find_bobber(contours, initial_cursor_threshold):
    move_mouse(0, 0)

    def get_bobber_centre(x, y, w, h):
        return (x + w / 1.8, y + h / 2.1)

    for cnt in reversed(contours):
        (x, y, w, h) = cv2.boundingRect(cnt)
        if cursor_found(initial_cursor_threshold, get_bobber_centre(x, y, w, h), bobber_cursor_threshold):
            return (x, y, w, h), get_bobber_centre(x, y, w, h)

    return [], []


hwnd = find_window('World of Warcraft')
if not hwnd:
    raise ValueError("Could not find window")
bring_to_front(hwnd)
move_window(hwnd, (0, 0, 1626, 919))


def request_water_bounds(hwnd):
    print('Crop potential bobber boundary')
    return request_fish_bounds(hwnd, screenshot(hwnd)) or (366, 181, 646, 335)


(misses_count, timeout_count, hit_count, faults_count) = start(
    hwnd, use_lure=False, runtime_mins=10, bounds=request_water_bounds(hwnd))
print(f'Misses: {misses_count}')
print(f'No bites: {timeout_count}')
print(f'Hits: {hit_count}')
print(f'Faults: {faults_count}')

logout()
