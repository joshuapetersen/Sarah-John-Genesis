import google.generativeai as genai
import os

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise RuntimeError('GEMINI_API_KEY not set in environment.')

genai.configure(api_key=api_key)

try:
    print('Available Gemini models:')
    for model in genai.list_models():
        print(f"- {model.name} (methods: {model.supported_generation_methods})")
except Exception as e:
    print('ERROR:', e)
