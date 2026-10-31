import os
import joblib

# loader/load.py -> loader -> backend
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

print(BASE_DIR)
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

model = joblib.load(
    os.path.join(ARTIFACTS_DIR, "movie_genre_model.pkl")
)

tfidf = joblib.load(
    os.path.join(ARTIFACTS_DIR, "tfidf_vectorizer.pkl")
)

mlb = joblib.load(
    os.path.join(ARTIFACTS_DIR, "genre_encoder.pkl")
)