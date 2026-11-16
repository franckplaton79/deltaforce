# -*- coding: utf-8 -*-
"""Génère les six pages de la base de données à partir de data/items_fr.json.

Chaque fiche affiche : icône JPG locale, nom français, nom d'origine en petit,
catégorie traduite, grade, description française rédigée à partir des
caractéristiques présentes, valeur de référence et valeur par case.
"""
import html
import json
import os
import sys

sys.path.insert(0, '/home/user/delta-force-guide/tools')
from lexique import translate  # noqa: E402

ROOT = '/home/user/delta-force-guide'
items = json.load(open(os.path.join(ROOT, 'data', 'items_fr.json'), encoding='utf-8'))

GROUP_FR = {'Weapons': 'Armes', 'Ammo': 'Munitions', 'Gear': 'Équipement',
            'Attachments': 'Accessoires', 'Collectibles': 'Objets de collection',
            'Keys': 'Cartes et clés', 'Consumables': 'Consommables'}
GRADE_FR = {0: 'non classé', 1: 'commun', 2: 'peu commun', 3: 'rare',
            4: 'épique', 5: 'légendaire', 6: 'mythique'}


def fr(n):
    return f'{n:,}'.replace(',', '\u202f') if n not in (None, 0) else '—'


def card(it):
    name_fr = translate(it['name'], it['group'], it['cat'])
    grade = it.get('grade') or 0
    bits = []
    if it.get('grid'):
        bits.append(f"{it['grid']} cases")
    if it.get('weight'):
        bits.append(f"{str(it['weight']).replace('.', ',')} kg")
    if it.get('pen'):
        bits.append(f'pénétration {it["pen"]}')
    if it.get('stack'):
        bits.append(f'pile de {it["stack"]}')
    if it.get('spots'):
        bits.append(f'{it["spots"]} lieu(x) de ramassage')
    desc = it.get('desc_fr') or ''
    cat = it.get('cat_fr') or ''
    search = ' '.join([name_fr, it['name'], cat, GROUP_FR.get(it['group'], '')]).lower()
    search = search.replace('"', '').replace("'", ' ')
    return (
        f'<article class="db-card g{grade}" data-grade="{grade}" data-cat="{cat}" data-name="{search}">'
        f'<img src="{it["icon"]}" alt="{name_fr}" loading="lazy" width="96" height="96">'
        f'<div class="db-body"><h3>{name_fr}</h3>'
        f'<p class="db-en">{it["name"]} · {cat}</p>'
        + (f'<p class="db-desc">{desc}</p>' if desc else
           '<p class="db-desc muted">Fiche technique non publiée par le jeu pour cet objet.</p>')
        + (f'<p class="db-meta">{". ".join(bits)}</p>' if bits else '')
        + f'<p class="db-val"><b>{fr(it.get("value"))}</b> Tekniq'
          f'<span>grade {grade} {GRADE_FR.get(grade, "")} · {fr(it.get("perSlot"))} par case</span></p>'
        f'</div></article>'
    )


def toolbar(prefix, cats, grades=True):
    out = [f'<div class="db-tools">',
           f'<div class="field"><label for="{prefix}Search">Chercher</label>'
           f'<input id="{prefix}Search" type="search" placeholder="Nom français ou d’origine…"></div>']
    if cats:
        out.append(f'<div class="field"><label for="{prefix}Cat">Catégorie</label><select id="{prefix}Cat">'
                   f'<option value="">Toutes</option>'
                   + ''.join(f'<option value="{c}">{lab}</option>' for c, lab in cats) + '</select></div>')
    if grades:
        out.append(f'<div class="field"><label for="{prefix}Grade">Grade minimum</label>'
                   f'<select id="{prefix}Grade"><option value="0">Tous</option>'
                   + ''.join(f'<option value="{g}">{g} · {GRADE_FR[g]}</option>' for g in range(1, 7))
                   + '</select></div>')
    out.append(f'<div class="field"><label for="{prefix}Sort">Trier par</label>'
               f'<select id="{prefix}Sort"><option value="name">Nom</option>'
               f'<option value="value">Valeur</option><option value="per">Valeur par case</option>'
               f'<option value="grade">Grade</option></select></div></div>')
    out.append(f'<p class="db-count" id="{prefix}Count"></p>')
    out.append(f'<div class="db-grid" id="{prefix}Grid">')
    return '\n'.join(out)


