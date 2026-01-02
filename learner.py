import os
import pandas as pd
import subprocess
from difflib import SequenceMatcher
from api_key_manager import verify_api_key
from config import OPENAI_API_KEY

from openai import OpenAI

DATA_FILE = "data.csv"

client = OpenAI(api_key=OPENAI_API_KEY)


# ---------------- CSV SIMILARITY ----------------
def find_similar_question(user_question, threshold=0.85):
    if not os.path.exists(DATA_FILE):
        return None

    df = pd.read_csv(DATA_FILE)

    if "question" not in df.columns or "answer" not in df.columns:
        return None

    df = df.dropna(subset=["question", "answer"])
    df["question"] = df["question"].astype(str)

    best_score = 0
    best_answer = None

    for _, row in df.iterrows():
        score = SequenceMatcher(
            None, user_question.lower(), row["question"].lower()
        ).ratio()

        if score > best_score and score >= threshold:
            best_score = score
            best_answer = row["answer"]

    return best_answer


# ---------------- SAVE MEMORY ----------------
def save_to_csv(question, answer):
    new_row = {"question": question, "answer": answer}

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(DATA_FILE, index=False)

# ---------------- CHATGPT ----------------
def ask_chatgpt(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": question},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"GenxAI error: {e}"



# ---------------- CORE ----------------
def core(question, api_key):
    if not verify_api_key(api_key):
        return "Invalid API key"

    similar = find_similar_question(question)
    if similar:
        return similar

    answer = ask_chatgpt(question)
    return answer


while True:
    user_input = input("You: ")
    answer = core(user_input, OPENAI_API_KEY)  # ✅ Pass the API key
    if answer == "GenxAI error: Connection error.":
        a=input("Teach me:")
        save_to_csv(user_input, a)
        print("learnt")