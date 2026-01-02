from config import OPENAI_API_KEY

# Make API_KEY available for CLI and other scripts
API_KEY = OPENAI_API_KEY

def verify_api_key(key):
    """
    Verifies that the provided key matches the OPENAI_API_KEY from config.py.
    """
    return key == OPENAI_API_KEY

