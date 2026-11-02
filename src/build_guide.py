"""Génère le guide imprimable desson-guide.pdf (2 pages A4).

Page 1 : les sons et les chiffres. Page 2 : des exemples, composés avec la police
Desson elle-même (lancer build_font.py avant).

Usage : python build_guide.py [--font ../Desson-Regular.ttf] [--out ../desson-guide.pdf]
"""
import argparse
import os
import pathlib

from playwright.sync_api import sync_playwright

import desson

HERE = os.path.dirname(os.path.abspath(__file__))
INK, VOWEL, DIGIT = '#222', '#D85A30', '#185FA5'

EXAMPLES = [  # (français, saisie Desson)
    ('café', 'kafé'), ('chocolat', 'ĉokola'), ('bonjour', 'bôjûr'), ('maison', 'mèzô'),
    ('oiseau', 'ûazo'), ('musique', 'muzik'), ('lapin', 'lapî'), ('vacances', 'vakâs'),
    ('heureux', 'êrê'), ("je t'aime", 'jê tèm'), ('gâteau', 'gato'), ('un secret', 'î sêkrè'),
    ('viens', 'viî'), ('yeux', 'yê'), ('travail', 'travay'),
    ('Salut ! Tu viens jouer au parc à 15 heures ?', 'salu ! tu viî jûé o park a 15 êr ?'),
]
NUMBERS = ['15', '2026', '407']


def svg(size, body, w=40):
    return f'<svg width="{size * w / 40:.0f}" height="{size}" viewBox="0 0 {w} 40">{body}</svg>'


def card(sound):
    color = VOWEL if sound in desson.VOWELS else INK
    ks = desson.keys(sound)
    kbd = ''.join(f'<kbd class="{"alt" if k in desson.ALT_KEYS else ""}">{k}</kbd>' for k in ks)
    return (f'<div class="c">{svg(44, desson.GLYPHS[sound](color))}<b>{sound}</b>'
            f'<span>{desson.HOOKS[sound]}</span><div class="keys">{kbd}</div></div>')


def digit_card(n):
    body = desson.digit_bar(0, desson.DIGIT_W, DIGIT) + desson.digit(n, DIGIT)
    return f'<div class="c d">{svg(40, body, desson.DIGIT_W)}<b>{n}</b></div>'


def html(font_url):
    cons = ''.join(card(s) for s in desson.CONSONANTS)
    vows = ''.join(card(s) for s in desson.VOWELS)
    digs = ''.join(digit_card(n) for n in range(10))
    ex = ''.join(f'<div class="ex"><span>{fr}</span><span class="ds">{ds}</span><code>{ds}</code></div>'
                 for fr, ds in EXAMPLES)
    nums = ''.join(f'<div class="ex"><span>{n}</span><span class="ds num">{n}</span></div>' for n in NUMBERS)
    return f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><style>
@font-face{{font-family:Desson;src:url("{font_url}")}}
@page{{size:A4;margin:13mm}}
body{{font-family:"DejaVu Sans",Arial,sans-serif;color:{INK};margin:0;font-size:12px}}
h1{{font-size:22px;margin:0}} .sub{{color:#777;margin:2px 0 10px}}
h2{{font-size:15px;margin:14px 0 6px}} p,li{{line-height:1.45;color:#444}}
.g{{display:grid;grid-template-columns:repeat(7,1fr);gap:7px}}
.c{{display:flex;flex-direction:column;align-items:center;padding:6px 2px;border:1px solid #ddd;border-radius:6px}}
.c b{{font-size:15px}} .c span{{font-size:10px;color:#777}}
.keys{{display:flex;gap:3px;margin-top:2px}}
.c kbd{{font:11px monospace;background:#f3f3f1;border:1px solid #ddd;border-radius:3px;padding:0 4px}}
.c kbd.alt{{background:#fff;border-style:dashed;color:#777}}
.d{{padding:6px 0}}
.pb{{break-before:page}}
.ex{{display:flex;align-items:baseline;gap:16px;margin:8px 0}}
.ex span:first-child{{min-width:120px;max-width:200px;color:#555;font-size:12px}}
.ds{{font-family:Desson;font-size:30px;color:{INK}}} .num{{color:{DIGIT}}}
.ex code{{font-size:11px;color:#999}}
</style></head><body>
<h1>Desson</h1><p class="sub">Des sons dessinés : un dessin par son.</p>
<p>On écrit les <b>sons</b>, pas les lettres. Chaque son a son dessin : un objet dont le nom commence par ce son
(sauf le peigne et le pont, où on l'entend à la fin). Un seul signe pour les deux « eu » (peu, peur).
Au clavier, un caractère par son : le circonflexe marque les sons composés (â an, î in, ô on, û ou, ê eu, ĉ ch, ĝ gn) ;
en secours (touches en pointillés), x ou ç pour ch, q ou ñ pour gn.</p>
<h2>Les consonnes</h2><div class="g">{cons}</div>
<h2>Les voyelles</h2><div class="g">{vows}</div>
<h2>Les chiffres (comme sur le soroban)</h2>
<p>Chaque chiffre est posé <b>sous une barre</b> : petit rond = 0, point = 1, trait = 2, V = 3, + = 4.
Pour 5 à 9, on ajoute <b>la perle du haut</b> (un point au-dessus de la barre, +5). Les chiffres d'un nombre partagent la même barre.</p>
<div class="g" style="grid-template-columns:repeat(10,1fr)">{digs}</div>
<div class="pb"></div><h2>Exemples</h2>
<p>On écrit ce qu'on entend : les lettres muettes disparaissent, « oi » s'écrit « ou » + « a », « un » s'écrit comme « in », et on met « i » ou « y » selon ce qu'on entend (viens, yeux).</p>
{ex}{nums}
</body></html>'''


def build(font, out):
    page = os.path.join(HERE, '_guide.html')
    pathlib.Path(page).write_text(html(pathlib.Path(font).as_uri()), encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(pathlib.Path(page).as_uri())
        pg.wait_for_timeout(300)
        pg.pdf(path=out, format='A4', print_background=True, prefer_css_page_size=True)
        b.close()
    os.remove(page)
    print('guide généré :', out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--font', default=os.path.join(HERE, '..', 'Desson-Regular.ttf'))
    ap.add_argument('--out', default=os.path.join(HERE, '..', 'desson-guide.pdf'))
    a = ap.parse_args()
    build(os.path.abspath(a.font), os.path.abspath(a.out))
