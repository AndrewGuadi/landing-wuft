from dotenv import load_dotenv, find_dotenv

# Find the nearest .env file by walking up the directory tree
dotenv_path = find_dotenv(filename=".env", raise_error_if_not_found=False)

if dotenv_path:
    load_dotenv(dotenv_path=dotenv_path, override=False)
    print(f"[dotenv] Loaded environment variables from: {dotenv_path}")
else:
    print("[dotenv] No .env file found. Using system environment variables only.")


from app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
