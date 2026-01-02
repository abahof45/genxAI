import pandas as pd
import requests
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = "data.csv"

# -------- Save Knowledge --------
def save_to_csv(question, answer, file_path=DATA_FILE):
    new_row = {"question": question, "answer": answer}
    try:
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([new_row])
    df.to_csv(file_path, index=False)
    print("Saved new knowledge to CSV.")

# -------- Core Logic --------
def core(question, api_key):
    if not is_valid_key(api_key):
        return "Invalid API Key. Access denied."

    # Step 1: check CSV
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        match = df[df["question"].str.lower() == question.lower()]
        if not match.empty:
            return match.iloc[0]["answer"]

        # Optional: Scikit-learn similarity search
        vectorizer = CountVectorizer().fit_transform(df["question"])
        vectors = vectorizer.toarray()
        input_vec = CountVectorizer().fit(df["question"]).transform([question]).toarray()
        similarity = cosine_similarity(input_vec, vectors)
        best_idx = similarity.argmax()
        if similarity[0][best_idx] > 0.5:
            return df.iloc[best_idx]["answer"]

    # Step 2: ask Gemini
    answer = ask_gemini(question, OPENAI_API_KEY)
    save_to_csv(question, answer)
    return answer