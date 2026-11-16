"""Rédige en français les fiches d'objets de collection sans description.

Deux cas :
1. Une phrase publique existe mais est tronquée à la source : on la traduit par
   un lexique de tournures, sans jamais compléter ce qui manque.
2. Aucune phrase n'existe : on décrit par catégorie de ramassage et par les
   chiffres mesurés (poids, encombrement, valeur par case).

Sortie : data/loot_desc.json  { id: "phrase française" }
"""
import json
import os
import re

ROOT = '/home/user/delta-force-guide'
items = json.load(open(os.path.join(ROOT, 'data', 'items_fr.json'), encoding='utf-8'))
raw = {json.loads(l)['id']: json.loads(l)['desc'] for l in open(os.path.join(ROOT, 'data', 'raw_desc.jsonl'), encoding='utf-8')}

# --- tournures anglaises relevées, traduites une par une -------------------
PHRASES = [
    ("A symbol of Haavk's outstanding staff", "un symbole du personnel d'exception de Haavk"),
    ("those who receive it keep it by their side", "ceux qui le reçoivent le gardent sur eux"),
    ("A unique work of art that showcases the charm of African culture", "une œuvre d'art unique qui montre le savoir-faire de la culture africaine"),
    ("with delicate carving", "finement sculptée"),
    ("Bringing readers joy and relaxation with the latest entertainment scoops", "un magazine de divertissement qui mise sur les dernières indiscrétions du milieu"),
    ("Featuring the fashion styles of the Ahsarah region", "un hebdomadaire consacré aux styles vestimentaires de la région d'Ahsarah"),
    ("it gives readers a unique aesthetic experience", "il offre à ses lecteurs une expérience esthétique à part"),
    ("A rough paper file folder documenting information on the Ahsarah Guard", "une chemise cartonnée qui documente les activités de la garde Ahsarah"),
    ("likely to contain", "susceptible de contenir"),
    ("A magazine rich in content and closely related to people's livelihood", "un magazine généraliste très lié au quotidien des habitants"),
    ("focusing on the current affairs", "centré sur l'actualité"),
    ("Special ceramics that embody the essence of ancient Ahsarah culture", "des céramiques qui reprennent l'essentiel de la culture ahsarienne ancienne"),
    ("brimming with endless", "débordantes de"),
    ("The wine pot that was the battlefield companion of the legendary Ahsarah general", "la gourde à vin qui accompagnait le général ahsarien légendaire sur le champ de bataille"),
    ("It contains fine", "elle contient un"),
    ("A special wine cup that has witnessed the endless battles and brave loyalty of Ahsarah warriors", "un verre à vin qui a vu les batailles et la loyauté des guerriers ahsariens"),
    ("This analog thermometer provides a simulation system for data collection", "un thermomètre analogique utilisé comme instrument de mesure pour la collecte de données"),
    ("A telescope with a sense of age", "une longue-vue qui porte son âge"),
    ("According to Ahsarah local records, this type of telescope was", "d'après les archives locales d'Ahsarah, ce type de longue-vue servait"),
    ("This intact pair of sharp horns taken from an adult bull is long and slender", "une paire de cornes intactes prélevée sur un taureau adulte, longues et fines"),
    ("Its weight makes those", "son poids en fait"),
    ("Tool & material", "outil et matériau"),
    ("Electronic product", "produit électronique"),
    ("Medical item", "matériel médical"),
    ("Intel item", "renseignement"),
    ("Household item", "objet domestique"),
    ("Craftwork", "artisanat"),
    ("Energy fuel", "carburant"),
    ("rare", "rare"),
    ("A delicious and nutritious fruit", "un fruit comestible"),
    ("healthy snack choice rich in vitamins", "une collation riche en vitamines"),
    ("An entire bar of gold, worth quite a fortune", "une barre d'or entière, qui vaut une petite fortune"),
    ("A stable solution", "une solution saline stable"),
    ("Used for medical purposes", "utilisé à des fins médicales"),
    ("Used in the production of", "utilisé dans la fabrication de"),
    ("This piece of equipment", "cette pièce d'équipement"),
    ("A valuable collectible", "un objet de collection recherché"),
    ("can be sold for a good price", "se revend à bon prix"),
    ("It is said that", "on raconte que"),
    ("legend has it that", "la légende dit que"),
]

