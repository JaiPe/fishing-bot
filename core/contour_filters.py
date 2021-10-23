import cv2

def create_contour_bounds_filter(screen_bounds, **options):
    match_type = options['match_type'] if 'match_type' in options else 'rect'
    verbose = options['verbose'] if 'verbose' in options else False
    inverse = options['inverse'] if 'inverse' in options else False
    def filter(cnt):
        x = 0
        y = 0
        w = 0
        h = 0
        (x2, y2, w2, h2) = screen_bounds
        bottom_right_match = False
        top_left_match = False
        if match_type == 'center_point':
            (x, y), _ = cv2.minEnclosingCircle(cnt)
            top_left_match = x >= x2 and x <= x2 + w2
            bottom_right_match = y >= y2 and y <= y2 + h2
        else:
            (x, y, w, h) = cv2.boundingRect(cnt)
            top_left_match = x >= x2 - 20 and y >= y2 - 20
            bottom_right_match =  x + w <= x2 + w2 + 20 and y + h <= y2 + h2 + 20
        
        if verbose == True:
            print(f'top_left_match: {top_left_match}')
            print(f'bottom_right_match: {bottom_right_match}')
            print(f'{x} {y} {w} {h}')
            print(f'{x2} {y2} {w2} {h2}')
        
        matches = top_left_match and bottom_right_match
        if inverse:
            return not matches
        return matches

    return filter

def create_contour_size_shape_filter(**options):
    inverse = options['inverse'] if 'inverse' in options else False
    num_contours = options['num_contours']
    min_radius = options['min_radius']
    max_radius = options['max_radius']
    def filter(cnt):
        (x, y, w, h) = cv2.boundingRect(cnt)
        _, radius = cv2.minEnclosingCircle(cnt)
        radius = int(radius)
        circle_match = radius > min_radius and radius < max_radius
        rect_shape_match = abs(w - h) < max(w, h) / 1.7
        
        matches_shape = circle_match and rect_shape_match
        matches = matches_shape or num_contours < 3
        if inverse:
            return not matches
        return matches

    return filter