import sys
import math
 
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
   prefs_profs = {}
 
   print("\nSaisie de la matrice (Appuyez sur Entrée sur une ligne vide pour finir) :")
   print("Format : Prof, Module, Groupes, NbSéancesTotal, IndicesDispos, IndicesPreférences")
 
   while True:
       ligne = input("> ")
       if not ligne:
           break
 
       parts = [p.strip() for p in ligne.split(",")]
       if len(parts) < 4:
           continue
 
       prof, module, groupe_brut, nb = parts[0], parts[1], parts[2], int(parts[3])
       groupes_liste = [g.strip() for g in groupe_brut.split("&")]
 
       # Disponibilités (colonne 5)
       if len(parts) >= 5 and parts[4]:
           indices = [int(i) for i in parts[4].split() if i.isdigit()]
           dispos_profs[prof] = indices
       elif prof in dispos_profs:
           indices = dispos_profs[prof]
       else:
           indices = list(range(20))
           dispos_profs[prof] = indices
 
       # Préférences de créneaux (colonne 6, optionnelle)
       if len(parts) >= 6 and parts[5]:
           prefs = [int(i) for i in parts[5].split() if i.isdigit()]
           prefs_profs[prof] = prefs
       elif prof in prefs_profs:
           prefs = prefs_profs[prof]
       else:
           prefs = []  # aucune préférence déclarée = pas de pénalité
           prefs_profs[prof] = prefs
 
       matrice.append({
           "prof": prof,
           "module": module,
           "groupes": groupes_liste,
           "nb": nb,
           "dispos": indices,
           "preferences": prefs,
       })
 
   return matrice, nb_salles
 
 
