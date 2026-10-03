"""Trace the cover's flag ribbons out of the artwork and emit them as SVG paths.

The ribbons and the sweeping bottom swoosh are flat graphics, so enlarging
them as pixels is what made the old plate look soft. Here they are recovered
as outlines instead, in a 0..1 coordinate space, and the deck draws them as
real vectors at whatever size it is projected.

Two shapes need two methods. The top-left wedge is straight-edged, so a
contour around the mask is already clean. The swoosh along the foot is a pair
of long arcs that thin to nothing at the tail, where a contour picks up every
stray pixel — so each band there is read column by column and its two edges
fitted as polynomials, which is what the artwork's own geometry is.

Only shapes reaching the frame edge are kept, which is what separates the
ribbons from the sunset and the Capitol glass: both land in the same colour
bins but float in the middle of the picture.

    python scripts/trace-cover-art.py            # -> components/cover-art.json
"""
import json
import numpy as np
from PIL import Image
from skimage import measure
from scipy import ndimage

SRC = 'popcom_files/new.jpg'
DST = 'components/cover-art.json'
TRIM = 2        # the source carries a pale rim that would fake a frame edge
UP = 6          # mask upsample before contouring
TOL = 1.1       # polygon simplification, source pixels
SIGMA = 0.95    # blur, in source pixels, that rounds the traced edge
EDGE = 6        # a shape counts as reaching the frame within this many pixels
SNAP = 6        # ...and a point this close to the frame is pulled onto it,
                # since the ribbons' outermost pixels are antialiased away
DEG = 4         # polynomial order for the swoosh edges

src = Image.open(SRC).convert('RGB')
src = src.crop((TRIM, TRIM, src.width - TRIM, src.height - TRIM))
a = np.asarray(src).astype(float)
H, W, _ = a.shape
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mx, mn = a.max(2), a.min(2)
sat = (mx - mn) / np.maximum(mx, 1)
lum = a @ [0.299, 0.587, 0.114]

BANDS = {
    'navy': (b > r + 45) & (lum < 125) & (sat > 0.42),
    'blue': (b > r + 40) & (lum >= 125) & (lum < 205) & (sat > 0.33),
    'gold': (r > 185) & (g > 125) & (b < 145) & (sat > 0.38),
    'red':  (r > 145) & (g < 115) & (b < 115) & (sat > 0.42),
}

CORNER = np.zeros((H, W), bool)
CORNER[:105, :105] = True
SWEEP = np.zeros((H, W), bool)
SWEEP[258:, :] = True


def touches_edge(m):
    return (m[:EDGE].any() or m[-EDGE:].any()
            or m[:, :EDGE].any() or m[:, -EDGE:].any())


def is_flag_colour(fill):
    f_mx, f_mn = fill.max(), fill.min()
    return (f_mx - f_mn) / max(f_mx, 1) >= 0.45 and fill @ [0.299, 0.587, 0.114] <= 205


def norm(x, y):
    x = 0.0 if x < SNAP else (float(W) if x > W - SNAP else x)
    y = 0.0 if y < SNAP else (float(H) if y > H - SNAP else y)
    return min(max(x, 0.0), W) / W, min(max(y, 0.0), H) / H


def smooth_path(pts):
    """Catmull-Rom through the points, as a closed run of cubic beziers."""
    n = len(pts)
    d = [f'M{pts[0][0]:.4f},{pts[0][1]:.4f}']
    for i in range(n):
        p0, p1 = pts[(i - 1) % n], pts[i]
        p2, p3 = pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f'C{c1[0]:.4f},{c1[1]:.4f} {c2[0]:.4f},{c2[1]:.4f} {p2[0]:.4f},{p2[1]:.4f}')
    return ''.join(d) + 'Z'


def poly_path(comp):
    """A swoosh band: its two edges fitted as curves in x, then joined."""
    cols = np.nonzero(comp.any(0))[0]
    if len(cols) < 24:
        return None
    x0, x1 = cols.min(), cols.max()
    xs, tops, bots = [], [], []
    for x in range(x0, x1 + 1):
        ys = np.nonzero(comp[:, x])[0]
        if not len(ys):
            continue
        xs.append(x); tops.append(ys.min()); bots.append(ys.max())
    xs = np.asarray(xs, float)
    # weight by band thickness so the ragged tail cannot steer the fit
    w = np.asarray(bots, float) - np.asarray(tops, float) + 1
    ft = np.polyfit(xs, tops, DEG, w=w)
    fb = np.polyfit(xs, bots, DEG, w=w)
    grid = np.linspace(x0, x1, 26)
    top = [norm(x, np.polyval(ft, x)) for x in grid]
    bot = [norm(x, np.polyval(fb, x)) for x in grid[::-1]]
    pts = top + bot
    d = [f'M{pts[0][0]:.4f},{pts[0][1]:.4f}']
    for x, y in pts[1:]:
        d.append(f'L{x:.4f},{y:.4f}')
    return ''.join(d) + 'Z'


def contour_paths(comp):
    pad = np.pad(comp.astype(float), 1)
    big = ndimage.zoom(pad, UP, order=1)
    big = ndimage.gaussian_filter(big, UP * SIGMA)
    out = []
    for c in measure.find_contours(big, 0.5):
        poly = measure.approximate_polygon(c, tolerance=TOL * UP)
        if len(poly) < 4:
            continue
        pts = [norm(float(x) / UP - 1, float(y) / UP - 1) for y, x in poly]
        if pts[0] == pts[-1]:
            pts = pts[:-1]
        out.append(pts)
    return out


def area_of(d):
    import re
    nums = [float(v) for v in re.findall(r'-?\d+\.?\d*(?:e-?\d+)?', d)]
    pts = list(zip(nums[0::2], nums[1::2]))
    n = len(pts)
    return abs(sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1]
                   for i in range(n))) / 2


shapes = []
for name, raw in BANDS.items():
    for zone, kind in ((CORNER, 'corner'), (SWEEP, 'sweep')):
        m = ndimage.binary_closing(raw & zone, np.ones((3, 3)), iterations=3)
        m = ndimage.binary_opening(m, np.ones((3, 3)))
        lab, n = ndimage.label(m)
        for i in range(1, n + 1):
            comp = lab == i
            if comp.sum() < 260 or not touches_edge(comp):
                continue
            core = ndimage.binary_erosion(comp, np.ones((3, 3)), iterations=2)
            fill = a[core if core.any() else comp].mean(0)
            if not is_flag_colour(fill):
                continue
            hexf = '#%02x%02x%02x' % tuple(int(round(v)) for v in fill)
            ds = []
            if kind == 'sweep':
                d = poly_path(comp)
                if d:
                    ds = [d]
            if not ds:
                ds = [smooth_path(p) for p in contour_paths(comp) if len(p) > 2]
            for d in ds:
                ar = area_of(d)
                if ar < 0.0007:
                    continue
                shapes.append({'band': name, 'kind': kind, 'fill': hexf,
                               'area': round(ar, 5), 'd': d})

shapes.sort(key=lambda s: -s['area'])
json.dump({'viewBox': '0 0 1 1', 'shapes': shapes}, open(DST, 'w'), indent=1)
print(f'{DST}: {len(shapes)} shapes')
for s in shapes:
    print(f"  {s['band']:5s} {s['kind']:6s} {s['fill']}  area {s['area']:.4f}")
