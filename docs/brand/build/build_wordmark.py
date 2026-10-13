"""PromptingCraft.com wordmark and lockups: Geist (SIL OFL 1.1) outlined, so no font is needed."""
import io
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = Path(__file__).parent
# Usage: python build_wordmark.py <path to geist-latin-wght-normal.woff2 from @fontsource-variable/geist>
SRC = Path(sys.argv[1])
OUT = HERE / 'svg'
EMBLEM = (OUT / 'emblem.svg').read_text()


def instance(weight):
    font = TTFont(SRC)
    font.flavor = None
    inst = instantiateVariableFont(font, {'wght': weight})
    buf = io.BytesIO()
    inst.save(buf)
    return inst, buf.getvalue()


def shape(text, weight, size, x0, baseline, tracking=0.0):
    """Return (svg path d, advance) for text set at `size` px with HarfBuzz kerning."""
    font, data = instance(weight)
    upem = font['head'].unitsPerEm
    hbfont = hb.Font(hb.Face(data))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {'kern': True, 'liga': True})
    glyphs = font.getGlyphSet()
    order = font.getGlyphOrder()
    scale = size / upem
    pen = SVGPathPen(glyphs)
    x = 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x0 + (x + pos.x_offset) * scale, baseline))
        glyphs[name].draw(tpen)
        x += pos.x_advance + tracking * upem
    return pen.getCommands(), x * scale


def wordmark(size, x0, baseline, main, quiet):
    d1, w1 = shape('PromptingCraft', 640, size, x0, baseline, tracking=-0.012)
    d2, w2 = shape('.com', 430, size, x0 + w1 + size * 0.01, baseline, tracking=-0.004)
    return (f'<path d="{d1}" fill="{main}"/><path d="{d2}" fill="{quiet}"/>', w1 + w2 + size * 0.01)


def emblem_group(x, y, h):
    inner = EMBLEM.split('>', 1)[1].rsplit('</svg>', 1)[0]
    inner = inner.replace('<title>PromptingCraft.com</title>', '')
    return f'<g transform="translate({x} {y}) scale({h / 512})">{inner}</g>'


def write(name, w, h, body):
    (OUT / name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
        f'role="img" aria-label="PromptingCraft.com"><title>PromptingCraft.com</title>{body}</svg>\n')


THEMES = {'light': ('#17181C', '#6A665F'), 'dark': ('#F4F1EA', '#A39F96')}
for theme, (main, quiet) in THEMES.items():
    # Wordmark alone (cap height ~ 0.7 * size).
    body, width = wordmark(64, 0, 62, main, quiet)
    write(f'wordmark-{theme}.svg', width + 2, 80, body)
    # Horizontal lockup: emblem 80 high, text optically centred on it.
    body, width = wordmark(46, 96, 56, main, quiet)
    write(f'lockup-{theme}.svg', 96 + width + 4, 80, emblem_group(0, 0, 80) + body)
print(sorted(p.name for p in OUT.glob('*mark*.svg')) + sorted(p.name for p in OUT.glob('lockup*.svg')))
