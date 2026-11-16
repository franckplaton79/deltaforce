"""Traduction française des noms d'objets, avec lexique et recomposition.

Le lexique couvre les 533 mots distincts qui apparaissent dans les noms
d'objets, d'équipement, de consommables et de cartes d'accès. Chaque entrée
porte sa nature (nom, adjectif, sigle) pour que la recomposition respecte
l'ordre français : nom principal, puis adjectifs, puis complément.

Export utilisé par make_db.py : translate(name, group, cat)
"""
import re

# --- adjectifs : (traduction, féminin) ---
ADJ = {
    'basic': 'basique', 'advanced': 'avancé', 'adapted': 'adapté', 'adjustable': 'réglable',
    'air-cooled': 'refroidi par air', 'alloy': 'en alliage', 'analog': 'analogique',
    'ancient': 'ancien', 'angled': 'incliné', 'antique': 'ancien', 'aramid': 'aramide',
    'architectural': 'architectural', 'armored': 'blindé', 'automated': 'automatisé',
    'bagged': 'en sachet', 'ballistic': 'balistique', 'big': 'grand', 'black': 'noir',
    'blue': 'bleu', 'boxed': 'en boîte', 'broken': 'cassé', 'canned': 'en conserve',
    'carbon': 'en carbone', 'carved': 'sculpté', 'ceramic': 'en céramique',
    'copper': 'en cuivre', 'cordless': 'sans fil', 'corrugated': 'ondulé',
    'crispy': 'croustillant', 'damaged': 'endommagé', 'dancing': 'dansant',
    'digital': 'numérique', 'drip': 'filtre', 'dry': 'sec', 'elastic': 'élastique',
    'electric': 'électrique', 'electronic': 'électronique', 'encrypted': 'chiffré',
    'experimental': 'expérimental', 'extended-release': 'à libération prolongée',
    'external': 'externe', 'effervescent': 'effervescent', 'fighting': 'de combat',
    'first': 'de premiers', 'free': 'gratuit', 'fried': 'frit', 'glass': 'en verre',
    'golden': 'doré', 'heavy': 'lourd', 'high-power': 'haute puissance',
    'high-power': 'haute puissance', 'high-precision': 'haute précision',
    'high-speed': 'haute vitesse', 'hydraulic': 'hydraulique', 'intermediate': 'intermédiaire',
    'light': 'léger', 'local': 'local', 'luxury': 'de luxe', 'mechanical': 'mécanique',
    'medical': 'médical', 'military': 'militaire', 'mobile': 'mobile', 'multi-purpose': 'multi-usage',
    'needle-nose': 'à bec fin', 'nylon': 'en nylon', 'outdoor': 'd’extérieur',
    'personal': 'personnel', 'polyethylene': 'en polyéthylène', 'polymer': 'en polymère',
    'portable': 'portable', 'premium': 'premium', 'pressure': 'de pression',
    'printed': 'imprimé', 'private': 'privé', 'professional': 'professionnel',
    'programmable': 'programmable', 'purified': 'purifiée', 'pure': 'pur', 'quick': 'rapide',
    'quick-use': 'à usage rapide', 'rechargeable': 'rechargeable', 'reinforced': 'renforcé',
    'retro': 'rétro', 'rusty': 'rouillé', 'saline': 'salé', 'secret': 'secret',
    'shiny': 'brillant', 'simple': 'simple', 'small': 'petit', 'smoothbore': 'à canon lisse',
    'solid': 'massif', 'sonic': 'sonique', 'special': 'spécial', 'specialty': 'spécial',
    'spinning': 'tournant', 'square': 'carré', 'stamped': 'estampé', 'standard': 'standard',
    'sterile': 'stérile', 'super': 'super', 'surgical': 'chirurgical', 'sugar': 'sans sucre',
    'thermal': 'thermique', 'titanium': 'en titane', 'top': 'de premier', 'universal': 'universel',
    'waterproof': 'étanche', 'weird': 'étrange', 'wide-angle': 'grand-angle', 'wooden': 'en bois',
    'steel': 'en acier', 'gold': 'en or', 'silver': 'en argent', 'rare': 'rare', 'old': 'vieux',
    'rapid': 'rapide', 'sharp': 'affûté', 'worn': 'usé', 'empty': 'vide', 'full': 'plein',
    'single': 'simple', 'double': 'double', 'triple': 'triple', 'mini': 'mini',
    'large': 'grand', 'medium': 'moyen', 'maximum': 'maximum', 'extra': 'extra',
}

