"""Project cards and the stack panel, laid out in HTML and rendered by Chromium into WebP/PNG images."""
import asyncio
import base64
import io
import os
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

HERE = Path(__file__).parent
SHOTS = HERE / "shots"
FONTS = HERE / "fonts"

PROJECTS = [
    dict(slug="veyra", num="01", name="Veyra", kind="Industrial machine vision and AI inspection",
         chips=["Commercial · since 2022", "72 vision and AI tools", "55 of 60 models verified on CPU"],
         dark="veyra-design-dark.png", light="veyra-design-light.png"),
    dict(slug="fluentqt", num="02", name="FluentQt", kind="Fluent Design UI framework for PyQt5",
         chips=["Community and Pro", "177 widgets in 12 families", "Maintained since 2022"],
         dark="fq-gallery-layouts-dark", light="fq-gallery-dashboard-charts-light"),
    dict(slug="comic-translator", num="03", name="ComicTranslator", kind="Local manga and comic translation",
         chips=["Detect · OCR · translate · inpaint · letter", "GGUF LLM through llama.cpp"],
         dark="comic-editor-dark.jpg", light="comic-editor.jpg"),
    dict(slug="legal-intelligence", num="04", name="Vietnamese Legal Intelligence",
         kind="Legal research workstation", chips=["3,765 documents", "120,000 citations in Neo4j", "BM25 + E5 hybrid retrieval"],
         dark="vli-graph_relations-dark.png", light="vli-graph_relations-light.png"),
]

STACK = [
    ("LLM, VLM and RAG", "llm", ["Gemini", "Vertex AI", "Ollama", "vLLM", "SGLang", "llama.cpp", "LoRA/QLoRA", "pgvector", "Neo4j"]),
    ("ML and vision", "vision", ["PyTorch", "TensorFlow", "ONNX Runtime", "OpenCV", "Ultralytics", "Anomalib"]),
    ("Software", "code", ["Python", "C#", "SQL", "TypeScript", "FastAPI", "Flask", "Django", "PyQt5", "PySide6", "FluentQt", "Next.js"]),
    ("Industrial and edge", "chip", ["PLC integration", "OPC UA", "Modbus RTU/TCP", "MQTT", "ESP32", "STM32", "NVIDIA Jetson"]),
    ("Data", "data", ["PostgreSQL", "SQLite", "DuckDB", "MongoDB", "MinIO"]),
]

ICONS = {
    "llm": '<path d="M4 6h16v10H9l-5 4z"/><path d="M8 10h8M8 13h5"/>',
    "vision": '<path d="M3 8V4h4M17 4h4v4M21 16v4h-4M7 20H3v-4"/><circle cx="12" cy="12" r="3.2"/>',
    "code": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M13.5 5l-3 14"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    "data": '<ellipse cx="12" cy="6" rx="7" ry="2.6"/><path d="M5 6v12c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6V6M5 12c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6"/>',
}

THEMES = {
    "dark": dict(bg="linear-gradient(135deg,#061024 0%,#0A1A33 55%,#0C2442 100%)", border="rgba(125,211,252,.16)",
                 title="#EAF4FF", text="#9DB2CC", num="#22D3EE", chipbg="rgba(34,211,238,.08)",
                 chipborder="rgba(34,211,238,.28)", chip="#8BEBFA", glow="rgba(34,211,238,.22)",
                 grid="rgba(255,255,255,.035)", shadow="0 30px 60px rgba(0,0,0,.55)", frame="rgba(125,211,252,.22)",
                 tile="rgba(255,255,255,.025)"),
    "light": dict(bg="linear-gradient(135deg,#FFFFFF 0%,#F2F7FC 60%,#E7F1F9 100%)", border="#D3E2F0",
                  title="#0B1B33", text="#43597A", num="#0891B2", chipbg="#E4F4F9", chipborder="#B9E1EC",
                  chip="#0B6E86", glow="rgba(8,145,178,.16)", grid="rgba(11,27,51,.04)",
                  shadow="0 24px 48px rgba(15,40,80,.18)", frame="#C9D9E8", tile="rgba(255,255,255,.7)"),
}


