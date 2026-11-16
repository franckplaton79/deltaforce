"""Traduction française des noms d'objets, par règles ordonnées puis dictionnaire.

Approche : on découpe le nom en mots, on traduit chaque mot ou expression connue,
on remet dans l'ordre français (nom principal d'abord pour les lieux et les
accessoires), et on conserve les sigles, calibres et marques tels quels.
Un dictionnaire explicite tranche les cas fréquents.
"""
import json
import os
import re

ROOT = '/home/user/delta-force-guide'
items = json.load(open(os.path.join(ROOT, 'data', 'items.json'), encoding='utf-8'))

# --- dictionnaire explicite (priorité absolue, insensible à la casse) ---
EXACT = {
    # armes
    'Assault Rifle': "fusil d'assaut", 'Battle Rifle': 'fusil de combat',
    'Marksman Rifle': 'fusil de précision semi-auto', 'Sniper Rifle': 'fusil de précision',
    'Submachine Gun': 'pistolet-mitrailleur', 'Light Machine Gun': 'mitrailleuse légère',
    'General Machine Gun': 'mitrailleuse lourde', 'Machine Gun': 'mitrailleuse',
    'Compact Assault Rifle': "fusil d'assaut compact", 'Shotgun': 'fusil à pompe',
    'Revolver': 'revolver', 'Pistol': 'pistolet',
    # équipement
    'Backpack': 'sac à dos', 'Chest Rig': 'gilet tactique', 'Vest': 'gilet',
    'Helmet': 'casque', 'Hat': 'chapeau', 'Load System': 'harnais modulaire',
    'Climbing Bag': 'sac d’escalade', 'Boonie Hat': 'chapeau boonie',
    # accessoires
    'Barrel': 'canon', 'Long Barrel': 'canon long', 'Short Barrel': 'canon court',
    'Stock': 'crosse', 'Collapsible Stock': 'crosse télescopique',
    'Fixed Stock': 'crosse fixe', 'Light Stock': 'crosse légère', 'Stable Stock': 'crosse stable',
    'Rear Grip': 'poignée arrière', 'Grip': 'poignée', 'Foregrip': 'poignée avant',
    'Handguard': 'garde-main', 'Handguard Panel': 'panneau de garde-main',
    'Magazine': 'chargeur', 'Mag': 'chargeur', 'Drum Mag': 'chargeur tambour',
    'Extended Mag': 'chargeur rallongé', 'Round Mag': 'chargeur',
    'Round Aluminum Mag': 'chargeur aluminium', 'Round Polymer Mag': 'chargeur polymère',
    'Scope': 'lunette', 'Optic': 'optique', 'Red Dot': 'point rouge',
    'Holographic Sight': 'viseur holographique', 'Sight': 'viseur',
    'Suppressor': 'silencieux', 'Compensator': 'compensateur',
    'Muzzle Brake': 'frein de bouche', 'Flash Hider': 'cache-flamme', 'Muzzle': 'frein',
    'Laser': 'laser', 'Flashlight': 'lampe tactique', 'Bipod': 'bipied',
    'Mount': 'montage', 'Adapter': 'adaptateur', 'Kit': 'kit', 'Rail': 'rail',
    'Panel': 'panneau', 'Base': 'base', 'Spring': 'ressort', 'Buffer Spring': 'ressort de recul',
    'Charging Handle': 'poignée d’armement', 'Bolt Carrier Group': 'ensemble culasse',
    'Fire Mods': 'module de tir', 'Trigger': 'détente',
    # lieux et cartes
    'Room': 'salle', 'Office': 'bureau', 'Storage Room': 'réserve',
    'Storeroom': 'réserve', 'Server Room': 'salle serveur',
    'Conference Room': 'salle de conférence', 'Reception Room': 'réception',
    'Infirmary': 'infirmerie', 'Laboratory': 'laboratoire', 'Lab': 'labo',
    'Dormitory': 'dortoir', 'Barracks': 'caserne', 'Workshop': 'atelier',
    'Assembly Workshop': 'atelier d’assemblage', 'Central Command': 'commandement central',
    'Cargo Plane': 'avion-cargo', 'Cement Plant': 'cimenterie',
    'Black Chamber': 'chambre noire', 'Buoyancy Lab': 'labo de flottabilité',
    'CEO': 'PDG', 'Bedroom': 'chambre', 'Passage': 'passage', 'Bridge': 'pont',
    'Checkpoint': 'point de contrôle', 'Room 3F': 'salle 3e étage',
    'East Town': 'ville est', 'East Wing': 'aile est', 'West Wing': 'aile ouest',
    'Residential': 'résidentiel', 'Manager’s Office': 'bureau du responsable',
    "Manager's Office": 'bureau du responsable', 'Diamonds Room': 'salle des diamants',
    # consommables
    'Injector': 'injecteur', 'Painkiller': 'antidouleur', 'Tourniquet': 'garrot',
    'Bandage': 'bandage', 'Antibiotics': 'antibiotiques', 'Med Crate': 'caisse médicale',
    'First Aid Kit': 'trousse de secours', 'Surgical Kit': 'kit chirurgical',
    'Repair Kit': 'kit de réparation', 'Helmet Repair Kit': 'kit de réparation de casque',
    'Vest Repair Kit': 'kit de réparation de gilet',
    # objets de collection fréquents
    'Gold Bar': 'lingot d’or', 'Battery': 'pile', 'Motherboard': 'carte mère',
    'Graphics Card': 'carte graphique', 'Sound Card': 'carte son', 'Heat Sink': 'dissipateur',
    'Thermometer': 'thermomètre', 'Telescope': 'longue-vue', 'Statue': 'statue',
    'Trophy': 'trophée', 'Sculpture': 'sculpture', 'Grinder': 'meuleuse',
    'Solar Panel': 'panneau solaire', 'Fuel Cell': 'pile à combustible',
    'Camera': 'appareil photo', 'Digital Camera': 'appareil photo numérique',
    'Binoculars': 'jumelles', 'Lighter': 'briquet', 'Dagger': 'dague',
    'Bone Saw': 'scie à os', 'Laptop': 'ordinateur portable', 'Phone': 'téléphone',
    'Cell Phone': 'téléphone portable', 'Coffee': 'café', 'Wine Glass': 'verre à vin',
    'Flask': 'flacon', 'Ceramics': 'céramique', 'Hookah': 'chicha',
    'Weekly': 'hebdomadaire', 'Monthly': 'mensuel', 'Fashion': 'mode',
    'Entertainment': 'divertissement', 'Confidential Files': 'dossiers confidentiels',
    'Guard': 'garde', 'Specialty': 'spécial', 'Antenna': 'antenne',
    'SATCOM Antenna': 'antenne SATCOM', 'Recorder': 'enregistreur',
    'Intel Recorder': 'enregistreur de renseignement', 'Explosive': 'explosif',
    'Military Explosive': 'explosif militaire', 'Crest': 'blason', 'Bolt': 'boulon',
    'Plug': 'prise', 'Socket': 'prise', 'Fan': 'ventilateur', 'Mirror': 'miroir',
    'Necklace': 'collier', 'Ring': 'bague', 'Watch': 'montre', 'Coin': 'pièce',
    'Painting': 'tableau', 'Vase': 'vase', 'Teapot': 'théière', 'Kettle': 'bouilloire',
    'Shampoo': 'shampooing', 'Soap': 'savon', 'Cup': 'tasse', 'Tissues': 'mouchoirs',
    'Matches': 'allumettes', 'Detergent': 'lessive', 'Toothpaste': 'dentifrice',
    'Shaver': 'rasoir', 'Hairdryer': 'sèche-cheveux', 'Apple': 'pomme',
    'Yogurt': 'yaourt', 'Coke': 'soda', 'Coffee Beans': 'grains de café',
    'Water': 'eau', 'Tea': 'thé', 'Noodles': 'nouilles', 'Energy Bar': 'barre énergétique',
    'Antenna': 'antenne', 'Satellite': 'satellite',
}

