import argparse
import secrets
import string
import os


def main():
    parser = argparse.ArgumentParser(description="Generate a new API key for your AI model.")
    parser.add_argument("-l", "--length", type=int, default=32, help="Length of the API key")
    args = parser.parse_args()

    new_key = generate_api_key(length=args.length)
    #print(f"Generated API key: {new_key}")

def generate_api_key(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# default key
API_KEY = generate_api_key()

print(API_KEY)
path="api"

with open(os.path.join(path, "api.txt"), "w") as f:
        f.write(API_KEY)

if __name__ == "__main__":
    main()