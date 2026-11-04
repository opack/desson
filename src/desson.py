"""Desson : définition des dessins, des chiffres et de la saisie clavier.

Chaque dessin est décrit en SVG dans une case de 40 x 40 (y vers le bas).
Ces définitions doivent rester identiques à celles de index.html (objet D).
"""
import math

STROKE = 2.2  # épaisseur du trait, en unités de la case


def _st(c, w=STROKE):
    return f'fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


def _line(x1, y1, x2, y2, c, w=STROKE):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {_st(c, w)}/>'


def _dot(x, y, c, r=2.0):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def _pts(points):
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in points)


_SPIRAL = _pts([(20 + (2 + i / 60 * 11) * math.cos(i / 60 * math.pi * 2.5),
                 20 + (2 + i / 60 * 11) * math.sin(i / 60 * math.pi * 2.5)) for i in range(61)])

# son -> fonction(couleur) -> éléments SVG
GLYPHS = {
    # consonnes
    'p': lambda c: f'<path d="M35 11 C26 30 8 30 8 20 C8 10 26 10 35 29" {_st(c)}/>',
    'b': lambda c: f'<path d="M5 15 L35 15 A15 15 0 0 1 5 15 Z" {_st(c)}/>',
    't': lambda c: f'<polyline points="7,29 20,10 33,29" {_st(c)}/>',
    'd': lambda c: f'<polygon points="20,5 32,20 20,35 8,20" {_st(c)}/>',
    'k': lambda c: f'<path d="M25 34 L25 14 Q25 7 18.5 7 Q12 7 12 14" {_st(c)}/>',
    'g': lambda c: f'<path d="M5 12 Q8 26 20 26 Q32 26 35 12" {_st(c)}/>' + _line(20, 26, 20, 35, c),
    'f': lambda c: f'<polyline points="12,4 12,16 28,16 28,4" {_st(c)}/>' + _line(20, 4, 20, 36, c),
    'v': lambda c: f'<path d="M5 22 C12 8 18 8 20 20 C22 32 28 32 35 18" {_st(c)}/>',
    's': lambda c: f'<polygon points="9,6 31,6 9,34 31,34" {_st(c)}/>',
    'z': lambda c: f'<polyline points="25,4 12,20 27,20 14,36" {_st(c)}/>',
    'ch': lambda c: _line(12, 5, 12, 35, c) + f'<polyline points="12,24 31,24 31,35" {_st(c)}/>',  # chaise de profil
    'j': lambda c: f'<polygon points="15,8 25,8 34,32 6,32" {_st(c)}/>',  # jupe
    'm': lambda c: f'<path d="M4 9 Q16 5 20 33 Q24 5 36 9" {_st(c)}/>',  # mouette, ailes bombées
    'n': lambda c: f'<path d="M4 28 L15 28 C27 28 28 10 20 10 C12 10 13 28 25 28 L36 28" {_st(c)}/>',  # corde nouée
    'gn': lambda c: _line(8, 9, 32, 9, c) + ''.join(_line(x, 9, x, 32, c) for x in (12, 20, 28)),
    'l': lambda c: f'<path d="M25 6 A14 14 0 1 0 25 34 A11 11 0 1 1 25 6 Z" {_st(c)}/>',
    'r': lambda c: f'<circle cx="20" cy="20" r="13" {_st(c)}/>' + _line(7, 20, 33, 20, c) + _line(20, 7, 20, 33, c),
    'y': lambda c: _line(20, 4, 20, 20, c) + f'<circle cx="20" cy="27" r="7" {_st(c)}/>',
    # voyelles
    'a': lambda c: f'<rect x="10" y="5" width="20" height="30" rx="1" {_st(c)}/>' + _line(20, 5, 20, 35, c),
    'i': lambda c: _line(4, 29, 36, 29, c) + f'<path d="M11 29 Q20 10 29 29" {_st(c)}/>',
    'é': lambda c: _line(20, 6, 20, 34, c) + _line(8, 13, 32, 27, c) + _line(8, 27, 32, 13, c),
    'è': lambda c: f'<polyline points="8,8 20,34 32,8" {_st(c)}/>' + _line(20, 34, 20, 6, c),
    'o': lambda c: f'<ellipse cx="20" cy="20" rx="14" ry="8" {_st(c)}/>',
    'ou': lambda c: f'<polyline points="{_SPIRAL}" {_st(c)}/>',
    'u': lambda c: f'<polyline points="6,28 18,12 18,28 30,12 30,28" {_st(c)}/>',
    'eu': lambda c: _dot(14, 26, c, 2.6) + _line(14, 26, 14, 6, c) + _line(14, 26, 30, 26, c),
    'an': lambda c: f'<polygon points="6,7 34,7 20,24" {_st(c)}/>' + _line(20, 24, 20, 35, c),
    'in': lambda c: f'<path d="M20 20 C14 10 4 10 4 20 C4 30 14 30 20 20 C26 10 36 10 36 20 C36 30 26 30 20 20 Z" {_st(c)}/>',
    'on': lambda c: f'<path d="M11 33 C11 5 29 5 29 33 Q20 26 11 33 Z" {_st(c)}/>',  # ongle : arche étroite fermée par un arc vers le haut
}

