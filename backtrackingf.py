import sys
JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
CRENEAUX = ["09:00-10:45", "11:00-12:45", "13:45-15:30", "15:45-17:30"]


def saisir_donnees():
    try:
        nb_salles = int(input("Nombre de salles disponibles : "))
        _ = input("Nombre de groupes (indicatif) : ")
    except ValueError:
        sys.exit("Erreur : Entrez des nombres entiers.")

    matrice = []
    dispos_profs = {}

    print("\nSaisie de la matrice (Appuyez sur Entrée sur une ligne vide pour finir) :")
    print("Format : Prof, Module, Groupes, NbSéancesTotal, IndicesDispos")

    while True:
        ligne = input("> ")
        if not ligne:
            break

        parts = [p.strip() for p in ligne.split(",")]

        if len(parts) < 4:
            print("Ligne incomplète (il faut au moins Prof, Module, Groupe, Nb).")
            continue

        prof, module, groupe_brut, nb = parts[0], parts[1], parts[2], int(parts[3])

        # Gestion multi-groupes : "G1 & G2" -> [G1, G2]
        groupes_liste = [g.strip() for g in groupe_brut.split("&")]

        # Gestion des disponibilités
        if len(parts) >= 5 and parts[4]:
            indices = [int(i) for i in parts[4].split() if i.isdigit()]
            dispos_profs[prof] = indices
        elif prof in dispos_profs:
            indices = dispos_profs[prof]
        else:
            indices = list(range(20))
            dispos_profs[prof] = indices

        matrice.append({
            "prof": prof,
            "module": module,
            "groupes": groupes_liste,
            "nb": nb,
            "dispos": indices
        })

    return matrice, nb_salles


class GenerateurEDT13Semaines:
    def __init__(self, data, nb_salles):
        self.data = data
        self.nb_salles = nb_salles

        # Extraire tous les groupes uniques
        tous_grps = set()
        for d in data:
            for g in d['groupes']:
                tous_grps.add(g)

        self.groupes_uniques = sorted(list(tous_grps))

        self.planning = {
            s: [
                [{g: None for g in self.groupes_uniques} for _ in range(4)]
                for _ in range(5)
            ]
            for s in range(13)
        }

    def verifier(self, s, j, c, groupes_cible, prof_nom, dispos_prof):
        #  disponibilité du prof
        if (j * 4 + c) not in dispos_prof:
            return False

        # le groupe est libre
        for g in groupes_cible:
            if self.planning[s][j][c][g] is not None:
                return False

        # le prof est libre
        for g_nom in self.groupes_uniques:
            occ = self.planning[s][j][c][g_nom]
            if occ and occ[0] == prof_nom:
                return False

        #  le nombre de salles
        profs_ce_creneau = set()
        for g_nom in self.groupes_uniques:
            occ = self.planning[s][j][c][g_nom]
            if occ:
                profs_ce_creneau.add(occ[0])

        if len(profs_ce_creneau) >= self.nb_salles:
            return False

        return True

    def resoudre(self, idx=0, reste=None):
        if idx >= len(self.data):
            return True

        curr = self.data[idx]

        if reste is None:
            reste = curr['nb']

        if reste <= 0:
            return self.resoudre(idx + 1)

        for s in range(13):
            for j in range(5):
                for c in range(4):
                    if self.verifier(s, j, c, curr['groupes'], curr['prof'], curr['dispos']):
                        # Assigner à tous les groupes
                        for g in curr['groupes']:
                            self.planning[s][j][c][g] = (curr['prof'], curr['module'])

                        if self.resoudre(idx, reste - 1):
                            return True

                        # Backtrack
                        for g in curr['groupes']:
                            self.planning[s][j][c][g] = None

        return False

    def afficher_tout(self):
        for s in range(13):
            print(f"\n\n{'='*90}\n SEMAINE {s+1}\n{'='*90}")

            for g in self.groupes_uniques:
                print(f"\nGROUPE : {g}")

                header = f"{'Jour':<10} | " + " | ".join([f"{c:<16}" for c in CRENEAUX])
                print(header)
                print("-" * len(header))

                for j in range(5):
                    ligne = []

                    for c in range(4):
                        info = self.planning[s][j][c][g]

                        if info:
                            txt = f"{info[1][:8]}({info[0][:6]})"
                            ligne.append(f"{txt:<16}")
                        else:
                            ligne.append(f"{'---':^16}")

                    print(f"{JOURS[j]:<10} | " + " | ".join(ligne))


