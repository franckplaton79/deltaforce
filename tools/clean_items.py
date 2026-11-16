"""Deuxième passe, hors ligne : nettoie les champs extraits des pages en cache.

Sortie : catégorie lisible, poids, taille de grille, niveau de pénétration,
taille de pile, nombre d'emplacements de ramassage, et la description courte
débarrassée des préfixes techniques.
"""
import json
import os
import re
from collections import Counter

ROOT = '/home/user/delta-force-guide'
DATA = os.path.join(ROOT, 'data', 'items.json')
CACHE = '/tmp/thgl_cache'

items = json.load(open(DATA, encoding='utf-8'))


def clean(desc, name):
    d = desc
    # retirer le préambule « Nom — Type in Delta Force. »
    d = re.sub(r'^.*?in Delta Force\.\s*', '', d)
    # retirer les blocs techniques en fin de description
    d = re.sub(r'\s*(Weight|Size|Stack Size|Armor Penetration Level|Reference Price|Found at)[^.]*\.\s*', ' ', d)
    d = re.sub(r'\s{2,}', ' ', d).strip()
    return d or None


for it in items:
    page = ''
    f = os.path.join(CACHE, it['id'] + '.html')
    if os.path.exists(f):
        page = open(f, encoding='utf-8', errors='ignore').read()
    m = re.search(r'name="description" content="([^"]*)"', page)
    if not m:
        it.update({'kind': None, 'desc': None, 'weight': None, 'grid': None, 'pen': None, 'stack': None, 'spots': None})
        continue
    import html as H
    d = H.unescape(m.group(1))
    kind = re.search(r'—\s*([A-Za-z ]+?)\s+in Delta Force', d)
    it['kind'] = kind.group(1).strip() if kind else None
    w = re.search(r'Weight: ([\d.]+) kg', d)
    it['weight'] = float(w.group(1)) if w else None
    g = re.search(r'Size: (\d+)×(\d+)', d)
    it['grid'] = f'{g.group(1)}×{g.group(2)}' if g else None
    pen = re.search(r'Armor Penetration Level: (\d)', d)
    it['pen'] = int(pen.group(1)) if pen else None
    st = re.search(r'Stack Size: (\d+)', d)
    it['stack'] = int(st.group(1)) if st else None
    sp = re.search(r'Found at (\d+) location', d)
    it['spots'] = int(sp.group(1)) if sp else None
    it['desc'] = clean(d, it['name'])

json.dump(items, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('items :', len(items))
print('types :', Counter(i['kind'] for i in items).most_common(10))
print('poids renseigné :', sum(1 for i in items if i['weight'] is not None))
print('grille renseignée :', sum(1 for i in items if i['grid']))
print('pénétration :', sum(1 for i in items if i['pen'] is not None))
print('description :', sum(1 for i in items if i['desc']))
print()
for i in [x for x in items if x['group'] == 'Ammo'][:5]:
    print(i['name'], '|', i['pen'], '|', i['weight'], '|', (i['desc'] or '')[:70])
