import sounddevice as sd
import vosk
import queue
import json
from core import core
from api_key_manager import API_KEY  # or ask user input
from core import speak
print("Welcome to GenxAI Voice to Voice AI model")
# Load model
model = vosk.Model("vosk-model-small-en-us-0.15")

# Audio queue
q = queue.Queue()

# Callback to feed audio into queue
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Start stream
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, 16000)
    print("Listening... Press Ctrl+C to stop.")
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            a=result.get("text", "")
            print(a)
            answer = core(a, API_KEY)
            speak(answer)
        else:
            partial = json.loads(rec.PartialResult())
            # print("Partial:", partial.get("partial", ""))



