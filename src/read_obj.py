

def parse_obj(file_path):
    obj_data = {}

    current_group = None
    current_material = None
    vertices = []
    texture_coords = []
    normals = []
    faces = []
    points = []
    lines = []

    # Ouvrir et lire le fichier .obj
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Enlever les espaces inutiles

            if line.startswith('#'):  # Ignorer les commentaires
                continue

            # Gérer les groupes (g) et matériaux (usemtl)
            if line.startswith('g '):
                current_group = line.split()[1]  # Extraire le nom du groupe
                obj_data[current_group] = {'v': [], 'vt': [], 'vn': [], 'f': [], 'p': [], 'l': [], 'usemtl': None}

            elif line.startswith('usemtl '):
                current_material = line.split()[1]  # Extraire le nom du matériau
                if current_group:
                    obj_data[current_group]['usemtl'] = current_material

            # Gérer les sommets (v)
            elif line.startswith('v '):
                coords = tuple(map(float, line.split()[1:]))  # Convertir en tuple de flottants
                vertices.append(coords)

                if current_group:
                    obj_data[current_group]['v'].append(coords)

            # Gérer les coordonnées de texture (vt)
            elif line.startswith('vt '):
                coords = tuple(map(float, line.split()[1:]))  # Convertir en tuple de flottants
                texture_coords.append(coords)

                if current_group:
                    obj_data[current_group]['vt'].append(coords)

            # Gérer les normales (vn)
            elif line.startswith('vn '):
                coords = tuple(map(float, line.split()[1:]))  # Convertir en tuple de flottants
                normals.append(coords)

                if current_group:
                    obj_data[current_group]['vn'].append(coords)

            # Gérer les points (p)
            elif line.startswith('p '):
                point = list(map(int, line.split()[1:]))  # Convertir en liste d'entiers
                points.append(point)

                if current_group:
                    obj_data[current_group]['p'].append(point)

            # Gérer les lignes (l)
            elif line.startswith('l '):
                line_data = list(map(int, line.split()[1:]))  # Convertir en liste d'entiers
                lines.append(line_data)

                if current_group:
                    obj_data[current_group]['l'].append(line_data)

            # Gérer les faces (f)
            elif line.startswith('f '):
                face = []
                elements = line.split()[1:]

                for element in elements:
                    vertex_data = element.split('/')  # Séparer les indices de sommet, texture et normal
                    vertex_index = int(vertex_data[0]) if vertex_data[0] else None
                    texture_index = int(vertex_data[1]) if len(vertex_data) > 1 and vertex_data[1] else None
                    normal_index = int(vertex_data[2]) if len(vertex_data) > 2 and vertex_data[2] else None
                    face.append((vertex_index, texture_index, normal_index))

                faces.append(face)

                if current_group:
                    obj_data[current_group]['f'].append(face)

    return obj_data


# Exemple d'utilisation
#file_path = r"C:\Users\drief\Desktop\opengl_test\DVI2\obj6.obj"
"""obj_data = parse_obj(file_path)

# Afficher le dictionnaire
print(obj_data.keys())
print(obj_data['group']['v'])"""

