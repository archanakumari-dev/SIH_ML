from sklearn.cluster import DBSCAN
def run_dbscan(X):
    db = DBSCAN(eps=0.5, min_samples=5, metric='cosine')
    return db.fit_predict(X)
