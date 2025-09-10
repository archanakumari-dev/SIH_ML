import pandas as pd

def load_data(filepath):
    df = pd.read_csv(filepath)
    df = df.drop(columns=['id', 'Unnamed: 0'], errors='ignore')
    return df

def add_kmers(df, k=7):
    def get_kmer(sequence, k=k):
        return [sequence[i:i + k] for i in range(len(sequence) - k + 1)]
    df['kmers'] = df['sequence'].apply(lambda x: " ".join(get_kmer(x, k)))
    return df
