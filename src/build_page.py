"""Met à jour index.html à partir de desson.py.

Réécrit le bloc compris entre les repères DESSON:GENERATED:BEGIN et DESSON:GENERATED:END :
les dessins (D), les chiffres (DG), la saisie clavier (CMAP), les touches affichées (KEYS),
les objets-repères (HOOKS) et l'ordre des sons (VOWELS, CONSONANTS).
Le reste de la page (mise en page, interface) n'est pas touché.

Usage : python build_page.py [--page ../index.html]
"""
import argparse
import json
import os
import re

import desson

HERE = os.path.dirname(os.path.abspath(__file__))
BEGIN, END = '/* DESSON:GENERATED:BEGIN */', '/* DESSON:GENERATED:END */'
TOKEN = '__COLOR__'


def js_fn(svg):
    """Transforme un SVG (couleur = TOKEN) en fonction JS c => `...${c}...`."""
    assert '`' not in svg and '${' not in svg
    return 'c=>`' + svg.replace(TOKEN, '${c}') + '`'


def generated():
    sounds = desson.CONSONANTS + desson.VOWELS
    j = lambda v: json.dumps(v, ensure_ascii=False)
    lines = [
        BEGIN,
        '/* Généré par src/build_page.py à partir de src/desson.py : ne pas modifier à la main. */',
        f'const VOWELS={j(desson.VOWELS)},CONSONANTS={j(desson.CONSONANTS)};',
        'const D={',
        *[f'{j(s)}:{js_fn(desson.GLYPHS[s](TOKEN))},' for s in sounds],
        '};',
        f'const DIGIT_W={desson.DIGIT_W};',
        'const DG=[',
        *[f'{js_fn(desson.digit(n, TOKEN))},' for n in range(10)],
        '];',
        f'const CMAP={j(desson.KEYMAP)};',
        f'const KEYS={j({s: desson.keys(s) for s in sounds})};',
        f'const HOOKS={j(desson.HOOKS)};',
        END,
    ]
    return '\n'.join(lines)


def build(page):
    with open(page, encoding='utf-8') as f:
        html = f.read()
    pattern = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END), re.S)
    if not pattern.search(html):
        raise SystemExit(f'Repères {BEGIN} / {END} introuvables dans {page}')
    html = pattern.sub(lambda _: generated(), html)
    with open(page, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('page mise à jour :', page)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--page', default=os.path.join(HERE, '..', 'index.html'))
    build(os.path.abspath(ap.parse_args().page))
