import pandas as pd
import matplotlib.pyplot as plt


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
                        'Traitement', 'Variation de stock', 'Aliments pour animaux']

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

#exporter le fichir sous nutrition au format excel
#sousNutrition.to_excel('sous_nutrition.xlsx', index=False)

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

#afficher le tableau pour les années 2015 à 2017
#print(sousNutrition[(sousNutrition['Année'] >= 2015) & (sousNutrition['Année'] <= 2017)])

#sousNutrition.to_excel('sous_nutrition1.xlsx', index=False)


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

#********************************************************************************************************************
# FOCUS SUR MANQUE DE DONNEES DE SOUS-NUTRITION
#********************************************************************************************************************
# Afficher la somme de Population dont sous_nutrition = 0
# print('Nombre de personnes dont nous n"avons pas de données de sous-nutrition :')
# print(resultats_2017[resultats_2017['sous_nutrition'] == 0]['Population'].sum())

# Nombre de personnes total du fichier
# print('Nombre total de personnes :')
# print(resultats_2017['Population'].sum())

# Calculer la proportion de la population ayant une sous-nutrition égale à zéro
proportion_sous_nutrition_0 = (resultats_2017[resultats_2017['sous_nutrition'] == 0]['Population'].sum() / resultats_2017['Population'].sum()) * 100
#print("Proportion de la population sans données de sous-nutrition: {:.2f}%".format(proportion_sous_nutrition_0))

# liste des pays sans données de sous-nutrition
# print('Pays sans données de sous-nutrition :')
# print(resultats_2017[resultats_2017['sous_nutrition'] == 0]['Zone'])

# les 118 pays sans données ou valeur nulle de sous nutrition sont des pays riches ou des pays en guerre
# Ils me semblent important de les conserver pour ne pas fausser les résultats
# les exclures revient à exclure presque la moitié de la population mondiale, sachant que dans cette liste
# il y a un bon nombre qui ne sont pas en sous-nutrition

#********************************************************************************************************************


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
#print("Le nombre total d'humains pouvant être nourris avec les produits végétaux est d'environ : {:.2f} milliards d'humains".format(nombre_total_humains_nourris_vegetaux / 1e9))

#3_4 Utilisation de la disponibilité intérieure

#Calculer la disponibilité intérieure mondiale en tonnes
dispo_int = dispoAlimentaire['Disponibilité intérieure'].sum()
#print("La disponibilité intérieure mondiale est de : {:.2f} kilos".format(dispo_int))

#Afficher les différentes valeurs en fonction des colonnes aliments pour animaux, pertes et nourritures grâce à une boucle
colonnes = ['Aliments pour animaux', 'Pertes', 'Nourriture']
for colonne in colonnes:
    dispo_int_colonne = dispoAlimentaire[colonne].sum()
    #print("La disponibilité intérieure mondiale en {} est de : {:.2f} kilos".format(colonne, dispo_int_colonne))

#faire un graphique pour visualiser la disponibilité intérieure mondiale
# Créer un dictionnaire pour stocker les valeurs
# dispo_int_dict = {'Aliments pour animaux': dispoAlimentaire['Aliments pour animaux'].sum(),
#                   'Pertes': dispoAlimentaire['Pertes'].sum(),
#                   'Nourriture': dispoAlimentaire['Nourriture'].sum()}
# Convertir le dictionnaire en DataFrame
# dispo_int_df = pd.DataFrame(list(dispo_int_dict.items()), columns=['Produit', 'Disponibilité intérieure'])

# Créer un graphique camenbert  pour visualiser la disponibilité intérieure mondiale (couleur bleu pour nourriture, rouge pour pertes et vert pour aliments pour animaux)
# dispo_int_df.plot.pie(y='Disponibilité intérieure', labels=dispo_int_df['Produit'], autopct='%1.1f%%', colors=['green', 'red', 'turquoise'], legend=False)
# plt.pyplot.title('Disponibilité intérieure mondiale')
# plt.pyplot.axis('equal')  # Pour que le camembert soit un cercle
# plt.pyplot.show()


# Calculer la disponibilité alimentaire de Autres Utilisations en kg
dispoAutresUtilisations = dispoAlimentaire['Autres Utilisations'].sum()
#print("La disponibilité alimentaire de Autres Utilisations est de : {:.2f} kilos".format(dispoAutresUtilisations))

#Afficher les différentes valeurs en fonction des colonnes aliments pour animaux, pertes, Autres Utilisations et nourritures grâce à une boucle
colonnes = ['Aliments pour animaux', 'Pertes', 'Autres Utilisations', 'Nourriture']
for colonne in colonnes:
    dispo_int_colonne = dispoAlimentaire[colonne].sum()
    #print("La disponibilité intérieure mondiale en {} est de : {:.2f} kilos".format(colonne, dispo_int_colonne))