# --- noms : traduction ---
NOUN = {
    'adapter': 'adaptateur', 'alcohol': 'alcool', 'antenna': 'antenne', 'antibiotics': 'antibiotiques',
    'apple': 'pomme', 'array': 'réseau', 'audio': 'audio', 'backpack': 'sac à dos',
    'bag': 'sac', 'bandage': 'bandage', 'bank': 'banque', 'bar': 'barre', 'baseball': 'baseball',
    'battery': 'pile', 'beans': 'grains', 'bee': 'abeille', 'bill': 'billet', 'binoculars': 'jumelles',
    'blade': 'lame', 'blueprints': 'plans', 'board': 'panneau', 'booster': 'booster',
    'bottle': 'bouteille', 'box': 'boîte', 'brush': 'brosse', 'bucket': 'seau', 'bun': 'pain',
    'bust': 'buste', 'cable': 'câble', 'caliper': 'pied à coulisse', 'camera': 'appareil photo',
    'candles': 'bougies', 'canister': 'cartouche', 'cap': 'casquette', 'capacitor': 'condensateur',
    'capsule': 'capsule', 'card': 'carte', 'cell': 'cellule', 'ceramics': 'céramique',
    'champagne': 'champagne', 'charm': 'breloque', 'chest': 'coffre', 'circuit': 'circuit',
    'claw': 'griffe', 'cleaner': 'nettoyant', 'clock': 'horloge', 'cloud': 'nuage',
    'coffee': 'café', 'coin': 'pièce', 'combo': 'ensemble', 'computer': 'ordinateur',
    'controller': 'manette', 'crate': 'caisse', 'crest': 'blason', 'crossbow': 'arbalète',
    'crusher': 'concasseur', 'cutlass': 'coutelas', 'dagger': 'dague', 'data': 'données',
    'decoration': 'décoration', 'defibrillator': 'défibrillateur', 'design': 'design',
    'device': 'appareil', 'disc': 'disque', 'dish': 'antenne parabolique', 'disk': 'disque',
    'djembe': 'djembé', 'document': 'document', 'documents': 'documents', 'drawing': 'dessin',
    'dressing': 'pansement', 'drill': 'perceuse', 'drive': 'disque', 'duct': 'conduit',
    'earrings': 'boucles d’oreilles', 'exhibit': 'pièce d’exposition', 'fabric': 'tissu',
    'fiber': 'fibre', 'fiberboard': 'panneau de fibres', 'files': 'dossiers',
    'flask': 'flacon', 'flight': 'vol', 'forceps': 'pinces', 'fossil': 'fossile',
    'fragment': 'fragment', 'fuel': 'carburant', 'gas': 'gaz', 'gel': 'gel', 'girl': 'fille',
    'gloves': 'gants', 'glue': 'colle', 'grinder': 'meuleuse', 'gun': 'arme', 'gunpowder': 'poudre',
    'hammer': 'marteau', 'handsaw': 'scie à main', 'hat': 'chapeau', 'heart': 'cœur',
    'heat': 'chaleur', 'helmet': 'casque', 'hookah': 'chicha', 'hotel': 'hôtel',
    'imager': 'imageur', 'infusion': 'perfusion', 'injector': 'injecteur',
    'interface': 'interface', 'iron': 'fer', 'issue': 'numéro', 'jammer': 'brouilleur',
    'jewelry': 'bijou', 'keyboard': 'clavier', 'kit': 'kit', 'lading': 'connaissement',
    'laptop': 'ordinateur portable', 'lens': 'objectif', 'leveler': 'niveleuse',
    'lighter': 'briquet', 'manometer': 'manomètre', 'mantel': 'manteau de cheminée',
    'mask': 'masque', 'matches': 'allumettes', 'measure': 'mesure', 'medal': 'médaille',
    'memory': 'mémoire', 'meter': 'compteur', 'model': 'modèle', 'motherboard': 'carte mère',
    'motorcycle': 'moto', 'mouse': 'souris', 'multitool': 'outil multifonction',
    'music': 'musique', 'nails': 'clous', 'network': 'réseau', 'newspaper': 'journal',
    'noodles': 'nouilles', 'note': 'note', 'notebook': 'carnet', 'oximeter': 'oxymètre',
    'pack': 'sac', 'packet': 'sachet', 'painkiller': 'antidouleur', 'paint': 'peinture',
    'panel': 'panneau', 'part': 'pièce', 'parts': 'pièces', 'pen': 'stylo',
    'pendant': 'pendentif', 'phone': 'téléphone', 'photo': 'photo', 'pipe': 'tuyau',
    'plank': 'planche', 'pliers': 'pinces', 'pot': 'pot', 'powder': 'poudre',
    'processor': 'processeur', 'protein': 'protéine', 'radio': 'radio', 'ration': 'ration',
    'reader': 'lecteur', 'recorder': 'enregistreur', 'relay': 'relais', 'ring': 'bague',
    'robot': 'robot', 'rocket': 'fusée', 'router': 'routeur', 'rucksack': 'sac à dos',
    'sample': 'échantillon', 'saw': 'scie', 'scissors': 'ciseaux', 'screen': 'écran',
    'screwdriver': 'tournevis', 'sculpture': 'sculpture', 'seasoning': 'assaisonnement',
    'server': 'serveur', 'set': 'ensemble', 'sheet': 'feuille', 'shell': 'coque',
    'sink': 'évier', 'sledgehammer': 'masse', 'sling': 'sangle', 'socket': 'prise',
    'solution': 'solution', 'sound': 'son', 'speakers': 'enceintes', 'spray': 'aérosol',
    'stamina': 'endurance', 'station': 'station', 'statue': 'statue', 'stethoscope': 'stéthoscope',
    'stimulant': 'stimulant', 'stove': 'réchaud', 'tablets': 'comprimés', 'tape': 'ruban',
    'tea': 'thé', 'telescope': 'longue-vue', 'terminal': 'terminal', 'tester': 'testeur',
    'thermometer': 'thermomètre', 'tool': 'outil', 'toothpaste': 'dentifrice',
    'torch': 'lampe torche', 'tourniquet': 'garrot', 'trophy': 'trophée', 'tube': 'tube',
    'unit': 'unité', 'vacuum': 'aspirateur', 'ventilator': 'ventilateur', 'vest': 'gilet',
    'vial': 'flacon', 'video': 'vidéo', 'vitamin': 'vitamine', 'watch': 'montre',
    'water': 'eau', 'wine': 'vin', 'wire': 'fil', 'wood': 'bois', 'worker': 'ouvrier',
    'wrench': 'clé', 'yogurt': 'yaourt', 'activator': 'activateur', 'alcohol': 'alcool',
    'ammo': 'munitions', 'bank': 'banque', 'blitz': 'blitz', 'board': 'panneau',
    'booster': 'booster', 'cable': 'câble', 'charm': 'breloque', 'claw': 'griffe',
    'combo': 'ensemble', 'crusher': 'concasseur', 'dance': 'danse', 'djembe': 'djembé',
    'drill': 'perceuse', 'exhibit': 'exposition', 'gazelle': 'gazelle', 'gloves': 'gants',
    'hawk': 'faucon', 'hurricane': 'ouragan', 'joker': 'joker', 'king': 'roi',
    'leveler': 'niveleuse', 'medusa': 'méduse', 'merit': 'mérite', 'pangolin': 'pangolin',
    'pirate': 'pirate', 'portrait': 'portrait', 'poster': 'affiche', 'queen': 'dame',
    'raider': 'pillard', 'rainforest': 'forêt tropicale', 'reactor': 'réacteur',
    'reis': 'reis', 'saeed': 'Saeed', 'sphinx': 'sphinx', 'spinosaurus': 'spinosaurus',
    'sports': 'sport', 'spy': 'espion', 'staff': 'état-major', 'tank': 'char',
    'titan': 'titan', 'trade': 'commerce', 'training': 'entraînement', 'trajectory': 'trajectoire',
    'transaction': 'transaction', 'trek': 'randonnée', 'warrior': 'guerrier',
    'wine': 'vin', 'champagne': 'champagne', 'cement': 'ciment', 'mocha': 'moka',
    'jewelry': 'bijoux', 'glass': 'verre', 'wine glass': 'verre à vin',
}

