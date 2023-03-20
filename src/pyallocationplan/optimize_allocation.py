import pyomo.environ as pe

# Création du modèle
model = pe.ConcreteModel()

# Ensemble des projets
projets: list[str] = ['FPI', 'FIJ', 'VBHC']

# Ensemble des compétences-clés
competences: list[str] = ['Data engineering', 'Data science', 'Project management']

# Nombre de jours-hommes disponibles pour chaque membre de l'équipe pour le trimestre
capacite: dict[str, int] = {'Membre 1': 400, 'Membre 2': 500, 'Membre 3': 300}

# Nombre de jours-hommes nécessaires pour chaque projet et compétence-clé
jours_hommes = {
    ('FPI', 'Data engineering'): 200,
    ('FPI', 'Data science'): 150,
    ('FPI', 'Project management'): 100,
    ('FIJ', 'Data science'): 250,
    ('FIJ', 'Project management'): 100,
    ('FIJ', 'Data engineering'): 0,
    ('VBHC', 'Data engineering'): 300,
    ('VBHC', 'Data science'): 0,
    ('VBHC', 'Project management'): 0,
}

# Variables de décision
model.x = pe.Var(capacite.keys(), projets, competences, domain=pe.NonNegativeIntegers)

# Fonction objectif
model.obj = pe.Objective(expr=sum(model.x[i, j, k] for i in capacite.keys() for j in projets for k in competences),
                         sense=pe.maximize)

# Contraintes de capacité
model.contrainte_capacite = pe.ConstraintList()
for i in capacite.keys():
    for k in competences:
        model.contrainte_capacite.add(sum(model.x[i, j, k] * jours_hommes[j, k] for j in projets) <= capacite[i])

# Contraintes de compétence
model.contrainte_competence = pe.ConstraintList()
for j in projets:
    for k in competences:
        model.contrainte_competence.add(sum(model.x[i, j, k] for i in capacite.keys()) >= jours_hommes[j, k])

# Résolution du modèle
solver = pe.SolverFactory('glpk')
solver.solve(model)

# Affichage de la solution
for i in capacite.keys():
    for j in projets:
        for k in competences:
            if model.x[i, j, k].value > 0:
                print(f"Le membre {i} est affecté à {model.x[i, j, k].value} jours pour le projet {j} et la compétence {k}")
