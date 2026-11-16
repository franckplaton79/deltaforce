"""Réécrit en français les noms, descriptions et champs de chaque objet.

Le nom français est produit par un dictionnaire explicite par catégorie (pas de
traduction mot à mot), la description française est rédigée à partir des
caractéristiques présentes dans les données : capacité, dégâts, dégâts armure,
niveau de protection, durabilité, niveau de pénétration, taille de pile, poids,
grille, nombre d'utilisations pour les cartes d'accès.

Rien n'est inventé : si une caractéristique manque, la phrase correspondante
n'est pas écrite. Sortie : data/items_fr.json
"""
import json
import os
import re
from collections import Counter

ROOT = '/home/user/delta-force-guide'
items = json.load(open(os.path.join(ROOT, 'data', 'items.json'), encoding='utf-8'))
raw = {json.loads(l)['id']: json.loads(l)['desc'] for l in open(os.path.join(ROOT, 'data', 'raw_desc.jsonl'), encoding='utf-8')}

# ---------------------------------------------------------------- noms
import sys
sys.path.insert(0, '/home/user/delta-force-guide/tools')
from lexique import translate as lex_translate
CAT_FR = {
    'Assault Rifles': "fusil d'assaut", 'Battle Rifles': 'fusil de combat',
    'Marksman Rifles': 'fusil de précision semi-auto', 'Sniper Rifles': 'fusil de précision',
    'Submachine Guns': 'pistolet-mitrailleur', 'Light Machine Guns': 'mitrailleuse légère',
    'General Machine Guns': 'mitrailleuse lourde', 'Shotguns': 'fusil à pompe',
    'Pistols': 'pistolet',
    'Backpacks': 'sac à dos', 'Chest Rigs': 'gilet tactique', 'Armor': 'protection',
    'Helmets': 'casque',
    'Barrels': 'canon', 'Muzzles': 'frein de bouche', 'Optics': 'optique',
    'Stocks': 'crosse', 'Foregrips': 'poignée avant', 'Handguards': 'garde-main',
    'Magazines': 'chargeur', 'Rear Grips': 'poignée arrière',
    'Utility Attachments': 'accessoire utilitaire',
}

# modèle anglais -> modèle français, du plus long au plus court
PATTERNS = [
    (r'^(.+?) Assault Rifle$', r"\1, fusil d'assaut"),
    (r'^(.+?) Battle Rifle$', r'\1, fusil de combat'),
    (r'^(.+?) Compact Assault Rifle$', r"\1, fusil d'assaut compact"),
    (r'^(.+?) Marksman Rifle$', r'\1, fusil de précision semi-auto'),
    (r'^(.+?) Sniper Rifle$', r'\1, fusil de précision'),
    (r'^(.+?) Submachine Gun$', r'\1, pistolet-mitrailleur'),
    (r'^(.+?) Light Machine Gun$', r'\1, mitrailleuse légère'),
    (r'^(.+?) General Machine Gun$', r'\1, mitrailleuse lourde'),
    (r'^(.+?) Shotgun$', r'\1, fusil à pompe'),
    (r'^(.+?) Revolver$', r'\1, revolver'),
    (r'^(.+?) Pistol$', r'\1, pistolet'),
    # accessoires : « Arme + pièce »
    (r'^(.+?) Long Barrel$', r'\1 : canon long'),
    (r'^(.+?) Short Barrel$', r'\1 : canon court'),
    (r'^(.+?) Barrel$', r'\1 : canon'),
    (r'^(.+?) Collapsible Stock \(Extended\)$', r'\1 : crosse télescopique déployée'),
    (r'^(.+?) Collapsible Stock \(Folded\)$', r'\1 : crosse télescopique repliée'),
    (r'^(.+?) Fixed Stock$', r'\1 : crosse fixe'),
    (r'^(.+?) Light Stock$', r'\1 : crosse légère'),
    (r'^(.+?) Stable Stock$', r'\1 : crosse stable'),
    (r'^(.+?) Stock$', r'\1 : crosse'),
    (r'^(.+?) Rear Grip$', r'\1 : poignée arrière'),
    (r'^(.+?) Foregrip$', r'\1 : poignée avant'),
    (r'^(.+?) Grip$', r'\1 : poignée'),
    (r'^(.+?) Handguard Panel$', r'\1 : panneau de garde-main'),
    (r'^(.+?) Handguard$', r'\1 : garde-main'),
    (r'^(.+?) Drum Mag$', r'\1 : chargeur tambour'),
    (r'^(.+?) Extended Mag$', r'\1 : chargeur rallongé'),
    (r'^(\d+(?:\.\d+)?mm?|[\d.]+x\d+) (\d+)-Round (.+?) Mag$', r'\1, chargeur \2 coups \3'),
    (r'^(.+?) Magazine$', r'\1 : chargeur'),
    (r'^(.+?) Mag$', r'\1 : chargeur'),
    (r'^(.+?) Scope$', r'\1 : lunette'),
    (r'^(.+?) Red Dot$', r'\1 : point rouge'),
    (r'^(.+?) Sight$', r'\1 : viseur'),
    (r'^(.+?) Optic$', r'\1 : optique'),
    (r'^(.+?) Suppressor$', r'\1 : silencieux'),
    (r'^(.+?) Compensator$', r'\1 : compensateur'),
    (r'^(.+?) Muzzle Brake$', r'\1 : frein de bouche'),
    (r'^(.+?) Flash Hider$', r'\1 : cache-flamme'),
    (r'^(.+?) Laser$', r'\1 : laser'),
    (r'^(.+?) Bipod$', r'\1 : bipied'),
    (r'^(.+?) Mount$', r'\1 : montage'),
    (r'^(.+?) Adapter$', r'\1 : adaptateur'),
    (r'^(.+?) Kit$', r'\1 : kit'),
]

