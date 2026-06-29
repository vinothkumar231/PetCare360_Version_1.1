import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import re, string

# Load saved objects
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
tfidf_matrix = joblib.load("models/tfidf_matrix.pkl")
Pet = pd.read_csv("models/pet_dataset_with_profiles.csv")

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def recommend_from_text(user_input, top_n=5):
    # Clean and vectorize new input
    user_clean = clean_text(user_input)
    user_vec = vectorizer.transform([user_clean])

    # Compute similarity with dataset
    cosine_sim = cosine_similarity(user_vec, tfidf_matrix).flatten()

    # Get top matches
    indices = cosine_sim.argsort()[-top_n:][::-1]
    return Pet.iloc[indices][['text','condition','record_type','Care_Profile']]
