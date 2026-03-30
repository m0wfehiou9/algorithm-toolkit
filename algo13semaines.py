#faut tester pdf et les polices qui peuvent marcher
import os
import random
from fpdf import FPDF

seances = [
    ("Analyse2", "JM1", 12, "A31"),
    ("Algebre2", "JM1", 12, "A31"),
    ("Mécanique générale", "JM1", 24, "A31"),
    ("Thermodynamique", "JM1", 14, "A31"),
    ("Algorithmique/Programmation", "JM1", 25, "A31"),
    ("Sciences de l'ingénieur", "JM1", 14, "A31"),
    ("Intro Gestion compta finance", "JM1", 15, "A31"),
    ("Projet collectif découverte domaine", "JM1", 12, "A31"),
    ("Anglais G1", "JM1", 12, "A31"),
    ("Anglais G2", "JM1", 12, "A31"),
    ("Communication G1", "JM1", 12, "A31"),
    ("Communication G2", "JM1", 12, "A31"),

    # JM2
    ("Probabilité", "JM2", 24, "A33"),
    ("Analyse numérique", "JM2", 14, "A33"),
    ("Systèmes Embarqués", "JM2", 24, "A33"),
    ("Développement WEB", "JM2", 28, "A33"),
    ("Réduction des Endomorphismes", "JM2", 14, "A33"),
    ("Mécanique des fluides", "JM2", 12, "A33"),
    ("Sciences de l'ingénieur", "JM2", 16, "A33"),
    ("Projet études - conception", "JM2", 12, "A33"),
    ("Communication for working", "JM2", 12, "A33"),
    ("Anglais G1", "JM2", 12, "A31"),
    ("Anglais G2", "JM2", 12, "A31"),
    ("Communication G1", "JM2", 12, "A31"),
    ("Communication G2", "JM2", 12, "A31"),

    # JM3
    ("Mathématiques", "JM3", 15, "A11"),
    ("Mécanique quantique", "JM3", 18, "A11"),
    ("Analyse des signaux & images", "JM3", 18, "A11"),
    ("Régulation industrielle", "JM3", 12, "A11"),
    ("Systèmes électroniques", "JM3", 12, "A11"),
    ("Ingénierie Mécanique", "JM3", 24, "A01"),
    ("Chimie", "JM3", 12, "A01"),
    ("Projet études - conception", "JM3", 12, "A11"),
    ("Electricité vect d'énergie", "JM3", 24, "A01"),
    ("Aide à la décision", "JM3", 18, "A11"),
    ("Principes de l'instrumentation", "JM3", 18, "A11"),
    ("Interculturalité", "JM3", 9, "A11"),
    ("Fondamentaux du marketing", "JM3", 9, "A11"),
    ("Automatisation II", "JM3", 12, "A11"),
    
    # JM4
    ("Analyse de Donnèes avec R", "JM4", 12, "B12"),
    ("Technologie WEB", "JM4", 12, "B12"),
    ("Entreprenariat", "JM4", 12, "B12"),
    ("BIG DATA et Analyse distribuée des donnèes", "JM4", 24, "B12"),
    ("BD et BD Avancèes", "JM4", 24, "B12"),
    ("Administration et sécurité des réseaux", "JM4", 24, "B12"),
    ("Apprentissage Automatique", "JM4", 12, "B12"),
    ("Infrastructures de Dèploiement d'applications", "JM4", 1, "B12"),
    ("Systèmes d'exploitation 2", "JM4", 12, "B12"),
    ("Anglais", "JM4", 12, "B12"),

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
    "BIG DATA et Analyse distribuée des donnèes": "M.EL HASSOUNI",
    "BD et BD Avancèes": "S:MOULINE",
    "Administration et sécurité des réseaux":"M.RZIZA",
    "Apprentissage Automatique": "H.NAQOS",
    "Infrastructures de Dèploiement d'applications":"PROF X",
    "Systèmes d'exploitation 2":"A. EL YAZIDI",
    "Anglais":"Y.AKALAY",
}
slots = [
    "Lundi 8h",    "Lundi 10h",    "Lundi 14h",    "Lundi 16h",
    "Mardi 8h",    "Mardi 10h",    "Mardi 14h",    "Mardi 16h",
    "Mercredi 8h", "Mercredi 10h",
    "Jeudi 8h",    "Jeudi 10h",    "Jeudi 14h",    "Jeudi 16h",
    "Vendredi 8h", "Vendredi 10h", "Vendredi 14h", "Vendredi 16h",
]

_ALL_SLOTS = set(range(len(slots)))
# Default: everyone is fully available. The user will override the availability for
# the non-full-time professors via prompts (see `_prompt_non_full_time_availability()`).
disponibilites_profs = {
    _prof: [_ALL_SLOTS, set(_ALL_SLOTS)]
    for _prof in set(profs.values())
}

def sont_en_conflit(s1, s2):
  
    cours1, classe1, _, salle1, _ = s1
    cours2, classe2, _, salle2, _ = s2

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


