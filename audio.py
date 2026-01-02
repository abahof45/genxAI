from core import core
from api_key_manager import API_KEY  # or ask user input
from core import speak
print("Welcome to Audio GenxAI! Ask me anything.")
while True:
    user_input = input("You: ")
    answer = core(user_input, API_KEY)  # ✅ Pass the API key
    speak(answer)