#faire un graphique pour visualiser la disponibilité intérieure mondiale
# Créer un dictionnaire pour stocker les valeurs
# dispo_int_dict = {'Aliments pour animaux': dispoAlimentaire['Aliments pour animaux'].sum(),
#                    'Pertes': dispoAlimentaire['Pertes'].sum(),
#                    'Nourriture': dispoAlimentaire['Nourriture'].sum(),
#                    'Autres Utilisations': dispoAlimentaire['Autres Utilisations'].sum()}
# Convertir le dictionnaire en DataFrame
# dispo_int_df = pd.DataFrame(list(dispo_int_dict.items()), columns=['Produit', 'Disponibilité intérieure'])

# Créer un graphique camenbert  pour visualiser la disponibilité intérieure mondiale (couleur bleu pour nourriture, rouge pour pertes et vert pour aliments pour animaux)
# dispo_int_df.plot.pie(y='Disponibilité intérieure', labels=dispo_int_df['Produit'], autopct='%1.1f%%', colors=['green', 'red', 'turquoise', 'grey'], legend=False)
# plt.pyplot.title('Disponibilité intérieure mondiale')
# plt.pyplot.axis('equal')  # Pour que le camembert soit un cercle
# plt.pyplot.show()

#3_5 Utilisation des céréales
#Création d'une liste avec toutes les variables du fichier DispoAlimentaire
# Création d'une liste avec toutes les variables du fichier DispoAlimentaire
variables = ['Autres Utilisations', 
             'Aliments pour animaux',
             'Nourriture', 
             'Pertes', 
             'Semences', 
             'Traitement',
             'Exportations - Quantité',
             'Importations - Quantité',
             'Production',
             'Variation de stock',
             'Disponibilité intérieure'
             ]

# Création d'un dataframe qui filtre sur toutes les céréales
cereales = dispoAlimentaire[dispoAlimentaire['Produit'].isin(['Blé', 'Riz (Eq Blanchi)', 'Orge', 'Maïs', 'Millet', 'Seigle', 'Avoine', 'Sorgho', 'Céréales, Autres'])]
quantite_totale_cereales_animaux = cereales['Aliments pour animaux'].sum()
#print("La quantité totale de céréales utilisée pour les animaux est de : {:.2f} kilos".format(quantite_totale_cereales_animaux))

quantite_totale_dispo_int = cereales['Disponibilité intérieure'].sum()
#print("La quantité totale de céréales pour la disponibilité intérieure est de : {:.2f} kilos".format(quantite_totale_dispo_int))

# Calculer la proportion totale de 'Aliments pour animaux' par rapport à la disponibilité intérieure totale
proportion_aliments_animaux = quantite_totale_cereales_animaux/ quantite_totale_dispo_int * 100
#print("La proportion totale d'Aliments pour animaux par rapport à la disponibilité intérieure totale est de : {:.2f}%".format(proportion_aliments_animaux))

#calculer la quantité totale de céréales utilisée pour la nourriture
quantite_totale_nourriture = cereales['Nourriture'].sum()
#print("La quantité totale de céréales utilisée pour la nourriture est de : {:.2f} kilos".format(quantite_totale_nourriture))


# Calculer la proportion totale de 'Nourriture' par rapport à la disponibilité intérieure totale
proportion_nourriture = cereales['Nourriture'].sum() / cereales['Disponibilité intérieure'].sum() * 100
#print("La proportion totale de Nourriture par rapport à la disponibilité intérieure totale est de : {:.2f}%".format(proportion_nourriture))

# Calculer la proportion totale par variable par rapport à la disponibilité intérieure totale
proportions = cereales[variables].sum() / cereales['Disponibilité intérieure'].sum() * 100
proportions = proportions.round(0)
#print(proportions)
#print("La différence entre les importation et les exportation + la variation de stock  annule le surplus de production de céréales")

#3.6 Pays avec la proportion de personnes sous-alimentées la plus élevée en 2017

#resultats_2017.to_excel('popSousNutJoint.xlsx', index=False)
#trouver le type de données de chaque colonne du dataFrame resultats_2017
#print(resultats_2017.dtypes)

#modifier le type de données proportion_sous_nutrition en float
resultats_2017['proportion_sous_nutrition'] = resultats_2017['proportion_sous_nutrition'].str.replace('%', '').astype(float)

# Trier le DataFrame par proportion_sous_nutrition de manière décroissante
resultats_tries = resultats_2017.sort_values(by='proportion_sous_nutrition', ascending=False)

# Afficher les 10 premières lignes du DataFrame trié
#print(resultats_tries[['Zone', 'proportion_sous_nutrition']].head(10))

#aideAlimentaire.to_excel('AideAlimentaire.xlsx', index=False)
#print(aideAlimentaire.dtypes)
resultats_tries.to_excel('resultats_tries.xlsx', index=False)

#3.7 Pays qui ont le plus bénéficié d'aide alimentaire depuis 2013
#total_general_aide = aideAlimentaire['Valeur'].sum()

#print (aideAlimentaire.head())

#création d'une table pivot pour avoir le montant total de l'aide alimentaire par pays et par année sur une ligne
pivot_aideAlimentaire = aideAlimentaire.pivot_table(index='Zone', columns='Année', values='Valeur', aggfunc='sum', fill_value=0)
pivot_aideAlimentaire['Valeur Totale'] = pivot_aideAlimentaire.sum(axis=1)

