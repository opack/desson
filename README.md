# Desson

**Des sons dessinés** : un code secret où chaque son du français s'écrit avec un petit dessin.
On écrit ce qu'on entend, sans les lettres muettes.

| Fichier | Rôle |
|---|---|
| `index.html` | Traducteur : on tape un message, il s'affiche en Desson. Un seul fichier, s'ouvre dans n'importe quel navigateur. |
| `Desson-Regular.ttf` | Police à installer pour écrire en Desson dans un traitement de texte. |
| `desson-guide.pdf` | Guide imprimable (2 pages) : tous les signes, les chiffres et des exemples. |
| `src/` | La source : les dessins (`desson.py`) et les scripts qui génèrent la police et le guide. |

## Les règles

- **29 sons**, un dessin par son. Chaque dessin représente un objet dont le nom commence par ce son
  (exception : le *peigne* pour « gn »).
- Un seul signe pour les deux « eu » (*peu*, *peur*). Pas de « w » : « oi » s'écrit « ou » + « a ».
- On écrit ce qu'on entend : `i` dans `viî` (viens) ou `pié` (pied), `y` dans `yê` (yeux), `yaûrt` (yaourt) ou `travay` (travail).
- **Chiffres façon soroban** : chaque chiffre est posé sous une barre (petit rond = 0, point = 1, trait = 2,
  V = 3, + = 4) ; pour 5 à 9, un point au-dessus de la barre ajoute 5. Les chiffres d'un nombre partagent la même barre.
- **Liaisons (facultatives)** : on écrit le son de liaison entre deux tirets, collé aux deux mots
  (`lè-z-âfâ`, `î-n-om`, `vû-z-édé`). Il se dessine par un trait à mi-hauteur à la place de l'espace, avec le son en petit au-dessus.
  Sans liaison, on écrit simplement les deux mots : `vû édé`.

## Saisie au clavier

**Un caractère = un son = un dessin.** Les sons simples gardent leur lettre (`p b t d k g f v s z j m n l r y a i é è o u`).
Le **circonflexe**, et lui seul, marque les sons composés :

| Son | Norme | Secours (claviers sans touche morte) |
|---|---|---|
| an | `â` | |
| in | `î` | |
| on | `ô` | |
| ou | `û` | |
| eu | `ê` | |
| ch | `ĉ` | `x` ou `ç` |
| gn | `ĝ` | `q` ou `ñ` |

Exemples : `ĉokola` (chocolat), `bôjûr` (bonjour), `ûazo` (oiseau), `vakâs` (vacances), `salu ! tu viî jûé ?`.

Les autres caractères (`c`, `h`, `e`, `w`, `à`, `ù`…) ne correspondent à aucun son. La page web convertit aussi `^c` et `^g`
en `ĉ` et `ĝ` ; la police, elle, ne peut lire qu'un caractère à la fois.

## La police

Installation sous Windows : double-clic sur `Desson-Regular.ttf`, puis *Installer*. Pour remplacer une version
précédente, la désinstaller d'abord, puis redémarrer Word (ou le PC) pour vider le cache des polices.

- Espacement proportionnel : chaque dessin a la même marge (60 unités) de chaque côté ; l'espace entre les mots fait 500 unités.
- Ponctuation incluse (reprise de DejaVu Sans ExtraLight, licence libre : `src/fonts/DejaVu-LICENSE.txt`).
- Pas d'espace visible devant `! ? : ; »` ni après `«` : les espaces insécables ont une largeur nulle, et une règle
  contextuelle masque les espaces normales. Dans Word, cette règle demande de cocher
  *Police > Paramètres avancés > Utiliser des alternatives contextuelles*.
- Liaisons : `-z-` (ou tout autre son entre deux tirets) se transforme en trait de liaison avec le son en petit au-dessus.
  Même réglage Word que ci-dessus (alternatives contextuelles) ; les applications qui activent les ligatures standard l'affichent aussi.

## Régénérer la police, la page et le guide

```bash
cd src
pip install -r requirements.txt
playwright install chromium        # une seule fois, pour le guide PDF
python make.py --version 2.200     # augmenter la version de la police à chaque changement
```

- `src/desson.py` : les dessins (SVG dans une case de 40 × 40), les objets-repères, la saisie clavier et les chiffres.
- `src/build_font.py` : la police. Réglages en tête de fichier (`SIDE_BEARING`, `SPACE`…).
- `src/build_page.py` : met à jour `index.html` (dessins, chiffres, clavier, objets-repères), entre les repères
  `DESSON:GENERATED:BEGIN` et `DESSON:GENERATED:END`. Ne pas modifier ce bloc à la main.
- `src/build_guide.py` : le guide PDF. Les exemples sont composés avec la police elle-même.
- `src/make.py` : lance les trois dans l'ordre.

`src/desson.py` est la seule source des dessins : on modifie là, puis on lance `make.py`.
"# desson" 
