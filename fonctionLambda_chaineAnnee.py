import pandas as pd
import nbformat as nbf
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell



population = pd.read_csv('population.csv')

dispoAlimentaire = pd.read_csv('dispo_alimentaire.csv')

aideAlimentaire = pd.read_csv('aide_alimentaire.csv')

sousNutrition = pd.read_csv('sous_nutrition.csv')

# modifier l'object Année de sousNutrition pour le convertir en int
# sousNutrition['Année'] = sousNutrition['Année'].apply(lambda x: x.split('-')[0])

# sousNutrition['Année'] = sousNutrition['Année'].astype(int)
# print(sousNutrition.dtypes)

# Déploiement du groupe d'année sur une ligne ['2012-2014'] => ['2012', '2013', '2014']
sousNutrition['Année'] = sousNutrition['Année'].apply(lambda x: '-'.join([str(year) for year in range(int(x.split('-')[0]), int(x.split('-')[1]) + 1)]))
# print("*********")
# print ("SOUS NUTRITION déploiement année sur 1 ligne : ", sousNutrition.head())
# print("*********")
# print("SOUS NUTRITION déploiement année sur 1 ligne : " , sousNutrition.dtypes)
# print("*********")

# Dupliquer les lignes pour chaque année
sousNutrition = sousNutrition.assign(Année=sousNutrition['Année'].str.split('-')).explode('Année')

# Réinitialiser les index
sousNutrition = sousNutrition.reset_index(drop=True)

# print("*********")
# print ("SOUS NUTRITION eclaté : ", sousNutrition.head())
# print("*********")
# print("SOUS NUTRITION eclaté : " , sousNutrition.dtypes)
# print("*********")

# Convertir la colonne 'Année' en type entier (int)
sousNutrition['Année'] = sousNutrition['Année'].astype(int)

# print("*********")
# print ("SOUS NUTRITION éclaté avec int : ", sousNutrition.head())
# print("*********")
# print("SOUS NUTRITION eclaté avec int: " , sousNutrition.dtypes)
# print("*********")
# print("LE NOMBRE DE LIGNE DU NOUVEAU TABLEAU SOUS NUTRITION : ", sousNutrition.shape[0])

# Jointure entre les DataFrames sousNutrition et population sur les colonnes 'Zone' et 'Année'
# jointure = pd.merge(sousNutrition, population, on=['Zone', 'Année'])

# Afficher le DataFrame résultant
# print(jointure)

# Effectuer la jointure entre la table population et la table sousNutrition sur les colonnes 'Zone' et 'Année'
jointure = pd.merge(population, sousNutrition, on=['Zone', 'Année'])

# Filtrer les résultats pour ne conserver que les lignes avec l'année 2017
resultats_2017 = jointure[jointure['Année'] == 2017]

# Renommer les colonnes 'Valeur_x' et 'Valeur_y' en 'Population' et 'Sous_nutrition'
resultats_2017.rename(columns={'Valeur_x': 'Population', 'Valeur_y': 'Sous_nutrition'}, inplace=True)

# Afficher le DataFrame résultant
print(resultats_2017)