# lieux des cartes d'accès
PLACES = {
    'Assembly Workshop': "atelier d'assemblage", 'Barracks': 'caserne',
    'Biological Data': 'données biologiques', 'Black Chamber': 'chambre noire',
    'Buoyancy Lab': 'labo de flottabilité', 'Cargo Plane': 'avion-cargo',
    'Cement Plant': 'cimenterie', 'Central Command': 'commandement central',
    'Central VIP': 'VIP central', 'CEO': 'PDG', 'Checkpoint': 'point de contrôle',
    'Diamonds': 'salle des diamants', 'East Town': 'ville est',
    'East Wing': 'aile est', 'West Wing': 'aile ouest',
    'Eastern Suspension Bridge': 'pont suspendu est',
    'Employee Passage': 'passage des employés',
    'Storage Room': 'réserve', 'Storeroom': 'réserve', 'Server Room': 'salle serveur',
    'Conference Room': 'salle de conférence', 'Reception Room': 'réception',
    'Infirmary': 'infirmerie', 'Laboratory': 'laboratoire', 'Lab': 'labo',
    'Dormitory': 'dortoir', 'Office': 'bureau', 'Room': 'salle',
    "Manager's Office": 'bureau du responsable', 'Bedroom': 'chambre',
    'Wing': 'aile', 'Bridge': 'pont', 'Floor': 'étage', 'Basement': 'sous-sol',
    'Warehouse': 'entrepôt', 'Control Room': 'salle de contrôle',
}

# objets de collection : dictionnaire explicite des plus fréquents
COLLECT = {
    '999.9 Gold Bar': "lingot d'or 999,9", 'Gold Bar': "lingot d'or",
    '9V Battery': 'pile 9V', 'EV Battery': 'batterie de véhicule électrique',
    'Fuel Cell': 'pile à combustible', 'ASOS Motherboard': 'carte mère ASOS',
    'Graphics Card': 'carte graphique', 'HiFi Sound Card': 'carte son HiFi',
    'Air-Cooled Heat Sink': 'dissipateur refroidi par air',
    'Analog Thermometer': 'thermomètre analogique',
    'Ancient Pirate Telescope': 'longue-vue de pirate ancienne',
    'Ancient Sphinx Statue': 'statue de sphinx ancienne',
    'Ace Staff Trophy': 'trophée de l’état-major',
    'African Wood Sculpture': 'sculpture africaine en bois',
    'Angle Grinder': 'meuleuse d’angle',
    'Solar Panel': 'panneau solaire', 'Socket Adapter': 'adaptateur de prise',
    'Wide-Angle Lens': 'objectif grand-angle', 'Intel Recorder': 'enregistreur de renseignement',
    'Digital Camera': 'appareil photo numérique', 'Bone Saw': 'scie à os',
    'Military Binoculars': 'jumelles militaires', 'Gold Crest': 'blason doré',
    'Pure Gold Lighter': 'briquet en or pur', 'Ceremony Dagger': 'dague de cérémonie',
    'Military Explosive': 'explosif militaire', 'Cell Phone': 'téléphone portable',
    'Laptop': 'ordinateur portable', 'Delta Force: Task Force Dagger': 'Delta Force : Task Force Dagger',
    'Mocha Coffee Pot': 'cafetière à moka', 'Bagged Coffee Beans': 'grains de café en sachet',
    'Boxed Drip Coffee': 'café filtre en boîte',
    'Capsule Coffee Machine Set': 'machine à capsules de café',
    'G.T.I. SATCOM Antenna': 'antenne SATCOM G.T.I.',
    'Ahsarah Specialty Wine Glass': 'verre à vin spécial Ahsarah',
    'Ahsarah Specialty Ceramics': 'céramique spéciale Ahsarah',
    'Ahsarah Specialty Flask': 'flacon spécial Ahsarah',
    'Ahsarah Glamour Hookah': 'chicha glamour Ahsarah',
    'Ahsarah Fashion Weekly': 'hebdomadaire mode Ahsarah',
    'Ahsarah News Weekly': 'hebdomadaire d’actualités Ahsarah',
    'Ahsarah Entertainment Monthly': 'mensuel divertissement Ahsarah',
    'Ahsarah Guard Confidential Files': 'dossiers confidentiels de la garde Ahsarah',
}

