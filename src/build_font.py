"""Génère la police Desson-Regular.ttf à partir des dessins de desson.py.

Usage : python build_font.py [--version 1.200] [--out ../Desson-Regular.ttf]
"""
import argparse
import os
import xml.etree.ElementTree as ET

import pathops
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

import desson

HERE = os.path.dirname(os.path.abspath(__file__))

# --- réglages ---
UPM = 1000
SCALE = 20          # 1 unité de la case de 40 = 20 unités de police
TOP = 700           # haut de la case, en unités de police (le bas est à -100)
SIDE_BEARING = 60   # marge identique à gauche et à droite de chaque dessin
SPACE = 500         # largeur de l'espace entre les mots
DIGIT_ADV = desson.DIGIT_W * SCALE
PUNCT_FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-ExtraLight.ttf')  # ponctuation (licence libre)
PUNCT = "!?.,;:'’\"“”«»()[]-–—…/%+=*&@#_¡¿°"
NO_SPACE_BEFORE = '!?:;»'

GLYPH_NAMES = {'é': 'eacute', 'è': 'egrave', 'in': 'in_'}


def gname(sound):
    return 's_' + GLYPH_NAMES.get(sound, sound)


def _el_to_d(e):
    t = e.tag
    a = e.attrib
    f = lambda k: float(a.get(k, 0))
    if t == 'line':
        return f"M{f('x1')} {f('y1')} L{f('x2')} {f('y2')}"
    if t in ('polyline', 'polygon'):
        p = a['points'].replace(',', ' ').split()
        d = 'M' + ' L'.join(f'{p[i]} {p[i + 1]}' for i in range(0, len(p), 2))
        return d + (' Z' if t == 'polygon' else '')
    if t == 'circle':
        cx, cy, r = f('cx'), f('cy'), f('r')
        return f"M{cx - r} {cy} A{r} {r} 0 1 0 {cx + r} {cy} A{r} {r} 0 1 0 {cx - r} {cy} Z"
    if t == 'ellipse':
        cx, cy, rx, ry = f('cx'), f('cy'), f('rx'), f('ry')
        return f"M{cx - rx} {cy} A{rx} {ry} 0 1 0 {cx + rx} {cy} A{rx} {ry} 0 1 0 {cx - rx} {cy} Z"
    if t == 'rect':
        x, y, w, h, r = f('x'), f('y'), f('width'), f('height'), f('rx')
        return (f"M{x + r} {y} L{x + w - r} {y} A{r} {r} 0 0 1 {x + w} {y + r} L{x + w} {y + h - r} "
                f"A{r} {r} 0 0 1 {x + w - r} {y + h} L{x + r} {y + h} A{r} {r} 0 0 1 {x} {y + h - r} "
                f"L{x} {y + r} A{r} {r} 0 0 1 {x + r} {y} Z")
    if t == 'path':
        return a['d']
    raise ValueError(t)


def outline(svg_body, ox):
    """Convertit des éléments SVG (traits et points) en un contour plein, décalé de ox."""
    acc = pathops.Path()
    for e in ET.fromstring(f'<g>{svg_body}</g>'):
        p = pathops.Path()
        parse_path(_el_to_d(e), TransformPen(p.getPen(), (SCALE, 0, 0, -SCALE, ox, TOP)))
        if e.attrib.get('fill', 'none') == 'none':
            cap = pathops.LineCap.BUTT_CAP if e.attrib.get('data-bar') else pathops.LineCap.ROUND_CAP
            p.stroke(float(e.attrib.get('stroke-width', desson.STROKE)) * SCALE, cap, pathops.LineJoin.ROUND_JOIN, 4)
            p.convertConicsToQuads()
        acc = pathops.op(acc, p, pathops.PathOp.UNION)
    acc.simplify()
    return acc


def ttglyph(path):
    pen = TTGlyphPen(None)
    path.draw(Cu2QuPen(pen, 1.0, reverse_direction=False))
    return pen.glyph()


