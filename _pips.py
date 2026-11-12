"""Exact playing-card pip overlay for the generated art decks.

The diffusion model paints the ornate card art (frame, crest, portrait
medallion) but it cannot count: asked for "two heart pips" it happily draws
four. So the model is told to leave the card face free of pips and this module
draws them afterwards at mathematically correct positions and counts.

Layout: two columns (left/right of the central medallion) plus a bottom-centre
pip for odd counts -- the classic arrangement, minus the true centre pip which
the portrait medallion occupies.

Positions are normalised (0..1) over the card face.
"""
from PIL import Image, ImageDraw

RED = (200, 16, 38)
BLACK = (26, 26, 34)
GOLD = (224, 166, 58)
CREAM = (250, 244, 226)

# (per-column count -> y positions down each column)
COLUMN_ROWS = {
    1: [0.38],
    2: [0.30, 0.70],
    3: [0.24, 0.50, 0.76],
    4: [0.20, 0.41, 0.60, 0.81],
    5: [0.17, 0.335, 0.50, 0.665, 0.83],
}
LEFT_X, RIGHT_X = 0.175, 0.825
BOTTOM_CENTRE_Y = 0.885


def pip_positions(rank):
    """Normalised (x, y) centres for every pip of a number card."""
    n = int(rank)
    per = n // 2
    pos = []
    for y in COLUMN_ROWS[per]:
        pos.append((LEFT_X, y))
        pos.append((RIGHT_X, y))
    if n % 2:
        pos.append((0.5, BOTTOM_CENTRE_Y))
    return pos


def _heart(d, cx, cy, r, fill):
    """Classic heart built from two lobes and a point."""
    w, h = r, r * 0.92
    d.ellipse([cx - r, cy - h * 0.95, cx - r * 0.06, cy + h * 0.15], fill=fill)
    d.ellipse([cx + r * 0.06, cy - h * 0.95, cx + r, cy + h * 0.15], fill=fill)
    d.polygon([(cx - r * 0.96, cy - h * 0.12), (cx + r * 0.96, cy - h * 0.12),
               (cx, cy + h)], fill=fill)


def _spade(d, cx, cy, r, fill):
    """Upside-down heart plus a stem."""
    w, h = r, r * 0.92
    d.ellipse([cx - r, cy - h * 0.95, cx - r * 0.06, cy + h * 0.15], fill=fill)
    d.ellipse([cx + r * 0.06, cy - h * 0.95, cx + r, cy + h * 0.15], fill=fill)
    d.polygon([(cx - r * 0.96, cy - h * 0.12), (cx + r * 0.96, cy - h * 0.12),
               (cx, cy - h * 0.62)], fill=fill)
    d.polygon([(cx - r * 0.30, cy + h * 0.05), (cx + r * 0.30, cy + h * 0.05),
               (cx, cy + h)], fill=fill)


def _club(d, cx, cy, r, fill):
    """Three lobes plus a stem."""
    d.ellipse([cx - r * 0.95, cy - r * 0.95, cx + r * 0.05, cy + r * 0.05], fill=fill)
    d.ellipse([cx - r * 0.05, cy - r * 0.95, cx + r * 0.95, cy + r * 0.05], fill=fill)
    d.ellipse([cx - r * 0.85, cy - r * 0.05, cx + r * 0.85, cy + r * 0.85], fill=fill)
    d.polygon([(cx - r * 0.26, cy + h(r) * 0.6), (cx + r * 0.26, cy + h(r) * 0.6),
               (cx, cy + r * 1.30)], fill=fill)


def h(r):
    return r * 0.92


def _diamond(d, cx, cy, r, fill):
    d.polygon([(cx, cy - r), (cx + r * 0.72, cy), (cx, cy + r), (cx - r * 0.72, cy)],
              fill=fill)


GLYPHS = {"hearts": _heart, "diamonds": _diamond, "clubs": _club, "spades": _spade}


def draw_pips(card_path, suit, rank, out_path=None):
    """Overlay exact pips on a generated card image (in place by default)."""
    if rank in ("A", "J", "Q", "K"):
        return card_path
    out_path = out_path or card_path
    with Image.open(card_path) as im:
        im = im.convert("RGB")
    W, H = im.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    fill = RED if suit in ("hearts", "diamonds") else BLACK
    r = int(W * 0.048)
    for x, y in pip_positions(rank):
        cx, cy = x * W, y * H
        # dark halo -> cream rim -> solid pip, so the pip stays crisp on
        # top of the busy painted card art.
        GLYPHS[suit](d, cx, cy, r * 1.20, (0, 0, 0, 95))
        GLYPHS[suit](d, cx, cy, r * 1.06, CREAM + (235,))
        GLYPHS[suit](d, cx, cy, r * 0.88, fill + (255,))
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    im.save(out_path)
    return out_path