def fontface():
    rules = []
    for fam, file, w in [("Inter", "inter/extras/ttf/Inter-Regular.ttf", 400), ("Inter", "inter/extras/ttf/Inter-Medium.ttf", 500),
                         ("Inter", "inter/extras/ttf/Inter-SemiBold.ttf", 600), ("Inter", "inter/extras/ttf/Inter-Bold.ttf", 700),
                         ("Inter", "inter/extras/ttf/Inter-ExtraBold.ttf", 800),
                         ("JBM", "jbm/fonts/ttf/JetBrainsMono-Medium.ttf", 500)]:
        rules.append(f"@font-face{{font-family:{fam};font-weight:{w};src:url('file://{(FONTS / file).resolve()}')}}")
    return "".join(rules)


def data_uri(path, max_w):
    im = Image.open(path).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:transparent}
body{font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.card{position:relative;overflow:hidden;border-radius:28px;background:var(--bg);border:2px solid var(--border)}
.grid{position:absolute;inset:0;background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:56px 56px}
.num{font-family:JBM;font-weight:500;color:var(--num);letter-spacing:.18em;font-size:22px;display:flex;align-items:center;gap:14px}
.num:before{content:"";width:34px;height:3px;background:var(--num);border-radius:2px}
.name{color:var(--title);font-weight:800;letter-spacing:-.02em;line-height:1.04}
.kind{color:var(--text);font-weight:500;line-height:1.3}
.chips{display:flex;flex-wrap:wrap;gap:12px}
.chip{font-family:JBM;font-weight:500;color:var(--chip);background:var(--chipbg);border:1.5px solid var(--chipborder);border-radius:999px;white-space:nowrap}
.shot{position:absolute;border-radius:16px;overflow:hidden;border:2px solid var(--frame);box-shadow:var(--shadow)}
.shot img{display:block;width:100%}
.glow{position:absolute;border-radius:50%;background:radial-gradient(closest-side,var(--glow),transparent)}
"""


def vars_css(t):
    th = THEMES[t]
    return ":root{" + "".join(f"--{k}:{v};" for k, v in th.items()) + "}"


def card_html(p, theme, narrow):
    shot = data_uri(SHOTS / p[theme], 1800)
    chips = "".join(f'<span class="chip">{c}</span>' for c in p["chips"])
    long_name = len(p["name"]) > 16
    if narrow:
        w, h = 960, None
        body = f"""
<div class="glow" style="left:80px;top:40px;width:800px;height:560px"></div>
<div style="position:relative;padding:48px 48px 60px">
  <div class="shot" style="position:relative">{f'<img src="{shot}">'}</div>
  <div style="padding:0 8px;margin-top:52px">
    <div class="num">{p['num']}</div>
    <div class="name" style="font-size:{60 if long_name else 72}px;margin-top:20px">{p['name']}</div>
    <div class="kind" style="font-size:32px;margin-top:14px">{p['kind']}</div>
    <div class="chips" style="margin-top:28px">{chips.replace('class="chip"', 'class="chip" style="font-size:22px;padding:9px 18px"')}</div>
  </div>
</div>"""
    else:
        w, h = 1600, 680
        body = f"""
<div class="glow" style="left:620px;top:20px;width:1000px;height:700px"></div>
<div style="position:absolute;left:72px;top:0;bottom:0;width:{520 if not long_name else 540}px;display:flex;flex-direction:column;justify-content:center">
  <div class="num">{p['num']}</div>
  <div class="name" style="font-size:{60 if long_name else 76}px;margin-top:24px">{p['name']}</div>
  <div class="kind" style="font-size:28px;margin-top:18px">{p['kind']}</div>
  <div class="chips" style="margin-top:34px;flex-direction:column;align-items:flex-start">{chips.replace('class="chip"', 'class="chip" style="font-size:19px;padding:8px 16px"')}</div>
</div>
<div class="shot" style="left:660px;top:64px;width:880px">{f'<img src="{shot}">'}</div>"""
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{fontface()}{BASE_CSS}{vars_css(theme)}</style></head>
<body><div class="card" id="c" style="width:{w}px;{f'height:{h}px' if h else ''}"><div class="grid"></div>{body}</div></body></html>"""
    return html, w, h


def stack_html(theme, narrow):
    th = THEMES[theme]
    tiles = []
    for i, (title, icon, items) in enumerate(STACK):
        span = "grid-column:1/-1;" if (not narrow and i == len(STACK) - 1) else ""
        pills = "".join(f'<span class="chip" style="font-size:{24 if narrow else 21}px;padding:{"9px 18px" if narrow else "8px 16px"}">{x}</span>' for x in items)
        tiles.append(f"""<div class="tile" style="{span}">
<div class="th"><svg viewBox="0 0 24 24" width="{40 if narrow else 36}" height="{40 if narrow else 36}" fill="none" stroke="{th['num']}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</svg>
<span style="font-size:{32 if narrow else 28}px">{title}</span></div><div class="chips">{pills}</div></div>""")
    w = 960 if narrow else 1600
    cols = "1fr" if narrow else "1fr 1fr"
    css = f"""
.wrap{{padding:{40 if narrow else 44}px;display:grid;grid-template-columns:{cols};gap:{24 if narrow else 22}px;position:relative}}
.tile{{background:var(--tile);border:1.5px solid var(--border);border-radius:20px;padding:{30 if narrow else 28}px}}
.th{{display:flex;align-items:center;gap:16px;color:var(--title);font-weight:700;margin-bottom:22px}}
"""
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{fontface()}{BASE_CSS}{vars_css(theme)}{css}</style></head>
<body><div class="card" id="c" style="width:{w}px"><div class="grid"></div><div class="wrap">{''.join(tiles)}</div></div></body></html>"""
    return html, w


async def render(page, html, path, w, fmt):
    tmp = HERE / "render.html"
    tmp.write_text(html, encoding="utf-8")
    await page.set_viewport_size({"width": w + 40, "height": 1400})
    await page.goto(f"file://{tmp.resolve()}")
    await page.evaluate("document.fonts.ready")
    # single long words (ComicTranslator) must shrink rather than overflow into the screenshot
    await page.evaluate("""() => { for (const el of document.querySelectorAll('.name')) {
        let fs = parseFloat(getComputedStyle(el).fontSize);
        while (el.scrollWidth > el.clientWidth && fs > 30) { fs -= 2; el.style.fontSize = fs + 'px'; } } }""")
    png = await page.locator("#c").screenshot(omit_background=True)
    im = Image.open(io.BytesIO(png))
    if fmt == "webp":
        im.save(path, "WEBP", quality=86, method=6)
    else:
        im = im.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
        im.save(path, "PNG", optimize=True)
    print(path.name, im.size, path.stat().st_size)


async def main(out):
    (out / "projects").mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, LD_LIBRARY_PATH=os.environ.get("CHROME_LIBS", ""))
    async with async_playwright() as pw:
        b = await pw.chromium.launch(env=env)
        page = await b.new_page()
        for p in PROJECTS:
            for theme in ("dark", "light"):
                for narrow in (False, True):
                    html, w, h = card_html(p, theme, narrow)
                    suffix = "-narrow" if narrow else ""
                    await render(page, html, out / "projects" / f"{p['slug']}-{theme}{suffix}.webp", w, "webp")
        for theme in ("dark", "light"):
            for narrow in (False, True):
                html, w = stack_html(theme, narrow)
                await render(page, html, out / f"stack-{theme}{'-narrow' if narrow else ''}.png", w, "png")
        await b.close()


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1])))
