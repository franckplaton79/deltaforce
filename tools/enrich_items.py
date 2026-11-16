"""Enrichit data/items.json avec les descriptions publiques de deltaforce.th.gl.

Pour chaque identifiant d'objet, on ne récupère que les 8 premiers kilo-octets
de la page (la balise meta description s'y trouve) et on en extrait le texte
descriptif, le poids, la taille de grille et le prix de référence quand ils sont
présents. Aucune donnée n'est inventée : les champs absents restent vides.
"""
import json
import re
import html
import os
import concurrent.futures
import urllib.request
from collections import Counter

ROOT = '/home/user/delta-force-guide'
DATA = os.path.join(ROOT, 'data', 'items.json')
CACHE = '/tmp/thgl_cache'
os.makedirs(CACHE, exist_ok=True)

items = json.load(open(DATA, encoding='utf-8'))


def fetch(item_id):
    dest = os.path.join(CACHE, item_id + '.html')
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return open(dest, encoding='utf-8', errors='ignore').read()
    url = f'https://deltaforce.th.gl/db/collectibles/item_{item_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-7000'})
    try:
        d = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'ignore')
    except Exception:
        return ''
    open(dest, 'w', encoding='utf-8').write(d)
    return d


def parse(page):
    m = re.search(r'name="description" content="([^"]*)"', page)
    if not m:
        return None
    desc = html.unescape(m.group(1))
    title = re.search(r'<title>([^<]+)</title>', page)
    out = {'desc': desc}
    if title:
        out['title'] = html.unescape(title.group(1)).split('–')[0].strip()
    out['weight'] = re.search(r'Weight: ([\d.]+) kg', desc)
    out['weight'] = float(out['weight'].group(1)) if out['weight'] else None
    size = re.search(r'Size: (\d+)×(\d+)', desc)
    out['grid'] = f'{size.group(1)}×{size.group(2)}' if size else None
    price = re.search(r'Reference Price: ([\d,]+)', desc)
    out['refPrice'] = int(price.group(1).replace(',', '')) if price else None
    kind = re.search(r'in Delta Force\. ([^.]+)\.', desc)
    out['kind'] = kind.group(1).strip() if kind else None
    return out


with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
    pages = list(ex.map(lambda it: fetch(it['id']), items))

ok = 0
for it, page in zip(items, pages):
    p = parse(page) if page else None
    if not p:
        it['desc'] = None
        continue
    ok += 1
    it['desc'] = p['desc']
    it['kind'] = p.get('kind')
    it['weight'] = p['weight']
    it['grid'] = p['grid']
    if p['refPrice'] and not it.get('value'):
        it['value'] = p['refPrice']

json.dump(items, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('descriptions récupérées :', ok, '/', len(items))
print('avec poids :', sum(1 for i in items if i.get('weight')),
      '| avec grille :', sum(1 for i in items if i.get('grid')))
print(Counter(i.get('kind') for i in items).most_common(12))
