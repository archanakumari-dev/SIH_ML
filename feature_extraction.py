from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

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
        batch = sequences[i:i+batch_size]
        batch_embs = [embedder.embed(seq) for seq in batch]
        embeddings.extend(batch_embs)
    return np.array(embeddings)
