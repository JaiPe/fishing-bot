def crop_bounds(img, screen_bounds):
    (x, y, w, h) = screen_bounds
    return img[y: y+h, x: x+w]