# --- expressions figées, prioritaires ---
FIXED = {
    '999.9 gold bar': "lingot d'or 999,9", 'gold bar': "lingot d'or",
    'air-cooled heat sink': 'dissipateur refroidi par air',
    'ancient pirate telescope': 'longue-vue de pirate ancienne',
    'ancient sphinx statue': 'statue de sphinx ancienne',
    'ace staff trophy': 'trophée de l’état-major',
    'african wood sculpture': 'sculpture africaine en bois',
    'angle grinder': 'meuleuse d’angle', 'solar panel': 'panneau solaire',
    'socket adapter': 'adaptateur de prise', 'wide-angle lens': 'objectif grand-angle',
    'intel recorder': 'enregistreur de renseignement',
    'digital camera': 'appareil photo numérique', 'bone saw': 'scie à os',
    'military binoculars': 'jumelles militaires', 'gold crest': 'blason doré',
    'pure gold lighter': 'briquet en or pur', 'ceremony dagger': 'dague de cérémonie',
    'military explosive': 'explosif militaire', 'cell phone': 'téléphone portable',
    'delta force: task force dagger': 'Delta Force : Task Force Dagger',
    'mocha coffee pot': 'cafetière à moka', 'bagged coffee beans': 'grains de café en sachet',
    'boxed drip coffee': 'café filtre en boîte',
    'capsule coffee machine set': 'machine à capsules de café',
    'g.t.i. satcom antenna': 'antenne SATCOM G.T.I.',
    'ahsarah specialty wine glass': 'verre à vin spécial Ahsarah',
    'ahsarah specialty ceramics': 'céramique spéciale Ahsarah',
    'ahsarah specialty flask': 'flacon spécial Ahsarah',
    'ahsarah glamour hookah': 'chicha glamour Ahsarah',
    'ahsarah fashion weekly': 'hebdomadaire mode Ahsarah',
    'ahsarah news weekly': 'hebdomadaire d’actualités Ahsarah',
    'ahsarah entertainment monthly': 'mensuel divertissement Ahsarah',
    'ahsarah guard confidential files': 'dossiers confidentiels de la garde Ahsarah',
    'heart of africa': "Cœur d'Afrique",
    'medical ventilator': 'Ventilateur médical',
    'power battery pack': 'Bloc de batteries haute puissance',
    'reinforced carbon fiberboard': 'Panneau de fibres de carbone renforcé',
    'armored vehicle battery': 'Batterie de véhicule blindé',
    'military power bank': 'Batterie externe militaire',
    'portable military radar': 'Radar militaire portable',
    'infantry fighting vehicle model': 'Modèle de véhicule de combat d’infanterie',
    'box of nails': 'Boîte de clous', 'bucket of paint': 'Seau de peinture',
    'bust of claudius': 'Buste de Claude',
    'pack of cement': 'Sac de ciment',
    'stamped through bill of lading': 'Connaissement visé',
    'power': 'Alimentation',
    'king\'s suite': 'Suite royale', 'prince\'s suite': 'Suite princière',
    "king's suite": 'Suite royale', "prince's suite": 'Suite princière',
    'hotel dining room': 'Salle à manger de l’hôtel',
    'hotel staff break room': 'Salle de pause du personnel de l’hôtel',
    'medical conference room': 'Salle de conférence médicale',
    'museum abandoned exhibition hall': 'Halle d’exposition abandonnée du musée',
    'museum exhibition suite': 'Suite d’exposition du musée',
    'museum surveillance room': 'Salle de surveillance du musée',
    'new tower of babel power supply access card': 'Carte d’accès à l’alimentation de la nouvelle tour de Babel',
    'old bath diner': 'Restaurant des bains anciens',
    'old bath vip room': 'Salon VIP des bains anciens',
    'radar station conference room': 'Salle de conférence de la station radar',
    'radar station control room': 'Salle de contrôle de la station radar',
    'radar station data center': 'Centre de données de la station radar',
    'radar station side entrance keycard': 'Carte d’accès à l’entrée latérale de la station radar',
    'radar station uav platform': 'Plateforme de drone de la station radar',
    'relink implant surgery room': 'Salle de chirurgie implant Relink',
    'small train station ticket office': 'Guichet de la petite gare',
    'substation dormitory': 'Dortoir du poste électrique',
    'substation tech room': 'Salle technique du poste électrique',
    'test range core': 'Noyau du champ de tir',
    'test range data center': 'Centre de données du champ de tir',
    'underground vault storage': 'Réserve du coffre souterrain',
    'vehicle first aid kit': 'Trousse de secours pour véhicule',
    'field energy bar': 'barre énergétique de campagne',
    'field med crate': 'caisse médicale de campagne',
    'field first aid kit': 'trousse de secours de campagne',
    'dek field surgical kit': 'kit chirurgical de campagne DEK',
    'diy helmet repair kit': 'kit de réparation de casque (improvisé)',
    'diy vest repair kit': 'kit de réparation de gilet (improvisé)',
    'cat tourniquet': 'garrot CAT', 'elastic bandage': 'bandage élastique',
    'bottled antibiotics': 'antibiotiques en flacon',
    'basic injector': 'injecteur basique', 'enhanced injector': 'injecteur amélioré',
    'dve painkiller': 'antidouleur DVE',
    'extended-release painkiller': 'antidouleur à libération prolongée',
    'ev battery': 'batterie de véhicule électrique', 'fuel cell': 'pile à combustible',
    '9v battery': 'pile 9V', 'asos motherboard': 'carte mère ASOS',
    'graphics card': 'carte graphique', 'hifi sound card': 'carte son HiFi',
    'analog thermometer': 'thermomètre analogique',
    'boonie hat': 'chapeau boonie', 'als load system': 'harnais modulaire ALS',
    'basic chest rig': 'gilet tactique basique',
    'basic portable chest rig': 'gilet tactique portable basique',
    'basic stab vest': 'gilet pare-coups basique',
    'portable chest rig': 'gilet tactique portable',
    'light chest rig': 'gilet tactique léger',
    'tactical chest rig': 'gilet tactique',
    'heavy tactical bag': 'sac tactique lourd',
    'field chest rig': 'gilet tactique de campagne',
    'recon chest rig': 'gilet tactique de reconnaissance',
    'tactical backpack': 'sac à dos tactique',
    'universal tactical backpack': 'sac à dos tactique universel',
    'tactical climbing bag': 'sac d’escalade tactique',
    'anti-riot helmet': 'casque anti-émeute',
    '3h tactical backpack': 'sac à dos tactique 3H',
    'd7 tactical backpack': 'sac à dos tactique D7',
    'dash tactical backpack': 'sac à dos tactique DASH',
    'assault tactical backpack': 'sac à dos tactique d’assaut',
    'assault tactical vest': 'gilet tactique d’assaut',
    'assault vest': 'gilet d’assaut',
    'adamantine vest': 'gilet Adamantine',
    'd01 light chest rig': 'gilet tactique léger D01',
    'g01 tactical chest rig': 'gilet tactique G01',
    'hd3 tactical chest rig': 'gilet tactique HD3',
    'hk3 portable chest rig': 'gilet tactique portable HK3',
    'dsa tactical chest rig': 'gilet tactique DSA',
    'dar assault chest rig': 'gilet tactique d’assaut DAR',
    'gir field chest rig': 'gilet tactique de campagne GIR',
    'gto heavy tactical bag': 'sac tactique lourd GTO',
    'hurricane tactical chest rig': 'gilet tactique Hurricane',
    'pangolin universal tactical backpack': 'sac à dos tactique universel Pangolin',
    'quick recon chest rig': 'gilet tactique de reconnaissance rapide',
    'black hawk field chest rig': 'gilet tactique de campagne Black Hawk',
    'drc advanced recon chest rig': 'gilet tactique de reconnaissance avancée DRC',
    'light tactical chest rig': 'gilet tactique léger',
    'universal tactical chest rig': 'gilet tactique universel',
    'basic chest rig': 'gilet tactique basique',
    'field hiking backpack': 'sac à dos de randonnée de campagne',
    'ga field backpack': 'sac à dos de campagne GA',
    'gt5 field backpack': 'sac à dos de campagne GT5',
    'camping backpack': 'sac à dos de camping',
    'hiking backpack': 'sac à dos de randonnée',
    'barracks storage room': 'réserve de la caserne',
}