def page(fname, title, desc, kicker, h1, lead, tags, intro, sel, prefix, grades=True, hero=None):
    sel = sorted(sel, key=lambda i: translate(i['name'], i['group'], i['cat']).lower())
    _raw = sorted({i.get('cat_fr') or i['cat'] for i in sel})
    # un libellé plus lisible que la valeur technique du jeu
    CAT_LABEL = {
        'accessoire utilitaire': 'accessoires utilitaires',
        'canon': 'canons',
        'chargeur': 'chargeurs',
        'crosse': 'crosses',
        'frein de bouche': 'freins de bouche',
        'garde-main': 'garde-mains',
        'optique': 'optiques et viseurs',
        'poignée arrière': 'poignées arrière',
        'poignée avant': 'poignées avant',
        'casque': 'casques',
        'protection': 'protections balistiques',
        'gilet tactique': 'gilets tactiques',
        'sac à dos': 'sacs à dos',
        "fusil d'assaut": "fusils d'assaut",
        'pistolet-mitrailleur': 'pistolets-mitrailleurs',
        'pistolet': 'pistolets',
        'fusil de précision semi-auto': 'fusils de précision semi-automatiques',
        'fusil de précision': 'fusils de précision',
        'fusil à pompe': 'fusils à pompe',
        'mitrailleuse légère': 'mitrailleuses légères',
    }
    cats = [(c, CAT_LABEL.get(c, c)) for c in _raw]
    frag = (f'<!-- TITLE:{title}|DESC:{desc} -->\n<section class="page-head">\n'
            f'<div class="section-kicker">{kicker}</div>\n<h1>{h1}</h1>\n'
            f'<p class="lead">{lead}</p>\n<div class="tag-row">{tags}</div>\n</section>\n\n'
            + (f'<figure class="page-hero"><img src="assets/{hero}" alt="{html.escape(h1)}"><figcaption>{html.escape(lead)}</figcaption></figure>' if hero else '')
            + f'<section class="page-body">\n{intro.strip()}\n{toolbar(prefix, cats, grades)}\n'
            + ''.join(card(i) for i in sel) + '</div>\n'
            f'<p class="mini" style="margin-top:18px">Valeurs de référence relevées hors direct : '
            f'elles servent à comparer deux objets, pas à fixer un prix de vente. Le nom d’origine reste '
            f'affiché sous chaque fiche pour que la correspondance avec l’écran du jeu soit immédiate.</p>\n'
            f'</section>\n')
    open(os.path.join(ROOT, 'src', fname), 'w', encoding='utf-8').write(frag)
    print(f'{fname:22} {len(sel):4} fiches  {len(frag)//1024:4} ko')


by = lambda g: [i for i in items if i['group'] == g]

