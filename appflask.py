from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Bio import SeqIO
from pymongo import MongoClient
import config
import time
import io

# Initialize Flask
app = Flask(__name__)

# MongoDB connection
client = MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB]
collection = db[config.MONGO_COLLECTION]

# ---- Helper functions ----
def get_kmer_string(sequence, k=6):
    return " ".join([sequence[i:i+k] for i in range(len(sequence)-k+1)])

def create_tfidf_embeddings(sequences, k_size=6):
    kmer_documents = [get_kmer_string(seq, k=k_size) for seq in sequences]
    vectorizer = TfidfVectorizer(analyzer="word", sublinear_tf=True)
    X = vectorizer.fit_transform(kmer_documents)
    return X.toarray()

# ---- Flask Routes ----

@app.route('/')
def home():
    return jsonify({"message": "Flask ML API running"})


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    df = pd.read_csv(file)

    if 'sequence' not in df.columns or 'species' not in df.columns:
        return jsonify({"error": "CSV must contain 'sequence' and 'species' columns"}), 400

    sequences = df['sequence'].dropna().tolist()
    species = df['species'].dropna().tolist()

    # Embeddings
    X = create_tfidf_embeddings(sequences, k_size=6)

    # DBSCAN clustering
    cluster_labels = DBSCAN(eps=0.3, min_samples=5, metric='cosine').fit_predict(X)

    novel_idxs = np.where(cluster_labels == -1)[0]
    known_idxs = np.where(cluster_labels != -1)[0]

    inserted_count = 0
    docs=[]
    for idx, seq in enumerate(sequences):
        row_species = species[idx]
        cluster = int(cluster_labels[idx])
        is_novel = cluster == -1

        if is_novel and len(known_idxs) > 0:
            sim_matrix = cosine_similarity(X[idx].reshape(1,-1), X[known_idxs])
            best_known_idx = known_idxs[np.argmax(sim_matrix)]
            closest_species = species[best_known_idx]
            closest_seq = sequences[best_known_idx]
            sim_score = float(sim_matrix[0][np.argmax(sim_matrix)])
            confidence = float((1 - sim_score) * 100)
            novel_taxon_id = f"NS{str(idx+1).zfill(3)}"
        else:
            closest_species = row_species
            closest_seq = seq
            sim_score = 1.0
            confidence = 0.0
            novel_taxon_id = "NA"

        doc = {
            "sequence": seq,
            "species": row_species,
            "novel_taxon_id": novel_taxon_id,
            "similarity": sim_score,
            "confidence": confidence,
            "closest_species": closest_species,
            "novel_sequence": seq,
            "closest_known_sequence": closest_seq,
            "cluster": cluster,
            "source": "CSV",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # collection.insert_one(doc)
        # inserted_count += 1
        docs.append(doc)
    # After building all docs in the loop
    if docs:
        collection.insert_many(docs)
    inserted_count = len(docs)

    return jsonify({"message": f"Inserted {inserted_count} sequences into MongoDB"})
    
@app.route('/upload_fasta', methods=['POST'])
def upload_fasta():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    fasta_records = list(SeqIO.parse(io.StringIO(file.stream.read().decode("utf-8")), "fasta"))
    
    sequences = [str(record.seq) for record in fasta_records]
    species = [record.id for record in fasta_records]
    # embeddings
    X = create_tfidf_embeddings(sequences, k_size=6)
    cluster_labels = DBSCAN(eps=0.3, min_samples=5, metric='cosine').fit_predict(X)

    novel_idxs = np.where(cluster_labels == -1)[0]
    known_idxs = np.where(cluster_labels != -1)[0]
    inserted_count = 0
    for idx, seq in enumerate(sequences):
        row_species = species[idx]
        cluster = int(cluster_labels[idx])
        is_novel = cluster == -1

        if is_novel and len(known_idxs) > 0:
            sim_matrix = cosine_similarity(X[idx].reshape(1,-1), X[known_idxs])
            best_known_idx = known_idxs[np.argmax(sim_matrix)]
            closest_species = species[best_known_idx]
            closest_seq = sequences[best_known_idx]
            sim_score = float(sim_matrix[0][np.argmax(sim_matrix)])
            confidence = float((1 - sim_score) * 100)
            novel_taxon_id = f"NS{str(idx+1).zfill(3)}"
        else:
            closest_species = row_species
            closest_seq = seq
            sim_score = 1.0
            confidence = 0.0
            novel_taxon_id = "NA"

        doc = {
            "sequence": seq,
            "species": row_species,
            "novel_taxon_id": novel_taxon_id,
            "similarity": sim_score,
            "confidence": confidence,
            "closest_species": closest_species,
            "novel_sequence": seq,
            "closest_known_sequence": closest_seq,
            "cluster": cluster,
            "source": "FASTA",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        collection.insert_one(doc)
        inserted_count += 1

    return jsonify({"message": f"Inserted {inserted_count} FASTA sequences into MongoDB"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