WEAPON_TAIL = {
    'assault rifle': "fusil d'assaut", 'battle rifle': 'fusil de combat',
    'compact assault rifle': "fusil d'assaut compact",
    'marksman rifle': 'fusil de précision semi-auto', 'sniper rifle': 'fusil de précision',
    'submachine gun': 'pistolet-mitrailleur', 'light machine gun': 'mitrailleuse légère',
    'general machine gun': 'mitrailleuse lourde', 'shotgun': 'fusil à pompe',
    'revolver': 'revolver', 'pistol': 'pistolet',
}

ATTACH_TAIL = [
    ('barrel combo', 'canon complet'), ('short barrel set', 'ensemble canon court'),
    ('barrel heat shield', 'protège-canon'), ('stock pad', 'pad de crosse'),
    ('recoil pad', 'pad anti-recul'), ('laser-light combo', 'ensemble laser-lampe'),
    ('suppressed combo', 'ensemble intégralement modéré'),
    ('long barrel', 'canon long'), ('short barrel', 'canon court'), ('barrel', 'canon'),
    ('collapsible stock (extended)', 'crosse télescopique déployée'),
    ('collapsible stock (folded)', 'crosse télescopique repliée'),
    ('fixed stock', 'crosse fixe'), ('light stock', 'crosse légère'),
    ('stable stock', 'crosse stable'), ('stock', 'crosse'),
    ('rear grip', 'poignée arrière'), ('foregrip', 'poignée avant'), ('grip', 'poignée'),
    ('handguard panel', 'panneau de garde-main'), ('handguard', 'garde-main'),
    ('drum mag', 'chargeur tambour'), ('extended mag', 'chargeur rallongé'),
    ('magazine', 'chargeur'), ('mag', 'chargeur'), ('scope', 'lunette'),
    ('red dot', 'point rouge'), ('sight', 'viseur'), ('optic', 'optique'),
    ('suppressor', 'silencieux'), ('compensator', 'compensateur'),
    ('muzzle brake', 'frein de bouche'), ('flash hider', 'cache-flamme'),
    ('laser', 'laser'), ('bipod', 'bipied'), ('mount', 'montage'),
    ('adapter', 'adaptateur'), ('kit', 'kit'), ('panel', 'panneau'), ('base', 'base'),
    ('spring', 'ressort'), ('buffer spring', 'ressort de recul'),
    ('charging handle', 'poignée d’armement'), ('bolt carrier group', 'ensemble culasse'),
    ('trigger', 'détente'), ('tube', 'tube'), ('rail', 'rail'),
    ('charging handle', 'poignée d’armement'), ('bolt carrier group', 'ensemble culasse'),
    ('rubber pad', 'pad en caoutchouc'), ('cheek pad', 'appui-joue'),
    ('mag well', 'puits de chargeur'), ('gas block', 'bloc de Gaz'), ('piston', 'piston'),
]

