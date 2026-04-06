import sys

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
CRENEAUX = ["09:00-10:45", "11:00-12:45", "13:45-15:30", "15:45-17:30"]


class GenerateurEDT1Semaine:
    def __init__(self, data, nb_salles):
        self.data = data
        self.nb_salles = nb_salles

        groupes = set()
        for d in data:
            for g in d["groupes"]:
                groupes.add(g)
        self.groupes_uniques = sorted(list(groupes))

        self.planning = [
            [{g: None for g in self.groupes_uniques} for _ in range(4)]
            for _ in range(5)
        ]

    def verifier(self, j, c, groupes, prof, dispos):
        if (j * 4 + c) not in dispos:
            return False

        for g in groupes:
            if self.planning[j][c][g] is not None:
                return False

        for g in self.groupes_uniques:
            occ = self.planning[j][c][g]
            if occ and occ[0] == prof:
                return False

        profs = set()
        for g in self.groupes_uniques:
            occ = self.planning[j][c][g]
            if occ:
                profs.add(occ[0])

        if len(profs) >= self.nb_salles:
            return False

        return True

    def resoudre(self, idx=0, reste=None):
        if idx >= len(self.data):
            return True

        curr = self.data[idx]

        if reste is None:
            reste = curr["nb"]

        if reste <= 0:
            return self.resoudre(idx + 1)

        for j in range(5):
            for c in range(4):
                if self.verifier(j, c, curr["groupes"], curr["prof"], curr["dispos"]):

                    for g in curr["groupes"]:
                        self.planning[j][c][g] = (curr["prof"], curr["module"])

                    if self.resoudre(idx, reste - 1):
                        return True

                    for g in curr["groupes"]:
                        self.planning[j][c][g] = None

        return False

    def afficher(self):
        for g in self.groupes_uniques:
            print(f"\nGROUPE : {g}")

            header = f"{'Jour':<10} | " + " | ".join([f"{c:<16}" for c in CRENEAUX])
            print(header)
            print("-" * len(header))

            for j in range(5):
                ligne = []

                for c in range(4):
                    info = self.planning[j][c][g]

                    if info:
                        txt = f"{info[1][:8]}({info[0][:6]})"
                        ligne.append(f"{txt:<16}")
                    else:
                        ligne.append(f"{'---':^16}")

                print(f"{JOURS[j]:<10} | " + " | ".join(ligne))


if __name__ == "__main__":
    salles = 5

    data_matrice = [
        {"prof":"H.NAQOS","module":"algèbre2","groupes":["jm1"],"nb":1,"dispos":list(range(20))},
        {"prof":"H.NAQOS","module":"analyse2","groupes":["jm1"],"nb":1,"dispos":list(range(20))},
        {"prof":"H.NAQOS","module":"mathématique","groupes":["hei","isen"],"nb":1,"dispos":list(range(20))},
        {"prof":"H.NAQOS","module":"analyse numérique","groupes":["jm2"],"nb":1,"dispos":list(range(20))},
        {"prof":"H.NAQOS","module":"apprentissage automatique","groupes":["jm4"],"nb":1,"dispos":list(range(20))},

        {"prof":"S.HDAFA","module":"algorithme et programmation","groupes":["jm1"],"nb":2,"dispos":list(range(20))},
        {"prof":"S.HDAFA","module":"développement web","groupes":["jm2"],"nb":2,"dispos":list(range(20))},
        {"prof":"S.HDAFA","module":"projet étude et conception","groupes":["isen"],"nb":1,"dispos":list(range(20))},

        {"prof":"H.ZEROUALI","module":"analyse2","groupes":["jm1"],"nb":1,"dispos":[0,1,12,13,16,17,18]},
        {"prof":"H.ZEROUALI","module":"algèbre2","groupes":["jm1"],"nb":1,"dispos":[0,1,12,13,16,17,18]},
        {"prof":"H.ZEROUALI","module":"probabilite","groupes":["jm2"],"nb":2,"dispos":[0,1,12,13,16,17,18]},

        {"prof":"A.DAHMANI","module":"science de l’ingénieur","groupes":["jm2"],"nb":1,"dispos":[4,5,8,9,16,17,18]},
        {"prof":"A.DAHMANI","module":"projet étude et conception","groupes":["hei"],"nb":1,"dispos":[4,5,8,9,16,17,18]},
        {"prof":"A.DAHMANI","module":"ingénierie mécanique","groupes":["hei"],"nb":2,"dispos":[4,5,8,9,16,17,18]},

        {"prof":"A.ELMANSOUR","module":"interculturalité","groupes":["hei","isen"],"nb":1,"dispos":[2,3,14,15]},

        {"prof":"A.ELYAZIDI","module":"aide à la decision","groupes":["hei","isen"],"nb":1,"dispos":[0,1,9,10,16,17]},
        {"prof":"A.ELYAZIDI","module":"système d’exploitation","groupes":["jm4"],"nb":1,"dispos":[0,1,9,10,16,17]},

        {"prof":"T.AKDIM","module":"intro gestion compta finance","groupes":["jm1"],"nb":1,"dispos":[0,1,2,3,6,7,10,11]},
        {"prof":"T.AKDIM","module":"marketing","groupes":["hei","isen"],"nb":1,"dispos":[0,1,2,3,6,7,10,11]},
        {"prof":"T.AKDIM","module":"entreprenariat","groupes":["jm4"],"nb":1,"dispos":[0,1,2,3,6,7,10,11]},

        {"prof":"S.ELFASSI","module":"mécanique générale","groupes":["jm1"],"nb":2,"dispos":[4,5,8,9,16,17]},
        {"prof":"S.ELFASSI","module":"mécanique quantique","groupes":["isen"],"nb":1,"dispos":[4,5,8,9,16,17]},
        {"prof":"S.ELFASSI","module":"mécanique des fluides","groupes":["jm2"],"nb":1,"dispos":[4,5,8,9,16,17]},
    ]

    moteur = GenerateurEDT1Semaine(data_matrice, salles)

    print("\n[Calcul] Génération de la semaine...")

    if moteur.resoudre():
        moteur.afficher()
        print("\n[SUCCÈS] Emploi du temps généré.")
    else:
        print("\n[ÉCHEC] Impossible de générer l'emploi du temps.")
