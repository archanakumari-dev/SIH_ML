import streamlit as st
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

class DNABERTEmbedder:
    def __init__(self, model_name="zhihan1996/DNA_bert_6", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)

    def kmerize(self, sequence, k=6):
        return " ".join([sequence[i:i+k] for i in range(len(sequence)-k+1)])

    def embed(self, sequence, max_len=512, stride=100):
        kmer_seq = self.kmerize(sequence)
        tokens = kmer_seq.split()
        all_embeddings = []

        special_tokens_count = self.tokenizer.num_special_tokens_to_add(pair=False)
        max_len_adjusted = max_len - special_tokens_count

        for start in range(0, len(tokens), stride):
            chunk_tokens = tokens[start:start + max_len_adjusted]
            if not chunk_tokens:
                break
            chunk_seq = " ".join(chunk_tokens)
            inputs = self.tokenizer(chunk_seq, return_tensors="pt", truncation=True, max_length=max_len)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                output = self.model(**inputs)[0].mean(dim=1)
            all_embeddings.append(output.cpu().numpy().flatten())

        if all_embeddings:
            return np.mean(all_embeddings, axis=0)
        else:
            return np.zeros(self.model.config.hidden_size)

def deep_embed_sequences(sequences, embedder):
    embeddings = []
    batch_size = 8
    for i in range(0, len(sequences), batch_size):
        batch = sequences[i:i + batch_size]
        batch_embs = [embedder.embed(seq) for seq in batch]
        embeddings.extend(batch_embs)
    return np.array(embeddings)

def plot_pie_chart(num_novel, num_clustered):
    labels = ['Novel Taxa', 'Clustered Taxa']
    sizes = [num_novel, num_clustered]
    colors = ['#1976D2', '#BDBDBD']
    explode = (0.08, 0)
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels,
        autopct='%1.1f%%', startangle=90,
        colors=colors, explode=explode,
        shadow=True,
        wedgeprops={'edgecolor': 'black', 'linewidth': 2},
        textprops={'color': 'navy', 'weight': 'bold'}
    )
    ax.set_title("Novel vs Clustered Taxa", fontsize=16)
    plt.legend(wedges, labels, loc="upper right", fontsize=13)
    st.pyplot(fig)
    plt.close()

def main():
    st.title("eDNA Novel Taxa Detector (DNABERT Enhanced)")
    st.write("Upload DNA sequences (CSV with 'sequence' column). The app clusters sequences and shows novel taxa with their closest known species.")

    uploaded_file = st.file_uploader("Upload CSV with 'sequence' column", type='csv')
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        sequences = df['sequence'].dropna().tolist()
        st.info(f"Loaded {len(sequences)} sequences.")

        embedder = DNABERTEmbedder()
        st.info("Generating DNABERT embeddings (this may take a while)...")
        X = deep_embed_sequences(sequences, embedder)

        st.info("Clustering with DBSCAN...")
        cluster_labels = DBSCAN(eps=0.5, min_samples=5, metric='cosine').fit_predict(X)

        df['cluster'] = cluster_labels

        novel_idxs = np.where(cluster_labels == -1)[0]
        known_idxs = np.where(cluster_labels != -1)[0]
        novel_embs = X[novel_idxs]
        known_embs = X[known_idxs]

        st.subheader("Pie Chart of Novel vs Clustered Taxa")
        plot_pie_chart(len(novel_idxs), len(known_idxs))

        st.subheader("Novel Taxa with Closest Known Species")
        cols = st.columns(2)
        for i, idx in enumerate(novel_idxs):
            if len(known_idxs) > 0:
                sims = cosine_similarity(novel_embs[i].reshape(1, -1), known_embs)
                best_idx = np.argmax(sims)
                closest_seq = sequences[known_idxs[best_idx]]
                sim_score = sims[0, best_idx]
            else:
                closest_seq = "N/A"
                sim_score = 0.0

            with cols[i % 2]:
                st.markdown(f"**Novel Taxon {idx+1}**")
                with st.expander("Show Full Novel Sequence"):
                    st.text(sequences[idx])
                st.write(f"Closest Known Species Sequence (first 100 bp): {closest_seq[:100]}...")
                st.write(f"Similarity Score: {sim_score:.3f}")

        st.write(f"Total novel taxa detected: {len(novel_idxs)}")

if __name__ == "__main__":
    main()
