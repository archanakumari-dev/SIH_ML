# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity

# def get_novel_species_for_display(df, cluster_labels, X, habitat_col=None):
#     novel_indices = np.where(cluster_labels == -1)[0]
#     known_indices = np.where(cluster_labels != -1)[0]
#     known_vectors = X[known_indices]
#     novel_vectors = X[novel_indices]
#     if len(known_indices) > 0 and len(novel_indices) > 0:
#         sim_matrix = cosine_similarity(novel_vectors, known_vectors)
#         similarity_scores = sim_matrix.max(axis=1) * 100
#     else:
#         similarity_scores = np.zeros(len(novel_indices))
#     confidence_scores = (100 - similarity_scores).clip(80, 99)
#     cards = []
#     for i, idx in enumerate(novel_indices):
#         cards.append({
#             "id": f"NS{str(idx+1).zfill(3)}",
#             "sequence": df['sequence'].iloc[idx],
#             "confidence": int(confidence_scores[i]),
#             "similarity": int(similarity_scores[i]),
#             "closest_known_idx": known_indices[np.argmax(sim_matrix[i])] if len(known_indices) else None,
#             "closest_known_seq": df['sequence'].iloc[known_indices[np.argmax(sim_matrix[i])]] if len(known_indices) else None
#         })
#     return cards

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_novel_species_for_display(df, cluster_labels, X):
    """
    Identifies novel taxa (cluster -1) and finds their closest match
    among the known taxa, including the species name.
    """
    novel_indices = np.where(cluster_labels == -1)[0]
    known_indices = np.where(cluster_labels != -1)[0]
    
    cards = []
    
    if len(novel_indices) == 0:
        return cards
        
    if len(known_indices) == 0:
        # Handle case where there are no known taxa to compare against
        for idx in novel_indices:
            cards.append({
                "id": f"NS{str(idx+1).zfill(3)}",
                "sequence": df['sequence'].iloc[idx],
                "confidence": 100, # Max confidence since no comparison
                "similarity": 0,
                "closest_known_species": "N/A (No known taxa in batch)",
            })
        return cards

    known_vectors = X[known_indices]
    novel_vectors = X[novel_indices]
    
    # Calculate cosine similarity between all novel vectors and all known vectors
    sim_matrix = cosine_similarity(novel_vectors, known_vectors)
    
    # Get the max similarity score for each novel vector
    similarity_scores = sim_matrix.max(axis=1) * 100
    
    # Get the index (within the known_vectors subset) of the closest match
    closest_known_vector_indices = np.argmax(sim_matrix, axis=1)
    
    # Calculate confidence based on similarity
    confidence_scores = (100 - similarity_scores).clip(80, 99) # Clip for display range
    
    for i, idx in enumerate(novel_indices):
        
        # 1. Get the global index (in the original DataFrame) of the closest match
        global_closest_idx = known_indices[closest_known_vector_indices[i]]
        
        # 2. Retrieve the species name using the global index
        closest_species = df['species'].iloc[global_closest_idx]
        
        cards.append({
            "id": f"NS{str(idx+1).zfill(3)}",
            "sequence": df['sequence'].iloc[idx],
            "confidence": int(confidence_scores[i]),
            "similarity": int(similarity_scores[i]),
            # --- NEW OUTPUT FIELD ---
            "closest_known_species": closest_species, 
            # --- END NEW OUTPUT FIELD ---
            "closest_known_idx": global_closest_idx, # Keeping for debugging/completeness
            "closest_known_seq": df['sequence'].iloc[global_closest_idx]
        })
        
    return cards