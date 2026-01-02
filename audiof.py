from flask import Flask, render_template, request, jsonify
from core import core, speak  # your existing AI + eSpeak logic
import vosk
import queue
import json
import soundfile as sf
import io
from pydub import AudioSegment

app = Flask(__name__)

# Load Vosk model once
model = vosk.Model("vosk-model-small-en-us-0.15")

@app.route("/")
def index():
    return render_template("voice_chat.html")

@app.route("/start_listen", methods=["POST"])
def start_listen():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    audio_data = audio_file.read()

    # Convert webm/ogg/mp4 to WAV using pydub
    audio = AudioSegment.from_file(io.BytesIO(audio_data))
    audio = audio.set_channels(1).set_frame_rate(16000)

    # Recognize using Vosk
    rec = vosk.KaldiRecognizer(model, 16000)
    rec.AcceptWaveform(audio.raw_data)
    result = json.loads(rec.Result())
    transcript = result.get("text", "")
    return jsonify({"transcript": transcript})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    answer = core(question, None)  # adjust API_KEY if needed
    speak(answer)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
