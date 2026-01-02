# core.py

import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE= 'data.csv'

class sim:
    def __init__(self, db_file=DATA_FILE, threshold=0.3):
        self.data_file= db_file
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer()
        self._load_data()

    def _load_data(self):
      if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        match = df[df["question"].str.lower() == question.lower()]
        if not match.empty:
            return match.iloc[0]["answer"]

    def get_answer(self, user_question):
        if not self.questions:
            return None, 0.0
        vectors = self.vectorizer.fit_transform(self.questions + [question])
        similarity = cosine_similarity(vectors[-1], vectors[:-1])
        best_idx = similarity.argmax()
        score = similarity[0, best_idx]
        if score >= self.threshold:
            return self.answers[best_idx], score
        return None, score