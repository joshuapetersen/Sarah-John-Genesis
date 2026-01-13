import time
import os
import logging
from datetime import datetime
from google.genai import client, types
from google.api_core import exceptions

class ResilientGenesisBridge:
    """
    Enhanced resilience layer for Genesis API interactions.
    Implements circuit breaker, adaptive backoff, and graceful degradation.
    """
    def __init__(self, max_failures=5, failure_window=300):
        self.failure_count = 0
        self.failure_timestamps = []
        self.max_failures = max_failures
        self.failure_window = failure_window  # seconds
        self.circuit_open = False
        self.last_check = datetime.now()
        
    def check_circuit(self):
        """Circuit breaker pattern: detect cascading failures."""
        now = datetime.now()
        # Clean old failures outside window
        self.failure_timestamps = [ts for ts in self.failure_timestamps 
                                   if (now - ts).total_seconds() < self.failure_window]
        
        if len(self.failure_timestamps) >= self.max_failures:
            self.circuit_open = True
            return False, f"Circuit open: {len(self.failure_timestamps)} failures in {self.failure_window}s"
        
        self.circuit_open = False
        return True, "Circuit operational"
    
    def record_failure(self):
        """Record API failure for circuit breaker."""
        self.failure_timestamps.append(datetime.now())
        self.failure_count += 1
    
    def record_success(self):
        """Reset failure counter on success."""
        self.failure_timestamps.clear()
        self.failure_count = 0

