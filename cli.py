from core import core
from api_key_manager import API_KEY  # or ask user input

print("Welcome to GenxAI! Ask me anything.")
while True:
    user_input = input("You: ")
    answer = core(user_input, API_KEY)  # ✅ Pass the API key
    print(f"AI: {answer}")