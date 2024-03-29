# #Importation de la librairie Pandas
import pandas as pd

#Importation du fichier population.csv
population = pd.read_csv('population.csv')

#Importation du fichier dispo_alimentaire.csv
dispoAlimentaire = pd.read_csv('dispo_alimentaire.csv')

#Importation du fichier aide_alimentaire.csv
aideAlimentaire = pd.read_csv('aide_alimentaire.csv')

#Importation du fichier sous_nutrition.csv
sousNutrition = pd.read_csv('sous_nutrition.csv')

#Afficher les dimensions du dataset
# print("Le tableau comporte {} observation(s) ou article(s)".format(population.shape[0]))
# print("Le tableau comporte {} colonne(s)".format(population.shape[1]))

#Consulter le nombre de colonnes
# print("Le tableau comporte {} colonne(s)".format(len(population.columns)))

#La nature des données dans chacune des colonnes
# Convertir la série des types de données en un DataFrame
dtypes_df = population.dtypes.to_frame()
# Formater le DataFrame en une chaîne
dtypes_str = dtypes_df.to_string()
# Afficher le résultat
# print("La nature des colonnes est :\n{}".format(dtypes_str))

#Le nombre de valeurs présentes dans chacune des colonnes
# print("Le nombre de valeurs présentes dans chacune des colonnes est :\n{}".format(population.count()))

#Affichage les 5 premières lignes de la table
# print("Les 5 premières lignes de la table population")
# print(population.head())

#Nous allons harmoniser les unités. Pour cela, nous avons décidé de multiplier la population par 1000
#Multiplication de la colonne valeur par 1000

# print("Nous allons harmoniser les unités en multipliant la population par 1000.")

# Multiplication de la colonne "Valeur" par 1000
population['Population'] = population['Valeur'] * 1000

# Convertir les valeurs en entiers
population['Population'] = population['Population'].astype(int)

# Afficher le résultat
# print("Nous avons harmonisé les unités en multipliant la population par 1000 :\n{}".format(population))

# Supprimer la colonne "Valeur" originale
population.drop(columns=['Valeur'], inplace=True)
#Affichage les 5 premières lignes de la table pour voir les modifications
# print(population.head())

#Afficher les dimensions du dataset

# print("Le tableau comporte {} observation(s) ou article(s)".format(dispoAlimentaire.shape[0]))

#Consulter le nombre de colonnes
# print("Le tableau comporte {} colonne(s)".format(dispoAlimentaire.shape[1]))

#Affichage les 5 premières lignes de la table
# print("Les 5 premières lignes de la table dispositions alimentaires sont :")
# print(dispoAlimentaire.head())


#remplacement des NaN dans le dataset par des 0
dispoAlimentaire = dispoAlimentaire.fillna(0)
# print(dispoAlimentaire.head())


#multiplication de toutes les lignes contenant des milliers de tonnes en Kg
colonnes_a_convertir = ['Autres Utilisations', 'Disponibilité intérieure', 'Exportations - Quantité',
                        'Importations - Quantité', 'Nourriture', 'Pertes', 'Production', 'Semences', 
                        'Traitement', 'Variation de stock']

for colonne in colonnes_a_convertir:
    dispoAlimentaire[colonne] *= 1000  # Convertir de milliers de tonnes à kg

#Affichage les 5 premières lignes de la table
# print(dispoAlimentaire.head())


# Afficher les premières lignes du DataFrame
# print(NewDispoAlimentaire_entier.head())

#Affichage les 5 premières lignes de la table
# print(NewDispoAlimentaire_entier.head())

#Afficher les dimensions du dataset
# print("Le tableau comporte {} observation(s) ou article(s)".format(aideAlimentaire.shape[0]))
# print("Le tableau comporte {} colonne(s)".format(aideAlimentaire.shape[1]))

#Consulter le nombre de colonnes
# print("Le nombre de colonnes est : {}".format(aideAlimentaire.shape[1]))

#Affichage les 5 premières lignes de la table
# print("les 5 premières lignes de la table aideAlimentaire sont : ")
# print(aideAlimentaire.head())

#changement du nom de la colonne Pays bénéficiaire par Zone
aideAlimentaire.rename(columns={'Pays bénéficiaire':'Zone'}, inplace=True)
# print(aideAlimentaire.head())