def coloration_graph(graph, week_idx=0):
    # Fast greedy coloring with random tie-breaking.
    # We assign each session a slot index (color) such that:
    #   - conflicting sessions (via `sont_en_conflit`) never share the same color
    #   - each session can only use slots allowed for its professor/week

    ALL_SLOTS = set(range(len(slots)))
    nodes = list(graph.keys())
    if not nodes:
        return {}

    def availability_for_prof(prof):
        avail = disponibilites_profs.get(prof)
        if avail is None:
            return ALL_SLOTS
        if isinstance(avail, (list, tuple)):
            if not avail:
                return ALL_SLOTS
            return avail[week_idx % len(avail)]
        return avail

    allowed = {}
    for node in nodes:
        # node = (cours, classe, nb, salle, occ_idx)
        cours = node[0]
        prof = profs[cours]
        allowed[node] = availability_for_prof(prof)
        if not allowed[node]:
            raise Exception(f"Aucun créneau dispo pour {cours} ({prof})")

    # MRV-ish ordering: sort by domain size then by degree.
    def domain_key(n):
        # random tie-break to get diversity across retry attempts
        return (len(allowed[n]), -len(graph[n]), random.random())

    order = sorted(nodes, key=domain_key)

    assignment = {}
    unassigned = set(nodes)

    for node in order:
        # Note: `graph[node]` is adjacency list of conflict edges.
        neighbor_colors = {assignment[v] for v in graph[node] if v in assignment}
        possible = list(allowed[node] - neighbor_colors)
        if not possible:
            cours = node[0]
            prof = profs[cours]
            raise Exception(f"Aucun créneau dispo pour {cours} ({prof})")

        # Least-constraining value heuristic for faster success.
        def impact(c):
            cnt = 0
            for v in graph[node]:
                if v in unassigned and c in allowed[v]:
                    cnt += 1
            return cnt

        possible.sort(key=lambda c: (impact(c), random.random()))
        assignment[node] = possible[0]
        unassigned.remove(node)

    return assignment


def coloration_graph_with_retries(graph, week_idx=0, max_attempts=20):
    last_exc = None
    for _ in range(max_attempts):
        try:
            return coloration_graph(graph, week_idx=week_idx)
        except Exception as e:
            last_exc = e
    raise last_exc


def _parse_slot_indices(text, slot_count):
    """
    Parse user input like:
      - "0,1,4,7"
      - "0-3,7,10-11"
      - "all"
    Returns a set[int].
    """
    t = text.strip().lower()
    if not t:
        return set()
    if t == "all":
        return set(range(slot_count))

    out = set()
    parts = [p.strip() for p in t.split(",") if p.strip()]
    for part in parts:
        if "-" in part:
            a_s, b_s = part.split("-", 1)
            a = int(a_s.strip())
            b = int(b_s.strip())
            if a > b:
                a, b = b, a
            for i in range(a, b + 1):
                out.add(i)
        else:
            out.add(int(part))
    return out


def _prompt_non_full_time_availability():
    """
    Ask the user for each non full-time professor's weekly availability patterns.
    Each pattern is a set of slot indices, and the scheduler uses:
      availability_for_week = patterns[week_idx % len(patterns)]
    """
    all_prof = sorted(set(profs.values()))
    print("Créneaux disponibles (indices -> libellés):")
    for i, s in enumerate(slots):
        print(f"  {i:>2}: {s}")

    print("\nProfesseurs détectés dans vos données:")
    for i, p in enumerate(all_prof):
        print(f"  {i:>2}: {p}")

    raw = input(
        "\nListe des professeurs NON à temps plein (séparés par virgules, ex: 'A. BENKHRABA, S. SHLAKA'). "
        "Laisser vide si aucun: "
    ).strip()
    if not raw:
        return

    names = [x.strip() for x in raw.split(",") if x.strip()]
    unknown = [n for n in names if n not in set(all_prof)]
    if unknown:
        raise ValueError(f"Professeurs inconnus (vérifiez l'orthographe): {', '.join(unknown)}")

    for prof in names:
        default_patterns = 2
        k_raw = input(f"\nNombre de patterns hebdomadaires pour {prof} (default {default_patterns}): ").strip()
        k = int(k_raw) if k_raw else default_patterns
        if k <= 0:
            raise ValueError("Nombre de patterns doit être >= 1")

        patterns = []
        for pi in range(k):
            example = "0-1,4-5,12-13"
            idx_raw = input(
                f"  Pattern {pi+1}/{k} - indices de créneaux dispo ({example} ou 'all'): "
            ).strip()
            idx_set = _parse_slot_indices(idx_raw, len(slots))
            invalid = [i for i in idx_set if i < 0 or i >= len(slots)]
            if invalid:
                raise ValueError(f"Indices hors plage pour {prof}: {sorted(set(invalid))}")
            if not idx_set:
                raise ValueError(f"Pattern {pi+1} pour {prof} est vide.")
            patterns.append(idx_set)

        disponibilites_profs[prof] = patterns


