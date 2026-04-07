#contraintes a prendre en compte
# profs a temps plein vs profs avec des horraires fixes 
disponibilites_profs = {
    "H. NAQOS": set(range(len(slots))),
    "S. HDAFA": set(range(len(slots))),

    "S. EL FASSI": {0, 1, 4, 5},
    "A. BENKHRABA": {8, 9, 10, 11},
    "S. SHLAKA": {2, 3, 6, 7},
}
#algo doit etre capable de generer tout un semestre (13semaines/720h de cours )
for semaine in range(13):
    emploi_semaine = coloration_graph_with_retries(graph)
    emplois_semestre.append(emploi_semaine)
#4 salles de capacites differentes

#eviter les heures creuses entre 2 matieres

#doit generer un pdf de 13semaines par classe


#contraintes 2 : eviter 2 seances de la meme matiere consecutives    // matieres scientifiques matin (couleur 1 2 5 6 9 10 13 14) // division euclidienne du module >13 sem   
#input based algorithm avec output sous forme de json

