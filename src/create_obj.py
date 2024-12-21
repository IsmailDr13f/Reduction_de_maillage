def create_obj_file(vertices, faces, filename="output.obj"):
    with open(filename, 'w') as f:
        # Écriture des sommets
        for vertex in vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

        # Écriture des faces
        for face in faces:
            # Les indices dans les faces sont 1-based, donc on ajoute 1 à chaque index
            f.write(f"f {' '.join(str(index) for index in face)}\n")

    print(f"Fichier {filename} créé avec succès.")


