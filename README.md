# Réduction de Maillage

Ce projet implémente deux algorithmes de réduction de maillage, **Vertex Clustering** et **Edge Collapse**, appliqués à des fichiers 3D au format `.obj`. L'objectif est de réduire la complexité des modèles tout en préservant leur structure essentielle.
## Réalisé par : DRIEF ISMAIL
## Structure du Projet

### 1. Dossier `DVI2`
Ce dossier contient les ressources et résultats :
- **Fichiers `.obj`** : Modèles 3D à réduire.
- **Dossiers de résultats** :
  - `output_VC` : Contient les modèles obtenus après application de l'algorithme **Vertex Clustering**.
  - `output_EC` : Contient les modèles obtenus après application de l'algorithme **Edge Collapse**.

### 2. Dossier `src`
Le dossier `src` contient les scripts Python pour l’implémentation et l’exécution des algorithmes :

- **`create_obj.py`** : Gènère des fichiers `.obj`.
- **`edge_collapse.py`** : Implémente l’algorithme **Edge Collapse**.
- **`main.py`** : Exécute les algorithmes de réduction de maillage sur les fichiers `.obj`.
- **`read_obj.py`** : Lit et parse les fichiers `.obj`.
- **`vertex_clust.py`** : Implémente l’algorithme **Vertex Clustering**.

### 3. Fichier Word
**`Résultats de réduction de maillage avec Vertex Clustering et Edge Collapse.docx`** : Document contenant une visualisation des résultats obtenus pour chaque fichier `.obj` avec les deux algorithmes. Les visualisations sont effectuées via le site [ImageToSTL](https://imagetostl.com).

## Prérequis

- **Python 3.9** : Veillez à utiliser cette version pour éviter les problèmes de compatibilité.
- Modules Python nécessaires :
  - `numpy`
  - `os`

Vous pouvez installer les dépendances avec la commande suivante :
```bash
pip install numpy
```

## Utilisation

1. **Organisation des fichiers** :
   Placez les fichiers `.obj` dans le dossier `DVI2`.

2. **Exécution des algorithmes** :
   Lancez le fichier `main.py` pour appliquer les algorithmes Vertex Clustering et Edge Collapse sur les fichiers `.obj`.
   ```bash
   python src/main.py
   ```

3. **Résultats** :
   Les fichiers réduits sont sauvegardés dans les dossiers `output_VC` et `output_EC`.

4. **Visualisation** :
   Utilisez le site [ImageToSTL](https://imagetostl.com) pour observer les transformations.

## Algorithmes Implémentés

### Vertex Clustering
Cet algorithme réduit le nombre de sommets en regroupant ceux qui appartiennent à une même cellule d’une grille.

### Edge Collapse
Cet algorithme réduit le nombre d’arêtes en fusionnant deux sommets connectés par une arête, simplifiant ainsi le maillage.

## Organisation des Résultats

- **Input** : Modèles `.obj` originaux situés dans `DVI2`.
- **Output** :
  - Résultats du Vertex Clustering dans `output_VC`.
  - Résultats de l'Edge Collapse dans `output_EC`.
- **Analyse des résultats** : Document Word contenant les différentes visualisations des modèles avant et après réduction.

![image](https://github.com/user-attachments/assets/8e8b11df-5840-4ce2-a42e-60a2e5667cb1)

## Réalisé par : DRIEF ISMAIL

