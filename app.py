import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import time # Added for timing/better info
from Bio import SeqIO # for FASTA parsing
from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB]
collection = db[config.MONGO_COLLECTION]

# --- FEATURE EXTRACTION FUNCTIONS (FROM PREVIOUS FILES) ---

def get_kmer_string(sequence, k=6):
    """Tokenizes a sequence into overlapping k-mers and joins them into a single string."""
    return " ".join([sequence[i:i+k] for i in range(len(sequence)-k+1)])

def create_tfidf_embeddings(sequences, k_size=6):
    """Creates feature vectors using TF-IDF on k-mers.
    This is much faster than DNABERT and does not require a GPU.
    """
    # 1. Prepare K-mer tokens for all sequences
    kmer_documents = [get_kmer_string(seq, k=k_size) for seq in sequences]
    # 2. Initialize and fit the TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 1), # Treats each k-mer as a unique word/token
        analyzer='word',
        sublinear_tf=True
    )
    # 3. Transform the k-mer documents into a matrix of embeddings (vectors)
    X = vectorizer.fit_transform(kmer_documents)
    # DBSCAN requires a dense array for 'cosine' metric, so we convert the sparse matrix
    return X.toarray()
# --- UTILITY FOR STREAMLIT DISPLAY ---
def plot_pie_chart(novel_count, known_count):
    labels = ['Novel Taxa (Cluster -1)', 'Known Taxa (Clustered)']
    sizes = [novel_count, known_count]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0) # Explode the novel slice
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

# --- MAIN STREAMLIT APP ---

