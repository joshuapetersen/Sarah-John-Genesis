import google.generativeai as genai
import os

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise RuntimeError('GEMINI_API_KEY not set in environment.')

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content('Genesis Handshake: Confirm Antigravity communication.')
    print('Antigravity/Gemini API Response:')
    print(response.text)
except Exception as e:
    print('ERROR:', e)