PLACES = [
    ('hotel dining room', 'salle à manger de l’hôtel'),
    ('hotel staff break room', 'salle de pause du personnel de l’hôtel'),
    ('medical conference room', 'salle de conférence médicale'),
    ('museum abandoned exhibition hall', 'halle d’exposition abandonnée du musée'),
    ('museum exhibition suite', 'suite d’exposition du musée'),
    ('museum surveillance room', 'salle de surveillance du musée'),
    ('radar station data center', 'centre de données de la station radar'),
    ('radar station conference room', 'salle de conférence de la station radar'),
    ('radar station control room', 'salle de contrôle de la station radar'),
    ('radar station side entrance keycard', 'entrée latérale de la station radar (carte)'),
    ('radar station uav platform', 'plateforme de drone de la station radar'),
    ('radar station', 'station radar'),
    ('relink implant surgery room', 'salle de chirurgie implant Relink'),
    ('small train station ticket office', 'guichet de la petite gare'),
    ('substation dormitory', 'dortoir du poste électrique'),
    ('substation tech room', 'salle technique du poste électrique'),
    ('test range data center', 'centre de données du champ de tir'),
    ('test range core', 'noyau du champ de tir'),
    ('test range', 'champ de tir'),
    ('underground vault storage', 'réserve du coffre souterrain'),
    ('underground vault', 'coffre souterrain'),
    ('new tower of babel power supply access card', 'carte d’accès à l’alimentation de la nouvelle tour de Babel'),
    ('old bath vip room', 'salon VIP des bains anciens'),
    ('old bath diner', 'restaurant des bains anciens'),
    ("king's suite", 'suite royale'), ("prince's suite", 'suite princière'),
    ('hotel', 'hôtel'), ('museum', 'musée'), ('substation', 'poste électrique'),
    ('assembly workshop', "atelier d'assemblage"),
    ('barracks storage room', 'réserve de la caserne'),
    ('barracks', 'caserne'),
    ('biological data', 'données biologiques'), ('black chamber', 'chambre noire'),
    ('buoyancy lab', 'labo de flottabilité'), ('cargo plane', 'avion-cargo'),
    ('cement plant', 'cimenterie'), ('central command', 'commandement central'),
    ('central vip', 'VIP central'), ('ceo office reception', 'réception du bureau du PDG'),
    ('ceo conference', 'salle de conférence du PDG'), ('ceo', 'PDG'),
    ('checkpoint', 'point de contrôle'), ('diamonds', 'salle des diamants'),
    ('east town', 'ville est'), ('east wing', 'aile est'), ('west wing', 'aile ouest'),
    ('eastern suspension bridge', 'pont suspendu est'),
    ('employee passage', 'passage des employés'), ('storage', 'réserve'),
    ('storeroom', 'réserve'), ('server room', 'salle serveur'),
    ('conference room', 'salle de conférence'), ('reception room', 'réception'),
    ('infirmary', 'infirmerie'), ('laboratory', 'laboratoire'), ('lab', 'labo'),
    ('dormitory', 'dortoir'), ('office', 'bureau'),
    ('room 3f', 'salle du 3e étage'), ('room', 'salle'),
    ("manager's office", 'bureau du responsable'), ('bedroom', 'chambre'),
    ('floor', 'étage'), ('basement', 'sous-sol'), ('warehouse', 'entrepôt'),
    ('control room', 'salle de contrôle'), ('bridge', 'pont'), ('wing', 'aile'),
]