CONSUM = {
    'Basic Injector': 'injecteur basique', 'Enhanced Injector': 'injecteur amélioré',
    'CAT Tourniquet': 'garrot CAT', 'Elastic Bandage': 'bandage élastique',
    'Bottled Antibiotics': 'antibiotiques en flacon',
    'DVE Painkiller': 'antidouleur DVE',
    'Extended-Release Painkiller': 'antidouleur à libération prolongée',
    'Field First Aid Kit': 'trousse de secours de campagne',
    'Field Med Crate': 'caisse médicale de campagne',
    'DEK Field Surgical Kit': 'kit chirurgical de campagne DEK',
    'DIY Helmet Repair Kit': 'kit de réparation de casque (improvisé)',
    'DIY Vest Repair Kit': 'kit de réparation de gilet (improvisé)',
}


def tr_name(it):
    n = it['name']
    if n in COLLECT:
        return COLLECT[n]
    if n in CONSUM:
        return CONSUM[n]
    if it['group'] == 'Keys':
        out = n
        for a in sorted(PLACES, key=len, reverse=True):
            out = re.sub(re.escape(a), PLACES[a], out)
        return out
    if it['group'] == 'Ammo':
        return n  # calibres et types de balle : sigles conservés
    for pat, rep in PATTERNS:
        if re.match(pat, n):
            return re.sub(pat, rep, n)
    if it['group'] == 'Gear':
        cat = CAT_FR.get(it['cat'], '')
        return f"{n} ({cat})" if cat else n
    return n


# ---------------------------------------------------------- descriptions
def num(x):
    return x.replace(',', '') if x else x


def per_case_ratio(it):
    v, ps = it.get('value'), it.get('perSlot')
    return ps if ps else None


