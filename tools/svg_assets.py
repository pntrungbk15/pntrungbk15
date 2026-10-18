"""Animated SVG assets for the profile README: hero (wide and narrow), divider and footer.

Text is converted to outlines so the SVGs render identically everywhere; motion is CSS only and stops under
prefers-reduced-motion.
"""
import math
import random
import sys
from pathlib import Path

from textpath import Font

FONTS = Path(__file__).parent / "fonts"
INTER = {w: Font(str(FONTS / f"inter/extras/ttf/Inter-{w}.ttf")) for w in ("ExtraBold", "Bold", "SemiBold", "Medium", "Regular")}
MONO = Font(str(FONTS / "jbm/fonts/ttf/JetBrainsMono-Medium.ttf"))

NAME = "PHẠM NGỌC TRUNG"
TITLE = "AI Engineer"
KICKER = "HO CHI MINH CITY · VIETNAM"
TAGLINE = "AI systems end to end: data, models, evaluation, inference and software"
ROLES = [
    "LLM, RAG and agentic systems",
    "Document AI and vision-language models",
    "Computer vision and industrial AI",
    "Desktop AI products built on FluentQt",
]

CYAN = "#22D3EE"
CYAN_SOFT = "#7DE7F7"
BLUE = "#3B82F6"
INK = "#EAF4FF"
MUTED = "#8BA3C1"

SLOT = 4.2          # seconds per role
TYPE = 1.5          # typing duration
HOLD_END = 3.3      # deleting starts
DEL = 0.45          # deleting duration


def pct(t, total):
    return f"{100 * t / total:.3f}%"


def typing_css(widths_by_role, x0, y0, total):
    """Keyframes for the clip width and caret position of the typing line."""
    frames = []  # (time, width)
    for i, (w_full, n) in enumerate(widths_by_role):
        start = i * SLOT
        frames.append((start, 0))
        for k in range(1, n + 1):
            frames.append((start + TYPE * k / n, w_full * k / n))
        frames.append((start + HOLD_END, w_full))
        for k in range(1, n + 1):
            frames.append((start + HOLD_END + DEL * k / n, w_full * (n - k) / n))
    frames.append((total, 0))
    clip = []
    caret = []
    for t, w in frames:
        clip.append(f"{pct(t, total)}{{transform:translate({x0}px,{y0}px) scaleX({max(w, 0.001):.2f})}}")
        caret.append(f"{pct(t, total)}{{transform:translateX({w + 3:.2f}px)}}")
    roles = []
    for i in range(len(widths_by_role)):
        a, b = i * SLOT, (i + 1) * SLOT
        kf = []
        if a > 0:
            kf.append("0%{opacity:0}")
        kf.append(f"{pct(a, total)}{{opacity:1}}")
        kf.append(f"{pct(b - 0.001, total)}{{opacity:1}}")
        if b < total:
            kf.append(f"{pct(b, total)}{{opacity:0}}")
            kf.append("100%{opacity:0}")
        roles.append(f"@keyframes r{i}{{{''.join(kf)}}}")
    return "@keyframes tw{" + "".join(clip) + "}@keyframes cp{" + "".join(caret) + "}" + "".join(roles)