def build(out, version):
    order, glyphs, adv = ['.notdef', 'space', 'zerospace'], {}, {}
    empty = pathops.Path()
    for g, w in (('.notdef', 860), ('space', SPACE), ('zerospace', 0)):
        glyphs[g], adv[g] = ttglyph(empty), w

    # sons : largeur proportionnelle au dessin
    for s in desson.CONSONANTS + desson.VOWELS:
        body = desson.GLYPHS[s]('#000')
        xmin, _, xmax, _ = outline(body, 0).bounds
        glyphs[gname(s)] = ttglyph(outline(body, SIDE_BEARING - xmin))
        adv[gname(s)] = round(xmax - xmin + 2 * SIDE_BEARING)
        order.append(gname(s))

    # chiffres : largeur fixe, barre sur toute la largeur pour former une barre continue
    for n in range(10):
        body = desson.digit_bar(0, desson.DIGIT_W, '#000') + desson.digit(n, '#000')
        glyphs[f'd{n}'], adv[f'd{n}'] = ttglyph(outline(body, 0)), DIGIT_ADV
        order.append(f'd{n}')

    # ponctuation empruntée à DejaVu Sans ExtraLight
    src = TTFont(PUNCT_FONT)
    gs, scmap, k = src.getGlyphSet(), src.getBestCmap(), UPM / src['head'].unitsPerEm
    punct = {}
    for ch in PUNCT:
        g = scmap.get(ord(ch))
        if not g:
            continue
        rec = DecomposingRecordingPen(gs)
        gs[g].draw(rec)
        pen = TTGlyphPen(None)
        rec.replay(TransformPen(pen, (k, 0, 0, k, 0, -60)))
        name = 'p_%04X' % ord(ch)
        glyphs[name], adv[name] = pen.glyph(), round(src['hmtx'][g][0] * k)
        order.append(name)
        punct[ord(ch)] = name

    # table de caractères
    cmap = {0x20: 'space', 0x2009: 'space', 0xA0: 'zerospace', 0x202F: 'zerospace'}
    cmap.update(punct)
    for ch, s in desson.KEYMAP.items():
        for c in {ch, ch.upper()}:
            if len(c) == 1:
                cmap[ord(c)] = gname(s)
    for n in range(10):
        cmap[ord(str(n))] = f'd{n}'

    ps = 'Desson-Regular'
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    glyf = fb.font['glyf']

    def lsb(g):
        gl = glyf[g]
        gl.recalcBounds(glyf)
        return gl.xMin if gl.numberOfContours else 0

    fb.setupHorizontalMetrics({g: (adv[g], lsb(g)) for g in order})
    fb.setupHorizontalHeader(ascent=850, descent=-250)
    fb.setupNameTable({'familyName': 'Desson', 'styleName': 'Regular',
                       'uniqueFontIdentifier': f'{ps};{version}', 'fullName': 'Desson Regular',
                       'psName': ps, 'version': f'Version {version}'})
    fb.setupOS2(sTypoAscender=850, sTypoDescender=-250, sTypoLineGap=100, usWinAscent=900, usWinDescent=300,
                usWeightClass=400, fsType=0, achVendID='DESN', fsSelection=0x40,
                ulUnicodeRange1=0b111 | (1 << 31), ulCodePageRange1=1)
    fb.setupPost()
    fb.font['head'].fontRevision = float(version)

    # pas d'espace visible devant ! ? : ; » ni après «
    before = ' '.join(punct[ord(c)] for c in NO_SPACE_BEFORE if ord(c) in punct)
    addOpenTypeFeaturesFromString(fb.font, f"""
languagesystem DFLT dflt; languagesystem latn dflt;
feature calt {{
  sub space' [{before}] by zerospace;
  sub {punct[ord('«')]} space' by zerospace;
}} calt;""")
    fb.save(out)
    print('police générée :', out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', default='1.200')
    ap.add_argument('--out', default=os.path.join(HERE, '..', 'Desson-Regular.ttf'))
    a = ap.parse_args()
    build(os.path.abspath(a.out), a.version)
