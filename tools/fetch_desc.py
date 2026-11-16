"""Récupère la meta description publique de chaque objet, par lots, avec reprise.

Écrit data/raw_desc.jsonl (une ligne par objet) : {"id": "...", "desc": "..."}
Le script peut être relancé : il saute les identifiants déjà collectés et
n'utilise que le cache disque pour éviter de re-télécharger.
"""
import json
import os
import re
import sys
import html as H
import urllib.request

ROOT = '/home/user/delta-force-guide'
CACHE = '/tmp/thgl_cache2'
OUT = os.path.join(ROOT, 'data', 'raw_desc.jsonl')
os.makedirs(CACHE, exist_ok=True)

PATH = {'Collectibles': 'collectibles', 'Attachments': 'attachments', 'Gear': 'gear',
        'Ammo': 'ammo', 'Weapons': 'weapons', 'Keys': 'keys', 'Consumables': 'consumables'}

items = json.load(open(os.path.join(ROOT, 'data', 'items.json'), encoding='utf-8'))
done = set()
if os.path.exists(OUT):
    for line in open(OUT, encoding='utf-8'):
        try:
            done.add(json.loads(line)['id'])
        except Exception:
            pass

todo = [i for i in items if i['id'] not in done]
limit = int(sys.argv[1]) if len(sys.argv) > 1 else 250
todo = todo[:limit]

with open(OUT, 'a', encoding='utf-8') as out:
    for n, it in enumerate(todo, 1):
        dest = os.path.join(CACHE, it['id'] + '.html')
        txt = ''
        if os.path.exists(dest):
            txt = open(dest, encoding='utf-8', errors='ignore').read()
        if not txt:
            seg = PATH.get(it['group'], 'collectibles')
            url = f'https://deltaforce.th.gl/db/{seg}/item_{it["id"]}'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-9000'})
            try:
                txt = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'ignore')
                open(dest, 'w', encoding='utf-8').write(txt)
            except Exception:
                txt = ''
        m = re.search(r'name="description" content="([^"]*)"', txt) if txt else None
        if m:
            out.write(json.dumps({'id': it['id'], 'desc': H.unescape(m.group(1))}, ensure_ascii=False) + '\n')
        else:
            out.write(json.dumps({'id': it['id'], 'desc': None}, ensure_ascii=False) + '\n')
        if n % 50 == 0:
            out.flush()
            print(n, 'traités', flush=True)

print('lot terminé :', len(todo), '| total collecté :', sum(1 for _ in open(OUT, encoding='utf-8')))
