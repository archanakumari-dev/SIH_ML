from data_processing import load_data, add_kmers
from feature_extraction import vectorize_kmers
from label_encoding import encode_species
from metrices import get_novel_species_for_display
# from model_training import  split_data, train_and_evaluate
from clustering import run_dbscan
from visualization import reduce_pca, plot_anomalies
import joblib

def main():
    df = load_data('updated_plasmids.csv')

    df = add_kmers(df, k=7)
    
    X, tfidf = vectorize_kmers(df)
    # Save vectorizer and trained models for deployment
    joblib.dump(tfidf, 'tfidf_vectorizer.pkl')
    
    cluster_labels = run_dbscan(X)
    df['clusters'] = cluster_labels

# Generate novel species discovery cards
    novel_species_cards = get_novel_species_for_display(df, cluster_labels, X, habitat_col='habitat')
    print("Novel species discovered (sample):")
    for card in novel_species_cards[:5]:  # print first 5 examples
        print(card)

    # reduced = reduce_pca(X)
    # plot_anomalies(reduced, cluster_labels)

if __name__ == "__main__":
    main()
