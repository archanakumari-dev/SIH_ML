from sklearn.model_selection import train_test_split

def filter_rare_classes(df, X, min_samples=2):
    counts = df['species_encoded'].value_counts()
    valid_classes = counts[counts >= min_samples].index
    mask = df['species_encoded'].isin(valid_classes)
    return df[mask], X[mask.values], df[mask]['species_encoded']

def split_data(X, y, test_size=0.3, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

def train_and_evaluate(models, X_train, y_train, X_test, y_test):
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        results[name] = {
            'train': {
                'accuracy': accuracy_score(y_train, y_train_pred),
                'f1': f1_score(y_train, y_train_pred, average='weighted'),
                'precision': precision_score(y_train, y_train_pred, average='weighted'),
                'recall': recall_score(y_train, y_train_pred, average='weighted')
            },
            'test': {
                'accuracy': accuracy_score(y_test, y_test_pred),
                'f1': f1_score(y_test, y_test_pred, average='weighted'),
                'precision': precision_score(y_test, y_test_pred, average='weighted'),
                'recall': recall_score(y_test, y_test_pred, average='weighted')
            }
        }
    return results