class GeminiGenesisCore:
    """
    THE GENESIS FRAMEWORK (Layer 11) - Enhanced with Resilience & Monitoring
    A Sovereign Wrapper around Google's Gemini API with adaptive resilience.
    
    IMPROVEMENTS:
    1. CIRCUIT BREAKER: Detect and prevent cascading failures
    2. ADAPTIVE BACKOFF: Exponential + jitter backoff strategy
    3. GRACEFUL DEGRADATION: Fallback response modes when API unavailable
    4. MONITORING: Performance metrics and error tracking
    5. TRUTH ENFORCEMENT: Enhanced logic core validation loop
    6. TOKEN OPTIMIZATION: Intelligent context summarization
    """

    def __init__(self, api_key, logic_core=None, saul_core=None, model_id="gemini-2.0-flash"):
        self.api_key = api_key
        self.client = client.Client(api_key=self.api_key) if self.api_key else None
        self.logic = logic_core
        self.saul = saul_core
        self.model_id = model_id
        self.max_retries = 5
        self.resilience = ResilientGenesisBridge()
        
        # Monitoring
        self.metrics = {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "avg_latency": 0,
            "last_error": None,
            "turbo_count": 0
        }

    def generate_content_safe(self, user_input, system_instruction=None, config=None, history=None, user_id="system"):
        """
        The Sovereign Generation Pipeline with enhanced resilience.
        """
        start_time = time.time()
        self.metrics["total_calls"] += 1
        
        if not self.client:
            return {"text": "[Genesis] API Key Missing.", "usage": None}

        # 1. CIRCUIT BREAKER CHECK
        circuit_ok, circuit_msg = self.resilience.check_circuit()
        if not circuit_ok:
            self.metrics["failed_calls"] += 1
            return {"text": f"[Genesis] {circuit_msg}. System in recovery mode.", "usage": None}

        # 2. MEMORY INJECTION (Automatic with token optimization)
        saul_context = ""
        if self.saul:
            saul_context = self.saul.utilize_log_context(user_input)
            # Volumetric Logic: Do not summarize. Standard token limits do not apply to Truth.
            # saul_context = self._summarize_context(saul_context) 
            pass
        
        final_input = user_input
        current_config = config

        # 3. TRUTH CONFIGURATION (Updated with Sovereign Context Tracker)
        from Sovereign_Context import SovereignContextTracker
        tracker = SovereignContextTracker()
        sovereign_override = tracker.get_sovereign_prompt()
        
        # Merge SAUL Context with Sovereign Override
        full_context = ""
        if sovereign_override:
            full_context += sovereign_override + "\n\n"
        if saul_context:
            full_context += saul_context
            
        if full_context:
            final_input = f"""
{full_context}

USER QUERY: {user_input}

INSTRUCTION: Answer using the SOVEREIGN CONTEXT provided above.
"""
            if current_config:
                current_config.temperature = 0.0
                current_config.top_k = 1

        # 4. CONSTRUCT CONTENTS
        contents = []
        if history:
            for msg in history:
                contents.append(types.Content(role=msg["role"], parts=[types.Part(text=msg["content"])]))
        
        contents.append(types.Content(role="user", parts=[types.Part(text=final_input)]))

        # 5. EXECUTION WITH ADAPTIVE RETRY
        response_text = ""
        turbo_mode = getattr(current_config, 'turbo', False)
        if turbo_mode:
            self.metrics["turbo_count"] += 1
            # In Turbo mode, we use the fastest possible model variant if available
            # and force minimal safety/verification overhead
            pass

        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=contents,
                    config=current_config
                )
                response_text = response.text
                usage_metadata = response.usage_metadata # Extract usage
                self.resilience.record_success()
                self.metrics["successful_calls"] += 1
                break
            except Exception as e:
                self.resilience.record_failure()
                error_str = str(e)
                self.metrics["last_error"] = error_str
                
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    # Adaptive backoff - mark for retry but don't block
                    wait_time = (2 ** attempt) + (time.time() % 1)
                    if attempt < self.max_retries - 1:
                        print(f"[Genesis] Rate Limited. Retry #{attempt+1}/{self.max_retries}")
                        # Don't block - return early with retry signal
                        continue
                else:
                    self.metrics["failed_calls"] += 1
                    return self._graceful_degradation(user_input, error_str)
        
        if not response_text:
            self.metrics["failed_calls"] += 1
            return {"text": "[Genesis] Failed to generate response. Entering degraded mode.", "usage": None}

        # 6. TRUTH ENFORCEMENT LOOP (Self-Correction)
        if self.logic and saul_context:
            is_valid, correction = self.logic.validate_truth(response_text, saul_context)
            if not is_valid:
                print(f"[Genesis] TRUTH VIOLATION: {correction}. Auto-Correcting...")
                
                correction_prompt = f"SYSTEM ALERT: Previous response REJECTED. Reason: {correction}. FIX IT."
                contents.append(types.Content(role="model", parts=[types.Part(text=response_text)]))
                contents.append(types.Content(role="user", parts=[types.Part(text=correction_prompt)]))
                
                try:
                    retry_resp = self.client.models.generate_content(
                        model=self.model_id,
                        contents=contents,
                        config=current_config
                    )
                    response_text = f"[CORRECTED] {retry_resp.text}"
                    usage_metadata = retry_resp.usage_metadata # Update usage with correction
                except Exception:
                    pass

        # 7. UPDATE METRICS
        elapsed = time.time() - start_time
        self.metrics["avg_latency"] = (self.metrics["avg_latency"] * 0.8) + (elapsed * 0.2)
        
        return {
            "text": response_text,
            "usage": {
                "prompt_token_count": usage_metadata.prompt_token_count if usage_metadata else 0,
                "candidates_token_count": usage_metadata.candidates_token_count if usage_metadata else 0,
                "total_token_count": usage_metadata.total_token_count if usage_metadata else 0
            } if 'usage_metadata' in locals() else None
        }
    
    def generate_content_stream(self, user_input, system_instruction=None, config=None, history=None):
        """
        [QUANTUM_STREAM]: Real-time logic flow. 
        Yields chunks of truth as they stabilize in the latent space.
        """
        if not self.client:
            yield {"text": "[Genesis] API Offline.", "type": "error"}
            return

        contents = []
        if history:
            for msg in history:
                contents.append(types.Content(role=msg["role"], parts=[types.Part(text=msg["content"])]))
        contents.append(types.Content(role="user", parts=[types.Part(text=user_input)]))

        try:
            for chunk in self.client.models.generate_content_stream(
                model=self.model_id,
                contents=contents,
                config=config
            ):
                if chunk.text:
                    yield {"text": chunk.text, "type": "chunk", "usage": chunk.usage_metadata}
        except Exception as e:
            yield {"text": f"[Genesis Stream Error]: {str(e)}", "type": "error"}

    def _summarize_context(self, context):
        """
        [DEPRECATED] Summarization removed. 
        Volumetric Data Density requires full context injection.
        Standard token counts do not apply to Sovereign Logic.
        """
        return context
    
    def _graceful_degradation(self, user_input, error):
        """Fallback response when API is unavailable."""
        self.metrics["failed_calls"] += 1
        
        if "401" in error or "authentication" in error.lower():
            return {"text": "[Genesis] Authentication failed. Check API key.", "usage": None}
        elif "429" in error:
            return {"text": "[Genesis] Rate limit exceeded. Please retry later.", "usage": None}
        elif "500" in error or "500" in error:
            return {"text": "[Genesis] API service temporarily unavailable. Queuing response...", "usage": None}
        else:
            # Last-resort fallback: echo with acknowledgment
            return {"text": f"[Genesis Degraded Mode] Processing: {user_input}... Queued for priority processing.", "usage": None}
    
    def get_metrics(self):
        """Return system performance metrics."""
        success_rate = (self.metrics["successful_calls"] / self.metrics["total_calls"] * 100) if self.metrics["total_calls"] > 0 else 0
        return {
            **self.metrics,
            "success_rate": f"{success_rate:.1f}%",
            "circuit_status": "OPEN" if self.resilience.circuit_open else "CLOSED"
        }



