from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_kmers(df, max_features=10000):
    tfidf = TfidfVectorizer(max_features=max_features)
    X = tfidf.fit_transform(df['kmers'])
    return X, tfidf
