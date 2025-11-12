import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    print("✅ Gemini API key found in .env")
    print(f"Key starts with: {GEMINI_API_KEY[:5]}...")
else:
    print("❌ No Gemini API key found in .env file")
    exit()

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-2.0-flash-001')
    
    print("✅ Gemini configured successfully")
    
    # Test the API
    response = model.generate_content("Say 'Hello from Gemini!' in one sentence.")
    print(f"✅ Gemini response: {response.text}")
    
except Exception as e:
    print(f"❌ Error calling Gemini API: {str(e)}")