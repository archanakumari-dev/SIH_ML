import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_novel_species_for_display(df, cluster_labels, X, habitat_col=None):
    novel_indices = np.where(cluster_labels == -1)[0]
    known_indices = np.where(cluster_labels != -1)[0]
    known_vectors = X[known_indices]
    novel_vectors = X[novel_indices]
    if len(known_indices) > 0 and len(novel_indices) > 0:
        sim_matrix = cosine_similarity(novel_vectors, known_vectors)
        similarity_scores = sim_matrix.max(axis=1) * 100
    else:
        similarity_scores = np.zeros(len(novel_indices))
    confidence_scores = (100 - similarity_scores).clip(80, 99)
    cards = []
    for i, idx in enumerate(novel_indices):
        cards.append({
            "id": f"NS{str(idx+1).zfill(3)}",
            "sequence": df['sequence'].iloc[idx],
            "confidence": int(confidence_scores[i]),
            "similarity": int(similarity_scores[i]),
            "closest_known_idx": known_indices[np.argmax(sim_matrix[i])] if len(known_indices) else None,
            "closest_known_seq": df['sequence'].iloc[known_indices[np.argmax(sim_matrix[i])]] if len(known_indices) else None
        })
    return cards
