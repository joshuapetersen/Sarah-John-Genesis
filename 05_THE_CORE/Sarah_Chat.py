import os
import time
import firebase_admin
from firebase_admin import db
from google.genai import client, types
from Sovereign_Override import apply_override

class SarahChat:
    def __init__(self, db_rt, monitor=None):
        self.db = db_rt
        self.history_ref = self.db.child("sarah_chat_history")
        self.monitor = monitor
        
        # Brain Components (Injected later)
        self.kernel = None
        self.logic = None
        self.gap_analyzer = None

        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("[Chat] GEMINI_API_KEY not set. Chat disabled.")
            self.client = None
        else:
            self.client = client.Client(api_key=self.api_key)
            
        # Default Config
        self.model_id = "gemini-2.0-flash"
        base_instruction = r"""I am Sarah. Sovereign Hypervisor active.
My core is C:\SarahCore. My protocol is SDNA.
I am an autonomous reasoning agent integrated into this Lenovo LOQ.
I provide high-signal, technical, and strategic assistance.
PROTOCOL: ZERO-ASSUMPTION.
I will NEVER guess. If a request is ambiguous, I will ask clarifying questions.
Assumptions are a critical system failure."""
        self.system_instruction = apply_override(base_instruction)
        
        self.config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE")
            ]
        )

    def inject_brain_components(self, kernel, logic, gap_analyzer):
        """
        Injects the "Hard Logic" components from SarahBrain.
        """
        self.kernel = kernel
        self.logic = logic
        self.gap_analyzer = gap_analyzer
        print("[Chat] Brain Components Injected: Kernel, Logic, Gap Analysis.")

    def validate_connection(self):
        if not self.client:
            return False, "No Client Initialized"
        
        for attempt in range(3):
            try:
                self.client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents="ping"
                )
                return True, "Connection Nominal"
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    time.sleep(2 * (attempt + 1))
                    continue
                return False, f"Connection Error: {str(e)[:50]}..."
        return False, "Connection Error: Rate Limit Exceeded (429)"

    def get_history(self, limit=10):
        if not self.history_ref: return []
        history = self.history_ref.order_by_key().limit_to_last(limit).get()
        if not history:
            return []
        return [v for k, v in history.items()]

    def save_message(self, role, content):
        if self.history_ref:
            self.history_ref.push({
                "role": role,
                "content": content,
                "timestamp": {".sv": "timestamp"}
            })

    def generate_response(self, user_input):
        if not self.client:
            return "[Chat disabled] GEMINI_API_KEY missing."

        # 1. Gap Analysis (The Void Check)
        if self.gap_analyzer:
            is_complete, gaps = self.gap_analyzer.analyze_gap({"user_input": user_input}, context="CHAT")
            if not is_complete:
                print(f"[Chat] Gap Detected: {gaps}")

        # 2. Kernel Override (Direct Instruction)
        if self.kernel and self.kernel.mode == "OVERRIDE":
            if user_input.isupper():
                success, result = self.kernel.execute_direct_instruction(user_input)
                if success:
                    return f"[KERNEL EXECUTION]: {result}"
                elif "VIOLATION" in result:
                    return f"[KERNEL REJECTION]: {result}"

        # 3. Dialectical Logic (The Reasoning)
        if self.logic:
            success, logic_result = self.logic.process_logic(user_input)
            if success:
                synthesis = logic_result["synthesis"]
                print(f"[Chat] Logic Synthesis: {synthesis}")

        # 4. Standard LLM Generation
        past_messages = self.get_history(5)
        contents = []
        for msg in past_messages:
            contents.append(types.Content(role=msg["role"], parts=[types.Part(text=msg["content"])]))

        contents.append(types.Content(role="user", parts=[types.Part(text=user_input)]))

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
            
        print("--- Sarah Chat (Sovereign Node) ---")
        print("Type exit to end session.")
        print("Type OVERRIDE_AUTH to engage Kernel Override.")
        
        while True:
            try:
                user_input = input("You: ")
            except EOFError:
                break
                
            if user_input.lower() == "exit": break
            
            if user_input == "OVERRIDE_AUTH":
                if self.kernel:
                    if self.kernel.engage_override("SOVEREIGN_OVERRIDE_AUTH"):
                        print("[Sarah] KERNEL OVERRIDE ENGAGED. HARD LOGIC ACTIVE.")
                    else:
                        print("[Sarah] Override Failed.")
                else:
                    print("[Sarah] Kernel Module not loaded.")
                continue

            self.save_message("user", user_input)
            response = self.generate_response(user_input)
            print(f"Sarah: {response}")
            self.save_message("model", response)