#Multiplication de la colonne Aide_alimentaire qui contient des tonnes par 1000 pour avoir des kg
aideAlimentaire['Valeur'] = aideAlimentaire['Valeur']*1000

#Affichage les 5 premières lignes de la table
# print(aideAlimentaire.head())

#Afficher les dimensions du dataset
# print("Le tableau comporte {} observation(s) ou article(s)".format(sousNutrition.shape[0]))

#Consulter le nombre de colonnes
# print("Le tableau comporte {} colonne(s)".format(sousNutrition.shape[1]))

#Afficher les 5 premières lignes de la table
# print(sousNutrition.head())

#Conversion de la colonne sous nutrition en numérique
sousNutrition['Valeur'] = pd.to_numeric(sousNutrition['Valeur'], errors='coerce')

#Conversion de la colonne (avec l'argument errors=coerce qui permet de convertir automatiquement les lignes qui ne sont pas des nombres en NaN)
#Puis remplacement des NaN en 0
sousNutrition['Valeur'] = sousNutrition['Valeur'].fillna(0)
# print(sousNutrition['Valeur'])

#changement du nom de la colonne Valeur par sous_nutrition
sousNutrition = sousNutrition.rename(columns={'Valeur': 'sous_nutrition'})
# print(sousNutrition)

#Multiplication de la colonne sous_nutrition par 1000000
sousNutrition['sous_nutrition'] *= 1000000

# Conversion en chiffres entiers
sousNutrition['sous_nutrition'] = sousNutrition['sous_nutrition'].astype(int)

#Afficher les 5 premières lignes de la table
# print(sousNutrition.head())



# # ************************************************************
# CALCULER LA PROPORTION DE PERSONNES EN SOUS NUTRITION PAR PAYS EN 2017
# # ************************************************************



# TRAVAIL SUR LA TABLE SOUS NUTRITION

# Déploiement du groupe d'année sur une ligne ['2012-2014'] => ['2012', '2013', '2014']
sousNutrition['Année'] = sousNutrition['Année'].str.split('-').apply(lambda x: list(range(int(x[0]), int(x[1])+1)))
sousNutrition = sousNutrition.explode('Année')
sousNutrition['Année'] = sousNutrition['Année'].astype(int)

# Réinitialiser les index /garantit que chaque ligne a un index unique et que les index sont contigus, ce qui facilite l'accès et la manipulation des données.
sousNutrition = sousNutrition.reset_index(drop=True)

# Convertir la colonne 'Année' en type entier (int)
sousNutrition['Année'] = sousNutrition['Année'].astype(int)


# ************************************************************


# Jointure entre les tables population et sousNutrition sur les colonnes 'Zone' et 'Année'
jointure = pd.merge(population, sousNutrition, on=['Zone', 'Année'])

# Filtrer les résultats pour ne conserver que les lignes avec l'année 2017
resultats_2017 = jointure[jointure['Année'] == 2017]

#Regrouper les données en fonction de la colonne Zone 
#puis retenir la première valeur de la colonne Population et la dernière valeurs de la colonne sous_nutrition (celle la plus récente)

# Trouver la valeur de personnes en sous-nutrition pour chaque pays en 2017
resultats_2017 = resultats_2017.groupby('Zone').agg({'Population': 'first', 'sous_nutrition': 'last'}).reset_index()


# resultats_2017 = resultats_2017.groupby('Zone').agg({'Population': 'first', 'sous_nutrition': 'sum'}).reset_index()

# Convertir la colonne 'sous_nutrition' en type entier
resultats_2017['sous_nutrition'] = resultats_2017['sous_nutrition'].astype(int)

# Calculer la proportion de sous-nutrition
resultats_2017['proportion_sous_nutrition'] = resultats_2017['sous_nutrition'] / resultats_2017['Population']*100

# Arrondir les valeurs à deux chiffres après la virgule et rajouter le signe % à la fin
resultats_2017['proportion_sous_nutrition'] = resultats_2017['proportion_sous_nutrition'].round(2).astype(str) + '%'

#print(resultats_2017)
# print to excel


# Calcul et affichage du nombre de personnes en état de sous-nutrition en 2017 avec des séparateurs entre les milliers
total_sous_nutrition = round(resultats_2017['sous_nutrition'].sum())

