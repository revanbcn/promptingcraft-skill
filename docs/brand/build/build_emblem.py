"""PromptingCraft.com emblem (approved concept C2, Forged Intelligence): one geometry, several variants."""
from pathlib import Path

OUT = Path(__file__).parent / 'svg'  # copy the results into docs/brand/
OUT.mkdir(exist_ok=True)

HEX = 'M256 22 L440 128 V384 L256 490 L72 384 V128 Z'

# Full emblem geometry (512 units). The P is one gold ribbon: the stem in front, the bowl
# folded behind it at the top, an intelligence core held in the counter.
STEM = 'M172 128 H228 V374 L200 404 L172 376 Z'
BOWL = ('M228 128 H282 C322 128 350 162 350 214 C350 266 322 300 282 300 H228 V250 H280 '
        'C292 250 300 234 300 214 C300 194 292 178 280 178 H228 Z')
FOLD = 'M192 128 H228 V164 Z'
CORE = 'M264 193 L282 203.5 V224.5 L264 235 L246 224.5 V203.5 Z'
TRACE = 'M280 214 H302'

# Micro geometry for 16-48 px: heavier ribbon, larger core, no fold, trace or shading.
M_STEM = 'M156 124 H236 V400 H156 Z'
M_BOWL = ('M236 124 H286 C336 124 372 162 372 218 C372 274 336 312 286 312 H236 V250 H282 '
          'C298 250 306 236 306 218 C306 200 298 186 282 186 H236 Z')
M_CORE = 'M264 186 L292 202 V234 L264 250 L236 234 V202 Z'

PALETTES = {
    # dark tile: works on light and dark pages
    'dark': dict(tile=('#272C35', '#0D1014'), rim=('#F5D687', '#C99232', '#8C5E1C'),
                 stem=('#F8DD92', '#D9A645', '#AE7826'), bowl=('#E3B052', '#A06C1C'),
                 fold='#7E5214', core='#43E2F7', halo='#43E2F7', edge=None),
    # light tile for light layouts that need a pale mark
    'light': dict(tile=('#FBF8F1', '#EAE2D1'), rim=('#D9A548', '#B07A26', '#7C5216'),
                  stem=('#D7A13F', '#B9832A', '#8F5D17'), bowl=('#B37A22', '#7E5011'),
                  fold='#6A430E', core='#0B9CBC', halo='#0B9CBC', edge=None, halo_op='0.18'),
}


def grad(gid, stops, x2='0', y2='1'):
    step = 1 / (len(stops) - 1)
    body = ''.join(f'<stop offset="{i * step:.2f}" stop-color="{c}"/>' for i, c in enumerate(stops))
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">{body}</linearGradient>'


def svg(body, defs='', title='PromptingCraft.com'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" '
            f'role="img" aria-label="{title}"><title>{title}</title>'
            f'{"<defs>" + defs + "</defs>" if defs else ""}{body}</svg>\n')


def full(name, p):
    defs = (grad('t', p['tile']) + grad('r', p['rim'], '1', '1') + grad('s', p['stem'])
            + grad('b', p['bowl'], '1', '1')
            + f'<radialGradient id="h"><stop offset="0" stop-color="{p["halo"]}" stop-opacity="{p.get("halo_op", "0.45")}"/>'
              f'<stop offset="1" stop-color="{p["halo"]}" stop-opacity="0"/></radialGradient>')
    body = (f'<path d="{HEX}" fill="url(#t)"/>'
            f'<path d="{HEX}" fill="none" stroke="url(#r)" stroke-width="20" stroke-linejoin="round"/>'
            f'<path d="{BOWL}" fill="url(#b)"/>'
            f'<path d="{STEM}" fill="url(#s)"/>'
            f'<path d="{FOLD}" fill="{p["fold"]}"/>'
            f'<circle cx="264" cy="214" r="40" fill="url(#h)"/>'
            f'<path d="{TRACE}" stroke="{p["core"]}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="{CORE}" fill="{p["core"]}"/>')
    (OUT / f'{name}.svg').write_text(svg(body, defs))


def micro(name, tile, rim, gold, core):
    body = (f'<path d="{HEX}" fill="{tile}" stroke="{rim}" stroke-width="30" stroke-linejoin="round"/>'
            f'<path d="{M_BOWL}" fill="{gold}"/><path d="{M_STEM}" fill="{gold}"/>'
            f'<path d="{M_CORE}" fill="{core}"/>')
    (OUT / f'{name}.svg').write_text(svg(body))


def mono(name, geometry):
    stem, bowl, core = geometry
    body = (f'<path d="{HEX}" fill="none" stroke="currentColor" stroke-width="24" stroke-linejoin="round"/>'
            f'<path d="{bowl}" fill="currentColor"/><path d="{stem}" fill="currentColor"/>'
            f'<path d="{core}" fill="currentColor"/>')
    (OUT / f'{name}.svg').write_text(svg(body).replace('<svg ', '<svg fill="currentColor" ', 1))


full('emblem', PALETTES['dark'])
full('emblem-light', PALETTES['light'])
micro('emblem-micro', '#15191F', '#D9A645', '#E6B04C', '#43E2F7')
micro('emblem-micro-light', '#FBF8F1', '#B07A26', '#B9832A', '#0B9CBC')
mono('emblem-mono', (STEM, BOWL, CORE))
mono('emblem-micro-mono', (M_STEM, M_BOWL, M_CORE))
print('\n'.join(sorted(p.name for p in OUT.glob('*.svg'))))