def main():
    st.title("eDNA Novel Taxa Detector (K-mer/TF-IDF Fast Mode)")
    st.write("Upload **CSV** with **'sequence'** and **'species'** columns. The app uses TF-IDF features and DBSCAN to cluster sequences and identify potential novel taxa (noise).")
    # csv upload
    uploaded_file = st.file_uploader("Upload CSV with 'sequence' and 'species' columns", type='csv')
    # FASTA upload
    uploaded_fasta = st.file_uploader("Upload FASTA file", type=['fasta', 'fa'])
    sequences=[]
    species=[]
    # ----load csv/handling---
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        # Check required columns
        if 'sequence' not in df.columns or 'species' not in df.columns:
            st.error("Uploaded CSV must contain 'sequence' and 'species' columns.")
            return

        df = df.dropna(subset=['sequence', 'species']).reset_index(drop=True)
        sequences.extend(df['sequence'].tolist())
        species.extend(df['species'].tolist())
        st.info(f"Loaded {len(sequences)} sequences for analysis.")
        # # Insert all CSV sequences into MongoDB if not already present
        # inserted_count = 0
        # for _, row in df.iterrows():
        #     exists = collection.find_one({"sequence": row['sequence'], "species": row['species']})
        #     if not exists:
        #         collection.insert_one({
        #             "sequence": row['sequence'],
        #             "species": row['species'],
        #             "source": "CSV",
        #             "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        #         })
        #         inserted_count += 1
        # st.success(f"Inserted {inserted_count} new sequences from CSV into MongoDB.")
    # --- Load FASTA ---
    if uploaded_fasta:
        fasta_records = list(SeqIO.parse(uploaded_fasta, "fasta"))
        sequences.extend([str(record.seq) for record in fasta_records])
        species.extend([record.id for record in fasta_records])
        st.info(f"Loaded {len(fasta_records)} sequences from FASTA.")

    if not sequences:
        st.warning("Please upload at least one CSV or FASTA file.")
        return
    # --- REPLACED DNABERT WITH TF-IDF ---
    st.subheader("1. Feature Embedding (K-mer/TF-IDF)")
    start_time = time.time()
    X = create_tfidf_embeddings(sequences, k_size=6)
    st.success(f"Generated TF-IDF embeddings in {time.time() - start_time:.2f} seconds. Feature space size: {X.shape[1]}")
        
    # ---DBSCAN CLUSTERING ---
    st.subheader("2. DBSCAN Clustering & Novelty Detection")
    start_time = time.time()
    # Using fixed, conservative DBSCAN parameters
    cluster_labels = DBSCAN(eps=0.3, min_samples=5, metric='cosine').fit_predict(X)
    st.success(f"DBSCAN clustering complete in {time.time() - start_time:.2f} seconds.")

    df['cluster'] = cluster_labels

    novel_idxs = np.where(cluster_labels == -1)[0]
    known_idxs = np.where(cluster_labels != -1)[0]
    novel_embs = X[novel_idxs]
    known_embs = X[known_idxs]

    st.subheader("3. Results Summary")
    plot_pie_chart(len(novel_idxs), len(known_idxs))
    st.write(f"**Total novel taxa (cluster -1):** {len(novel_idxs)}")

    # --- Insert/Update MongoDB ---
    st.subheader("4. Saving Data to MongoDB")
    for idx, seq in enumerate(sequences):
        row_species = species[idx]
        cluster = int(cluster_labels[idx])
        is_novel = cluster == -1

        # Similarity/novel detection for novel sequences
        if is_novel and len(known_idxs) > 0:
            novel_idx_in_array = np.where(novel_idxs == idx)[0][0]
            sim_matrix = cosine_similarity(X[idx].reshape(1,-1), X[known_idxs])
            best_known_idx = known_idxs[np.argmax(sim_matrix)]
            closest_species = species[best_known_idx]
            closest_seq = sequences[best_known_idx]
            sim_score = float(sim_matrix[0][np.argmax(sim_matrix)])
            confidence = float((1 - sim_score) * 100)
            novel_taxon_id = f"NS{str(idx+1).zfill(3)}"
        else:
            # closest_species = None
            # closest_seq = None
            # sim_score = None
            # confidence = None
            # novel_taxon_id = None
            closest_species = row_species
            closest_seq = seq
            sim_score = 1.0      # or None
            confidence = 0.0
            novel_taxon_id = "NA"  # Could also put "Known" if you want

        # Upsert into MongoDB
        result_doc={
            "sequence": seq,
            "species": row_species,
            "novel_taxon_id": novel_taxon_id,
            "similarity": sim_score,
            "confidence": confidence,
            "closest_species": closest_species,
            "novel_sequence": seq,
            "closest_known_sequence": closest_seq,
            "cluster": cluster,
            "source": "CSV/FASTA",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        collection.insert_one(result_doc)   
    st.success(f"All {len(sequences)} sequences saved/updated in MongoDB.")

if __name__ == "__main__":
    main()
#         if len(novel_idxs) > 0 and len(known_idxs) > 0:
#             sim_matrix = cosine_similarity(novel_embs, known_embs)
#             for i, idx in enumerate(novel_idxs):
#                 best_known_emb_idx = np.argmax(sim_matrix[i])
#                 sim_score = sim_matrix[i, best_known_emb_idx]
#                 global_closest_idx = known_idxs[best_known_emb_idx]

#                 closest_species = df['species'].iloc[global_closest_idx]
#                 closest_seq = sequences[global_closest_idx]
#                 confidence_score = (1 - sim_score) * 100

#                 result_doc = {
#                     "novel_taxon_id": f"NS{str(idx+1).zfill(3)}",
#                     "similarity": float(sim_score),
#                     "confidence": float(confidence_score),
#                     "closest_species": closest_species,
#                     "novel_sequence": sequences[idx],
#                     "closest_known_sequence": closest_seq,
#                     "source": "NovelDetection",
#                     "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
#                 }
#                 collection.insert_one(result_doc)
#             st.info("Novel taxa details saved to MongoDB.")

#     # --- FASTA Handling ---
#     if uploaded_fasta:
#         fasta_sequences = list(SeqIO.parse(uploaded_fasta, "fasta"))
#         st.info(f"Loaded {len(fasta_sequences)} sequences from FASTA.")

#         inserted_count = 0
#         for record in fasta_sequences:
#             seq = str(record.seq)
#             species_name = record.id  # FASTA header

#             exists = collection.find_one({"sequence": seq, "species": species_name})
#             if not exists:
#                 collection.insert_one({
#                     "sequence": seq,
#                     "species": species_name,
#                     "source": "FASTA",
#                     "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
#                 })
#                 inserted_count += 1

#         st.success(f"Inserted {inserted_count} new sequences from FASTA into MongoDB.")


# if __name__ == "__main__":
#     main()

        
#         st.subheader("Novel Taxa with Closest Known Species Match")
        
#         if len(novel_idxs) == 0:
#             st.info("No novel taxa detected in this dataset based on current DBSCAN parameters.")
#             return

#         if len(known_idxs) == 0:
#             st.warning("No known/clustered taxa found for comparison. All detected sequences are considered novel.")
#             return

#         cols = st.columns(2)
        
#         # Calculate full similarity matrix between novel and known embeddings
#         sim_matrix = cosine_similarity(novel_embs, known_embs)
        
#         # Iterate over novel taxa
#         for i, idx in enumerate(novel_idxs):
            
#             # Find the best match index within the known_embs subset
#             best_known_emb_idx = np.argmax(sim_matrix[i])
#             sim_score = sim_matrix[i, best_known_emb_idx]
            
#             # Map the subset index back to the global index in the original dataframe
#             global_closest_idx = known_idxs[best_known_emb_idx]
            
#             # Retrieve the required information
#             closest_species = df['species'].iloc[global_closest_idx]
#             closest_seq = sequences[global_closest_idx]
#             confidence_score = (1 - sim_score) * 100 # Novelty Confidence

#             # MongoDB insertion
#             # Prepare MongoDB document
#             result_doc = {
#                 "novel_taxon_id": f"NS{str(idx+1).zfill(3)}",
#                 "similarity": float(sim_score),
#                 "confidence": float(confidence_score),
#                 "closest_species": closest_species,
#                 "novel_sequence": sequences[idx],
#                 "closest_known_sequence": closest_seq,
#                 "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
#             }

#             # Insert into MongoDB
#             collection.insert_one(result_doc)
#         st.info("saved to Mongodb")
            
#             # with cols[i % 2]:
#             #     st.markdown(f"**🔬 Novel Taxon ID: NS{str(idx+1).zfill(3)}**")
                
#             #     # Display Similarity and Confidence
#             #     st.write(f"**Closest Similarity:** {sim_score:.3f}")
#             #     st.write(f"**Novelty Confidence:** {confidence_score:.2f}%")
                
#             #     # Display Closest Known Species
#             #     st.success(f"**Closest Known Species:** {closest_species}")

#             #     # Display Sequences
#             #     with st.expander("Show Novel Sequence"):
#             #         st.text(sequences[idx])
#             #     with st.expander("Show Closest Known Sequence"):
#             #         st.text(f"(First 100 bp): {closest_seq[:100]}...")

# if __name__ == "__main__":
#     main()