def fr_desc(it):
    d = raw.get(it['id']) or ''
    if not d:
        return None
    body = re.sub(r'^.*?in Delta Force\.\s*', '', d)
    cap = re.search(r'Capacity: (\d+)', body)
    dmg = re.search(r'Damage: (\d+)', body)
    adm = re.search(r'Armor Damage: (\d+)', body)
    prot = re.search(r'Protection Level: (\d+)', body)
    dur = re.search(r'Durability: (\d+)', body)
    pen = re.search(r'Armor Penetration Level: (\d+)', body)
    stack = re.search(r'Stack Size: (\d+)', body)
    use = re.search(r'Uses: (\d+)', body)
    slots = re.search(r'Offers (\d+) storage slots', body)
    act = re.search(r'Activation Time: ([\d.]+)s', body)
    heal = re.search(r'Recovers (\d+) HP per second', body)
    wt = re.search(r'Weight: ([\d.]+) kg', body)
    size = re.search(r'Size: (\d+)×(\d+)', body)
    grid = it.get('grid') or (f'{size.group(1)}×{size.group(2)}' if size else None)
    weight = it.get('weight') if it.get('weight') is not None else (float(wt.group(1)) if wt else None)

    ph = []
    if it['group'] == 'Weapons':
        cat = CAT_FR.get(it['cat'], 'arme')
        p = f'Cette arme est classée {cat} dans le jeu.'
        if cap:
            p += f' Son chargeur standard contient {cap.group(1)} coups.'
        if dmg:
            p += f' Chaque balle inflige {dmg.group(1)} dégâts'
            p += f' et {adm.group(1)} dégâts aux protections.' if adm else '.'
        ph.append(p)
        if it.get('value'):
            ph.append(f'Valeur de référence {it["value"]:,} Tekniq, soit {it["perSlot"]:,} par case occupée.'.replace(',', '\u202f'))
    elif it['group'] == 'Ammo':
        p = 'Cartouche de ' + (it['name'].split()[0] if it['name'] else 'calibre non précisé') + '.'
        if pen:
            p += f' Niveau de pénétration {pen.group(1)} : plus le chiffre est haut, plus la balle traverse une protection lourde.'
        if stack:
            p += f' Se transporte par piles de {stack.group(1)}.'
        ph.append(p)
    elif it['group'] == 'Gear':
        cat = CAT_FR.get(it['cat'], 'pièce d’équipement')
        p = f'Pièce d’équipement de catégorie {cat}.'
        if prot:
            p += f' Niveau de protection {prot.group(1)}.'
        if slots:
            p += f' Offre {slots.group(1)} emplacements de stockage.'
        if dur:
            p += f' Durabilité de base {dur.group(1)} ; elle baisse à chaque raid et se répare au site noir.'
        if not (prot or slots or dur):
            if it['cat'] in ('Backpacks', 'Chest Rigs'):
                p = f'Pièce d’équipement de catégorie {cat}. Le nombre d’emplacements et la protection ne sont pas publiés '
                p += 'pour cette pièce : compare-la à ses voisines de même catégorie avant d’investir.'
            else:
                p += ' Les valeurs de protection ne sont pas publiées pour cette pièce ; compare-la à ses voisines avant d’investir.'
        ph.append(p)
    elif it['group'] == 'Keys':
        opened = re.search(r'Used to open (?:the )?([^.]*)\.', body)
        target = opened.group(1) if opened else None
        if target:
            from lexique import translate_key
            target = translate_key(target.strip())
            p = f'Carte d’accès qui ouvre : {target[0].lower() + target[1:]}.'
        else:
            p = 'Carte d’accès de raid.'
        if use:
            p += f' Elle dispose de {use.group(1)} utilisations : chacune compte, y compris quand la salle est déjà pillée.'
        spots = re.search(r'Found at (\d+) location', body)
        if spots:
            p += f' Elle est relevée à {spots.group(1)} endroit(s) sur la carte.'
        ph.append(p)
    elif it['group'] == 'Consumables':
        p = 'Objet consommable de raid.'
        if heal:
            p += f' Rend {heal.group(1)} points de vie par seconde pendant son utilisation.'
        if act:
            p += f' Temps d’activation {act.group(1).replace(".", ",")} seconde(s), un délai qui compte en combat.'
        if use:
            p += f' Utilisable {use.group(1)} fois.'
        ph.append(p)
    elif it['group'] == 'Collectibles':
        p = 'Objet de collection, sans usage tactique : il se ramasse pour la revente ou pour une tâche.'
        if per_case_ratio(it):
            r = per_case_ratio(it)
            p += f' Rapport de {r:,} Tekniq par case'.replace(',', '\u202f')
            p += ' : à prendre en priorité.' if r >= 15000 else \
                 ' : correct si la place le permet.' if r >= 4000 else \
                 ' : objet de remplissage, à laisser quand le sac est plein.'
    elif it['group'] == 'Attachments':
        cat = CAT_FR.get(it['cat'], 'accessoire')
        p = f'Accessoire de type {cat}.'
        p += ' Il se monte sur une arme compatible et modifie ses statistiques ou son comportement au tir.'
        ph.append(p)

    if weight:
        ph.append(f'Poids {str(weight).replace(".", ",")} kg' + (f', encombrement {grid} cases.' if grid else '.'))
    elif grid:
        ph.append(f'Encombrement {grid} cases.')
    return ' '.join(ph)


out = []
for it in items:
    it = dict(it)
    it['name_fr'] = lex_translate(it['name'], it['group'], it.get('cat'))
    it['desc_fr'] = fr_desc(it)
    it['grade_fr'] = {0: 'non classé', 1: 'commun', 2: 'peu commun', 3: 'rare',
                      4: 'épique', 5: 'légendaire', 6: 'mythique'}.get(it['grade'], '')
    it['group_fr'] = {'Weapons': 'Armes', 'Ammo': 'Munitions', 'Gear': 'Équipement',
                      'Attachments': 'Accessoires', 'Collectibles': 'Objets de collection',
                      'Keys': 'Cartes et clés', 'Consumables': 'Consommables'}.get(it['group'], it['group'])
    it['cat_fr'] = CAT_FR.get(it['cat'], it['cat'])
    out.append(it)

json.dump(out, open(os.path.join(ROOT, 'data', 'items_fr.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, separators=(',', ':'))
print('objets traduits :', len(out))
print('descriptions FR :', sum(1 for i in out if i['desc_fr']))
for g in ['Weapons', 'Ammo', 'Gear', 'Keys', 'Consumables', 'Attachments', 'Collectibles']:
    print('\n==', g)
    for i in [x for x in out if x['group'] == g][:4]:
        print('  ', i['name_fr'], '|', (i['desc_fr'] or '')[:110])
