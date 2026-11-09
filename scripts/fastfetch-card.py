#!/usr/bin/env python3
"""Draw the fastfetch-style "About me" card (assets/fastfetch.svg).

Usage:  python3 scripts/fastfetch-card.py
Edit the HUMAN / SOFTWARE lists below, rerun, then commit and push.
Keep values short (about 24 characters): the card sits next to the GIF,
so long lines make it wider and the text smaller.
The logo comes from ~/.local/share/omarchy/icon.txt (drawn as pixel blocks,
so it looks the same in every browser, no font needed).
Colours: the Omarchy "Dos Moos" theme (~/.config/omarchy/current/theme/colors.toml).
"""
from pathlib import Path
from html import escape

LOGO_FILE = Path.home() / ".local/share/omarchy/icon.txt"
OUT = Path(__file__).resolve().parent.parent / "assets/fastfetch.svg"

USER, HOST = "ahmed", "VIKking96"
HUMAN = [
    ("Name", "Ahmed Amr Helal"),
    ("Location", "Cairo, Egypt"),
    ("Degree", "B.Sc. CS (Big Data) '24"),
    ("Training", "Route DevOps → Mar 2027"),
    ("Learning", "Linux · Bash · Docker"),
    ("Goal", "first DevOps / Cloud role"),
]
SOFTWARE = [
    ("OS", "Omarchy (Arch, btw)"),
    ("WM", "Hyprland"),
    ("Theme", "Dos Moos"),
    ("Editor", "Neovim"),
    ("Multiplexer", "herdr"),
    ("Shell", "bash + Starship"),
]

# Dos Moos
BG, BAR, BORDER = "#04090F", "#020508", "#1f3a33"
FG, DIM = "#e5fffb", "#5b6065"
KEY1, KEY2, PROMPT = "#00facf", "#79b262", "#55ed82"
LOGO_FROM, LOGO_TO = "#00facf", "#46b43d"
PALETTE = ["#1d2227", "#d75640", "#2b8b37", "#3cc172", "#5b8a4f", "#c75663", "#00facf", "#e5fffb"]

FONT = "'JetBrains Mono','Fira Code','DejaVu Sans Mono',Menlo,Consolas,monospace"
SIZE = 15           # font size
CHAR = SIZE * 0.6   # width of one monospace character
ROW = 23
CW, CH = 3, 6       # size of one logo "pixel"
PAD = 26


def logo_rects():
    lines = LOGO_FILE.read_text().splitlines()
    out = []
    for r, line in enumerate(lines):
        c = 0
        while c < len(line):
            if line[c] == "█":
                start = c
                while c < len(line) and line[c] == "█":
                    c += 1
                out.append(f'<rect x="{start*CW}" y="{r*CH}" width="{(c-start)*CW}" height="{CH + 1}"/>')
            else:
                c += 1
    return "\n    ".join(out), max(map(len, lines)) * CW, len(lines) * CH


def box(title, rows, x, top, width, key_w, colour):
    height = 26 + len(rows) * ROW + 6
    parts = [
        f'<rect x="{x}" y="{top}" width="{width:.0f}" height="{height}" rx="6" fill="none" stroke="{BORDER}"/>',
        f'<rect x="{x + width/2 - 50:.0f}" y="{top - 9}" width="100" height="18" fill="{BG}"/>',
        f'<text x="{x + width/2:.0f}" y="{top + 5}" text-anchor="middle" fill="{colour}" font-weight="700">{title}</text>',
    ]
    for i, (k, v) in enumerate(rows):
        y = top + 30 + i * ROW
        branch = "└" if i == len(rows) - 1 else "├"
        parts.append(f'<text x="{x + 12}" y="{y}" fill="{DIM}">{branch}</text>')
        parts.append(f'<text x="{x + 30}" y="{y}" fill="{colour}">{escape(k)}</text>')
        parts.append(f'<text x="{x + 30 + key_w:.0f}" y="{y}" fill="{FG}">{escape(v)}</text>')
    return "\n  ".join(parts), top + height


def main():
    rects, lw, lh = logo_rects()
    rows = HUMAN + SOFTWARE
    key_w = (max(len(k) for k, _ in rows) + 2) * CHAR
    box_w = 30 + key_w + max(len(v) for _, v in rows) * CHAR + 16
    rx = PAD + lw + PAD                     # right column x
    W = int(rx + box_w + PAD)

    human, end1 = box("Human", HUMAN, rx, 120, box_w, key_w, KEY1)
    software, end2 = box("Software", SOFTWARE, rx, end1 + 26, box_w, key_w, KEY2)

    logo_x, logo_y = PAD, 120 + (end2 - 120 - lh) / 2
    pal_y = end2 + 20
    sw = (box_w - 7 * 6) / 8
    swatches = "".join(
        f'<rect x="{rx + i*(sw + 6):.1f}" y="{pal_y}" width="{sw:.1f}" height="14" rx="3" fill="{c}"/>'
        for i, c in enumerate(PALETTE)
    )
    prompt_y = pal_y + 46
    H = prompt_y + 24

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" font-size="{SIZE}">
  <defs>
    <linearGradient id="logo" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{lw}" y2="{lh}">
      <stop offset="0" stop-color="{LOGO_FROM}"/><stop offset="1" stop-color="{LOGO_TO}"/>
    </linearGradient>
    <style>
      .cursor {{ animation: blink 1.1s steps(1) infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      .fade {{ animation: fadein 0.9s ease-out both; }}
      @keyframes fadein {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    </style>
  </defs>

  <rect width="{W}" height="{H}" rx="12" fill="{BG}" stroke="{BORDER}"/>
  <path d="M0 12a12 12 0 0 1 12-12h{W-24}a12 12 0 0 1 12 12v22H0z" fill="{BAR}"/>
  <circle cx="22" cy="17" r="6" fill="#d75640"/><circle cx="42" cy="17" r="6" fill="#3cc172"/><circle cx="62" cy="17" r="6" fill="#00facf"/>
  <text x="{W/2}" y="22" text-anchor="middle" fill="{DIM}" font-size="13">{USER}@{HOST}: ~</text>

  <text x="{PAD}" y="66"><tspan fill="{PROMPT}">❯</tspan><tspan x="{PAD + 20}" fill="{FG}">fastfetch</tspan></text>

  <g class="fade">
  <g transform="translate({logo_x:.0f} {logo_y:.0f})" fill="url(#logo)" shape-rendering="crispEdges">
    {rects}
  </g>

  <text x="{rx}" y="96" font-size="{SIZE + 3}" font-weight="700"><tspan fill="{PROMPT}">{USER}</tspan><tspan fill="{FG}">@</tspan><tspan fill="{KEY1}">{HOST}</tspan></text>
  <line x1="{rx}" y1="105" x2="{rx + (len(USER + HOST) + 1) * (SIZE + 3) * 0.6:.0f}" y2="105" stroke="{BORDER}"/>

  {human}
  {software}

  {swatches}
  </g>

  <text x="{PAD}" y="{prompt_y}" fill="{PROMPT}">❯</text>
  <rect class="cursor" x="{PAD + 18}" y="{prompt_y - 14}" width="9" height="18" fill="{FG}"/>
</svg>
'''
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg)
    print(f"wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