page('db-armes.html', 'Base de données · les 50 armes du jeu',
     'Les 50 armes avec icône, nom français, capacité, dégâts, valeur de référence et valeur par case.',
     '20 · Base de données', 'Les 50 armes, fiche par fiche',
     'Chaque fiche donne la catégorie, la capacité du chargeur, les dégâts par balle quand ils sont publiés, et la valeur de revente. Le nom d’origine reste sous le nom français, parce que c’est celui que tu lis à l’écran.',
     '<span class="tag good">50 armes</span><span class="tag">Données publiques</span>',
     '<h2>Comment lire une fiche d’arme</h2><p>La ligne du haut donne la catégorie réelle du jeu, pas une appréciation. La description reprend la capacité, les dégâts par balle et les dégâts aux protections quand le jeu les publie. Les valeurs de revente varient : elles servent à trancher entre deux armes trouvées dans le même raid.</p>'
     '<h2>Les menues options du menu, et à quoi elles servent</h2>'
     '<div class="table-wrap"><table class="data-table"><thead><tr><th>Filtre</th><th>Ce que tu obtiens</th><th>Quand l’utiliser</th></tr></thead><tbody>'
     '<tr><td>Chercher</td><td>Résultat en tapant le nom français ou le nom d’origine</td><td class="muted">Quand tu connais le nom exact affiché à l’écran du jeu, souvent en anglais.</td></tr>'
     '<tr><td>Catégorie</td><td>Une famille d’armes, avec le libellé du jeu traduit</td><td class="muted">Pour comparer deux armes du même rôle avant de dépenser.</td></tr>'
     '<tr><td>Grade minimum</td><td>Tout ce qui est au moins aussi rare que le grade choisi</td><td class="muted">Pour ne garder que la partie haute du catalogue, celle qui se revend.</td></tr>'
     '<tr><td>Trier par</td><td>Nom, valeur, valeur par case ou grade</td><td class="muted">La valeur par case pour un sac plein ; la valeur brute pour une arme qu’on garde.</td></tr>'
     '</tbody></table></div>'
     '<p>Un mot sur le tri par valeur : sur une arme, la valeur brute et la valeur par case ne racontent pas la même chose. Une arme encombrante vaut plus cher à la revente, mais elle occupe des cases dans le sac pendant tout le raid. Si tu comptes la sortir, regarde la valeur brute ; si tu comptes la revendre en chemin, regarde la valeur par case.</p>',
     by('Weapons'), 'wpn', grades=False, hero='hero-db-armes.jpg')

page('db-munitions.html', 'Base de données · les 71 munitions',
     'Les 71 munitions avec niveau de pénétration, taille de pile, poids, valeur et valeur par case.',
     '21 · Base de données', 'Toutes les munitions, du .338 au 12 gauge',
     'Le niveau de pénétration est le seul chiffre qui compte face à une protection lourde. La taille de pile, elle, décide du poids réel dans le sac.',
     '<span class="tag">71 munitions</span><span class="tag warn">Pénétration : données publiques</span>',
     '<h2>Trois chiffres, trois décisions</h2><p>Le niveau de pénétration décide si la balle traverse. La taille de pile décide combien de balles tiennent dans une case. La valeur par case décide ce qui reste à la sortie. Un chargeur plein de balles à pénétration basse est un poids mort contre un gilet correct.</p>',
     by('Ammo'), 'ammo', hero='hero-db-munitions.jpg')

page('db-equipement.html', 'Base de données · les 93 pièces d’équipement',
     'Casques, protections balistiques, gilets tactiques et sacs à dos : grade, protection, durabilité, poids et valeur.',
     '22 · Base de données', 'Casques, gilets et sacs : ce que ça protège et ce que ça vaut',
     'Une pièce d’équipement se juge sur trois critères : ce qu’elle arrête, ce qu’elle pèse et ce qu’elle coûte à remplacer. Les deux derniers sont dans le tableau.',
     '<span class="tag">93 pièces</span><span class="tag">Grade 1 à 6</span>',
     '<h2>Le grade n’est pas tout</h2><p>Un grade élevé signale une meilleure protection. Une pièce de grade moyen en bon état survit souvent mieux qu’une pièce de grade haut abîmée, parce que la durabilité se répare mal au-delà d’un certain seuil. La colonne du poids compte aussi : un sac lourd réduit la vitesse et l’endurance.</p>',
     by('Gear'), 'gear', hero='hero-db-equipement.jpg')

