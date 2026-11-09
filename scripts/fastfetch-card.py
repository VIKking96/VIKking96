#!/usr/bin/env python3
"""Draw the fastfetch-style "About me" card (assets/fastfetch.svg).

Usage:  python3 scripts/fastfetch-card.py
Edit the HUMAN / SOFTWARE lists below, rerun, then commit and push.
The logo comes from ~/.local/share/omarchy/icon.txt (drawn as pixel blocks,
so it looks the same in every browser, no font needed).
"""
from pathlib import Path
from html import escape

LOGO_FILE = Path.home() / ".local/share/omarchy/icon.txt"
OUT = Path(__file__).resolve().parent.parent / "assets/fastfetch.svg"

USER_HOST = "ahmed@VIKking96"
HUMAN = [
    ("Name", "Ahmed Amr Helal"),
    ("Location", "Cairo, Egypt"),
    ("Degree", "B.Sc. Computer Science (Big Data), 2024"),
    ("Training", "Route DevOps Diploma (until Mar 2027)"),
    ("Learning", "Linux · Bash · Docker · CI/CD"),
    ("Goal", "my first DevOps / Cloud role"),
]
SOFTWARE = [
    ("OS", "Omarchy (Arch Linux, btw)"),
    ("WM", "Hyprland (Wayland)"),
    ("Editor", "Neovim"),
    ("Multiplexer", "herdr"),
    ("Shell", "SHELL_PLACEHOLDER"),
    ("Speaks", "Arabic · English"),
]

# Tokyo Night
BG, BAR, BORDER = "#1a1b26", "#16161e", "#414868"
FG, DIM, BLUE, PURPLE, GREEN, CYAN = "#c0caf5", "#565f89", "#7aa2f7", "#bb9af7", "#9ece6a", "#7dcfff"
PALETTE = ["#15161e", "#f7768e", "#9ece6a", "#e0af68", "#7aa2f7", "#bb9af7", "#7dcfff", "#a9b1d6"]

W, H = 880, 520
FONT = "'JetBrains Mono','Fira Code','DejaVu Sans Mono',Menlo,Consolas,monospace"
ROW = 22
RX = 330          # right column x
KEY_W = 120       # width of the key column


def logo_rects(x0, y0, cw=4, ch=8):
    lines = LOGO_FILE.read_text().splitlines()
    out = []
    for r, line in enumerate(lines):
        c = 0
        while c < len(line):
            if line[c] == "█":
                start = c
                while c < len(line) and line[c] == "█":
                    c += 1
                out.append(f'<rect x="{x0 + start*cw}" y="{y0 + r*ch}" width="{(c-start)*cw}" height="{ch + 1}"/>')
            else:
                c += 1
    return "\n    ".join(out), max(map(len, lines)) * cw, len(lines) * ch


def box(title, rows, top, colour):
    height = 24 + len(rows) * ROW + 8
    width = W - RX - 30
    parts = [
        f'<rect x="{RX}" y="{top}" width="{width}" height="{height}" rx="6" fill="none" stroke="{BORDER}"/>',
        f'<rect x="{RX + width/2 - 52}" y="{top - 8}" width="104" height="16" fill="{BG}"/>',
        f'<text x="{RX + width/2}" y="{top + 5}" text-anchor="middle" fill="{colour}" font-weight="700">{title}</text>',
    ]
    for i, (k, v) in enumerate(rows):
        y = top + 28 + i * ROW
        branch = "└" if i == len(rows) - 1 else "├"
        parts.append(f'<text x="{RX + 14}" y="{y}" fill="{DIM}">{branch}</text>')
        parts.append(f'<text x="{RX + 32}" y="{y}" fill="{colour}">{escape(k)}</text>')
        parts.append(f'<text x="{RX + 32 + KEY_W}" y="{y}" fill="{FG}">{escape(v)}</text>')
    return "\n  ".join(parts), top + height


def main(shell):
    rows_sw = [(k, shell if v == "SHELL_PLACEHOLDER" else v) for k, v in SOFTWARE]
    human, end1 = box("Human", HUMAN, 132, BLUE)
    software, end2 = box("Software", rows_sw, end1 + 26, PURPLE)

    rects, lw, lh = logo_rects(0, 0)
    logo_x = 40 + (RX - 40 - 30 - lw) / 2
    logo_y = 132 + (end2 - 132 - lh) / 2

    pal_y = end2 + 22
    swatches = "".join(
        f'<rect x="{RX + i*34}" y="{pal_y}" width="28" height="14" rx="3" fill="{c}"/>' for i, c in enumerate(PALETTE)
    )
    prompt_y = pal_y + 48

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}" font-size="14">
  <defs>
    <linearGradient id="logo" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{lw}" y2="{lh}">
      <stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{PURPLE}"/>
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
  <circle cx="22" cy="17" r="6" fill="#f7768e"/><circle cx="42" cy="17" r="6" fill="#e0af68"/><circle cx="62" cy="17" r="6" fill="#9ece6a"/>
  <text x="{W/2}" y="22" text-anchor="middle" fill="{DIM}" font-size="13">{USER_HOST}: ~</text>

  <text x="30" y="70"><tspan fill="{GREEN}">❯</tspan><tspan x="50" fill="{FG}">fastfetch</tspan></text>

  <g class="fade">
  <g transform="translate({logo_x:.0f} {logo_y:.0f})" fill="url(#logo)" shape-rendering="crispEdges">
    {rects}
  </g>

  <text x="{RX}" y="104" font-size="17" font-weight="700"><tspan fill="{GREEN}">ahmed</tspan><tspan fill="{FG}">@</tspan><tspan fill="{BLUE}">VIKking96</tspan></text>
  <line x1="{RX}" y1="114" x2="{RX + 160}" y2="114" stroke="{BORDER}"/>

  {human}
  {software}

  {swatches}
  </g>

  <text x="30" y="{prompt_y}"><tspan fill="{GREEN}">❯</tspan></text>
  <rect class="cursor" x="48" y="{prompt_y - 13}" width="9" height="17" fill="{FG}"/>
</svg>
'''
    svg = svg.replace(f'height="{H}" viewBox="0 0 {W} {H}"', f'height="{prompt_y + 28}" viewBox="0 0 {W} {prompt_y + 28}"')
    svg = svg.replace(f'<rect width="{W}" height="{H}"', f'<rect width="{W}" height="{prompt_y + 28}"')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "zsh")
