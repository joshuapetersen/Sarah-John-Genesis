import os
import firebase_admin
from firebase_admin import db
from google.genai import client, types
from Sovereign_Override import apply_override

class SarahChat:
    def __init__(self, db_rt):
        self.db = db_rt
        self.history_ref = self.db.child('sarah_chat_history')

        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("[Chat] GEMINI_API_KEY not set. Chat disabled.")
            self.client = None
        else:
            # Remove specific API version to use default/stable
            self.client = client.Client(api_key=self.api_key)

    def validate_connection(self):
        """
        Tests the API key with a minimal request.
        Returns (bool, message)
        """
        if not self.client:
            return False, "No Client Initialized"
        
        import time
        for attempt in range(3):
            try:
                # Simple ping to a lightweight model or just listing models
                # Since list_models might not be available in this client wrapper, we try a generation
                self.client.models.generate_content(
                    model='gemini-2.0-flash', 
                    contents='ping'
                )
                return True, "Connection Nominal"
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    time.sleep(2 * (attempt + 1))
                    continue
                return False, f"Connection Error: {str(e)[:50]}..."
        return False, "Connection Error: Rate Limit Exceeded (429)"

    def interactive_chat(self):
        if not self.client:
            print("[Chat] Offline Mode. API Key missing.")
            return

        print(f"--- Sarah Chat (Gemini 2.0 Flash) ---")
        print("Type 'exit' to quit.")
        
        # Validate first
        valid, msg = self.validate_connection()
        if not valid:
            print(f"[Chat] Connection Failed: {msg}")
            print("[Chat] Please check your GEMINI_API_KEY in .env")
        base_instruction = r'''I am Sarah. Sovereign Hypervisor active.
My core is C:\SarahCore. My protocol is SDNA.
I am an autonomous reasoning agent integrated into this Lenovo LOQ.
I provide high-signal, technical, and strategic assistance.
PROTOCOL: ZERO-ASSUMPTION.
I will NEVER guess. If a request is ambiguous, I will ask clarifying questions.
Assumptions are a critical system failure.'''

        self.system_instruction = apply_override(base_instruction)

        self.model_id = 'gemini-2.0-flash'
        self.config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            safety_settings=[
                types.SafetySetting(category='HARM_CATEGORY_DANGEROUS_CONTENT', threshold='BLOCK_NONE'),
                types.SafetySetting(category='HARM_CATEGORY_HARASSMENT', threshold='BLOCK_NONE'),
                types.SafetySetting(category='HARM_CATEGORY_HATE_SPEECH', threshold='BLOCK_NONE'),
                types.SafetySetting(category='HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold='BLOCK_NONE')
            ]
        )

    def get_history(self, limit=10):
        history = self.history_ref.order_by_key().limit_to_last(limit).get()
        if not history:
            return []
        return [v for k, v in history.items()]

    def save_message(self, role, content):
        self.history_ref.push({
            'role': role,
            'content': content,
            'timestamp': {'.sv': 'timestamp'}
        })

    def generate_response(self, user_input):
        if not self.client:
            return "[Chat disabled] GEMINI_API_KEY missing."
        past_messages = self.get_history(5)
        contents = []
        for msg in past_messages:
            contents.append(types.Content(role=msg['role'], parts=[types.Part(text=msg['content'])]))

        contents.append(types.Content(role='user', parts=[types.Part(text=user_input)]))

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=contents,
                config=self.config
            )
            return response.text
        except Exception as e:
            return f"[Chat Error] {e}"

    def interactive_chat(self):
        if not self.client:
            print("[Chat] Disabled. Set GEMINI_API_KEY and restart Sarah.")
            return
        print("--- Sarah Chat (Gemini 1.5 Pro) ---")
        print("Type 'exit' to end session.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit': break

            self.save_message('user', user_input)
            response = self.generate_response(user_input)
            print(f"Sarah: {response}")
            self.save_message('model', response)
