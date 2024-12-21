import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

class VertexClustering:
    def __init__(self, vertices, faces, cell_size):
        self.vertices = np.array(vertices)  # Liste des sommets (coordonnées)
        self.faces = self._extract_face_indices(faces)  # Extraction des indices des sommets
        self.cell_size = cell_size
        self.clusters = {}

    def _extract_face_indices(self, faces):
        """Extrait uniquement les indices des sommets à partir des faces."""
        indices = []
        for face in faces:
            face_indices = [vertex[0] - 1 for vertex in face]
            for idx in face_indices:
                if idx < 0 or idx >= len(self.vertices):
                    raise ValueError(f"Indice hors limites : {idx + 1} pour les sommets donnés.")
            indices.append(face_indices)
        return indices

    def grade_vertices(self):
        """Attribue un poids à chaque sommet basé sur sa probabilité d'appartenir aux silhouettes."""
        weights = []
        for idx, vertex in enumerate(self.vertices):
            incident_edges = self._find_incident_edges(idx)  # Utilise l'indice
            max_angle = self._max_angle_between_edges(incident_edges)
            weights.append(np.cos(max_angle / 2))
        return np.array(weights)

    def _find_incident_edges(self, vertex_idx):
        """Trouve les arêtes incidentes à un sommet donné via son indice."""
        return [face for face in self.faces if vertex_idx in face]

    def _max_angle_between_edges(self, edges):
        """Calcule l'angle maximum entre des arêtes incidentes."""
        vectors = []
        for edge in edges:
            for i in range(len(edge)):
                v1_idx = edge[i]
                v2_idx = edge[(i + 1) % len(edge)]
                vector = self.vertices[v2_idx] - self.vertices[v1_idx]
                vectors.append(vector)

        angles = [
            np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1, 1))
            for i, v1 in enumerate(vectors) for j, v2 in enumerate(vectors) if i != j
        ]
        return max(angles, default=0)

    def cluster_vertices(self, weights):
        """Regroupe les sommets dans des clusters en fonction de leur poids et de leur position."""
        sorted_indices = np.argsort(-weights)  # Tri décroissant des poids
        visited = set()

        for idx in sorted_indices:
            if idx in visited:
                continue
            cluster = self._create_cluster(idx, visited)
            representative = self._compute_representative(cluster)
            self.clusters[idx] = representative

    def _create_cluster(self, idx, visited):
        """Crée un cluster à partir d'un sommet donné."""
        cluster = []
        queue = [idx]
        while queue:
            current = queue.pop()
            if current in visited:
                continue
            visited.add(current)
            cluster.append(current)
            neighbors = self._find_neighbors(current)
            queue.extend([n for n in neighbors if n not in visited])
        return cluster

    def _compute_representative(self, cluster):
        """Calcule le sommet représentatif d'un cluster."""
        # Utilisation du PCA pour obtenir un représentant plus stable
        cluster_vertices = self.vertices[cluster]
        pca = PCA(n_components=1)  # Réduction à une dimension pour trouver un représentant
        pca.fit(cluster_vertices)
        center = pca.components_[0]  # Direction principale
        return np.mean(cluster_vertices, axis=0)  # Barycentre ou autre méthode si nécessaire

    def _find_neighbors(self, vertex_idx):
        """Trouve les voisins géométriques d'un sommet."""
        vertex = self.vertices[vertex_idx]
        distances = np.linalg.norm(self.vertices - vertex, axis=1)
        return np.where(distances < self.cell_size)[0]

    def simplify(self):
        """Simplifie le modèle en remplaçant les sommets par leurs représentants."""
        new_vertices = []
        vertex_mapping = {}

        for cluster_idx, rep in self.clusters.items():
            vertex_mapping[cluster_idx] = len(new_vertices)
            new_vertices.append(rep)

        new_faces = []
        for face in self.faces:
            new_face = [vertex_mapping.get(v, v) for v in face]
            if len(set(new_face)) == 3:  # Vérifie que la face reste valide après simplification
                new_faces.append(new_face)

        return np.array(new_vertices), np.array(new_faces)
