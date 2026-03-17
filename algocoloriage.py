    ("Maths",    "3A", 1, "A11"),
    ("Maths",    "3A", 2, "A11"),
    ("Physique", "3A", 1, "B1"),
    ("Physique", "3A", 2, "B1"),
    ("Info",     "3A", 1, "C1"),
    ("Histoire", "3A", 1, "D1"),
    ("Français", "3A", 1, "A1"),
    ("Français", "3A", 2, "A1"),

    ("Maths",    "1B", 1, "A2"),
    ("Maths",    "1B", 2, "A2"),
    ("Physique", "1B", 1, "B2"),
    ("Chimie",   "1B", 1, "B1"),   
    ("Info",     "1B", 1, "C1"),   
    ("Histoire", "1B", 1, "D2"),
    ("Français", "1B", 1, "A2"),

    ("Maths",    "2C", 1, "A3"),
    ("Maths",    "2C", 2, "A3"),
    ("Chimie",   "2C", 1, "B2"),   
    ("Info",     "2C", 1, "C2"),
    ("Histoire", "2C", 1, "D1"),   
    ("Français", "2C", 1, "A3"),
    ("Français", "2C", 2, "A3"),
]

profs = {
    "Maths":    "M. Hatim",
    "Physique": "Mme Khadija",
    "Chimie":   "Mme layla",   
    "Info":     "M. Anas",
    "Histoire": "M Oussama",
    "Français": "M Mehdi",
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
    for node in sorted(graph, key=lambda n: -len(graph[n])):
        neighbor_colors = {color[v] for v in graph[node] if v in color}
        c = 0
        while c in neighbor_colors:
            c += 1
        color[node] = c
    return color


slots = [
    "Lundi 8h",    "Lundi 10h",    "Lundi 14h",    "Lundi 16h",
    "Mardi 8h",    "Mardi 10h",    "Mardi 14h",    "Mardi 16h",
    "Mercredi 8h", "Mercredi 10h",
    "Jeudi 8h",    "Jeudi 10h",    "Jeudi 14h",    "Jeudi 16h",
    "Vendredi 8h", "Vendredi 10h", "Vendredi 14h", "Vendredi 16h",
]


graph  = generate_graph(seances)
emploi = coloration_graph(graph)

print("=== Emploi du temps — semaine complète ===\n")
for jour in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]:
    seances_du_jour = [
        (s, c) for s, c in emploi.items()
        if c < len(slots) and slots[c].startswith(jour)
    ]
    if not seances_du_jour:
        continue
    print(f"── {jour} ──")
    for (cours, classe, nb, salle), creneau in sorted(seances_du_jour, key=lambda x: x[1]):
        print(f"  {slots[creneau]:<16} | {cours:<10} | Classe {classe} | Salle {salle:<4} | {profs[cours]}")
    print()

print(f"→ {len(set(emploi.values()))} créneaux utilisés pour {len(seances)} séances.")

print("\n=== Validation ===")
conflits_trouves = 0
seance_list = list(emploi.keys())
for i in range(len(seance_list)):
    for j in range(i + 1, len(seance_list)):
        s1, s2 = seance_list[i], seance_list[j]
        if emploi[s1] == emploi[s2] and sont_en_conflit(s1, s2):
            print( "CONFLIT ")
            conflits_trouves += 1

if conflits_trouves == 0:
    print("Emploi du temps valide.")
