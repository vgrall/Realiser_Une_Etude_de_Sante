import pandas as pd
import matplotlib as plt

#Importation du fichier population.csv
population = pd.read_csv('population.csv')

#Importation du fichier dispo_alimentaire.csv
dispoAlimentaire = pd.read_csv('dispo_alimentaire.csv')

#Importation du fichier aide_alimentaire.csv
aideAlimentaire = pd.read_csv('aide_alimentaire.csv')

#Importation du fichier sous_nutrition.csv
sousNutrition = pd.read_csv('sous_nutrition.csv')

#Nous allons harmoniser les unités. Pour cela, nous avons décidé de multiplier la population par 1000


# Multiplication de la colonne "Valeur" par 1000
population['Population'] = population['Valeur'] * 1000

# Convertir les valeurs en entiers
population['Population'] = population['Population'].astype(int)

# Afficher le résultat
#print("Nous avons harmonisé les unités en multipliant la population par 1000 :\n{}".format(population))

# Supprimer la colonne "Valeur" originale
population.drop(columns=['Valeur'], inplace=True)

#remplacement des NaN dans le dataset par des 0
dispoAlimentaire = dispoAlimentaire.fillna(0)
#multiplication de toutes les lignes contenant des milliers de tonnes en Kg
colonnes_a_convertir = ['Autres Utilisations', 'Disponibilité intérieure', 'Exportations - Quantité',
                        'Importations - Quantité', 'Nourriture', 'Pertes', 'Production', 'Semences', 
                        'Traitement', 'Variation de stock']

for colonne in colonnes_a_convertir:
    dispoAlimentaire[colonne] *= 1000  # Convertir de milliers de tonnes à kg

#changement du nom de la colonne Pays bénéficiaire par Zone
aideAlimentaire.rename(columns={'Pays bénéficiaire':'Zone'}, inplace=True)

#Multiplication de la colonne Aide_alimentaire qui contient des tonnes par 1000 pour avoir des kg
aideAlimentaire['Valeur'] = aideAlimentaire['Valeur']*1000

#Conversion de la colonne sous nutrition en numérique
sousNutrition['Valeur'] = pd.to_numeric(sousNutrition['Valeur'], errors='coerce')

#Conversion de la colonne (avec l'argument errors=coerce qui permet de convertir automatiquement les lignes qui ne sont pas des nombres en NaN)
#Puis remplacement des NaN en 0
sousNutrition['Valeur'] = sousNutrition['Valeur'].fillna(0)

#changement du nom de la colonne Valeur par sous_nutrition
sousNutrition = sousNutrition.rename(columns={'Valeur': 'sous_nutrition'})

#Multiplication de la colonne sous_nutrition par 1000000
sousNutrition['sous_nutrition'] *= 1000000

# Conversion en chiffres entiers
sousNutrition['sous_nutrition'] = sousNutrition['sous_nutrition'].astype(int)

#3_1 PROPORTION DE PERSONNES EN SOUS NUTRITION

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
#puis retenir la première valeur de la colonne Population et la dernière valeurs de la colonne sous_nutrition
# les données de la FAO en sous-nutrition sont déjà une moyenne sur trois ans (vérification sur le site FAOSTAT), donc je récupère la valeur la plus récente
# Trouver la valeur de personnes en sous-nutrition pour chaque pays en 2017
resultats_2017 = resultats_2017.groupby('Zone').agg({'Population': 'first', 'sous_nutrition': 'last'}).reset_index()

# Convertir la colonne 'sous_nutrition' en type entier
resultats_2017['sous_nutrition'] = resultats_2017['sous_nutrition'].astype(int)

# Calculer la proportion de sous-nutrition
resultats_2017['proportion_sous_nutrition'] = resultats_2017['sous_nutrition'] / resultats_2017['Population']*100

# Arrondir les valeurs à deux chiffres après la virgule et rajouter le signe % à la fin
resultats_2017['proportion_sous_nutrition'] = resultats_2017['proportion_sous_nutrition'].round(2).astype(str) + '%'


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


#3_2 NOMBRE THEORIQUE DE PERSONNES QUI POURRAIENT ÊTRE NOURRIES

#Combien mange en moyenne un être humain ? Source => dispoAlimentaire
# Calculer la disponibilité alimentaire moyenne par personne par produit en 2017

disponibilite_moyenne_par_personne = dispoAlimentaire[['Produit', 'Disponibilité alimentaire en quantité (kg/personne/an)']].groupby('Produit').mean()
#print(disponibilite_moyenne_par_personne)

#Filtrer la table population sur l'année 2017 
population_2017 = population[population['Année'] == 2017]

#Faire une jointure entre les tables disponibilité alimentaire et population sur la colonne Zone
dispoAlimentaire = pd.merge(dispoAlimentaire, population_2017, on='Zone')

