# find_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the API key from your .env file
load_dotenv()
try:
    genai.configure(api_key=os.getenv("AIzaSyDAk6sBFcDnJFku8CYXZ27BnhKWWsTd3Iw"))
except Exception as e:
    print(f"Error configuring API key: {e}")
    exit()

print("\nFinding available models for your API key...")
print("------------------------------------------")

# List all models and check which ones support the 'generateContent' method
found_model = False
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(f"✅ Found usable model: {m.name}")
    found_model = True

if not found_model:
    print("\n❌ No usable models found. This might be an issue with your API key or account setup.")

print("------------------------------------------")