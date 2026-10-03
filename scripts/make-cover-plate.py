"""Lift the baked-in lettering off the cover artwork, leaving only photography.

The source (popcom_files/new.jpg) is a flattened 672x378 design. Its type is
thin dark strokes over much lighter surroundings, so a top-hat — local maximum
minus the pixel — isolates the glyphs while leaving the family silhouettes
alone, since those are broad enough to stay dark under the max filter. The
holes are closed by diffusion, which is all the near-flat white behind the type
needs, and the result is upscaled for the 1280-wide canvas.

Rows and columns below are source pixels, measured off the artwork itself; they
fence the top-hat in so it cannot nibble at the stairs or the palms.

    python scripts/make-cover-plate.py
"""
import numpy as np
from PIL import Image, ImageFilter

SRC = 'popcom_files/new.jpg'
DST = 'public/cover-plate.jpg'
SCALE = 3
TRIM = 2  # the source carries a pale one-pixel rim

# y0, y1, x0, x1 per line of type
TYPE_ROWS = [
    (62, 82, 170, 504),    # PROVINCIAL GOVERNMENT OF BATAAN
    (84, 96, 185, 491),    # rule + tricolour
    (123, 158, 139, 545),  # OFFICE OF THE PROVINCIAL
    (158, 196, 158, 512),  # POPULATION OFFICER
    (197, 212, 182, 494),  # rule + tricolour
    (211, 238, 193, 482),  # DEPARTMENT REPORT
    (252, 271, 254, 422),  # October 5, 2026
    (271, 291, 249, 426),  # Bataan People's Center
]

# the crowd pyramid, redrawn as figures by scripts/make-crowd.py
CROWD = (34, 215, 497, 672)


def maxfilter(x, r):
    out = x.copy()
    for d in range(1, r + 1):
        out = np.maximum(out, np.roll(x, d, 0))
        out = np.maximum(out, np.roll(x, -d, 0))
    v = out.copy()
    for d in range(1, r + 1):
        out = np.maximum(out, np.roll(v, d, 1))
        out = np.maximum(out, np.roll(v, -d, 1))
    return out


def grow(mask, n):
    for _ in range(n):
        m = mask.copy()
        for axis, d in ((0, 1), (0, -1), (1, 1), (1, -1)):
            mask = mask | np.roll(m, d, axis)
    return mask


def blur(x, r, passes=2):
    out = x.astype(np.float64)
    for _ in range(passes):
        acc = np.zeros_like(out)
        for d in range(-r, r + 1):
            acc += np.roll(np.roll(out, d, 0), 0, 1)
        out = acc / (2 * r + 1)
        acc = np.zeros_like(out)
        for d in range(-r, r + 1):
            acc += np.roll(out, d, 1)
        out = acc / (2 * r + 1)
    return out


src = Image.open(SRC).convert('RGB')
a = np.asarray(src).astype(np.float64)
lum = a @ [0.299, 0.587, 0.114]

fence = np.zeros(lum.shape, bool)
for y0, y1, x0, x1 in TYPE_ROWS:
    fence[y0:y1, x0:x1] = True

core = ((maxfilter(lum, 9) - lum) > 32) & fence
mask = grow(core, 3) & fence

# the pyramid: small, textured, and sitting on plain sky, so local contrast
# finds it and a generous dilation takes the halo with it
y0, y1, x0, x1 = CROWD
box = np.zeros(lum.shape, bool)
box[y0:y1, x0:x1] = True
crowd = (blur(lum, 9) - lum > 5) & box
mask |= grow(crowd, 4) & box

# Diffuse the surrounding colour into the holes.
fill = a.copy()
seed = a[~mask].mean(0)
fill[mask] = seed
for _ in range(1200):
    s = (np.roll(fill, 1, 0) + np.roll(fill, -1, 0)
         + np.roll(fill, 1, 1) + np.roll(fill, -1, 1)) / 4.0
    fill = np.where(mask[..., None], s, a)

# Feather the seam so no stroke leaves a hard outline behind the new type.
# The ramp has to start outside the strokes: feathering across them would let
# the original ink bleed back at the edge of every letter.
ramp = blur(grow(mask, 3).astype(np.float64), 2)
alpha = np.maximum(ramp, mask.astype(np.float64))[..., None]
out = a * (1 - alpha) + fill * alpha

plate = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
w, h = plate.size
plate = plate.crop((TRIM, TRIM, w - TRIM, h - TRIM))
plate = plate.resize((plate.width * SCALE, plate.height * SCALE), Image.LANCZOS)
plate = plate.filter(ImageFilter.UnsharpMask(radius=1.1, percent=30, threshold=3))
plate.save(DST, quality=92, subsampling=0, optimize=True)
print(DST, plate.size, '| pixels lifted:', int(mask.sum()))