# Calculer la somme de la disponibilité alimentaire en calories par personne et par jour par pays
Nbre_cal_journaliere_par_personne_disponibles = dispoAlimentaire.groupby('Zone')['Disponibilité alimentaire (Kcal/personne/jour)'].sum().reset_index()
Nbre_cal_journaliere_par_personne_disponibles.rename(columns={'Disponibilité alimentaire (Kcal/personne/jour)': 'Nbre_cal_journaliere_par_personne_disponibles'}, inplace=True)

# Fusionner les DataFrames sur la colonne 'Zone'
dispoAlimentaire = pd.merge(dispoAlimentaire, Nbre_cal_journaliere_par_personne_disponibles, on='Zone')

# Grouper par pays et obtenir la première ligne de chaque groupe
NourritureDispo = dispoAlimentaire.groupby('Zone').first().reset_index()[['Zone', 'Population', 'Nbre_cal_journaliere_par_personne_disponibles']]

# Calculer la colonne Nbre_cal_dispo_totale
NourritureDispo['Nbre_cal_dispo_totale'] = NourritureDispo['Population'] * NourritureDispo['Nbre_cal_journaliere_par_personne_disponibles']

# Afficher les premières lignes du DataFrame mis à jour
#print(NourritureDispo.head())

# Nombre moyen de calories nécessaires par personne par jour (valeur fictive)
calories_necessaires_par_personne = 2350  # en calories

# Calculer le nombre d'humains pouvant être nourris
NourritureDispo['Nb_humains_nourris'] = NourritureDispo['Nbre_cal_dispo_totale'] / calories_necessaires_par_personne

# Calculer le nombre total d'humains nourris
nombre_total_humains_nourris = NourritureDispo['Nb_humains_nourris'].sum()

#print("Le nombre total d'humains pouvant être nourris est d'environ : {:.2f} milliards d'humains".format(nombre_total_humains_nourris / 1e9))

#3_3 Nombre théorique de personnes qui pourraient être nourries avec les produits végétaux

#Transfert des données avec les végétaux dans un nouveau dataframe
dispoAlimentaire_vegetaux = dispoAlimentaire[dispoAlimentaire['Origine'] == 'vegetale']

# Supprimer la colonne 'Nbre_cal_journaliere_par_personne_disponibles' du DataFrame dispoAlimentaire_vegetaux car elle regroupe toutes les origines
dispoAlimentaire_vegetaux = dispoAlimentaire_vegetaux.drop('Nbre_cal_journaliere_par_personne_disponibles', axis=1)

#calculer le Nbre_cal_vege_journaliere_par_personne_disponibles pour les produits végétaux
Nbre_cal_vege_journaliere_par_personne_disponibles = dispoAlimentaire_vegetaux.groupby('Zone')['Disponibilité alimentaire (Kcal/personne/jour)'].sum().reset_index()
Nbre_cal_vege_journaliere_par_personne_disponibles.rename(columns={'Disponibilité alimentaire (Kcal/personne/jour)': 'Nbre_cal_vege_journaliere_par_personne_disponibles'}, inplace=True)

#Ajouter cette colonne au DataFrame dispoAlimentaire_vegetaux
dispoAlimentaire_vegetaux = pd.merge(dispoAlimentaire_vegetaux, Nbre_cal_vege_journaliere_par_personne_disponibles, on='Zone')

#Grouper par pays et obtenir la première ligne de chaque groupe
NourritureDispo_vegetaux = dispoAlimentaire_vegetaux.groupby('Zone').first().reset_index()[['Zone', 'Population', 'Nbre_cal_vege_journaliere_par_personne_disponibles']]
#print(NourritureDispo_vegetaux.head())

#Calculer la colonne Nbre_cal_vege_dispo_totale
NourritureDispo_vegetaux['Nbre_cal_vege_dispo_totale'] = NourritureDispo_vegetaux['Population'] * NourritureDispo_vegetaux['Nbre_cal_vege_journaliere_par_personne_disponibles']

#Calculer le nombre d'humains pouvant être nourris avec les produits végétaux
NourritureDispo_vegetaux['Nb_humains_nourris_vegetaux'] = NourritureDispo_vegetaux['Nbre_cal_vege_dispo_totale'] / calories_necessaires_par_personne

#Calculer le nombre total d'humains nourris avec les produits végétaux
nombre_total_humains_nourris_vegetaux = NourritureDispo_vegetaux['Nb_humains_nourris_vegetaux'].sum()
print("Le nombre total d'humains pouvant être nourris avec les produits végétaux est d'environ : {:.2f} milliards d'humains".format(nombre_total_humains_nourris_vegetaux / 1e9))