def _generate_semester_timetables():
    emplois_semestre = []
    # Interpret seances[i][2] ("nb of seances") as the number of times the
    # course appears within the 13-week semester span.
    # We distribute occurrences across weeks, then solve coloring per week.
    from collections import Counter, defaultdict

    active_by_week = [[] for _ in range(13)]
    slot_capacity = len(slots)  # max sessions for a given resource in a week

    all_occurrences = []
    prof_total = Counter()
    class_total = Counter()
    salle_total = Counter()

    # Build all seance occurrences (the "nb" field is total occurrences over 13 weeks).
    for cours, classe, nb, salle in seances:
        total = int(nb) if int(nb) > 0 else 1
        prof = profs[cours]
        prof_total[prof] += total
        class_total[classe] += total
        salle_total[salle] += total
        for occ_idx in range(total):
            # Extra occ_idx prevents dict-key collapse.
            all_occurrences.append((cours, classe, nb, salle, occ_idx))

    # Order: place occurrences with the "tightest" overall resources first.
    # (High professor load first, then class load, then room load.)
    def occ_sort_key(node):
        cours, classe, _, salle, _ = node
        return (
            -prof_total[profs[cours]],
            -class_total[classe],
            -salle_total[salle],
            node[4],
        )

    all_occurrences.sort(key=occ_sort_key)

    prof_load = [defaultdict(int) for _ in range(13)]
    class_load = [defaultdict(int) for _ in range(13)]
    salle_load = [defaultdict(int) for _ in range(13)]

    for node in all_occurrences:
        cours, classe, _, salle, _ = node
        prof = profs[cours]

        def score_for_week(w):
            # Minimize current load on professor/class/room.
            return (
                prof_load[w][prof],
                class_load[w][classe],
                salle_load[w][salle],
                random.random(),  # tie-break
            )

        candidates = list(range(13))
        feasible = [
            w
            for w in candidates
            if prof_load[w][prof] < slot_capacity
            and class_load[w][classe] < slot_capacity
            and salle_load[w][salle] < slot_capacity
        ]
        chosen = min(feasible if feasible else candidates, key=score_for_week)

        prof_load[chosen][prof] += 1
        class_load[chosen][classe] += 1
        salle_load[chosen][salle] += 1
        active_by_week[chosen].append(node)

    for week_idx in range(13):
        graph = generate_graph(active_by_week[week_idx])
        emploi_semaine = coloration_graph_with_retries(graph, week_idx=week_idx)
        emplois_semestre.append(emploi_semaine)

    return emplois_semestre


def _print_semester_timetables(emplois_semestre):
    for idx, emploi in enumerate(emplois_semestre):
        print(f"\n================ Semaine {idx+1} ================\n")

        for jour in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]:
            seances_du_jour = [
                (s, c)
                for s, c in emploi.items()
                if c < len(slots) and slots[c].startswith(jour)
            ]
            if not seances_du_jour:
                continue

            print(f"── {jour} ──")
            for (cours, classe, _, salle, _), creneau in sorted(seances_du_jour, key=lambda x: x[1]):
                print(f"  {slots[creneau]:<16} | {cours:<35} | Classe {classe} | Salle {salle:<4} | {profs[cours]}")
            print()

        conflits_trouves = 0
        seance_list = list(emploi.keys())
        for i in range(len(seance_list)):
            for j in range(i + 1, len(seance_list)):
                s1, s2 = seance_list[i], seance_list[j]
                if emploi[s1] == emploi[s2] and sont_en_conflit(s1, s2):
                    print("CONFLIT")
                    conflits_trouves += 1

        if conflits_trouves == 0:
            print("Emploi du temps valide.")


def _export_pdfs_by_class(emplois_semestre, out_dir="pdfs"):
    if FPDF is None:
        print("`fpdf` n'est pas installé: export PDF ignoré.")
        return

    os.makedirs(out_dir, exist_ok=True)
    classes = sorted(set(s[1] for s in seances))

    for classe in classes:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, txt=f"Emploi du temps - {classe} (13 semaines)")
        pdf.ln(2)

        for idx, emploi in enumerate(emplois_semestre):
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 7, txt=f"Semaine {idx+1}")
            pdf.ln(1)

            for jour in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]:
                sessions = [
                    (s, c)
                    for s, c in emploi.items()
                    if s[1] == classe and c < len(slots) and slots[c].startswith(jour)
                ]
                if not sessions:
                    continue
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 6, txt=f"{jour}")

                pdf.set_font("Arial", size=9)
                for (cours, _, _, salle, _), creneau in sorted(sessions, key=lambda x: x[1]):
                    prof = profs[cours]
                    line = f"  {slots[creneau]} | {cours} | Salle {salle} | {prof}"
                    pdf.multi_cell(0, 5, txt=line)
                pdf.ln(1)

            pdf.ln(2)

        out_path = os.path.join(out_dir, f"{classe}_13_semaines.pdf")
        pdf.output(out_path)
        print(f"PDF généré: {out_path}")


def main():
    _prompt_non_full_time_availability()
    emplois_semestre = _generate_semester_timetables()
    _print_semester_timetables(emplois_semestre)
    _export_pdfs_by_class(emplois_semestre)


if __name__ == "__main__":
    main()