def network(cx, cy, scale, rng):
    """A small layered network: edges, travelling signals and nodes."""
    layers = [4, 6, 6, 4, 2]
    gap_x, gap_y = 92 * scale, 44 * scale
    cols = []
    for li, n in enumerate(layers):
        x = cx + (li - (len(layers) - 1) / 2) * gap_x
        cols.append([(x, cy + (j - (n - 1) / 2) * gap_y) for j in range(n)])
    edges = []
    for a, b in zip(cols, cols[1:]):
        for p in a:
            for q in b:
                edges.append((p, q))
    out = ['<g class="edges" stroke="url(#edge)" stroke-width="1" fill="none">']
    for (x1, y1), (x2, y2) in edges:
        mx = (x1 + x2) / 2
        out.append(f'<path d="M{x1:.1f} {y1:.1f}C{mx:.1f} {y1:.1f} {mx:.1f} {y2:.1f} {x2:.1f} {y2:.1f}"/>')
    out.append("</g>")
    # signals along a few full chains through the network
    out.append('<g class="signals" fill="none" stroke-linecap="round">')
    for s in range(7):
        pts = [rng.choice(col) for col in cols]
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            mx = (x1 + x2) / 2
            d += f"C{mx:.1f} {y1:.1f} {mx:.1f} {y2:.1f} {x2:.1f} {y2:.1f}"
        delay = s * 1.15
        out.append(f'<path class="sig" pathLength="100" style="animation-delay:{delay:.2f}s" d="{d}" '
                   f'stroke="{CYAN_SOFT}" stroke-width="{2 * scale:.1f}"/>')
    out.append("</g>")
    out.append('<g class="nodes">')
    for li, col in enumerate(cols):
        for j, (x, y) in enumerate(col):
            r = (5.5 if li in (0, len(cols) - 1) else 4.5) * scale
            last = li == len(cols) - 1
            fill = CYAN if last else "#0B1E39"
            stroke = CYAN if last else "#3FA9D6"
            if last:
                out.append(f'<circle class="ring" style="animation-delay:{j * 1.6:.1f}s" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" '
                           f'fill="none" stroke="{CYAN}" stroke-width="1.5"/>')
            cls = ' class="glow"' if (li + j) % 3 == 0 else ""
            out.append(f'<circle{cls} style="animation-delay:{(li * 0.7 + j * 0.45) % 5:.2f}s" cx="{x:.1f}" cy="{y:.1f}" '
                       f'r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    out.append("</g>")
    xs = [p[0] for c in cols for p in c]
    ys = [p[1] for c in cols for p in c]
    return "".join(out), (min(xs), min(ys), max(xs), max(ys))


def brackets(x0, y0, x1, y1, arm=18):
    d = (f"M{x0} {y0 + arm}V{y0}H{x0 + arm}M{x1 - arm} {y0}H{x1}V{y0 + arm}"
         f"M{x1} {y1 - arm}V{y1}H{x1 - arm}M{x0 + arm} {y1}H{x0}V{y1 - arm}")
    return f'<path d="{d}" fill="none" stroke="{CYAN}" stroke-opacity=".55" stroke-width="1.5"/>'


def hero(width, height, narrow):
    rng = random.Random(7)
    total = SLOT * len(ROLES)
    if narrow:
        net, box = network(width / 2, 176, 0.95, rng)
        name_size, title_size, kick_size, role_size = 50, 28, 13, 19
        tx = 48
        ky, ny, ty, ry = 338, 404, 450, 510
    else:
        net, box = network(925, height / 2 + 4, 1.0, rng)
        name_size, title_size, kick_size, role_size = 60, 30, 13, 20
        tx = 64
        ky, ny, ty, ry = 116, 188, 240, 306
    kick_d, kick_w = MONO.path(KICKER, kick_size, tx + 26, ky, tracking=0.12)
    name_d, name_w = INTER["ExtraBold"].path(NAME, name_size, tx - 2, ny, tracking=0.01)
    title_d, title_w = INTER["SemiBold"].path(TITLE, title_size, tx, ty, tracking=-0.005)
    prompt_d, prompt_w = MONO.path("›", role_size, tx, ry)
    tag_d, tag_w = INTER["Medium"].path(TAGLINE, 15 if narrow else 16, tx, ry + 52)
    rx = tx + prompt_w + 12
    role_paths, widths = [], []
    for i, role in enumerate(ROLES):
        d, w = MONO.path(role, role_size, 0, 0)
        role_paths.append(d)
        widths.append((w, len(role)))
    css = typing_css(widths, rx, ry - role_size * 0.95, total)
    pad = 14
    bx0, by0, bx1, by1 = box[0] - 2 * pad, box[1] - 2 * pad, box[2] + 2 * pad, box[3] + 2 * pad
    label_d, label_w = MONO.path("inference", 11, bx0, by0 - 8, tracking=0.12)
    scan_h = by1 - by0

    roles_svg = "".join(
        f'<path class="role r{i}" transform="translate({rx:.1f} {ry})" d="{d}"/>' for i, d in enumerate(role_paths))
    caret_h = role_size * 1.15
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">
<title id="t">{NAME}, {TITLE}</title>
<desc id="d">{TITLE} working on {"; ".join(ROLES)}.</desc>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050C1A"/><stop offset=".55" stop-color="#0A1830"/><stop offset="1" stop-color="#0C2442"/></linearGradient>
<radialGradient id="halo" cx="{(box[0] + box[2]) / 2 / width:.3f}" cy="{(box[1] + box[3]) / 2 / height:.3f}" r="{0.55 if narrow else 0.42}"><stop offset="0" stop-color="{CYAN}" stop-opacity=".16"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<linearGradient id="name" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#BDEFFA"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3B82F6" stop-opacity=".22"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".26"/></linearGradient>
<linearGradient id="scan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".85" stop-color="{CYAN}" stop-opacity=".07"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".28"/></linearGradient>
<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#FFFFFF" stroke-opacity=".035"/></pattern>
<clipPath id="card"><rect width="{width}" height="{height}" rx="20"/></clipPath>
<clipPath id="netbox"><rect x="{bx0}" y="{by0}" width="{bx1 - bx0}" height="{scan_h}"/></clipPath>
<clipPath id="type"><rect class="tw" width="1" height="{role_size * 1.4:.1f}"/></clipPath>
</defs>
<style>
.tw{{transform:translate({rx:.1f}px,{ry - role_size * 0.95:.1f}px) scaleX({widths[0][0]:.2f});animation:tw {total}s step-end infinite}}
.caret{{transform:translateX({widths[0][0] + 3:.2f}px);animation:cp {total}s step-end infinite}}
.caret rect{{animation:blink 1.05s step-end infinite}}
.role{{fill:{INK}}}
.r1,.r2,.r3{{opacity:0}}
{"".join(f".r{i}{{animation:r{i} {total}s step-end infinite}}" for i in range(len(ROLES)))}
.sig{{stroke-dasharray:7 100;stroke-dashoffset:7;opacity:0;animation:sig 8s cubic-bezier(.45,0,.55,1) infinite}}
.glow{{animation:glow 5s ease-in-out infinite}}
.ring{{transform-box:fill-box;transform-origin:center;opacity:0;animation:ring 4.8s ease-out infinite}}
.scan{{animation:scan 9s linear infinite}}
@keyframes sig{{0%{{stroke-dashoffset:7;opacity:0}}6%{{opacity:1}}55%{{stroke-dashoffset:-100;opacity:1}}60%,100%{{stroke-dashoffset:-100;opacity:0}}}}
@keyframes glow{{0%,100%{{fill:#0B1E39}}50%{{fill:#1C6E8F}}}}
@keyframes ring{{0%{{transform:scale(1);opacity:.7}}60%,100%{{transform:scale(3.2);opacity:0}}}}
@keyframes scan{{0%{{transform:translateX(0)}}70%,100%{{transform:translateX({bx1 - bx0 + 150:.0f}px)}}}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
{css}
@media (prefers-reduced-motion:reduce){{.tw,.caret,.caret rect,.role,.sig,.glow,.ring,.scan{{animation:none}}.scan,.sig{{opacity:0}}}}
</style>
<g clip-path="url(#card)">
<rect width="{width}" height="{height}" fill="url(#bg)"/>
<rect width="{width}" height="{height}" fill="url(#grid)"/>
<rect width="{width}" height="{height}" fill="url(#halo)"/>
<g clip-path="url(#netbox)"><rect class="scan" x="{bx0 - 150}" y="{by0}" width="150" height="{scan_h}" fill="url(#scan)" style="transform:translateX(-9999px)"/></g>
{net}
{brackets(bx0, by0, bx1, by1)}
<path d="{label_d}" fill="{CYAN}" fill-opacity=".7"/>
<rect x="{tx}" y="{ky - 5}" width="16" height="2" fill="url(#rule)"/>
<path d="{kick_d}" fill="{CYAN_SOFT}" fill-opacity=".85"/>
<path d="{name_d}" fill="url(#name)"/>
<path d="{title_d}" fill="{CYAN}"/>
<path d="{prompt_d}" fill="{MUTED}"/>
<path d="{tag_d}" fill="{MUTED}"/>
<g clip-path="url(#type)">{roles_svg}</g>
<g class="caret" transform="translate(0 0)"><rect x="{rx}" y="{ry - role_size * 0.85:.1f}" width="{role_size * 0.5:.1f}" height="{caret_h:.1f}" fill="{CYAN}" fill-opacity=".85"/></g>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="19.5" fill="none" stroke="#7DD3FC" stroke-opacity=".14"/>
</g>
</svg>
'''


def divider():
    w, h = 1200, 28
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="presentation" aria-hidden="true">
<defs>
<linearGradient id="l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0EA5C6" stop-opacity="0"/><stop offset=".5" stop-color="#0EA5C6" stop-opacity=".75"/><stop offset="1" stop-color="#0EA5C6" stop-opacity="0"/></linearGradient>
<radialGradient id="dot"><stop offset="0" stop-color="#22D3EE"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></radialGradient>
</defs>
<style>.dot{{animation:run 7s ease-in-out infinite}}@keyframes run{{0%{{transform:translateX(160px);opacity:0}}15%{{opacity:1}}85%{{opacity:1}}100%{{transform:translateX(1040px);opacity:0}}}}@media (prefers-reduced-motion:reduce){{.dot{{animation:none;opacity:0}}}}</style>
<rect x="120" y="13.5" width="960" height="1" fill="url(#l)"/>
<rect x="594" y="8" width="12" height="12" transform="rotate(45 600 14)" fill="none" stroke="#0EA5C6" stroke-width="1.5"/>
<circle cx="600" cy="14" r="2" fill="#0EA5C6"/>
<circle class="dot" cx="0" cy="14" r="9" fill="url(#dot)" opacity="0"/>
</svg>
'''


def footer():
    w, h = 1200, 120
    rng = random.Random(3)
    pts = []
    for i in range(25):
        x = 120 + i * 40
        y = 52 + 14 * math.sin(i * 0.55) + rng.uniform(-4, 4)
        pts.append((x, y))
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    nodes = "".join(
        f'<circle class="n" style="animation-delay:{(i * 0.37) % 6:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="{3 if i % 4 else 4.5}"/>'
        for i, (x, y) in enumerate(pts))
    text_d, text_w = MONO.path("PHẠM NGỌC TRUNG  ·  AI ENGINEER", 15, 0, 0, tracking=0.16)
    tx = (w - text_w) / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{NAME}, {TITLE}">
<defs>
<linearGradient id="f" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0EA5C6" stop-opacity="0"/><stop offset=".5" stop-color="#0EA5C6" stop-opacity=".7"/><stop offset="1" stop-color="#0EA5C6" stop-opacity="0"/></linearGradient>
<mask id="m"><rect width="{w}" height="{h}" fill="url(#fm)"/></mask>
<linearGradient id="fm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".25" stop-color="#fff"/><stop offset=".75" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<style>.n{{fill:#0EA5C6;animation:p 6s ease-in-out infinite}}@keyframes p{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}@media (prefers-reduced-motion:reduce){{.n{{animation:none;opacity:.6}}}}</style>
<g mask="url(#m)"><path d="{line}" fill="none" stroke="url(#f)" stroke-width="1.2"/>{nodes}</g>
<path transform="translate({tx:.1f} 104)" d="{text_d}" fill="#0EA5C6"/>
</svg>
'''


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "hero.svg").write_text(hero(1200, 420, False), encoding="utf-8")
    (out / "hero-narrow.svg").write_text(hero(720, 616, True), encoding="utf-8")
    (out / "divider.svg").write_text(divider(), encoding="utf-8")
    (out / "footer.svg").write_text(footer(), encoding="utf-8")
    for f in sorted(out.glob("*.svg")):
        print(f.name, f.stat().st_size)
