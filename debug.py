from debug.cast import cast as cast_debug
from common.fs import empty
import time

empty(f'./.tmp/*.png')
empty(f'./.tmp/**/*.png')

bounds = (450, 80, 826, 519)

start = time.time()

cast_debug(0, screen_bounds=bounds, max_match_radius=45, min_match_radius=10, max_match_contours=9,
           #annotate_hits=True
           )

print(f'Elapsed: {round(time.time() - start, 2)}')