def _cap(s):
    return s[:1].upper() + s[1:] if s else s


def translate_weapon(name):
    low = name.lower()
    for tail, fr in WEAPON_TAIL.items():
        if low.endswith(' ' + tail):
            base = name[:-(len(tail) + 1)]
            return f'{base}, {fr}'
        if low == tail:
            return _cap(fr)
    return name


ATTACH_WORDS = {
    'russian': 'russe', 'adjustable': 'réglable', 'accuracy': 'précision',
    'precision': 'précision', 'recon': 'reconnaissance', 'hybrid': 'hybride',
    'tactical': 'tactique', 'light': 'léger', 'heavy': 'lourd', 'stable': 'stable',
    'practical': 'pratique', 'quick': 'rapide', 'extended': 'rallongé',
    'short': 'court', 'long': 'long', 'compact': 'compact', 'combat': 'combat',
    'precision': 'précision', 'vertical': 'vertical', 'angled': 'incliné',
    'skeleton': 'squelette', 'sniper': 'précision', 'marksman': 'tireur d’élite',
    'assault': 'assaut', 'special': 'spécial', 'elite': 'élite', 'pro': 'pro',
    'high-power': 'haute puissance', 'reinforced': 'renforcé', 'ultralight': 'ultraléger',
    'ergonomic': 'ergonomique', 'titanium': 'titane', 'carbon': 'carbone',
    'aluminum': 'aluminium', 'polymer': 'polymère', 'steel': 'acier',
    'beaver': 'Beaver', 'performance': 'performance', 'transcendent': 'Transcendent',
    'carbon fiber': 'fibre de carbone', 'gabriel': 'Gabriel', 'raid': 'raid',
    'specops': 'opérations spéciales', 'trench': 'tranchée', 'integral': 'intégral',
    'integrally': 'intégré', 'stock': 'crosse', 'pad': 'pad', 'base': 'base',
    'balanced': 'équilibrée', 'grip': 'poignée', 'platform': 'plateforme',
    'marksman': 'tireur d’élite', 'guard': 'garde', 'hurricane': 'ouragan',
    'elite': 'élite', 'heavy': 'lourd', 'long': 'long', 'short': 'court',
    'tidal': 'Tidal', 'ultra-long': 'ultra-long', 'scout': 'éclaireur',
    'stealth': 'furtif', 'stinger': 'Stinger', 'longbow': 'arc long',
    'breakthrough': 'percée', 'defender': 'défense', 'bastion': 'Bastion',
    'longsword': 'épée longue', 'rail': 'rail', 'tsunami': 'Tsunami',
    'resonant': 'résonant', 'rifle': 'fusil', 'sniper': 'précision',
    'grip adapter': 'adaptateur de poignée', 'suppressor': 'silencieux',
    'purple': 'violet', 'green': 'vert', 'red': 'rouge', 'blue': 'bleu',
    'heat shield': 'protège-canon', 'combo': 'ensemble', 'set': 'ensemble',
    'light': 'lampe', 'laser': 'laser',
}


