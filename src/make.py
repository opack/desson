"""Régénère tout : la police, la page (index.html) et le guide PDF.

Usage : python make.py --version 1.300
"""
import argparse
import os

import build_font
import build_guide
import build_page

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', required=True, help='nouvelle version de la police, ex. 1.300')
    v = ap.parse_args().version
    font = os.path.join(ROOT, 'Desson-Regular.ttf')
    build_font.build(font, v)
    build_page.build(os.path.join(ROOT, 'index.html'))
    build_guide.build(font, os.path.join(ROOT, 'desson-guide.pdf'))
