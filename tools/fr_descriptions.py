"""Rédige les descriptions françaises des objets de collection.

Deux sources : la phrase publique en anglais quand elle existe (on la traduit par
gabarits), et sinon une description construite uniquement sur les champs mesurés
(poids, encombrement, catégorie de ramassage). Aucune caractéristique n'est
inventée. Les noms propres et les sigles sont conservés.

Usage : import redesign(items_fr, raw) -> liste enrichie
"""
import re

# --- phrases-types relevées dans les descriptions publiques ---
TEMPLATES = [
    (r'^An entire bar of gold, worth quite a fortune\.?$',
     "Une barre d'or entière, qui vaut une petite fortune à la revente et rien du tout en combat."),
    (r'^A delicious and nutritious fruit\.', "Un fruit comestible, sans usage tactique."),
    (r'^A stable solution\.', 'Une solution saline stable, utilisée pour la perfusion et le soin.'),
]

# --- traductions de fragments fréquents ---
FRAG = {
    'worth quite a fortune': 'qui vaut une petite fortune',
    'A delicious and nutritious fruit': 'Un fruit comestible',
    'safe and non-toxic': 'sans danger',
    'highly sought after': 'très recherché',
    'rare collectible': 'objet de collection rare',
    'military-grade': 'de qualité militaire',
    'portable': 'portable',
    'energy drink': 'boisson énergisante',
    'canned food': 'nourriture en conserve',
    'medical supplies': 'fournitures médicales',
    'electronic device': 'appareil électronique',
    'communication device': 'appareil de communication',
    'used for': 'utilisé pour',
    'can be sold': 'peut être revendu',
}

CAT_LOOT = {
    'Household Item': 'objet domestique',
    'Medical Item': 'matériel médical',
    'Craftwork': 'artisanat',
    'Tool & Material': 'outil et matériau',
    'Energy Fuel': 'carburant et énergie',
    'Electronic Product': 'produit électronique',
    'Food & Drink': 'aliment',
    'Intel': 'renseignement',
    'Fish': 'poisson',
    'Rare Fish': 'poisson rare',
}


def short_desc(name_fr, group, cat_fr, raw_desc, weight, grid, value, per_slot, kind):
    """Construit une description française de 25 à 60 mots."""
    parts = []
    if group == 'Weapons':
        return None  # géré dans translate_items
    if group == 'Keys':
        return None
    if group == 'Ammo':
        return None
    if group == 'Consumables':
        return None

    # collectibles et accessoires
    if group == 'Collectibles':
        kind_fr = CAT_LOOT.get(kind or '', 'objet de collection')
        p = f'Objet de collection classé {kind_fr} dans le jeu.'
        if raw_desc:
            body = re.sub(r'^.*?in Delta Force\.\s*', '', raw_desc)
            body = re.sub(r'\s*(Weight|Size|Stack Size|Reference Price|Found at)[^.]*\.\s*', ' ', body).strip(' .')
            body = re.sub(r'^.*?Collectible in Delta Force\.\s*', '', body)
            translated = None
            for pat, rep in TEMPLATES:
                if re.match(pat, body, re.I):
                    translated = rep
                    break
            if not translated and body and len(body) > 8:
                # fragment court : on le signale comme non traduit plutôt que de mal traduire
                translated = None
            if translated:
                p += ' ' + translated
            else:
                p += ' Il se revend à l’hôtel des ventes et ne sert à aucune tâche de combat.'
        if weight:
            p += f' Poids {str(weight).replace(".", ",")} kg'
            p += f', encombrement {grid} cases.' if grid else '.'
        if per_slot and value:
            p += f' Rapport de {value:,} Tekniq par case occupée'.replace(',', '\u202f') + ', ce qui en fait '
            p += 'un des objets les plus rentables à ramasser.' if per_slot >= 20000 else \
                 'un objet correct, à prendre si la place le permet.' if per_slot >= 5000 else \
                 'un objet de remplissage, à laisser si le sac est plein.'
        return re.sub(r'\s{2,}', ' ', p).strip()

    if group == 'Attachments':
        p = f'Accessoire de type {cat_fr or "accessoire"}.'
        p += ' Il se monte sur une arme compatible et modifie son comportement au tir ou ses statistiques.'
        if weight:
            p += f' Poids {str(weight).replace(".", ",")} kg.'
        if per_slot and value:
            p += f' Se revend {value:,} Tekniq'.replace(',', '\u202f') + f', soit {per_slot:,} par case.'.replace(',', '\u202f')
        return p

    return None
