import hashlib

class ACEContextEngine:
    def __init__(self, persona_signature, window=2048):
        self.persona_signature = persona_signature
        self.window = window
        self.history = []

    def update(self, text):
        self.history.append(text)
        if len(self.history) > self.window:
            self.history = self.history[-self.window:]

    def check_integrity(self):
        # Persona integrity: hash of last N messages must match persona signature
        context = ' '.join(self.history[-10:])
        context_hash = hashlib.sha256(context.encode()).hexdigest()
        return context_hash.startswith(self.persona_signature)

    def get_context(self):
        return self.history[-self.window:] if self.history else []
