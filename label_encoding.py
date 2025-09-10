from sklearn.preprocessing import LabelEncoder

def encode_species(df):
    le = LabelEncoder()
    df['species_encoded'] = le.fit_transform(df['species'])
    return df, le
