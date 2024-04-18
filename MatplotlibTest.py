#faire un graphique pour visualiser la disponibilité intérieure mondiale
# Créer un dictionnaire pour stocker les valeurs
# dispo_int_dict = {'Autres Utilisations': cereales['Autres Utilisations'].sum(),
#                   'Aliments pour animaux': cereales['Aliments pour animaux'].sum(),
#                   'Nourriture': cereales['Nourriture'].sum(),
#                   'Pertes': cereales['Pertes'].sum(),
#                   'Semences': cereales['Semences'].sum(),
#                   'Traitement': cereales['Traitement'].sum()}
# Convertir le dictionnaire en DataFrame
# dispo_int_df = pd.DataFrame(list(dispo_int_dict.items()), columns=['Produit', 'Disponibilité intérieure'])

# Créer un graphique camenbert  pour visualiser la disponibilité intérieure mondiale des céréales (couleur bleu pour nourriture, rouge pour pertes et vert pour aliments pour animaux)
# dispo_int_df.plot.pie(y='Disponibilité intérieure', labels=dispo_int_df['Produit'], autopct='%1.1f%%', colors=['green', 'red', 'turquoise', 'grey', 'purple', 'orange'], legend=False)
# plt.pyplot.title('Disponibilité intérieure mondiale des céréales')
# plt.pyplot.axis('equal')  # Pour que le camembert soit un cercle
#plt.pyplot.show()