page('db-collectibles.html', 'Base de données · les 272 objets de collection',
     'Les 272 collectibles avec description, poids, encombrement, valeur de référence et valeur par case.',
     '23 · Base de données', 'Ce qui se ramasse et ce que ça rapporte',
     'Les objets de collection ne servent à rien en combat : ils se revendent, ou ils remplissent une tâche. La colonne qui compte est la valeur par case, parce que c’est elle qui décide quoi jeter quand le sac est plein.',
     '<span class="tag">272 objets</span><span class="tag good">Tri par valeur par case</span>',
     '<h2>Le tri le plus rentable du jeu</h2><p>Sur un même volume, un lingot d’or en une case bat un lot d’objets en cinq cases, même si le total affiché du lot est supérieur. Le filtre par grade donne la rareté, pas la rentabilité : un objet épique lourd peut rapporter moins qu’un objet rare compact.</p>',
     by('Collectibles'), 'col', hero='hero-db-collectibles.jpg')

page('db-cartes.html', 'Base de données · les 59 cartes d’accès et clés',
     'Les 59 cartes d’accès du jeu, la salle qu’elles ouvrent, leur nombre d’utilisations et leur valeur de référence.',
     '24 · Base de données', 'Cartes d’accès : ce que chaque porte cache',
     'Une carte d’accès est le seul objet du jeu dont la valeur dépend de l’endroit où tu te trouves. Ici, ce qu’elle ouvre, combien de fois, et ce qu’elle vaut.',
     '<span class="tag">59 cartes</span><span class="tag warn">Utilisations : à vérifier en jeu</span>',
     '<h2>Le nombre d’utilisations change tout</h2><p>Une carte à quarante utilisations n’a pas la même valeur qu’une carte à quatre. La première se rentabilise sur plusieurs raids, la seconde se joue une fois. Les valeurs de référence affichées sont parfois supérieures à plusieurs millions de Tekniq pour les cartes les plus rares : ce sont les prix des salles les plus rentables du jeu.</p>',
     by('Keys'), 'key', grades=True, hero='hero-db-cartes.jpg')

page('db-consommables.html', 'Base de données · les 30 consommables',
     'Les 30 consommables de raid : soins, antidouleurs, kits chirurgicaux et kits de réparation, avec effets et temps d’activation.',
     '25 · Base de données', 'Soigner, réparer, tenir : les trente consommables',
     'Le temps d’activation est la statistique la plus importante d’un soin : il se paie en secondes d’exposition. Les valeurs de soin et de durabilité sont dans les fiches.',
     '<span class="tag">30 objets</span><span class="tag">Soins et réparations</span>',
     '<h2>Ce qu’un consommable doit régler</h2><p>Un bandage soigne une plaie, un antidouleur supprime les effets visuels de la douleur, un kit chirurgical retire un débuff d’une partie du corps, un kit de réparation remet une protection en état en pleine partie. Le choix se fait sur ce qu’on sait gérer : mieux vaut deux petits soins rapides qu’un gros soin lent quand on est à découvert.</p>',
     by('Consumables'), 'cons', hero='hero-db-consommables.jpg')

page('db-accessoires.html', 'Base de données · les 433 accessoires d’armes',
     'Canons, freins, optiques, crosses, poignées et chargeurs : 433 accessoires avec catégorie, poids et valeur par case.',
     '26 · Base de données', 'Les 433 accessoires, le marché le plus rapide du jeu',
     'Petits, chers, et utiles à quelqu’un qui monte un build : les accessoires se revendent plus vite que tout le reste. Le nom de l’arme est conservé en début de fiche pour que la recherche fonctionne.',
     '<span class="tag">433 pièces</span><span class="tag good">Recherche par arme</span>',
     '<h2>Chercher par arme</h2><p>Tape « AN-94 », « M7 » ou « SR-25 » dans la recherche pour ne garder que les pièces de cette arme. Les catégories séparent canons, freins, optiques, crosses, poignées avant et arrière, garde-mains et chargeurs.</p>',
     by('Attachments'), 'att', hero='hero-db-accessoires.jpg')

total = sum(len(by(g)) for g in ['Weapons', 'Ammo', 'Gear', 'Collectibles', 'Keys', 'Consumables', 'Attachments'])
print('total fiches :', total)
