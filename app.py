import streamlit as st
import pandas as pd
from Bio import SeqIO
import joblib
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# Load pre-trained TF-IDF vectorizer (pickle) used in your project
@st.cache_resource(show_spinner=True)
def load_vectorizer():
    return joblib.load('tfidf_vectorizer.pkl')


# Function to create k-mers from sequence
def get_kmer(sequence, k=7):
    return " ".join([sequence[i:i+k] for i in range(len(sequence) - k + 1)])


# DBSCAN clustering function (with cosine metric)
def cluster_sequences(X):
    dbscan = DBSCAN(eps=0.5, min_samples=5, metric='cosine')
    return dbscan.fit_predict(X)


# Function to generate novel taxa cards with confidence and similarity
def get_novel_species_for_display(sequences, cluster_labels, X):
    novel_indices = np.where(cluster_labels == -1)[0]
    known_indices = np.where(cluster_labels != -1)[0]
    known_vectors = X[known_indices]
    novel_vectors = X[novel_indices]

    if len(known_indices) > 0 and len(novel_indices) > 0:
        sim_matrix = cosine_similarity(novel_vectors, known_vectors)
        similarity_scores = sim_matrix.max(axis=1) * 100  # convert to %
    else:
        similarity_scores = np.zeros(len(novel_indices))

    confidence_scores = (100 - similarity_scores).clip(80, 99)  # higher confidence for lower similarity

    cards = []
    for i, idx in enumerate(novel_indices):
        cards.append({
            "id": f"NS{str(idx+1).zfill(3)}",
            "sequence": sequences[idx],
            "confidence": int(confidence_scores[i]),
            "similarity": int(similarity_scores[i])
        })
    return cards


# Main app UI and logic
def main():
    st.title("eDNA Novel Taxa Detector")
    st.write("""
        Upload your DNA sequences (CSV with 'sequence' column or FASTA format).
        The app will cluster sequences and show DNA sequences identified as novel taxa (anomalies).
    """)

    uploaded_file = st.file_uploader("Upload CSV or FASTA", type=['csv', 'fasta', 'fa'])

    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            if 'sequence' not in df.columns:
                st.error("CSV must contain a 'sequence' column.")
                return
            sequences = df['sequence'].dropna().tolist()
        else:
            # Parse FASTA sequences
            sequences = [str(record.seq) for record in SeqIO.parse(uploaded_file, 'fasta')]
            if not sequences:
                st.error("No sequences found in FASTA file.")
                return

        st.info(f"Loaded {len(sequences)} sequences.")

        # Generate k-mers
        kmers = [get_kmer(seq) for seq in sequences]

        # Load vectorizer and transform
        tfidf = load_vectorizer()
        X = tfidf.transform(kmers)

        # Cluster with DBSCAN
        cluster_labels = cluster_sequences(X)

        # Get novel species cards with confidence and similarity
        novel_species_cards = get_novel_species_for_display(sequences, cluster_labels, X)

        # Display total number of novel taxa detected
        num_novel_taxa = len(novel_species_cards)
        st.subheader("Novel Species Discovery")
        st.metric(label="Total novel taxa detected", value=num_novel_taxa)

        if novel_species_cards:
            cols = st.columns(2)
            for i, card in enumerate(novel_species_cards):
                with cols[i % 2]:
                    st.markdown(f"**{card['id']}**")
                    st.write(f"Sequence: {card['sequence'][:50]}...")  # show first 50 bases
                    st.write(f"Confidence: {card['confidence']}%")
                    st.progress(card["confidence"] / 100)
                    st.write(f"Similarity to known species: {card['similarity']}%")
                    st.progress(card["similarity"] / 100)
        else:
            st.write("No novel taxa detected.")


if __name__ == "__main__":
    main()
