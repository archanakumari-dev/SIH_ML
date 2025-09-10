from data_processing import load_data, add_kmers
from feature_extraction import vectorize_kmers
from label_encoding import encode_species
from model_training import filter_rare_classes, split_data, train_and_evaluate
from clustering import run_dbscan
from visualization import reduce_pca, plot_anomalies
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import joblib

def main():
    df = load_data('updated_plasmids.csv')
    df = add_kmers(df, k=7)

    # Save compressed CSV version for efficient storage
    df.to_csv("updated_plasmids.csv.gz", compression='gzip', index=False)
    X, tfidf = vectorize_kmers(df)
    df, le = encode_species(df)
    
    df_filtered, X_filtered, y_filtered = filter_rare_classes(df, X)
    from sklearn.preprocessing import LabelEncoder
    le2 = LabelEncoder()
    y_filtered_encoded = le2.fit_transform(y_filtered)
    X_train, X_test, y_train, y_test = split_data(X_filtered, y_filtered_encoded)
    
    models = {
        "Random Forest": RandomForestClassifier(),
        "Xgboost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
    }
    
    results = train_and_evaluate(models, X_train, y_train, X_test, y_test)
    print(results)
    
    # Save vectorizer and trained models for deployment
    joblib.dump(tfidf, 'tfidf_vectorizer.pkl')
    joblib.dump(models["Random Forest"], 'random_forest_model.pkl')
    joblib.dump(models["Xgboost"], 'xgb_model.pkl')
    
    # Clustering and Visualization on full dataset
    cluster_labels = run_dbscan(X)
    df['clusters'] = cluster_labels
    reduced = reduce_pca(X)
    plot_anomalies(reduced, cluster_labels)

if __name__ == "__main__":
    main()
