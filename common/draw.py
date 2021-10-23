import cv2
import numpy as np

def annotate_contours_rect(image, contours, color=(0, 0, 255)):
    annotated_image = image.copy()

    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        ((x, y), (w, h), _) = rect
        cv2.drawContours(annotated_image, [box], 0, color, 2)

    return annotated_image

def annotate_contours_circle(image, contours, **options):
    mark_center=options['mark_center'] if 'mark_center' in options else False
    border_thickness=options['border_thickness'] if 'border_thickness' in options else 2
    color=options['color'] if 'color' in options else (0, 0, 255)
    annotated_image = image.copy()

    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)

        cv2.circle(annotated_image, center, radius, color, border_thickness)

        if mark_center == True:
            cv2.circle(annotated_image, center, 2, color, border_thickness)

    return annotated_image

