#1er essai 1/2
cours, classe, numéro_séances,salle = []
seances ={(cours, classe, numéro_séances,salle)}
profs = {}

def sont_pas_en_conflit(n1, n2):
    cours1, classe1 = n1
    cours2, classe2 = n2

    if classe1 == classe2:
        return False
    if salle[cours] == salle[cours2]:
        return False

    if profs[cours1] == profs[cours2]:
        return False

    return True
def generate_graph(seances):
    graph = {s:[] for s in seances}
        for i, s1 in enumerate(seances):
        for j, s2 in enumerate(seances):
            if i < j and sont_pas_en_conflit(s1, s2):
                graph[s1].append(s2)
                graph[s2].append(s1)

    return graph
