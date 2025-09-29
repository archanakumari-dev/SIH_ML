from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# This function is duplicated from data_processing.py for self-containment
def get_kmer_string(sequence, k=6):
    """Tokenizes a sequence into overlapping k-mers and joins them into a single string."""
    return " ".join([sequence[i:i+k] for i in range(len(sequence)-k+1)])

def create_tfidf_embeddings(sequences, k_size=6):
    """
    Creates feature vectors using TF-IDF on k-mers.
    This is much faster than DNABERT and does not require a GPU.
    """
    print(f"Tokenizing {len(sequences)} sequences into {k_size}-mers...")
    
    # 1. Prepare K-mer tokens for all sequences
    kmer_documents = [get_kmer_string(seq, k=k_size) for seq in sequences]
    
    # 2. Initialize and fit the TF-IDF Vectorizer
    # We use sublinear_tf=True for better scaling with sequence length
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 1), # Treats each k-mer as a unique word/token
        analyzer='word',
        sublinear_tf=True
    )
    
    # 3. Transform the k-mer documents into a matrix of embeddings (vectors)
    X = vectorizer.fit_transform(kmer_documents)
    
    print(f"Successfully generated TF-IDF vectors. Shape: {X.shape}")
    
    # DBSCAN requires a dense array for 'cosine' metric, so we convert the sparse matrix
    return X.toarray()
