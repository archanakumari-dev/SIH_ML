import pandas as pd
import time
import json
import numpy as np

# Import core components from your existing files
from data_processing import load_data
from feature_extraction import create_tfidf_embeddings # Use k_size=6
from clustering import run_dbscan
from metrices import get_novel_species_for_display # Already modified to include closest species

def generate_full_model_json(filepath='updated_plasmids.csv'):
    """
    Runs the entire eDNA analysis pipeline and formats the results into a single JSON object.
    """
    start_pipeline_time = time.time()
    
    # 1. Load Data
    try:
        df = load_data(filepath)
    except FileNotFoundError:
        return {"error": "File not found.", "status": "failed"}

    sequences = df['sequence'].tolist()
    
    # 2. Feature Extraction (TF-IDF)
    try:
        X = create_tfidf_embeddings(sequences, k_size=6)
    except Exception as e:
        return {"error": f"TF-IDF feature generation failed: {e}", "status": "failed"}

    # 3. Clustering (DBSCAN)
    cluster_labels = run_dbscan(X)
    df['cluster'] = cluster_labels
    
    # 4. Novel Taxa Metrics (Populates novel_taxa_cards list)
    # The metrices function is perfect for generating the novel_taxa_cards list.
    novel_taxa_cards = get_novel_species_for_display(df.copy(), cluster_labels, X)
    
    # 5. Known Clusters Summary (Generate known_clusters_summary list)
    known_clusters_summary = []
    known_clusters = df[df['cluster'] != -1]
    
    for cluster_id, group in known_clusters.groupby('cluster'):
        if cluster_id >= 0: # Ensure we only process non-novel clusters
            # Find the most frequent species in the cluster
            dominant_species = group['species'].mode().iloc[0] if not group['species'].mode().empty else "Unknown"
            
            known_clusters_summary.append({
                "cluster_id": int(cluster_id),
                "count": len(group),
                "dominant_species": dominant_species,
                "representative_sequence_snippet": group['sequence'].iloc[0][:100] + "..." # Use first sequence as representative
            })

    end_pipeline_time = time.time()

    # 6. Final JSON Construction
    novel_count = len(df[df['cluster'] == -1])
    known_count = len(df[df['cluster'] != -1])
    
    final_json_data = {
        "run_summary": {
            "status": "success",
            "total_sequences": len(df),
            "novel_taxa_count": novel_count,
            "known_taxa_count": known_count,
            "execution_time_seconds": round(end_pipeline_time - start_pipeline_time, 2)
        },
        "novel_taxa_cards": [
             {
                "id": card["id"],
                "confidence": card["confidence"],
                "similarity": card["similarity"],
                "closest_known_species": card["closest_known_species"],
                "sequence_snippet": card["sequence"][:100] + "..." 
            } for card in novel_taxa_cards
        ],
        "known_clusters_summary": known_clusters_summary
    }

    return final_json_data

# Example of how to use this function:
if __name__ == "__main__":
    # Ensure you are running this from a directory where updated_plasmids.csv exists
    # and all your Python modules (clustering, metrices, etc.) are importable.
    
    results = generate_full_model_json()
    
    if results.get("status") != "failed":
        # Save the output to a JSON file
        with open('pipeline_results.json', 'w') as f:
            json.dump(results, f, indent=4)
        print("\nPipeline run complete. Results saved to pipeline_results.json")
        print(f"Total novel taxa detected: {results['run_summary']['novel_taxa_count']}")
    else:
        print(f"Pipeline failed: {results['error']}")