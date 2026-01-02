import os
def api_connect(filename="api/api.txt"):
    """
    Asks the user for input, reads the file content, and performs 
    a direct comparison.
    
    NOTE: This version does NOT handle FileNotFoundError if 
    the file is missing.
    """
    
    # 1. Get the user input
    user_input = input("🔑 Enter the api key: ").strip()

    # 2. Read the content of the file
    # This line will cause a 'FileNotFoundError' if 'secret_text.txt' does not exist.
    with open(filename, 'r') as file:
        # Read and clean the file content
        file_content = file.read().strip()
    
    # 3. Check for a match
    print("-" * 25)
    if user_input == file_content:
        from core import core
        from api_key_manager import API_KEY  # or ask user input

        print("Welcome to GenxAI! Ask me anything.")
        while True:
            user_input = input("You: ")
            answer = core(user_input, API_KEY)  # ✅ Pass the API key
            print(f"AI: {answer}")
    else:
        print("Wrong api key")
    print("-" * 25)

# Execute the function
if __name__ == "__main__":
    api_connect()