import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

def reduce_pca(X, n_components=2):
    pca = PCA(n_components=n_components)
    reduced = pca.fit_transform(X.toarray())
    return reduced

def plot_anomalies(reduced, cluster_labels):
    import numpy as np
    anomaly_indices = np.where(cluster_labels == -1)[0]
    sns.scatterplot(
        x=reduced[anomaly_indices, 0],
        y=reduced[anomaly_indices, 1],
        color='red',
        label='Anomalies'
    )
    plt.title('DBSCAN Anomalies in PCA-reduced space')
    plt.xlabel('PC 1')
    plt.ylabel('PC 2')
    plt.legend()
    plt.show()
