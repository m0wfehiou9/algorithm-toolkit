import random

seances = [
    # JM1
    ("Analyse2", "JM1", 1, "A31"),
    ("Algebre2", "JM1", 1, "A31"),
    ("Mécanique générale", "JM1", 1, "A31"),
    ("Thermodynamique", "JM1", 1, "A31"),
    ("Algorithmique/Programmation", "JM1", 1, "A31"),
    ("Sciences de l'ingénieur", "JM1", 1, "A31"),
    ("Intro Gestion compta finance", "JM1", 1, "A31"),
    ("Projet collectif découverte domaine", "JM1", 1, "A31"),
    ("Anglais G1", "JM1", 1, "A31"),
    ("Communication G1", "JM1", 1, "A31"),
    ("Communication G2", "JM1", 1, "A32"),

    # JM2
    ("Probabilité", "JM2", 1, "A33"),
    ("Analyse numérique", "JM2", 1, "A33"),
    ("Systèmes Embarqués", "JM2", 1, "A33"),
    ("Développement WEB", "JM2", 1, "A33"),
    ("Réduction des Endomorphismes", "JM2", 1, "A33"),
    ("Mécanique des fluides", "JM2", 1, "A33"),
    ("Sciences de l'ingénieur", "JM2", 1, "A33"),
    ("Projet études - conception", "JM2", 1, "A33"),
    ("Communication for working", "JM2", 1, "A33"),
    ("Anglais G2", "JM2", 1, "A35"),
    ("Communication G1", "JM2", 1, "A34"),
    ("Communication G2", "JM2", 1, "A35"),

    # JM3
    ("Mathématiques", "JM3", 1, "A11"),
    ("Mécanique quantique", "JM3", 1, "A11"),
    ("Analyse des signaux & images", "JM3", 1, "A11"),
    ("Régulation industrielle", "JM3", 1, "A11"),
    ("Systèmes électroniques", "JM3", 1, "A11"),
    ("Ingénierie Mécanique", "JM3", 1, "A01"),
    ("Chimie", "JM3", 1, "A01"),
    ("Projet études - conception", "JM3", 1, "A11"),
    ("Electricité vect d'énergie", "JM3", 1, "A01"),
    ("Aide à la décision", "JM3", 1, "A11"),
    ("Principes de l'instrumentation", "JM3", 1, "A11"),
    ("Interculturalité", "JM3", 1, "A11"),
    ("Fondamentaux du marketing", "JM3", 1, "A11"),
    ("Automatisation II", "JM3", 1, "A11"),

    # JM4
    ("Analyse de Donnèes avec R", "JM4", 1, "B12"),
    ("Technologie WEB", "JM4", 1, "B12"),
    ("Entreprenariat", "JM4", 1, "B12"),
    ("BIG DATA et Analyse distribuée des donnèes", "JM4", 1, "B12"),
    ("BD et BD Avancèes", "JM4", 1, "B12"),
    ("Administration et sécurité des réseaux", "JM4", 1, "B12"),
    ("Apprentissage Automatique", "JM4", 1, "B12"),
    ("Infrastructures de Dèploiement d'applications", "JM4", 1, "B12"),
    ("Systèmes d'exploitation 2", "JM4", 1, "B12"),
    ("Anglais", "JM4", 1, "B12"),
]

profs = {
    "Analyse2": "H. ZEROUALI",
    "Algebre2": "H. ZEROUALI",
    "Mécanique générale": "S. EL FASSI",
    "Thermodynamique": "N. AHAMI",
    "Algorithmique/Programmation": "S. HDAFA",
    "Sciences de l'ingénieur": "C. BAQA",
    "Intro Gestion compta finance": "T. AKDIM",
    "Projet collectif découverte domaine": "D. GUENDOUZ",
    "Anglais G1": "A. BENKHRABA",
    "Anglais G2": "A. BENKHRABA",
    "Communication G1": "S. SHLAKA",
    "Communication G2": "S. SHLAKA",

    "Probabilité": "H. ZEROUALI",
    "Analyse numérique": "H. NAQOS",
    "Systèmes Embarqués": "M. SEBGUI",
    "Développement WEB": "S. HDAFA",
    "Réduction des Endomorphismes": "H. NAQOS",
    "Mécanique des fluides": "S. EL FASSI",
    "Projet études - conception": "A. DAHMANI",
    "Communication for working": "D. GUENDOUZ",

    "Mathématiques": "H. NAQOS",
    "Mécanique quantique": "S. EL FASSI",
    "Analyse des signaux & images": "A. CHEFCHAOUNI",
    "Régulation industrielle": "A. ESSADKI",
    "Systèmes électroniques": "H. AMMOR",
    "Ingénierie Mécanique": "A. DAHMANI",
    "Chimie": "A. EL BOUKILI",
    "Electricité vect d'énergie": "A. ESSADKI",
    "Aide à la décision": "S. A. EL YAZIDI",
    "Principes de l'instrumentation": "A. ESSADKI",
    "Interculturalité": "A. ELMANSOUR",
    "Fondamentaux du marketing": "T. AKDIM",
    "Automatisation II": "A. ESSADKI",

    "Analyse de Donnèes avec R": "A. CHEFCHAOUNI",
    "Technologie WEB": "A. EL YAZIDI",
    "Entreprenariat": "T. AKDIM",
    "BIG DATA et Analyse distribuée des donnèes": "M. EL HASSOUNI",
    "BD et BD Avancèes": "S. MOULINE",
    "Administration et sécurité des réseaux": "M. RZIZA",
    "Apprentissage Automatique": "H. NAQOS",
    "Infrastructures de Dèploiement d'applications": "PROF X",
    "Systèmes d'exploitation 2": "A. EL YAZIDI",
    "Anglais": "Y. AKALAY",
}

