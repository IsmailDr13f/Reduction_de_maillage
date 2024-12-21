import numpy as np
from collections import defaultdict


class EdgeCollapse:
    def __init__(self, vertices, faces):
        self.vertices = np.array(vertices)  # Liste des sommets
        self.faces = self._extract_face_indices(faces)  # Liste des faces (indices des sommets)
        self.vertex_count = len(vertices)
        self.face_count = len(faces)

    def _extract_face_indices(self, faces):
        """Extrait les indices des sommets à partir des faces sous format (sommet, [texture, normale])."""
        indices = []
        for face in faces:
            face_indices = []
            for vertex in face:
                # Si le format de vertex est une chaîne (par exemple '2/5/3')
                if isinstance(vertex, str):
                    vertex_parts = vertex.split('/')  # Découpe la face par '/'
                elif isinstance(vertex, tuple):  # Si c'est déjà un tuple, on l'utilise directement
                    vertex_parts = vertex
                else:
                    raise ValueError(f"Format de vertex invalide : {vertex}")

                # Extraire l'indice du sommet et vérifier les autres informations
                if len(vertex_parts) == 3:  # Format f vertex/texture/normal
                    vertex_idx = int(vertex_parts[0]) - 1  # Indice du sommet (0-indexé)
                elif len(vertex_parts) == 1:  # Format f vertex (seulement sommet)
                    vertex_idx = int(vertex_parts[0]) - 1  # Indice du sommet (0-indexé)
                elif len(vertex_parts) == 2:  # Format f vertex//normal (sans texture)
                    vertex_idx = int(vertex_parts[0]) - 1  # Indice du sommet (0-indexé)
                else:
                    raise ValueError(f"Format de face invalide : {vertex_parts}")

                face_indices.append(vertex_idx)
            indices.append(face_indices)
        return indices

    def find_edge_cost(self, v1, v2):
        """Calcule le coût d'effondrement de l'arête (v1, v2) basé sur la longueur de l'arête."""
        return np.linalg.norm(self.vertices[v1] - self.vertices[v2])

    def collapse_edge(self, v1, v2):
        """Effondre l'arête entre les sommets v1 et v2."""
        # Fusionne les deux sommets en un seul, à la moyenne des positions
        new_vertex = (self.vertices[v1] + self.vertices[v2]) / 2
        new_vertex_idx = self.vertex_count
        self.vertices = np.vstack([self.vertices, new_vertex])

        # Met à jour les faces
        new_faces = []
        for face in self.faces:
            new_face = []
            for vertex in face:
                if vertex == v1 or vertex == v2:
                    new_face.append(new_vertex_idx)  # Remplace v1 et v2 par le nouveau sommet
                else:
                    new_face.append(vertex)
            if len(set(new_face)) == 3:  # Vérifie que la face est valide (triangulaire)
                new_faces.append(new_face)

        self.faces = new_faces
        self.vertex_count += 1  # Incrémente le nombre de sommets
        self.face_count = len(new_faces)

    def collapse_mesh(self, num_collapses):
        """Effectue une série de collapses sur le maillage."""
        for _ in range(num_collapses):
            # Sélectionner l'arête avec le coût le plus faible
            min_cost = float('inf')
            edge_to_collapse = None

            for face in self.faces:
                for i in range(3):
                    v1, v2 = face[i], face[(i + 1) % 3]  # Crée les arêtes de la face
                    cost = self.find_edge_cost(v1, v2)
                    if cost < min_cost:
                        min_cost = cost
                        edge_to_collapse = (v1, v2)

            if edge_to_collapse:
                self.collapse_edge(*edge_to_collapse)

        return self.vertices, self.faces