KIND = {
    'Household Item': 'objet domestique', 'Medical Item': 'matériel médical',
    'Craftwork': 'artisanat local', 'Tool & Material': 'outil et matériau',
    'Energy Fuel': 'carburant et énergie', 'Electronic Product': 'produit électronique',
    'Food & Drink': 'aliment', 'Intel': 'renseignement',
    'Fish': 'poisson', 'Rare Fish': 'poisson rare',
}


def translate_fragment(body):
    s = body
    for a, b in sorted(PHRASES, key=lambda x: -len(x[0])):
        s = re.sub(re.escape(a), b, s, flags=re.I)
    return s


def build(it):
    name = it.get('name_fr') or it['name']
    kind_en = it.get('kind')
    kind = KIND.get(kind_en or '', None)
    body = raw.get(it['id']) or ''
    body = re.sub(r'^.*?in Delta Force\.\s*', '', body)
    body = re.sub(r'\s*(Weight|Size|Reference Price|Found at|Stack Size)[^.]*\.\s*', ' ', body).strip(' .…')

    parts = []
    if body:
        fr = translate_fragment(body).strip(' .…')
        # si la traduction laisse beaucoup d'anglais, on ne la garde pas
        words = fr.split()
        left = sum(1 for w in words if re.fullmatch(r"[A-Za-z'’\-]+", w)
                   and w.lower() not in {'de', 'la', 'le', 'les', 'un', 'une', 'des', 'du', 'en', 'et', 'à',
                                         'au', 'aux', 'pour', 'qui', 'que', 'sur', 'dans', 'par', 'ce', 'cette',
                                         'son', 'sa', 'ses', 'il', 'elle', 'on', 'avec', 'est', 'sont', 'plus'})
        ratio = left / max(1, len(words))
        if ratio < 0.25 and len(words) >= 5:
            parts.append(fr[0].upper() + fr[1:] + '.')
        else:
            parts.append(None)
    else:
        parts.append(None)

    if not parts[0]:
        label = f'objet de collection classé {kind}' if kind else 'objet de collection'
        parts[0] = f'Un {label} : aucun usage tactique, il se ramasse pour la revente ou pour une tâche.'
        if kind_en in ('Intel',):
            parts[0] = "Un document de renseignement : il se ramasse pour la revente ou pour une tâche, sans usage en combat."

    # valeur et poids : toujours chiffrés
    if it.get('value') and it.get('perSlot'):
        r = it['perSlot']
        verdict = ('à prendre en priorité' if r >= 15000 else
                   'correct si la place le permet' if r >= 4000 else
                   'objet de remplissage, à laisser quand le sac est plein')
        parts.append(f'Valeur de référence {it["value"]:,} Tekniq, soit {it["perSlot"]:,} par case occupée : {verdict}.'
                     .replace(',', '\u202f'))
    if it.get('weight'):
        w = str(it['weight']).replace('.', ',')
        g = it.get('grid')
        parts.append(f'Poids {w} kg' + (f', encombrement {g} cases.' if g else '.'))
    return ' '.join(p for p in parts if p)


if __name__ == '__main__':
    out = {}
    for it in items:
        if it['group'] != 'Collectibles':
            continue
        if it.get('desc_fr'):
            continue
        out[it['id']] = build(it)
    json.dump(out, open(os.path.join(ROOT, 'data', 'loot_desc.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, separators=(',', ':'))
    print('fiches complétées :', len(out))
    for k in list(out)[:8]:
        print('  •', out[k][:170])
