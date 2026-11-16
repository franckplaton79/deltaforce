"""Construit data/items.json depuis la liste publique de deltaforceitems.com.

Découpage par bloc d'item (chaque ligne est un <a href="/items/...">), puis
extraction champ par champ avec des motifs tolérants : les grades changent la
couleur de la pastille et certaines valeurs valent 0 ou N/A.

Champs : slug, nom, groupe, catégorie, grade, valeur de référence CN,
valeur par case, identifiant, URL et chemin local de l'icône.
"""
import re
import json
import html
import os
from collections import Counter

SRC = '/tmp/list.html'
ROOT = '/home/user/delta-force-guide'
OUT = os.path.join(ROOT, 'data', 'items.json')

s = open(SRC, encoding='utf-8', errors='ignore').read()
parts = s.split('<a href="/items/')[1:]

def first(pat, txt, flags=0):
    m = re.search(pat, txt, flags)
    return m.group(1) if m else None

items, skipped = [], 0
for p in parts:
    slug = p.split('"', 1)[0]
    if not re.fullmatch(r'[a-z0-9\-]+', slug):
        continue
    img = first(r'<img src="(https://assets\.deltaforceitems\.com/items/[^"]+)"', p)
    name = first(r'<span class="block truncate font-medium text-white">([^<]+)</span>', p)
    if not img or not name:
        skipped += 1
        continue
    cats = re.findall(r'<span class="hidden min-w-0 truncate text-slate-300 md:block">([^<]+)</span>', p)
    grade = first(r'rounded-md border px-2 text-xs font-semibold [^"]*">(\d+)</span>', p)
    val = first(r'CN value </span>\s*([\d,]+|-)</span>', p)
    slot = first(r'Per slot </span>\s*([\d,]+|N/A|-)</span>', p)

    def num(x):
        if x is None or x in ('N/A', '-'):
            return None
        return int(x.replace(',', ''))

    items.append({
        'slug': slug,
        'name': html.unescape(name.strip()),
        'group': cats[0].strip() if cats else '',
        'cat': cats[1].strip() if len(cats) > 1 else '',
        'grade': int(grade) if grade else None,
        'value': num(val),
        'perSlot': num(slot),
        'id': (re.search(r'/items/(\d+)', img) or [None, None])[1],
        'img': img,
        'icon': '/assets/items/' + img.rsplit('/', 1)[-1].rsplit('.', 1)[0] + '.jpg',
    })

seen, uniq = set(), []
for it in items:
    if it['slug'] in seen:
        continue
    seen.add(it['slug'])
    uniq.append(it)

os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
json.dump(uniq, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(parts), 'segments ->', len(uniq), 'items ;', skipped, 'ignorés')
print(Counter(i['group'] for i in uniq).most_common())
print('armes/équipement :', Counter(i['cat'] for i in uniq if i['group'] in ('Weapons', 'Gear')).most_common())
print('sans grade :', sum(1 for i in uniq if i['grade'] is None),
      '| sans valeur :', sum(1 for i in uniq if i['value'] is None))
