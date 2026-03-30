import sys
JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
CRENEAUX = ["09:00-10:45", "11:00-12:45", "13:45-15:30", "15:45-17:30"]
def saisir_donnees():
try:
nb_salles = int(input("Nombre de salles disponibles : "))
_ = input("Nombre de groupes (indicatif) : ") # Gardé pour
respecter ton ordre
except ValueError:
sys.exit("Erreur : Entrez des nombres entiers.")
matrice = []
dispos_profs = {}
print("\nSaisie de la matrice (Appuyez sur Entrée sur une ligne vide
pour finir) :")
IndicesDispos")
print("Format : Prof, Module, Groupes, NbSéancesTotal,
while True:
ligne = input("> ")
if not ligne: break
parts = [p.strip() for p in ligne.split(",")]
if len(parts) < 4:
print("Ligne incomplète (il faut au moins Prof, Module,
Groupe, Nb).")
continu
prof, module, groupe_brut, nb = parts[0], parts[1], parts[2],
int(parts[3])
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
# Extraire tous les noms de groupes uniques (même s'ils
s'appellent "XY Rouge")
tous_grps = set()
for d in data:
for g in d['groupes']: tous_grps.add(g)
self.groupes_uniques = sorted(list(tous_grps))
# Planning general
self.planning = {s: [[{g: None for g in self.groupes_uniques}
for _ in range(4)] for _ in range(5)] for s
in range(13)}
def verifier(self, s, j, c, groupes_cible, prof_nom, dispos_prof):
# Dispo prof
if (j * 4 + c) not in dispos_prof: return False
# le groupe n'a pas de seance avec d'autre groupe
for g in groupes_cible:
if self.planning[s][j][c][g] is not None: return False
# le prof n'a pas de seance avec un autre groupe
for g_nom in self.groupes_uniques:
occ = self.planning[s][j][c][g_nom]
if occ and occ[0] == prof_nom: return False
# Nombre de salles disponibles
profs_ce_creneau = set()
for g_nom in self.groupes_uniques:
if self.planning[s][j][c][g_nom]:
profs_ce_creneau.add(self.planning[s][j][c][g_nom][0])
if len(profs_ce_creneau) >= self.nb_salles: return False
return True
def resoudre(self, idx=0, reste=None):
if idx >= len(self.data): return True
curr = self.data[idx]
if reste is None: reste = curr['nb']
if reste <= 0: return self.resoudre(idx + 1)
for s in range(13):
for j in range(5):
for c in range(4):
curr['prof'], curr['dispos']):
if self.verifier(s, j, c, curr['groupes'],
# Assigner à TOUS les groupes de la liste (ex:
G1 et G2 en même temps)
for g in curr['groupes']:
self.planning[s][j][c][g] = (curr['prof'],
curr['module'])
if self.resoudre(idx, reste - 1): return True
# Backtrack
for g in curr['groupes']:
self.planning[s][j][c][g] = None
return False
def afficher_tout(self):
for s in range(13):
print(f"\n\n{'='*90}\n SEMAINE {s+1}\n{'='*90}")
for g in self.groupes_uniques:
print(f"\nGROUPE : {g}")
header = f"{'Jour':<10} | " + " | ".join([f"{c:<16}" for
c in CRENEAUX])
print(header)
print("-" * len(header))
for j in range(5):
ligne = []
for c in range(4):
info = self.planning[s][j][c][g]
if info:
# Affiche "Module(Prof)"
txt = f"{info[1][:8]}({info[0][:6]})"
ligne.append(f"{txt:<16}")
else:
ligne.append(f"{'---':^16}")
print(f"{JOURS[j]:<10} | " + " | ".join(ligne))
if __name__ == "__main__":
data_matrice, salles = saisir_donnees()
if data_matrice:
moteur = GenerateurEDT13Semaines(data_matrice, salles)
print("\n[Calcul] Génération des 13 semaines en cours...")
if moteur.resoudre():
moteur.afficher_tout()
print("\n[SUCCÈS] Emploi du temps terminé.")
else:
print("\n[ÉCHEC] Impossible de placer toutes les séances.")