class GenerateurEDT13Semaines:
   def __init__(self, data, nb_salles):
       self.data = data
       self.nb_salles = nb_salles
 
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
 
       # Poids des pénalités pour les contraintes faibles
       self.POIDS_DISPO       = 3  # créneau hors disponibilités déclarées
       self.POIDS_PREFERENCE  = 1  # créneau non préféré (mais dans les dispos)
 
 
   # CONTRAINTES FORTES
 
 
   def contrainte_forte_groupe(self, s, j, c, groupes_cible):
       """Aucun groupe cible ne doit déjà avoir un cours sur ce créneau."""
       for g in groupes_cible:
           if self.planning[s][j][c][g] is not None:
               return False
       return True
 
   def contrainte_forte_prof(self, s, j, c, prof_nom):
       """Le prof ne doit pas déjà enseigner sur ce créneau."""
       for g_nom in self.groupes_uniques:
           occ = self.planning[s][j][c][g_nom]
           if occ and occ[0] == prof_nom:
               return False
       return True
 
   def contrainte_forte_salles(self, s, j, c):
       """Le nombre de cours simultanés ne dépasse pas le nombre de salles."""
       profs_ce_creneau = set()
       for g_nom in self.groupes_uniques:
           occ = self.planning[s][j][c][g_nom]
           if occ:
               profs_ce_creneau.add(occ[0])
       return len(profs_ce_creneau) < self.nb_salles
 
   def contrainte_forte_repartition(self, s, module, groupes_cible, max_par_semaine):
       """
       La semaine s ne doit pas déjà atteindre le quota de séances
       pour ce module et ces groupes. (Ancienne contrainte faible → forte)
       """
       count = sum(
           1
           for j in range(5)
           for c in range(4)
           for g in groupes_cible
           if self.planning[s][j][c][g]
           and self.planning[s][j][c][g][1] == module
       )
       return count < max_par_semaine
 
   def verifier_contraintes_fortes(self, s, j, c, groupes_cible, prof_nom,
                                   module, max_par_semaine):
       """Vérifie toutes les contraintes fortes. Retourne False si l'une est violée."""
       return (
           self.contrainte_forte_groupe(s, j, c, groupes_cible)
           and self.contrainte_forte_prof(s, j, c, prof_nom)
           and self.contrainte_forte_salles(s, j, c)
           and self.contrainte_forte_repartition(s, module, groupes_cible, max_par_semaine)
       )
 
 
   # CONTRAINTES FAIBLES — score de pénalité (≥ 0)
 
 
   def penalite_dispo_prof(self, j, c, dispos_prof):
       """
       Pénalise si le créneau est hors des disponibilités déclarées du prof.
       Priorité haute : cette violation est fortement déconseillée.
       """
       if (j * 4 + c) not in dispos_prof:
           return self.POIDS_DISPO
       return 0
 
   def penalite_preference_prof(self, j, c, dispos_prof, preferences_prof):
       """
       Pénalise si le créneau est dans les dispos mais hors des créneaux
       préférés. Si aucune préférence n'est déclarée, pas de pénalité.
       """
       idx = j * 4 + c
       if not preferences_prof:
           return 0
       # On ne pénalise que si le créneau est dans les dispos (sinon
       # la pénalité dispo couvre déjà la violation)
       if idx in dispos_prof and idx not in preferences_prof:
           return self.POIDS_PREFERENCE
       return 0
 
   def calculer_penalite(self, j, c, dispos_prof, preferences_prof):
       """Retourne la pénalité totale des contraintes faibles pour ce créneau."""
       return (
           self.penalite_dispo_prof(j, c, dispos_prof)
           + self.penalite_preference_prof(j, c, dispos_prof, preferences_prof)
       )
 
 
   # RÉSOLUTION
 
 
   def candidats_tries(self, curr, max_par_semaine):
       """
       Génère tous les créneaux valides (contraintes fortes OK),
       triés par pénalité croissante (contraintes faibles).
       """
       candidats = []
       for s in range(13):
           for j in range(5):
               for c in range(4):
                   if not self.verifier_contraintes_fortes(
                       s, j, c, curr['groupes'], curr['prof'],
                       curr['module'], max_par_semaine
                   ):
                       continue
 
                   penalite = self.calculer_penalite(
                       j, c, curr['dispos'], curr['preferences']
                   )
                   candidats.append((penalite, s, j, c))
 
       candidats.sort(key=lambda x: x[0])
       return candidats
 
   def resoudre(self, idx=0, reste=None):
       if idx >= len(self.data):
           return True
 
       curr = self.data[idx]
       max_par_semaine = math.ceil(curr['nb'] / 13)
 
       if reste is None:
           reste = curr['nb']
 
       if reste <= 0:
           return self.resoudre(idx + 1)
 
       for _penalite, s, j, c in self.candidats_tries(curr, max_par_semaine):
           for g in curr['groupes']:
               self.planning[s][j][c][g] = (curr['prof'], curr['module'])
 
           if self.resoudre(idx, reste - 1):
               return True
 
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
       # Les disponibilités sont les créneaux autorisés (contrainte faible forte pénalité).
       # Les préférences sont les créneaux idéaux parmi les dispos (pénalité légère si ignorées).
       # Format : dispos = indices 0..19,  preferences = sous-ensemble de dispos
 
       {"prof":"H.NAQOS","module":"algèbre2","groupes":["jm1"],"nb":6,
        "dispos":list(range(20)),"preferences":[0,1,4,5]},
 
       {"prof":"H.NAQOS","module":"analyse2","groupes":["jm1"],"nb":6,
        "dispos":list(range(20)),"preferences":[0,1,4,5]},
 
       {"prof":"H.NAQOS","module":"mathématique","groupes":["hei","isen"],"nb":15,
        "dispos":list(range(20)),"preferences":[0,1,4,5]},
 
       {"prof":"H.NAQOS","module":"analyse numérique","groupes":["jm2"],"nb":14,
        "dispos":list(range(20)),"preferences":[0,1,4,5]},
 
       {"prof":"H.NAQOS","module":"apprentissage automatique","groupes":["jm4"],"nb":8,
        "dispos":list(range(20)),"preferences":[0,1,4,5]},
 
       {"prof":"S.HDAFA","module":"algorithme et programmation","groupes":["jm1"],"nb":25,
        "dispos":list(range(20)),"preferences":[]},
 
       {"prof":"S.HDAFA","module":"développement web","groupes":["jm2"],"nb":28,
        "dispos":list(range(20)),"preferences":[]},
 
       {"prof":"S.HDAFA","module":"projet étude et conception","groupes":["isen"],"nb":16,
        "dispos":list(range(20)),"preferences":[]},
 
       {"prof":"H.ZEROUALI","module":"analyse2","groupes":["jm1"],"nb":6,
        "dispos":[0,1,12,13,16,17,18],"preferences":[0,1]},
 
       {"prof":"H.ZEROUALI","module":"algèbre2","groupes":["jm1"],"nb":6,
        "dispos":[0,1,12,13,16,17,18],"preferences":[0,1]},
 
       {"prof":"H.ZEROUALI","module":"probabilite","groupes":["jm2"],"nb":24,
        "dispos":[0,1,12,13,16,17,18],"preferences":[12,13]},
 
       {"prof":"A.DAHMANI","module":"science de l'ingénieur","groupes":["jm2"],"nb":16,
        "dispos":[4,5,8,9,16,17,18],"preferences":[8,9]},
 
       {"prof":"A.DAHMANI","module":"projet étude et conception","groupes":["hei"],"nb":16,
        "dispos":[4,5,8,9,16,17,18],"preferences":[8,9]},
 
       {"prof":"A.DAHMANI","module":"ingénierie mécanique","groupes":["hei"],"nb":24,
        "dispos":[4,5,8,9,16,17,18],"preferences":[4,5]},
 
       {"prof":"A.ELMANSOUR","module":"interculturalité","groupes":["hei","isen"],"nb":9,
        "dispos":[2,3,14,15],"preferences":[14,15]},
 
       {"prof":"A.ELYAZIDI","module":"aide à la decision","groupes":["hei","isen"],"nb":18,
        "dispos":[0,1,9,10,16,17],"preferences":[9,10]},
 
       {"prof":"A.ELYAZIDI","module":"système d'exploitation","groupes":["jm4"],"nb":12,
        "dispos":[0,1,9,10,16,17],"preferences":[0,1]},
 
       {"prof":"T.AKDIM","module":"intro gestion compta finance","groupes":["jm1"],"nb":15,
        "dispos":[0,1,2,3,6,7,10,11],"preferences":[6,7]},
 
       {"prof":"T.AKDIM","module":"marketing","groupes":["hei","isen"],"nb":9,
        "dispos":[0,1,2,3,6,7,10,11],"preferences":[10,11]},
 
       {"prof":"T.AKDIM","module":"entreprenariat","groupes":["jm4"],"nb":12,
        "dispos":[0,1,2,3,6,7,10,11],"preferences":[2,3]},
 
       {"prof":"S.ELFASSI","module":"mécanique générale","groupes":["jm1"],"nb":24,
        "dispos":[4,5,8,9,16,17],"preferences":[16,17]},
 
       {"prof":"S.ELFASSI","module":"mécanique quantique","groupes":["isen"],"nb":18,
        "dispos":[4,5,8,9,16,17],"preferences":[4,5]},
 
       {"prof":"S.ELFASSI","module":"mécanique des fluides","groupes":["jm2"],"nb":12,
        "dispos":[4,5,8,9,16,17],"preferences":[8,9]},
 
       {"prof":"A.BENKHRABA","module":"anglais1","groupes":["jm1"],"nb":12,
        "dispos":[2,3,10,19],"preferences":[2,3]},
 
       {"prof":"A.BENKHRABA","module":"anglais2","groupes":["jm2"],"nb":12,
        "dispos":[2,3,10,19],"preferences":[10,19]},
 
       {"prof":"D.GUENDOUZ","module":"projet collectif découverte domaine","groupes":["jm1"],"nb":12,
        "dispos":list(range(20)),"preferences":[]},
 
       {"prof":"D.GUENDOUZ","module":"communication for working","groupes":["jm2"],"nb":12,
        "dispos":list(range(20)),"preferences":[]},
 
       {"prof":"S.SHLAKA","module":"communication1","groupes":["jm1"],"nb":12,
        "dispos":[6,7,14,15],"preferences":[14,15]},
 
       {"prof":"S.SHLAKA","module":"communication2","groupes":["jm2"],"nb":12,
        "dispos":[6,7,14,15],"preferences":[6,7]},
 
       {"prof":"N.AHAMI","module":"thermodynamique","groupes":["jm1"],"nb":14,
        "dispos":[10,11,12,13,16,17],"preferences":[12,13]},
 
       {"prof":"C.BAQA","module":"science de l'ingénieur","groupes":["jm1"],"nb":14,
        "dispos":[16,17],"preferences":[16,17]},
 
       {"prof":"M.SEBGUI","module":"systèmes embarqués","groupes":["jm2"],"nb":24,
        "dispos":[4,5,8,9,14,15],"preferences":[14,15]},
 
       {"prof":"S.MOULINE","module":"BD et BD Avancées","groupes":["jm4"],"nb":24,
        "dispos":[0,1,8,9],"preferences":[8,9]},
 
       {"prof":"M.RZIZA","module":"administration et sécurité des réseaux","groupes":["jm4"],"nb":24,
        "dispos":[0,1,8,9,12,13],"preferences":[12,13]},
 
       {"prof":"Y.AKALAY","module":"anglais","groupes":["jm4"],"nb":12,
        "dispos":[16,17],"preferences":[16,17]},
 
       {"prof":"M.ELHASSOUNI","module":"big data et analyse distribuée des données","groupes":["jm4"],"nb":24,
        "dispos":[6,7,8,9,15,16],"preferences":[6,7]},
 
       {"prof":"A.ESSADKI","module":"principe de l'instrumentation","groupes":["hei","isen"],"nb":18,
        "dispos":[6,7,10,11,12,13,14,15],"preferences":[10,11]},
 
       {"prof":"A.ESSADKI","module":"automatisation2","groupes":["hei","isen"],"nb":18,
        "dispos":[6,7,10,11,12,13,14,15],"preferences":[12,13]},
 
       {"prof":"A.ESSADKI","module":"electrecite vecteur d'énergie","groupes":["hei"],"nb":18,
        "dispos":[6,7,10,11,12,13,14,15],"preferences":[14,15]},
 
       {"prof":"A.ESSADKI","module":"regulation industrielle","groupes":["isen"],"nb":18,
        "dispos":[6,7,10,11,12,13,14,15],"preferences":[6,7]},
   ]
 
   moteur = GenerateurEDT13Semaines(data_matrice, salles)
   print("\n[Calcul] Génération des 13 semaines en cours...")
 
   if moteur.resoudre():
       moteur.afficher_tout()
       print("\n[SUCCÈS] Emploi du temps terminé.")
   else:
       print("\n[ÉCHEC] Impossible de placer toutes les séances.")
