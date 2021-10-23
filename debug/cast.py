from common.transforms import merge
from core.image_processor import process
from core.find_contours import find_contours
from core.contour_filters import create_contour_bounds_filter, create_contour_size_shape_filter
from common.draw import annotate_contours_circle
from common.fs import write_tmp
from common.crop import crop_bounds
from debug.sample import get_samples
import cv2

def write_annotations(annotated, filename, img_removed_background, img_merged):
    write_tmp(annotated, f'{filename}.png')
    write_tmp(img_removed_background, f'{filename}-processed.png')
    write_tmp(img_merged, f'{filename}-background.png')

def cast(_, **options):
    screen_bounds = options['screen_bounds']
    min_match_radius = options['min_match_radius']
    max_match_radius = options['max_match_radius']
    annotate_hits = options['annotate_hits'] if 'annotate_hits' in options else False
    max_match_contours = options['max_match_contours']
    matches = 0
    total_num_accepted_contours = 0
    highest_num_accepted_contours = 0
    samples = get_samples()
    for sample in samples:
        image = sample['image']
        filename = sample['filename']

        verbose = False
        #verbose = '43-680-194-57' in filename

        sample_bounds = sample['bounds']

        pre_cast_screens = list(map(lambda img: crop_bounds(img, screen_bounds), sample['base_images']))

        (image_processed, base_image_processed) = process(image, screen_bounds, *pre_cast_screens)
        accepted_contours, contours_within_bounds = find_contours(image_processed, screen_bounds, min_match_radius=min_match_radius, max_match_radius=max_match_radius)

        annotated = annotate_contours_circle(image, accepted_contours, mark_center=True)
        annotated = cv2.rectangle(annotated, (sample_bounds[0], sample_bounds[1]), (sample_bounds[0] + sample_bounds[2], sample_bounds[1] + sample_bounds[3]), (200, 200, 100), 3)
        annotated = cv2.rectangle(annotated, (screen_bounds[0], screen_bounds[1]), (screen_bounds[0] + screen_bounds[2], screen_bounds[1] + screen_bounds[3]), (100, 200, 100), 5)
        annotated = annotate_contours_circle(annotated, list(filter(create_contour_size_shape_filter(
                                             max_radius=max_match_radius, min_radius=min_match_radius, inverse=True, num_contours=len(contours_within_bounds)), contours_within_bounds)), color=(255, 0, 0))
        num_correct_contours = len(list(filter(create_contour_bounds_filter(sample_bounds, match_type='center_point', verbose=verbose), accepted_contours)))
        num_accepted_contours = len(accepted_contours)

        highest_num_accepted_contours = max(highest_num_accepted_contours, num_accepted_contours)

        if num_accepted_contours > 0 and num_accepted_contours <= max_match_contours and num_correct_contours > 0:
            total_num_accepted_contours += num_accepted_contours
            matches += 1
            if annotate_hits:
                write_annotations(annotated, f'{filename}-success', image_processed, base_image_processed)
            continue
        else:
            write_annotations(annotated, filename, image_processed, base_image_processed)
    if matches > 0:
        print(
            f'Accuracy: {matches}/{len(samples)} ({round(matches / len(samples) * 100)}%) ({round(total_num_accepted_contours / matches, 2)} avg contours) ({highest_num_accepted_contours} max contours)')
    else:
        print('No matches')
