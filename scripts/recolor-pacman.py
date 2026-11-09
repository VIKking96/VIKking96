#!/usr/bin/env python3
"""Repaint the Pac-Man contribution graph in the Omarchy "Dos Moos" colours.

Usage:  python3 scripts/recolor-pacman.py dist/pacman-contribution-graph-dark.svg
Needs Pillow (pip install pillow) to repaint the ghost sprites (tiny PNGs).
The daily workflow (.github/workflows/profile.yml) runs it after drawing the game.
"""
import base64
import io
import re
import sys
from collections import Counter

from PIL import Image

# Plain colour swaps (GitHub dark colour -> Dos Moos)
SWAPS = {
    "#0d1117": "none",      # background: transparent, like the snake was
    "#161b22": "#1d2227",   # empty days
    "#8b949e": "#5b6065",   # month labels
    "#ffffff": "#1f6b4a",   # maze walls: dim jade
    # days with commits: the email badge colour
    "#0e4429": "#0d5c4a",
    "#006d32": "#0d5c4a",
    "#26a641": "#0d5c4a",
    "#39d353": "#0d5c4a",
    '"yellow"': '"#00facf"',  # Pac-Man himself: mint
    "yellow;": "#00facf;",
    ";red\"": ";#d75640\"",   # the red flash when he gets caught
}

# Ghost body colours
GHOSTS = {
    "blinky": "#d75640",   # red
    "pinky": "#c75663",    # magenta
    "inky": "#79b262",     # jade
    "clyde": "#3cc172",    # green
    "scared": "#5b8a4f",   # dim green
}


def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def repaint(png_b64, colour):
    """Swap the sprite's main body colour, keep eyes (white/blue/black)."""
    im = Image.open(io.BytesIO(base64.b64decode(png_b64))).convert("RGBA")
    px = im.load()
    counts = Counter(px[x, y][:3] for x in range(im.width) for y in range(im.height) if px[x, y][3])
    body = next((c for c, _ in counts.most_common() if c != (255, 255, 255) and sum(c) > 80), None)
    if body is None:
        return png_b64
    new = hex_rgb(colour)

    def near(c, ref, tol=90):   # the sprites have soft edges in many close shades
        return sum((p - q) ** 2 for p, q in zip(c, ref)) <= tol ** 2

    for x in range(im.width):
        for y in range(im.height):
            r, g, b, a = px[x, y]
            if a and near((r, g, b), body):
                px[x, y] = (*new, a)
    out = io.BytesIO()
    im.save(out, "PNG")
    return base64.b64encode(out.getvalue()).decode()


def main(path):
    svg = open(path).read()
    for old, new in SWAPS.items():
        svg = re.sub(re.escape(old), new, svg, flags=re.I)

    def ghost(m):
        name = m.group(1)
        colour = next((c for g, c in GHOSTS.items() if g in name), None)
        if colour is None:      # "ghost-eyes-*": leave as is
            return m.group(0)
        return m.group(0).replace(m.group(2), repaint(m.group(2), colour))

    svg = re.sub(r'<symbol id="(ghost-[^"]+)"[^>]*>\s*<image href="data:image/png;base64,([^"]+)"', ghost, svg)
    open(path, "w").write(svg)
    print(f"recoloured {path}")


if __name__ == "__main__":
    main(sys.argv[1])
