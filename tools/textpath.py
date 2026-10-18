"""Shape text with HarfBuzz and return it as SVG path data, so SVGs need no web fonts."""
import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont


def _num(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Font:
    def __init__(self, path):
        face = hb.Face(hb.Blob.from_file_path(path))
        self.hb = hb.Font(face)
        self.upem = face.upem
        tt = TTFont(path)
        self.glyphs = tt.getGlyphSet()
        self.order = tt.getGlyphOrder()

    def shape(self, text, size, tracking=0.0):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        s = size / self.upem
        out, pen_x = [], 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((self.order[info.codepoint], (pen_x + pos.x_offset) * s, pos.y_offset * s))
            pen_x += pos.x_advance + tracking * self.upem
        width = (pen_x - tracking * self.upem) * s
        return out, width, s

    def width(self, text, size, tracking=0.0):
        return self.shape(text, size, tracking)[1]

    def path(self, text, size, x, y, tracking=0.0):
        glyphs, width, s = self.shape(text, size, tracking)
        parts = []
        for name, gx, gy in glyphs:
            pen = SVGPathPen(self.glyphs, ntos=_num)
            self.glyphs[name].draw(TransformPen(pen, (s, 0, 0, -s, x + gx, y - gy)))
            cmd = pen.getCommands()
            if cmd:
                parts.append(cmd)
        return "".join(parts), width
