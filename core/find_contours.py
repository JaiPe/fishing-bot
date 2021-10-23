import cv2
import numpy as np
from common.draw import annotate_contours_circle
from core.contour_filters import create_contour_bounds_filter, create_contour_size_shape_filter

def find_contours(processed_image, screen_bounds, **options):
    min_match_radius = options['min_match_radius']
    max_match_radius = options['max_match_radius']

    # Strip off the last match, as it will always be the entire cropped image
    unfiltered_contours = cv2.findContours(processed_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0][:-1]

    contours_within_bounds = list(filter(create_contour_bounds_filter(screen_bounds), unfiltered_contours))
    return (__merge_overlap_filters(processed_image.shape, 
                    list(filter(create_contour_size_shape_filter(max_radius=max_match_radius,
                                min_radius=min_match_radius, num_contours=len(contours_within_bounds)), contours_within_bounds))), contours_within_bounds)

def __merge_overlap_filters(shape, contours):
    contour_mask = np.zeros(shape[:2], dtype=np.uint8)
    contour_mask.fill(0)
    contour_mask = annotate_contours_circle(contour_mask, contours, color=(255, 255, 255), border_thickness=-1)

    return cv2.findContours(contour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
