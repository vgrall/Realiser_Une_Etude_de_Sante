import nbformat as nbf

# Ouvrir le fichier notebook existant
with open('Template+Julien+(1).ipynb', 'r') as f:
    nb = nbf.read(f, as_version=4)

# Parcourir les cellules du notebook
for cell in nb.cells:
    # Si la cellule est une cellule de code et qu'elle contient un marqueur spécifique, la modifier
    if cell.cell_type == 'code' and 'remplacer_ici' in cell.source:
        # Modifier le contenu de la cellule
        cell.source = cell.source.replace('remplacer_ici', 'nouveau_contenu')

# Sauvegarder les modifications dans le même fichier
with open('template.ipynb', 'w') as f:
    nbf.write(nb, f)
