from sklearn.cluster import DBSCAN

def run_dbscan(X, eps=0.5, min_samples=5, metric='cosine'):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
    labels = dbscan.fit_predict(X)
    return labels
