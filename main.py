from data_processing import load_data
from feature_extraction import DNABERTEmbedder, deep_embed_sequences
from clustering import run_dbscan
from metrices import get_novel_species_for_display

def main():
    df = load_data('updated_plasmids.csv')
    embedder = DNABERTEmbedder()
    X = deep_embed_sequences(df['sequence'].tolist(), embedder)
    cluster_labels = run_dbscan(X)
    df['clusters'] = cluster_labels
    # Use metrices.py functionality for novelty/similarity
    novel_species_cards = get_novel_species_for_display(df, cluster_labels, X)
    print("Novel species discovered (sample):")
    for card in novel_species_cards[:5]:
        print(card)

if __name__ == "__main__":
    main()
