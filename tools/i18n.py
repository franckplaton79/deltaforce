"""Dictionnaire de traduction des noms d'objets du jeu.

Objectif : un nom français stable et vérifiable pour chaque objet de la base.
Les sigles militaires restent en l'état (AKM, M4A1, SR-25, AP, FMJ...), les
marques et les noms propres ne sont pas traduits. Le nom d'origine reste
toujours affiché juste en dessous, pour que la recherche corresponde à l'écran.
"""
import json
import os
import re

ROOT = '/home/user/delta-force-guide'
items = json.load(open(os.path.join(ROOT, 'data', 'items.json'), encoding='utf-8'))
raw = {json.loads(l)['id']: json.loads(l)['desc'] for l in open(os.path.join(ROOT, 'data', 'raw_desc.jsonl'), encoding='utf-8')}

# --- mots et expressions traduits, appliqués du plus long au plus court ---
PHRASES = [
    ("Ahsarah Specialty Wine Glass", "Verre à vin spécial Ahsarah"),
    ("Ahsarah Specialty Ceramics", "Céramique spéciale Ahsarah"),
    ("Ahsarah Specialty Flask", "Flacon spécial Ahsarah"),
    ("Ahsarah Glamour Hookah", "Chicha glamour Ahsarah"),
    ("Ahsarah Fashion Weekly", "Hebdo mode Ahsarah"),
    ("Ahsarah News Weekly", "Hebdo actualités Ahsarah"),
    ("Ahsarah Entertainment Monthly", "Mensuel divertissement Ahsarah"),
    ("Ahsarah Guard Confidential Files", "Dossiers confidentiels de la garde Ahsarah"),
    ("Ahsarah", "Ahsarah"),
    ("G.T.I. SATCOM Antenna", "Antenne SATCOM G.T.I."),
    ("Delta Force: Task Force Dagger", "Delta Force : Task Force Dagger"),
    ("Task Force Dagger", "Task Force Dagger"),
    ("Mocha Coffee Pot", "Cafetière à moka"),
    ("HiFi Sound Card", "Carte son HiFi"),
    ("Intel Recorder", "Enregistreur de renseignement"),
    ("Solar Panel", "Panneau solaire"),
    ("Wide-Angle Lens", "Objectif grand-angle"),
    ("Socket Adapter", "Adaptateur de prise"),
    ("Bagged Coffee Beans", "Grains de café en sachet"),
    ("Boxed Drip Coffee", "Café filtre en boîte"),
    ("Capsule Coffee Machine Set", "Machine à capsules"),
    ("Cell Phone", "Téléphone portable"),
    ("Gold Crest", "Blason doré"),
    ("Military Explosive", "Explosif militaire"),
    ("Ceremony Dagger", "Dague de cérémonie"),
    ("Digital Camera", "Appareil photo numérique"),
    ("Bone Saw", "Scie à os"),
    ("Fuel Cell", "Pile à combustible"),
    ("Military Binoculars", "Jumelles militaires"),
    ("Pure Gold Lighter", "Briquet en or pur"),
    ("EV Battery", "Batterie de véhicule électrique"),
    ("Graphics Card", "Carte graphique"),
    ("Laptop", "Ordinateur portable"),
    ("9V Battery", "Pile 9V"),
    ("Air-Cooled Heat Sink", "Dissipateur à air"),
    ("Analog Thermometer", "Thermomètre analogique"),
    ("Ancient Pirate Telescope", "Longue-vue de pirate ancienne"),
    ("999.9 Gold Bar", "Lingot d'or 999,9"),
    ("Ace Staff Trophy", "Trophée de l'état-major"),
    ("African Wood Sculpture", "Sculpture africaine en bois"),
    # consommables
    ("Field Med Crate", "Caisse médicale de campagne"),
    ("Field First Aid Kit", "Trousse de premiers secours de campagne"),
    ("DEK Field Surgical Kit", "Kit chirurgical de campagne DEK"),
    ("DIY Helmet Repair Kit", "Kit de réparation de casque improvisé"),
    ("DIY Vest Repair Kit", "Kit de réparation de gilet improvisé"),
    ("Extended-Release Painkiller", "Antidouleur à libération prolongée"),
    ("DVE Painkiller", "Antidouleur DVE"),
    ("Bottled Antibiotics", "Antibiotiques en flacon"),
    ("Basic Injector", "Injecteur basique"),
    ("Enhanced Injector", "Injecteur amélioré"),
    ("CAT Tourniquet", "Garrot CAT"),
    ("Elastic Bandage", "Bande élastique"),
    # équipement / divers
    ("Chest Rig", "Gilet tactique"),
    ("Backpack", "Sac à dos"),
    ("Ballistic Vest", "Gilet balistique"),
    ("Helmet", "Casque"),
    ("Body Armor", "Protection corporelle"),
    ("Assault Rifle", "Fusil d'assaut"),
    ("Battle Rifle", "Fusil de combat"),
    ("Marksman Rifle", "Fusil de précision semi-auto"),
    ("Sniper Rifle", "Fusil de précision"),
    ("Submachine Gun", "Pistolet-mitrailleur"),
    ("Light Machine Gun", "Mitrailleuse légère"),
    ("General Machine Gun", "Mitrailleuse lourde"),
    ("Machine Gun", "Mitrailleuse"),
    ("Compact Assault Rifle", "Fusil d'assaut compact"),
    ("Shotgun", "Fusil à pompe"),
    ("Revolver", "Revolver"),
    ("Pistol", "Pistolet"),
    ("Suppressor", "Silencieux"),
    ("Compensator", "Compensateur"),
    ("Muzzle Brake", "Frein de bouche"),
    ("Flash Hider", "Cache-flamme"),
    ("Handguard", "Garde-main"),
    ("Handguard Panel", "Panneau de garde-main"),
    ("Barrel", "Canon"),
    ("Long Barrel", "Canon long"),
    ("Short Barrel", "Canon court"),
    ("Extended Barrel", "Canon rallongé"),
    ("Stock", "Crosse"),
    ("Rear Grip", "Poignée arrière"),
    ("Pistol Grip", "Poignée pistolet"),
    ("Grip", "Poignée"),
    ("Foregrip", "Poignée avant"),
    ("Magazine", "Chargeur"),
    ("Extended Mag", "Chargeur rallongé"),
    ("Drum Mag", "Chargeur tambour"),
    ("Optic", "Optique"),
    ("Scope", "Lunette"),
    ("Red Dot", "Point rouge"),
    ("Holographic Sight", "Viseur holographique"),
    ("Laser", "Laser"),
    ("Flashlight", "Lampe tactique"),
    ("Bipod", "Bipied"),
    ("Mount", "Montage"),
    ("Adapter", "Adaptateur"),
    ("Kit", "Kit"),
    ("Keycard", "Carte d'accès"),
    ("Key", "Clé"),
    ("Room", "Salle"),
    ("Office", "Bureau"),
    ("Storage Room", "Réserve"),
    ("Server Room", "Salle serveur"),
    ("Conference Room", "Salle de conférence"),
    ("Reception Room", "Réception"),
    ("Infirmary", "Infirmerie"),
    ("Laboratory", "Laboratoire"),
    ("Lab", "Labo"),
    ("Dormitory", "Dortoir"),
    ("Barracks", "Caserne"),
    ("Workshop", "Atelier"),
    ("Assembly", "Assemblage"),
    ("Central Command", "Commandement central"),
    ("Cargo Plane", "Avion-cargo"),
    ("Cement Plant", "Cimenterie"),
    ("Buoyancy", "Flottabilité"),
    ("Black Chamber", "Chambre noire"),
    ("CEO", "PDG"),
    ("VIP", "VIP"),
    ("Golden Egg Nest", "Nid de l'œuf doré"),
]

