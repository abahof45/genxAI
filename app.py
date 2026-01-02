# app.py
from flask import Flask, render_template, request, jsonify
from core import core
from config import OPENAI_API_KEY

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"answer": "No question provided."})

    try:
        answer = core(question, OPENAI_API_KEY)
        return jsonify({"answer": answer})
    except Exception as e:
        print("CORE ERROR:", e)
        return jsonify({"answer": f"Server error: {e}"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)

