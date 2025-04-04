import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Load API Key from .env file

# Configure API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models and filter useful ones
def list_models():
    models = genai.list_models()
    free_models = [m.name for m in models if "flash" in m.name or "pro" in m.name]

    print("\n✅ Available Gemini Models (Free & Recommended):")
    for model in free_models:
        print(f"   ➜ {model}")

    if "gemini-1.5-pro" in free_models:
        print("\n🚀 Recommended: Use 'gemini-1.5-pro' for best results.")
    elif "gemini-1.5-flash" in free_models:
        print("\n⚡ Alternative: Use 'gemini-1.5-flash' (Faster, but less powerful).")

list_models()