WORD = {
    'Small': 'petit', 'Large': 'grand', 'Heavy': 'lourd', 'Light': 'léger',
    'Long': 'long', 'Short': 'court', 'Extended': 'rallongé', 'Quick': 'rapide',
    'Tactical': 'tactique', 'Practical': 'pratique', 'Stable': 'stable',
    'Angled': 'incliné', 'Vertical': 'vertical', 'Horizontal': 'horizontal',
    'Combat': 'de combat', 'Field': 'de campagne', 'Military': 'militaire',
    'Standard': 'standard', 'Enhanced': 'amélioré', 'Advanced': 'avancé',
    'Reinforced': 'renforcé', 'Improved': 'amélioré', 'Precision': 'de précision',
    'Sniper': 'de précision', 'Hunter': 'de chasse', 'Ranger': 'de randonnée',
    'Digital': 'numérique', 'Portable': 'portable', 'Electric': 'électrique',
    'Gold': 'en or', 'Pure': 'pur', 'Silver': 'en argent', 'Antique': 'ancien',
    'Ancient': 'ancien', 'Rare': 'rare', 'Broken': 'cassé', 'Old': 'vieux',
}

GRADE_FR = {0: 'Non classé', 1: 'Commun', 2: 'Peu commun', 3: 'Rare', 4: 'Épique', 5: 'Légendaire', 6: 'Mythique'}


def translate(name):
    n = name
    for a, b in PHRASES:
        if a.lower() in n.lower():
            n = re.sub(re.escape(a), b, n, flags=re.I)
    for a, b in WORD.items():
        n = re.sub(r'\b' + re.escape(a) + r'\b', b, n)
    return n


if __name__ == '__main__':
    out = []
    changed = 0
    for it in items:
        fr = translate(it['name'])
        if fr != it['name']:
            changed += 1
        out.append((it['group'], it['name'], fr))
    print('noms modifiés :', changed, '/', len(items))
    for g in ['Weapons', 'Gear', 'Keys', 'Consumables']:
        print('==', g)
        for it in [i for i in out if i[0] == g][:6]:
            print('  ', it[1], '->', it[2])
    print('== exemples collectibles')
    for it in [i for i in out if i[0] == 'Collectibles'][:8]:
        print('  ', it[1], '->', it[2])