# --- adjectifs et petits mots, appliqués mot à mot ---
WORDS = {
    'Light': 'léger', 'Heavy': 'lourd', 'Long': 'long', 'Short': 'court',
    'Extended': 'rallongé', 'Collapsible': 'télescopique', 'Folded': 'plié',
    'Fixed': 'fixe', 'Stable': 'stable', 'Practical': 'pratique', 'Quick': 'rapide',
    'Tactical': 'tactique', 'Angled': 'incliné', 'Vertical': 'vertical',
    'Horizontal': 'horizontal', 'Combat': 'combat', 'Field': 'campagne',
    'Military': 'militaire', 'Standard': 'standard', 'Enhanced': 'amélioré',
    'Advanced': 'avancé', 'Reinforced': 'renforcé', 'Improved': 'amélioré',
    'Precision': 'précision', 'Hunter': 'chasse', 'Camping': 'camping',
    'Portable': 'portable', 'Electric': 'électrique', 'Digital': 'numérique',
    'Gold': 'or', 'Pure': 'pur', 'Silver': 'argent', 'Antique': 'ancien',
    'Ancient': 'ancien', 'Rare': 'rare', 'Broken': 'cassé', 'Old': 'vieux',
    'Specialty': 'spécial', 'Premium': 'premium', 'Basic': 'basique',
    'Elite': 'élite', 'Pro': 'pro', 'Super': 'super', 'Mini': 'mini',
    'Adjustable': 'réglable', 'Aluminum': 'aluminium', 'Polymer': 'polymère',
    'Circle': 'rond', 'Angled': 'incliné', 'Skeleton': 'squelette',
    'Riot': 'anti-émeute', 'Load': 'charge', 'System': 'système',
    'Storage': 'stockage', 'Data': 'données', 'Biological': 'biologique',
    'Eastern': 'est', 'Western': 'ouest', 'Central': 'central',
    'North': 'nord', 'South': 'sud', 'Wing': 'aile', 'Town': 'ville',
    'Plane': 'avion', 'Cargo': 'cargo', 'Plant': 'usine', 'Cement': 'ciment',
    'Chamber': 'chambre', 'Black': 'noir', 'Bridge': 'pont',
}

KEEP = re.compile(r'^[A-Z0-9\.\-/×x]+$')


def tr(name):
    if name in EXACT:
        return EXACT[name]
    # expressions du dictionnaire, du plus long au plus court
    keys = sorted(EXACT, key=len, reverse=True)
    out = name
    if not KEEP.match(name):
        for k in keys:
            if len(k) < 4:
                continue
            out = re.sub(r'(?<![A-Za-z])' + re.escape(k) + r'(?![A-Za-z])', EXACT[k], out, flags=re.I)
    # mots isolés restants
    def repl(m):
        w = m.group(0)
        return WORDS.get(w, w)
    out = re.sub(r'\b[A-Za-z][A-Za-z\-’\']*\b', repl, out)
    out = re.sub(r'\s{2,}', ' ', out).strip()
    return out


if __name__ == '__main__':
    for g in ['Weapons', 'Gear', 'Keys', 'Consumables', 'Attachments', 'Collectibles']:
        print('==', g)
        for i in [x for x in items if x['group'] == g][:8]:
            print('  ', i['name'], '->', tr(i['name']))