# Utiliser la méthode format avec le spécificateur de format {:,} pour ajouter des séparateurs entre les milliers
formatted_total_sous_nutrition = "{:,.0f}".format(total_sous_nutrition)

#print("Le nombre de personnes en état de sous-nutrition en 2017 est de : {} personnes".format(formatted_total_sous_nutrition))

#calcul du nombre de personnes dans la population mondiale en 2017
total_population = round(resultats_2017['Population'].sum())
formatted_total_population = "{:,.0f}".format(total_population)
#print("Le nombre de personnes dans la population mondiale en 2017 est de : {} personnes".format(formatted_total_population))

# Calcul et affichage du pourcentage de personnes en état de sous-nutrition dans le monde en 2017
pourcentage_sous_nutrition = total_sous_nutrition / total_population * 100
pourcentage_sous_nutrition_arrondi = round(pourcentage_sous_nutrition, 2)
#print("Le pourcentage de personnes en état de sous-nutrition dans le monde en 2017 est de : {}%".format(pourcentage_sous_nutrition_arrondi))


#Combien mange en moyenne un être humain ?  
# Calculer la disponibilité alimentaire moyenne par personne par produit
disponibilite_moyenne_par_personne = dispoAlimentaire[['Produit', 'Disponibilité alimentaire en quantité (kg/personne/an)']].groupby('Produit').mean()

# Afficher la disponibilité alimentaire moyenne par personne par produit
# print(disponibilite_moyenne_par_personne)
# print(disponibilite_moyenne_par_personne.loc['Blé'])

#Faire une jointure entre les tables disponibilité alimentaire et population sur la colonne Zone
# la table disponibilité alimentaire ne comporte pas de colonne année, il faut donc faire une moyenne de population par pays
# pour pouvoir faire la jointure
# Calculer la population moyenne par pays
population_moyenne = population.groupby('Zone')['Population'].mean().reset_index()

# Renommer la colonne 'Population' en 'Population_moyenne'
population_moyenne.rename(columns={'Population': 'Population_moyenne'}, inplace=True)

# Faire une jointure entre les tables disponibilité alimentaire et population sur la colonne Zone
dispoAlimentaire = pd.merge(dispoAlimentaire, population_moyenne, on='Zone')

# Définition de la fonction de formatage
def format_population(valeur):
    return "{:,.0f}".format(valeur).replace(",", " ")

# Appliquer la fonction de formatage à la colonne 'Population_moyenne'
dispoAlimentaire['Population_moyenne'] = dispoAlimentaire['Population_moyenne'].apply(format_population)

# Afficher les premières lignes du DataFrame
#print(dispoAlimentaire.head())

#Convertir le type de la colonne 'Population_moyenne' en entier float64

dispoAlimentaire['Population_moyenne'] = dispoAlimentaire['Population_moyenne'].str.replace(' ', '').astype('float64')


# Création de la colonne dispo_kcal à partir de la colonne Disponibilité alimentaire (Kcal/personne/jour) de la table dispoAlimentaire
# puis calcul des kcal disponibles mondialement
dispoAlimentaire['dispo_kcal'] = dispoAlimentaire['Disponibilité alimentaire (Kcal/personne/jour)'] * dispoAlimentaire['Population_moyenne'] * 365

# Définition de la fonction de formatage pour dispo_kcal
def format_dispo_kcal(valeur):
    return "{:,.0f}".format(valeur).replace(",", " ")

# Appliquer la fonction de formatage à la colonne 'dispo_kcal'
dispoAlimentaire['dispo_kcal'] = dispoAlimentaire['dispo_kcal'].apply(format_dispo_kcal)

# Afficher les premières lignes du DataFrame
#print(dispoAlimentaire.head())

#convertir le type de la colonne 'dispo_kcal' en entier float64
dispoAlimentaire['dispo_kcal'] = dispoAlimentaire['dispo_kcal'].str.replace(' ', '').astype('float64')


#Calcul du nombre d'humains pouvant être nourris
# Calculer le nombre d'humains pouvant être nourris avec les kcal disponibles dans le monde
kcal_disponibles = dispoAlimentaire['dispo_kcal'].sum()
nb_humains_nourris = kcal_disponibles / 2500 / 365

# Afficher le nombre d'humains pouvant être nourris
print("Le nombre d'humains pouvant être nourris avec les kcal disponibles dans le monde est de : {:,.0f} personnes".format(nb_humains_nourris))




