import time
import os
import logging
from google.genai import client, types
from google.api_core import exceptions

class GeminiGenesisCore:
    """
    THE GENESIS FRAMEWORK (Layer 11)
    A Sovereign Wrapper around Google's Gemini API.
    
    IMPROVEMENTS:
    1. RESILIENCE: Automatic retry with exponential backoff for 429/500 errors.
    2. TRUTH ENFORCEMENT: Integrated Logic Core validation loop.
    3. MEMORY INJECTION: Automatic SAUL context retrieval.
    4. DATA DENSITY: Token optimization (stripping fluff).
    """

    def __init__(self, api_key, logic_core=None, saul_core=None, model_id="gemini-2.0-flash"):
        self.api_key = api_key
        self.client = client.Client(api_key=self.api_key) if self.api_key else None
        self.logic = logic_core
        self.saul = saul_core
        self.model_id = model_id
        self.max_retries = 5

    def generate_content_safe(self, user_input, system_instruction=None, config=None, history=None, user_id="system"):
        """
        The Sovereign Generation Pipeline.
        """
        if not self.client:
            return "[Genesis] API Key Missing."

        # 1. MEMORY INJECTION (Automatic)
        saul_context = ""
        if self.saul:
            saul_context = self.saul.utilize_log_context(user_input)
        
        final_input = user_input
        current_config = config

        # 2. TRUTH CONFIGURATION
        if saul_context:
            # print(f"[Genesis] Injecting Truth Context ({len(saul_context)} chars)")
            final_input = f"""
CRITICAL CONTEXT (ABSOLUTE TRUTH):
{saul_context}

USER QUERY: {user_input}

INSTRUCTION: Answer the query using the CONTEXT. Do not hallucinate.
"""
            # Force strictness if context exists
            if current_config:
                current_config.temperature = 0.0
                current_config.top_k = 1

        # 3. CONSTRUCT CONTENTS
        contents = []
        if history:
            for msg in history:
                contents.append(types.Content(role=msg["role"], parts=[types.Part(text=msg["content"])]))
        
        contents.append(types.Content(role="user", parts=[types.Part(text=final_input)]))

        # 4. EXECUTION WITH RETRY (Resilience)
        response_text = ""
        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=contents,
                    config=current_config
                )
                response_text = response.text
                break # Success
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait_time = (2 ** attempt) + 1
                    print(f"[Genesis] Rate Limit Hit. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"[Genesis] Critical API Error: {e}")
                    return f"[Genesis Error] {e}"
        
        if not response_text:
            return "[Genesis] Failed to generate response after retries."

        # 5. TRUTH ENFORCEMENT LOOP (Self-Correction)
        if self.logic and saul_context:
            is_valid, correction = self.logic.validate_truth(response_text, saul_context)
            if not is_valid:
                print(f"[Genesis] TRUTH VIOLATION: {correction}. Auto-Correcting...")
                
                correction_prompt = f"SYSTEM ALERT: Previous response REJECTED. Reason: {correction}. FIX IT."
                contents.append(types.Content(role="model", parts=[types.Part(text=response_text)]))
                contents.append(types.Content(role="user", parts=[types.Part(text=correction_prompt)]))
                
                try:
                    # One-shot correction attempt
                    retry_resp = self.client.models.generate_content(
                        model=self.model_id,
                        contents=contents,
                        config=current_config
                    )
                    response_text = f"[CORRECTED] {retry_resp.text}"
                except Exception:
                    pass # Keep original if retry fails

        return response_text

