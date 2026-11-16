# Injecte une illustration dans chaque « entrée » (carte, bloc, section) des pages.
# Source de vérité : tools/entries.json  ->  {"page.html": {"Titre de l'entrée": "fichier.jpg"}}
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
DATA = pathlib.Path(__file__).resolve().parent / 'entries.json'

def inject(page, mapping):
    p = SRC / page
    s = p.read_text(encoding='utf-8')
    done = 0
    # 1) entrées en carte : <article ...> ... <h3>Titre</h3>
    for title, img in mapping.items():
        if not (ROOT/'assets'/'entries'/img).exists():
            print(f'  ! image manquante, ignorée : {img}')
            continue
        pat = re.compile(r'(<article\b[^>]*>)(\s*)(?!.*?entry-img)', re.S)
        # parcours par bloc d'article pour trouver le bon h3
        for m in re.finditer(r'<article\b[^>]*>.*?</article>', s, re.S):
            block = m.group(0)
            h = re.search(r'<h3>(.*?)</h3>', block, re.S)
            if not h:
                continue
            label = re.sub(r'<[^>]+>', '', h.group(1)).strip()
            if label != title or 'entry-img' in block:
                continue
            tag_end = block.index('>') + 1
            new_block = (block[:tag_end]
                         + f'\n<div class="entry-img"><img src="assets/entries/{img}" alt="{label}" loading="lazy" width="640" height="360"></div>'
                         + block[tag_end:])
            s = s.replace(block, new_block, 1)
            done += 1
            break
    p.write_text(s, encoding='utf-8')
    return done

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    total = 0
    for page, mapping in data.items():
        n = inject(page, mapping)
        total += n
        print(f'{page}: {n} entrée(s) illustrée(s)')
    print('total', total)

if __name__ == '__main__':
    main()