slots = [
    "Lundi 8h",    "Lundi 10h",    "Lundi 14h",    "Lundi 16h",
    "Mardi 8h",    "Mardi 10h",    "Mardi 14h",    "Mardi 16h",
    "Mercredi 8h", "Mercredi 10h",
    "Jeudi 8h",    "Jeudi 10h",    "Jeudi 14h",    "Jeudi 16h",
    "Vendredi 8h", "Vendredi 10h", "Vendredi 14h", "Vendredi 16h",
]

disponibilites_profs = {
    "H. NAQOS": set(range(len(slots))),
    "S. HDAFA": set(range(len(slots))),

    "S. EL FASSI": {0, 1, 4, 5},
    "S. SHLAKA": {2, 3, 6, 7},
}

def sont_en_conflit(s1, s2):
    cours1, classe1, _, salle1 = s1
    cours2, classe2, _, salle2 = s2

    if classe1 == classe2:
        return True
    if salle1 == salle2:
        return True
    if profs[cours1] == profs[cours2]:
        return True

    return False


def generate_graph(seances):
    graph = {s: [] for s in seances}

    for i in range(len(seances)):
        for j in range(i + 1, len(seances)):
            s1, s2 = seances[i], seances[j]
            if sont_en_conflit(s1, s2):
                graph[s1].append(s2)
                graph[s2].append(s1)

    return graph


def coloration_graph(graph):
    color = {}
    nodes = list(graph.keys())

    nodes.sort(
        key=lambda n: (
            len(disponibilites_profs.get(profs[n[0]], set(range(len(slots))))),
            -len(graph[n]),
        )
    )

    for node in nodes:
        cours, _, _, _ = node
        prof = profs[cours]

        neighbor_colors = {color[v] for v in graph[node] if v in color}
        dispo = disponibilites_profs.get(prof, set(range(len(slots))))

        dispo_list = list(dispo)
        random.shuffle(dispo_list)

        for c in dispo_list:
            if c not in neighbor_colors:
                color[node] = c
                break
        else:
            raise Exception(f"Aucun créneau dispo pour {cours} ({prof})")

    return color


graph = generate_graph(seances)

emplois_semestre = []
for semaine in range(13):
    emploi_semaine = None
    for _ in range(200):
        try:
            emploi_semaine = coloration_graph(graph)
            break
        except Exception:
            continue
    if emploi_semaine is None:
        raise Exception(f"Impossible de générer la semaine {semaine + 1} après plusieurs tentatives.")
    emplois_semestre.append(emploi_semaine)

for idx, emploi in enumerate(emplois_semestre):
    print(f"\n================ Semaine {idx + 1} ================\n")

    for jour in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]:
        seances_du_jour = [
            (s, c) for s, c in emploi.items()
            if c < len(slots) and slots[c].startswith(jour)
        ]
        if not seances_du_jour:
            continue

        print(f"{jour} hg jhgf'p098")
        for (cours, classe, nb, salle), creneau in sorted(seances_du_jour, key=lambda x: x[1]):
            print(f"  {slots[creneau]:<16} | {cours:<42} | Classe {classe} | Salle {salle:<4} | {profs[cours]}")
        print()

    conflits_trouves = 0
    seance_list = list(emploi.keys())
    for i in range(len(seance_list)):
        for j in range(i + 1, len(seance_list)):
            s1, s2 = seance_list[i], seance_list[j]
            if emploi[s1] == emploi[s2] and sont_en_conflit(s1, s2):
                cours1, classe1, _, salle1 = s1
                cours2, classe2, _, salle2 = s2
                print("   CONFLIT ")
                conflits_trouves += 1

    if conflits_trouves == 0:
        print(" Emploi du temps valide.")
