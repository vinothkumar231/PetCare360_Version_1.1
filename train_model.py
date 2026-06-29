import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

# Paths
os.makedirs("models", exist_ok=True)
dataset_path = "models/pet-health-symptoms-dataset.csv"

# Load dataset
df = pd.read_csv(dataset_path)

# Train TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["text"])

# Save vectorizer and matrix
with open("models/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("models/tfidf_matrix.pkl", "wb") as f:
    pickle.dump(tfidf_matrix, f)

print("✅ Model trained and saved successfully!")
