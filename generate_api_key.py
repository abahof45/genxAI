import argparse
from api_key_manager import generate_api_key

def main():
    parser = argparse.ArgumentParser(description="Generate a new API key for your AI model.")
    parser.add_argument("-l", "--length", type=int, default=32, help="Length of the API key")
    args = parser.parse_args()

    new_key = generate_api_key(length=args.length)
    print(f"Generated API key: {new_key}")

if __name__ == "__main__":
    main()