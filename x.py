from collections import defaultdict


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
    ("Anglais G2", "JM1", 1, "A31"),
    ("Communication G1", "JM1", 1, "A31"),
    ("Communication G2", "JM1", 1, "A31"),
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
    ("Anglais G1", "JM2", 1, "A31"),
    ("Anglais G2", "JM2", 1, "A31"),
    ("Communication G1", "JM2", 1, "A31"),
    ("Communication G2", "JM2", 1, "A31"),
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

TOTAL_SLOTS = 20
SLOTS_PER_DAY = 4
DAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]



# ETAPE 2 : CONSTRUIRE EXACT COVER

def build_exact_cover(seances, profs):
    """
    Colonnes:
      - Primaires: ('SEANCE', i) => chaque séance doit être placée.
      - Secondaires: ('CLASSE', classe, slot), ('PROF', prof, slot), ('SALLE', salle, slot)
        => évitent les conflits (au plus une fois).

    Lignes:
      - Une ligne = placer séance i dans slot t.
    """
    primary_cols = {("SEANCE", i) for i in range(len(seances))}

    rows = {}  
    row_info = {} 
    col_to_rows = defaultdict(set)  

    row_id = 0
    for i, (matiere, classe, duree, salle) in enumerate(seances):
        prof = profs[matiere]
        for slot in range(TOTAL_SLOTS):
            cols = {
                ("SEANCE", i),
                ("CLASSE", classe, slot),
                ("PROF", prof, slot),
                ("SALLE", salle, slot),
            }
            rows[row_id] = cols
            row_info[row_id] = (i, slot)
            for c in cols:
                col_to_rows[c].add(row_id)
            row_id += 1

    return primary_cols, rows, col_to_rows, row_info


# =========================
# ETAPE 3 : ALGORITHM X
# =========================
def choose_column_mrv(primary_cols, col_to_rows, active_rows):
   
    best_col = None
    best_count = None
    for col in primary_cols:
        count = len(col_to_rows[col] & active_rows)
        if best_count is None or count < best_count:
            best_col, best_count = col, count
        if best_count == 0:
            break
    return best_col, best_count


def algorithm_x(primary_cols, rows, col_to_rows):
   
    solution = []
    active_rows = set(rows.keys())

    def search(primary_cols, active_rows):
        if not primary_cols:
            return True

        col, count = choose_column_mrv(primary_cols, col_to_rows, active_rows)
        if col is None or count == 0:
            return False

        for r in list(col_to_rows[col] & active_rows):
            solution.append(r)
            covered_cols = rows[r]

            new_primary = set(primary_cols)
            for c in covered_cols:
                if c in new_primary:
                    new_primary.remove(c)

            to_disable = set()
            for c in covered_cols:
                to_disable |= (col_to_rows[c] & active_rows)

            new_active = active_rows - to_disable

            if search(new_primary, new_active):
                return True

            solution.pop()

        return False

    ok = search(set(primary_cols), active_rows)
    return solution if ok else None


# =========================
# ETAPE 4 : RESOUDRE + CONVERTIR
# =========================
def solve_timetable(seances, profs):
    primary_cols, rows, col_to_rows, row_info = build_exact_cover(seances, profs)
    sol_rows = algorithm_x(primary_cols, rows, col_to_rows)
    if sol_rows is None:
        return None
    return [(row_info[r][0], row_info[r][1]) for r in sol_rows]


# =========================
# ETAPE 5 : AFFICHAGE
# =========================
def display(solution, seances, profs):
    if solution is None:
        print("✗ Aucune solution trouvée.")
        return

    slot_map = defaultdict(list)
    for idx_seance, slot in solution:
        slot_map[slot].append(idx_seance)

    print("\n" + "=" * 110)
    print("EMPLOI DU TEMPS (Exact Cover / Algorithm X)".center(110))
    print("=" * 110)

    for day in range(5):
        print(f"\n{DAYS[day].upper()}")
        print("-" * 110)
        for p in range(SLOTS_PER_DAY):
            slot = day * SLOTS_PER_DAY + p
            if slot not in slot_map:
                print(f"C{p}: [LIBRE]")
            else:
                for idx in slot_map[slot]:
                    mat, cl, dur, salle = seances[idx]
                    prof = profs[mat]
                    print(f"C{p}: {cl:<3} | {mat:<35} | {prof:<18} | {salle}")

    print("\n" + "=" * 110)


if __name__ == "__main__":
    sol = solve_timetable(seances, profs)
    display(sol, seances, profs)