CONSONANTS = ['p', 'b', 't', 'd', 'k', 'g', 'f', 'v', 's', 'z', 'ch', 'j', 'm', 'n', 'gn', 'l', 'r', 'y']
VOWELS = ['a', 'i', 'é', 'è', 'o', 'ou', 'u', 'eu', 'an', 'in', 'on']

# objet-repère de chaque son
HOOKS = {
    'p': 'poisson', 'b': 'bol', 't': 'toit', 'd': 'diamant', 'k': 'canne', 'g': 'guidon', 'f': 'fourchette',
    'v': 'vague', 's': 'sablier', 'z': 'zigzag', 'ch': 'chaise', 'j': 'jupe', 'm': 'mouette', 'n': 'nœud',
    'gn': 'peigne', 'l': 'lune', 'r': 'roue', 'y': 'yoyo',
    'a': 'armoire', 'i': 'île', 'é': 'étoile', 'è': 'herbe', 'o': 'ovale', 'ou': 'ouragan', 'u': 'usine',
    'eu': 'heure', 'an': 'entonnoir', 'in': 'infini', 'on': 'ongle',
}

# caractère tapé -> son. Règle : un caractère = un son ; le circonflexe marque les sons composés.
KEYMAP = {k: k for k in ['p', 'b', 't', 'd', 'k', 'g', 'f', 'v', 's', 'z', 'j', 'm', 'n', 'l', 'r', 'y',
                         'a', 'i', 'é', 'è', 'o', 'u']}
KEYMAP.update({'â': 'an', 'î': 'in', 'ô': 'on', 'û': 'ou', 'ê': 'eu', 'ĉ': 'ch', 'ĝ': 'gn'})
KEYMAP.update({'x': 'ch', 'ç': 'ch', 'q': 'gn', 'ñ': 'gn'})  # variantes de secours
ALT_KEYS = {'x', 'ç', 'q', 'ñ'}


def keys(sound):
    """Touches d'un son : la norme d'abord, puis les variantes de secours."""
    ks = [k for k, s in KEYMAP.items() if s == sound]
    return [k for k in ks if k not in ALT_KEYS] + [k for k in ks if k in ALT_KEYS]


# --- chiffres (soroban) : barre, signe 0-4 dessous, perle du haut (+5) au-dessus ---
DIGIT_W = 22  # largeur d'un chiffre ; la barre court sur toute la largeur pour se joindre


def _digit_under(n, x, c, y=27):
    if n == 0:
        return f'<circle cx="{x}" cy="{y}" r="4.5" {_st(c)}/>'
    if n == 1:
        return _dot(x, y, c, 2.6)
    if n == 2:
        return _line(x - 6, y, x + 6, y, c)
    if n == 3:
        return f'<polyline points="{x-5},{y-5} {x},{y+5} {x+5},{y-5}" {_st(c)}/>'
    return _line(x, y - 6, x, y + 6, c) + _line(x - 6, y, x + 6, y, c)


def digit(n, c, x=DIGIT_W / 2):
    """Un chiffre, sans sa barre."""
    return _digit_under(n % 5, x, c) + (_dot(x, 9, c, 2.6) if n >= 5 else '')


def digit_bar(x1, x2, c):
    return f'<line data-bar="1" x1="{x1}" y1="16" x2="{x2}" y2="16" {_st(c)}/>'