def translate_attachment(name):
    low = name.lower()
    # « calibre 30 coups » : 5.56x45 30-Round Aluminum Mag
    m = re.match(r'^([\d.]+x?\d*[a-z]*) (\d+)-Round (.+?) (?:Mag|Magazine)$', name, re.I)
    if m:
        mat = {'aluminum': 'aluminium', 'polymer': 'polymère', 'steel': 'acier'}.get(m.group(3).lower(), m.group(3).lower())
        return f'{m.group(1)}, chargeur {m.group(2)} coups en {mat}'
    for tail, fr in ATTACH_TAIL:
        if low.endswith(' ' + tail):
            base = name[:-(len(tail) + 1)]
            def w(m):
                return ATTACH_WORDS.get(m.group(0).lower(), m.group(0))
            base = re.sub(r'\b[A-Za-z][A-Za-z\-]*\b', w, base)
            base = re.sub(r'\bScope\b', 'lunette', base)
            return f'{base} : {fr}'
    return name


def translate_key(name):
    out = name
    for a, b in sorted(PLACES, key=lambda x: -len(x[0])):
        out = re.sub(r'(?<![A-Za-z])' + re.escape(a) + r'(?![A-Za-z])', b, out, flags=re.I)
    return _cap(out)


def translate_common(name):
    low = name.lower().strip()
    if low in FIXED:
        fr = FIXED[low]
        return _cap(fr)
    words = re.findall(r"[A-Za-z][A-Za-z\-'’]*|[0-9][\w.\-]*|[^A-Za-z0-9\s]+", name)
    out = []
    for w in words:
        lw = w.lower()
        if lw in ADJ:
            out.append(ADJ[lw])
        elif lw in NOUN:
            out.append(NOUN[lw])
        else:
            out.append(w)
    s = ' '.join(out)
    s = re.sub(r'\s+([,;:])', r'\1', s)
    return _cap(s.strip())


def translate(name, group, cat=None):
    if group == 'Weapons':
        return translate_weapon(name)
    if group == 'Attachments':
        return translate_attachment(name)
    if group == 'Keys':
        return translate_key(name)
    if group == 'Ammo':
        return name
    return translate_common(name)


if __name__ == '__main__':
    import json, os
    items = json.load(open('/home/user/delta-force-guide/data/items.json', encoding='utf-8'))
    for g in ['Collectibles', 'Gear', 'Consumables', 'Keys', 'Attachments', 'Weapons']:
        print('==', g)
        for i in [x for x in items if x['group'] == g][:10]:
            print('  ', i['name'], '->', translate(i['name'], g, i['cat']))