pivot_aideAlimentaire.reset_index(inplace=True)
# print('LA TABLE PIVOT : ')
# print (pivot_aideAlimentaire.head())

# Tri décroissant par la colonne 'Valeur Totale'
pivot_aideAlimentaire_sorted = pivot_aideAlimentaire.sort_values(by='Valeur Totale', ascending=False)

#print('TABLE PIVOT TRIÉE PAR VALEUR TOTALE : ')
#print(pivot_aideAlimentaire_sorted.head())

top_10 = pivot_aideAlimentaire_sorted.head(10)
#print('Les 10 premiers pays selon la valeur totale de l\'aide alimentaire :')
#print(top_10)


#3.8 Evolution du top 5 des pays les plus aidés entre 2013 et 2016

#calcul des 5 pays qui ont reçu le plus d'aide alimentaire entre 2013 et 2016
top_5 = pivot_aideAlimentaire_sorted.head(5)
#print('Les 5 premiers pays selon la valeur totale de l\'aide alimentaire :')
#print(top_5)

# aideAlimentaire['Taux Croissance'] = aideAlimentaire['Valeur'].pct_change() * 100
# #print(aideAlimentaire.head())


#3.9 Liste des pays qui ont la plus faible disponibilité alimentaire par habitant
# Calculer la somme totale de Disponibilité alimentaire en quantité par pays
dispo_total_par_pays = dispoAlimentaire.groupby('Zone')['Disponibilité alimentaire (Kcal/personne/jour)'].sum().reset_index()

# Trier les pays par ordre croissant selon leur Disponibilité alimentaire en quantité
pays_dispo_faible = dispo_total_par_pays.sort_values(by='Disponibilité alimentaire (Kcal/personne/jour)')
print("Les 10 pays avec la disponibilité alimentaire la plus faible sont :")
print(pays_dispo_faible.head(10))
print('la somme totale de la disponibilité alimentaire en kcal/personne/jour est de : ', dispo_total_par_pays['Disponibilité alimentaire (Kcal/personne/jour)'].sum())


#3.10 Liste des pays qui ont le plus de disponibilité alimentaire par habitant

# Trier les pays par ordre décroissant selon la Disponibilité alimentaire en quantité
pays_dispo_elevee = dispo_total_par_pays.sort_values(by='Disponibilité alimentaire (Kcal/personne/jour)', ascending=False)

# Afficher les 10 premiers pays ayant la Disponibilité alimentaire en quantité la plus haute
print("Les 10 pays ayant la Disponibilité alimentaire en quantité la plus haute sont :")
print(pays_dispo_elevee.head(10))


#3.11 Etude sur la Thaïlande

#création d'un dataframe avec uniquement la Thaïlande 
# Filtrer les résultats pour ne conserver que les lignes avec l'année 2017 et la Thaïlande
resultats_thailande_2017 = resultats_2017[resultats_2017['Zone'] == 'Thaïlande']


# Calculer le nombre de personnes en état de sous-nutrition en Thaïlande en 2017
sous_nutrition_thailande_2017 = resultats_thailande_2017['sous_nutrition'].sum()


# Calculer le nombre de personnes dans la population en Thaïlande en 2017
population_thailande_2017 = population[(population['Zone'] == 'Thaïlande') & (population['Année'] == 2017)]['Population'].values[0]


# Calculer le pourcentage de sous-nutrition en Thaïlande en 2017
pourcentage_sous_nutrition_thailande = (sous_nutrition_thailande_2017 / population_thailande_2017) * 100


# Calculer la quanité de Manioc Thaïlandais qui est exporté
# Filtrer les données pour ne conserver que celles concernant le Manioc en Thaïlande
manioc_thailande_data = dispoAlimentaire[(dispoAlimentaire['Zone'] == 'Thaïlande') & (dispoAlimentaire['Produit'] == 'Manioc')]

# Calculer la quantité de Manioc Thaïlandais exporté
exportations_manioc_thailande = manioc_thailande_data['Exportations - Quantité'].sum()

#Calculer la production de Manioc en Thaïlande
production_manioc_thailande = manioc_thailande_data['Production'].sum()


# Calculer la proportion d'exportations par rapport à la production
proportion_export_production = exportations_manioc_thailande / production_manioc_thailande

#print(f"Proportion d'exportations par rapport à la production : {proportion_export_production:.2%}")

#Quelle est la disponibilité alimentaire en manioc pour la Thaïlande
# Filtrer les données pour ne conserver que celles concernant la Thaïlande et le manioc
dispo_manioc_thailande = dispoAlimentaire[(dispoAlimentaire['Zone'] == 'Thaïlande') & (dispoAlimentaire['Produit'] == 'Manioc')]
# Calculer la disponibilité par personne de manioc en Thaïlande (kg)
dispo_totale_manioc_thailande = dispo_manioc_thailande['Disponibilité alimentaire en quantité (kg/personne/an)'].sum()
#print(f"La disponibilité alimentaire en manioc (kg/personne/an) en Thaïlande est de : {dispo_totale_manioc_thailande:.2f} kg")

