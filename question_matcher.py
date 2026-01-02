import pandas as pd
from difflib import SequenceMatcher
import os

DATA_FILE = "data.csv"

# 1️⃣ Load CSV FIRST
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["question", "answer"])

# 2️⃣ Clean AFTER loading
df = df.dropna(subset=["question"])
df["question"] = df["question"].astype(str)

# 3️⃣ Function
def find_similar_question(user_question, threshold=0.8):
    best_score = 0
    best_answer = None

    for _, row in df.iterrows():
        score = SequenceMatcher(
            None,
            user_question.lower(),
            row["question"].lower()
        ).ratio()

        if score >= threshold and score > best_score:
            best_score = score
            best_answer = row["answer"]

    return best_answer
