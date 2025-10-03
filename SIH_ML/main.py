from data_processing import load_data
from clustering import run_dbscan
from metrices import get_novel_species_for_display
import pandas as pd
import numpy as np
import time
import os

# Import the fast, CPU-friendly feature extractor
try:
    from feature_extraction import create_tfidf_embeddings
except ImportError:
    # Fallback definition if the file is missing (though it shouldn't be for the demo)
    print("FATAL ERROR: 'feature_extraction_alt.py' not found. Please ensure it is in the repository.")
    create_tfidf_embeddings = None


def main():
    print("--- SIH HACKATHON DEMO MODE ACTIVE (K-mer/TF-IDF Mode) ---")
    
    # 1. Load the Data
    try:
        # NOTE: This load_data MUST load the 'species' column from 'updated_plasmids.csv'
        df = load_data('updated_plasmids.csv')
    except FileNotFoundError:
        print("FATAL ERROR: 'updated_plasmids.csv' not found. Cannot proceed.")
        return
        
    X = None # Initialize feature matrix

    # --- Feature Extraction (FAST) ---
    if create_tfidf_embeddings:
        print("\n--- Generating K-mer/TF-IDF Features (CPU-Fast) ---")
        try:
            start_time = time.time()
            # X now contains the dense TF-IDF vectors
            X = create_tfidf_embeddings(df['sequence'].tolist(), k_size=6)
            end_time = time.time()
            print(f"Feature Generation Time: {end_time - start_time:.2f} seconds.")
        except Exception as e:
            print(f"FATAL ERROR during TF-IDF generation: {e}")
            X = None
             
    
    # --- Clustering and Metrics (Always fast) ---
    if X is not None:
        start_time = time.time()
        print("\nStarting fast DBSCAN clustering and novelty detection...")
        
        # DBSCAN and metrics are fast operations on the feature matrix X
        cluster_labels = run_dbscan(X)
        df['clusters'] = cluster_labels
        
        # The get_novel_species_for_display function (from metrices.py) now
        # internally retrieves and includes 'closest_known_species'
        novel_species_cards = get_novel_species_for_display(df, cluster_labels, X)
        
        end_time = time.time()
        
        # 4. Results
        print("\n--- Pipeline Results ---")
        novel_count = len([c for c in cluster_labels if c == -1])
        
        #modified this part to return the results as a dictionary so Flask can handle them.

        results = {
            "execution_time": end_time - start_time,
            "novel_species_count": novel_count,
            "novel_species_cards": novel_species_cards
        }
        
        print("\n--- Pipeline Results ---")
        print(results)

        # print(f"Total Execution Time (Clustering & Metrics): {end_time - start_time:.2f} seconds.")
        # print(f"Novel species discovered (cluster -1): {novel_count}")
        
        # if novel_count > 0:
        #     print("\nTop Novel Taxa Summary:")
        #     for i, card in enumerate(novel_species_cards[:3]):
        #         # --- MODIFIED PRINT STATEMENT ---
        #         print(f"  {i+1}. ID: {card['id']}, Novelty Confidence: {card['confidence']}%, Closest Similarity: {card['similarity']}%, ClosEST KNOWN SPECIES: {card['closest_known_species']}")
        #         # --- END MODIFIED PRINT STATEMENT ---
        # else:
        #     print("No novel species found.")
            
    # elif not create_tfidf_embeddings:
    #     print("\nERROR: Cannot run. Please provide 'feature_extraction.py' file.")
    return results

if __name__ == "__main__":
    output=main()
    print("Final output:", output)