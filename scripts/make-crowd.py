"""Rebuild the cover's crowd pyramid as crisp figures.

In the source artwork the pyramid is a few hundred photographed people about
five pixels tall each, which is the one element that cannot survive being
enlarged — it turns to mush. It is regenerated here instead: the envelope,
the scale gradient, the density and the palette are all measured off the
artwork, then figures are placed to match, so it reads the same and stays
sharp at any projection size.

Coordinates come out in the same 0..1 frame space the traced ribbons use.

    python scripts/make-crowd.py                 # -> components/cover-crowd.json
"""
import json
import random

W, H = 668.0, 374.0          # the artwork, rimmed off, in source pixels
APEX_X, APEX_Y = 568.0, 44.0
BASE_Y = 208.0
SPREAD = 0.465               # half-width gained per pixel of descent
DRIFT = 0.15                 # the pyramid leans right as it widens
H_TOP, H_BOT = 4.1, 13.6     # figure height at the apex and at the base
COUNT = 880
SEED = 11

# measured off the artwork: three in four figures are washed out, the rest
# carry the warm and blue notes that give the crowd its colour
PALETTE = [
    ('#d9d3ce', 26), ('#e7e1db', 18), ('#c3b7b1', 14),
    ('#d98f80', 7), ('#c9705f', 5), ('#e8b49c', 5), ('#a87461', 4),
    ('#5c84b4', 6), ('#7ea5cc', 5), ('#4a4f63', 3),
    ('#c7544a', 4), ('#d9a05e', 3),
]


def figure_path(x, y, h, w):
    """One standing figure, origin at the feet, as a compact SVG path."""
    s = h
    hx, hy, r = x, y - 0.87 * s, 0.100 * s
    p = [
        f'M{x - 0.145 * w:.4f},{y - 0.72 * s:.4f}',
        f'Q{x:.4f},{y - 0.78 * s:.4f} {x + 0.145 * w:.4f},{y - 0.72 * s:.4f}',
        f'L{x + 0.115 * w:.4f},{y - 0.34 * s:.4f}',
        f'L{x + 0.082 * w:.4f},{y:.4f}',
        f'L{x + 0.028 * w:.4f},{y:.4f}',
        f'L{x:.4f},{y - 0.30 * s:.4f}',
        f'L{x - 0.028 * w:.4f},{y:.4f}',
        f'L{x - 0.082 * w:.4f},{y:.4f}',
        f'L{x - 0.115 * w:.4f},{y - 0.34 * s:.4f}',
        'Z',
        # head, as a circle drawn with two arcs so it stays in one path
        f'M{hx - r * w / h:.4f},{hy:.4f}',
        f'a{r * w / h:.4f},{r:.4f} 0 1,0 {2 * r * w / h:.4f},0',
        f'a{r * w / h:.4f},{r:.4f} 0 1,0 {-2 * r * w / h:.4f},0',
        'Z',
    ]
    return ''.join(p)


PALE = {'#d9d3ce', '#e7e1db', '#c3b7b1'}


def pick(rng, bold):
    """Colour one figure. The upper mass of the pyramid reads much more
    strongly than its hazy foot, so pale picks are re-rolled up there."""
    total = sum(w for _, w in PALETTE)
    for _ in range(3):
        t = rng.random() * total
        for col, w in PALETTE:
            t -= w
            if t <= 0:
                break
        if not (bold and col in PALE and rng.random() < 0.55):
            return col
    return col


rng = random.Random(SEED)
figures = []
span = BASE_Y - APEX_Y
while len(figures) < COUNT:
    # bias downward: the crowd thickens as the pyramid widens
    t = rng.random() ** 0.76
    y = APEX_Y + t * span
    half = SPREAD * (y - APEX_Y)
    cx = APEX_X + DRIFT * (y - APEX_Y)
    # fill the triangle, leaning only slightly to the middle
    u = (rng.random() * 2 - 1)
    u = u * (0.82 + 0.18 * abs(u))
    x = cx + u * half
    if half > 1 and abs(x - cx) > half:
        continue
    h = H_TOP + (H_BOT - H_TOP) * t
    # the foot of the pyramid dissolves into haze, and so do its outer edges
    fade_y = 1.0 if y < 178 else max(0.26, 1.0 - (y - 178) / 46)
    # the pyramid is washed out on the side the title runs into, and holds
    # its colour on the open side towards the frame edge
    off = (x - cx) / half if half > 1 else 0.0
    fade_x = max(0.42, 1.0 - (0.62 if off < 0 else 0.34) * abs(off) ** 2.2)
    figures.append({
        'd': figure_path(x / W, y / H, h / H, h / W),
        'f': pick(rng, y < 162),
        'o': round(min(1.0, 0.9 * fade_y * fade_x * rng.uniform(0.72, 1.0)) * 20) / 20,
        'y': round(y, 1),
    })

figures.sort(key=lambda f: f['y'])          # draw back to front

# A path each would be nearly nine hundred nodes on a slide that never moves.
# Opacity is quantised to twentieths and figures sharing a colour and a step
# are merged into one path, which costs nothing visually and leaves a couple
# of hundred nodes.
groups: dict = {}
for f in figures:
    groups.setdefault((f['f'], f['o']), []).append(f['d'])
out = [{'f': fill, 'o': op, 'd': ''.join(ds)} for (fill, op), ds in groups.items()]
json.dump({'viewBox': '0 0 1 1', 'groups': out},
          open('components/cover-crowd.json', 'w'), separators=(',', ':'))
print(f'components/cover-crowd.json: {len(figures)} figures in {len(out)} paths')
