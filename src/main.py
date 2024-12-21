import os
from read_obj import parse_obj
from create_obj import create_obj_file
from vertex_clust import VertexClustering
from edge_collapse import EdgeCollapse

# Liste des fichiers à traiter
obj_files = [
    r"C:\Users\drief\Desktop\opengl_test\DVI2\obj1.obj",
    r"C:\Users\drief\Desktop\opengl_test\DVI2\obj2.obj",
    r"C:\Users\drief\Desktop\opengl_test\DVI2\obj3.obj",
    r"C:\Users\drief\Desktop\opengl_test\DVI2\obj4.obj",
    r"C:\Users\drief\Desktop\opengl_test\DVI2\obj5.obj"
]

cell_size = 0.01  # Taille de la cellule pour le clustering
output_dir1 = r"C:\Users\drief\Desktop\opengl_test\DVI2\output_VC"  # Dossier de sortie pour les fichiers modifiés
output_dir2 = r"C:\Users\drief\Desktop\opengl_test\DVI2\output_EC"
# Vérifier si le dossier de sortie existe, sinon le créer
os.makedirs(output_dir1, exist_ok=True)
os.makedirs(output_dir2, exist_ok=True)

# Fonction pour appliquer les deux algorithmes et sauvegarder le résultat
def process_obj_file(file_path, output_dir,methode=1):
    # Lire les données du fichier .obj
    obj_data = parse_obj(file_path)
    print(f"Traitement de {file_path}")

    # Récupérer les clés disponibles dans obj_data pour chaque groupe
    for group_name in obj_data.keys():
        print(f"Traitement du groupe : {group_name}")

        # Accéder aux vertices et faces du groupe
        vertices = obj_data[group_name]['v']
        faces = obj_data[group_name]['f']

        if methode==1:
            # Initialiser le clustering des vertices
            vc = VertexClustering(vertices, faces, cell_size)
            weights = vc.grade_vertices()
            vc.cluster_vertices(weights)
            new_vertices, new_faces = vc.simplify()
        elif methode==2:
            # Initialiser l'algorithme de simplification par Edge Collapse
            edge_collapse = EdgeCollapse(vertices, faces)
            new_vertices, new_faces = edge_collapse.collapse_mesh(2)

        else:
            print("you should choose 1 for vertices clustering or 2 for edge collapse")

        # Créer un fichier .obj de sortie avec les nouveaux sommets et faces
        output_file_path = os.path.join(output_dir, f"{group_name}_{os.path.basename(file_path)}")
        create_obj_file(new_vertices, new_faces, output_file_path)
        print(f"Fichier sauvegardé : {output_file_path}")


# Traiter tous les fichiers .obj
for file_path in obj_files:
    process_obj_file(file_path, output_dir1,1)
    process_obj_file(file_path, output_dir2, 2)