if __name__ == "__main__":
    salles = 5

    data_matrice = [
        {"prof":"H.NAQOS","module":"algèbre2","groupes":["jm1"],"nb":6,"dispos":list(range(20))},
        {"prof":"H.NAQOS","module":"analyse2","groupes":["jm1"],"nb":6,"dispos":list(range(20))},
        {"prof":"H.NAQOS","module":"mathématique","groupes":["hei","isen"],"nb":15,"dispos":list(range(20))},
        {"prof":"H.NAQOS","module":"analyse numérique","groupes":["jm2"],"nb":14,"dispos":list(range(20))},
        {"prof":"H.NAQOS","module":"apprentissage automatique","groupes":["jm4"],"nb":8,"dispos":list(range(20))},

        {"prof":"S.HDAFA","module":"algorithme et programmation","groupes":["jm1"],"nb":25,"dispos":list(range(20))},
        {"prof":"S.HDAFA","module":"développement web","groupes":["jm2"],"nb":28,"dispos":list(range(20))},
        {"prof":"S.HDAFA","module":"projet étude et conception","groupes":["isen"],"nb":16,"dispos":list(range(20))},

        {"prof":"H.ZEROUALI","module":"analyse2","groupes":["jm1"],"nb":6,"dispos":[0,1,12,13,16,17,18]},
        {"prof":"H.ZEROUALI","module":"algèbre2","groupes":["jm1"],"nb":6,"dispos":[0,1,12,13,16,17,18]},
        {"prof":"H.ZEROUALI","module":"probabilite","groupes":["jm2"],"nb":24,"dispos":[0,1,12,13,16,17,18]},

        {"prof":"A.DAHMANI","module":"science de l’ingénieur","groupes":["jm2"],"nb":16,"dispos":[4,5,8,9,16,17,18]},
        {"prof":"A.DAHMANI","module":"projet étude et conception","groupes":["hei"],"nb":16,"dispos":[4,5,8,9,16,17,18]},
        {"prof":"A.DAHMANI","module":"ingénierie mécanique","groupes":["hei"],"nb":24,"dispos":[4,5,8,9,16,17,18]},

        {"prof":"A.ELMANSOUR","module":"interculturalité","groupes":["hei","isen"],"nb":9,"dispos":[2,3,14,15]},

        {"prof":"A.ELYAZIDI","module":"aide à la decision","groupes":["hei","isen"],"nb":18,"dispos":[0,1,9,10,16,17]},
        {"prof":"A.ELYAZIDI","module":"système d’exploitation","groupes":["jm4"],"nb":12,"dispos":[0,1,9,10,16,17]},

        {"prof":"T.AKDIM","module":"intro gestion compta finance","groupes":["jm1"],"nb":15,"dispos":[0,1,2,3,6,7,10,11]},
        {"prof":"T.AKDIM","module":"marketing","groupes":["hei","isen"],"nb":9,"dispos":[0,1,2,3,6,7,10,11]},
        {"prof":"T.AKDIM","module":"entreprenariat","groupes":["jm4"],"nb":12,"dispos":[0,1,2,3,6,7,10,11]},

        {"prof":"S.ELFASSI","module":"mécanique générale","groupes":["jm1"],"nb":24,"dispos":[4,5,8,9,16,17]},
        {"prof":"S.ELFASSI","module":"mécanique quantique","groupes":["isen"],"nb":18,"dispos":[4,5,8,9,16,17]},
        {"prof":"S.ELFASSI","module":"mécanique des fluides","groupes":["jm2"],"nb":12,"dispos":[4,5,8,9,16,17]},

        {"prof":"A.BENKHRABA","module":"anglais1","groupes":["jm1"],"nb":12,"dispos":[2,3,10,19]},
        {"prof":"A.BENKHRABA","module":"anglais2","groupes":["jm2"],"nb":12,"dispos":[2,3,10,19]},

        {"prof":"D.GUENDOUZ","module":"projet collectif découverte domaine","groupes":["jm1"],"nb":12,"dispos":list(range(20))},
        {"prof":"D.GUENDOUZ","module":"communication for working","groupes":["jm2"],"nb":12,"dispos":list(range(20))},

        {"prof":"S.SHLAKA","module":"communication1","groupes":["jm1"],"nb":12,"dispos":[6,7,14,15]},
        {"prof":"S.SHLAKA","module":"communication2","groupes":["jm2"],"nb":12,"dispos":[6,7,14,15]},

        {"prof":"N.AHAMI","module":"thermodynamique","groupes":["jm1"],"nb":14,"dispos":[10,11,12,13,16,17]},
        {"prof":"C.BAQA","module":"science de l’ingénieur","groupes":["jm1"],"nb":14,"dispos":[16,17]},

        {"prof":"M.SEBGUI","module":"systèmes embarqués","groupes":["jm2"],"nb":24,"dispos":[4,5,8,9,14,15]},

        {"prof":"S.MOULINE","module":"BD et BD Avancées","groupes":["jm4"],"nb":24,"dispos":[0,1,8,9]},
        {"prof":"M.RZIZA","module":"administration et sécurité des réseaux","groupes":["jm4"],"nb":24,"dispos":[0,1,8,9,12,13]},
        {"prof":"Y.AKALAY","module":"anglais","groupes":["jm4"],"nb":12,"dispos":[16,17]},

        {"prof":"M.ELHASSOUNI","module":"big data et analyse distribuée des données","groupes":["jm4"],"nb":24,"dispos":[6,7,8,9,15,16]},

        {"prof":"A.ESSADKI","module":"principe de l’instrumentation","groupes":["hei","isen"],"nb":18,"dispos":[6,7,10,11,12,13,14,15]},
        {"prof":"A.ESSADKI","module":"automatisation2","groupes":["hei","isen"],"nb":18,"dispos":[6,7,10,11,12,13,14,15]},
        {"prof":"A.ESSADKI","module":"electrecite vecteur d’énergie","groupes":["hei"],"nb":18,"dispos":[6,7,10,11,12,13,14,15]},
        {"prof":"A.ESSADKI","module":"regulation industrielle","groupes":["isen"],"nb":18,"dispos":[6,7,10,11,12,13,14,15]}
    ]

    moteur = GenerateurEDT13Semaines(data_matrice, salles)

    print("\n[Calcul] Génération des 13 semaines en cours...")

    if moteur.resoudre():
        moteur.afficher_tout()
        print("\n[SUCCÈS] Emploi du temps terminé.")
    else:
        print("\n[ÉCHEC] Impossible de placer toutes les séances.")
