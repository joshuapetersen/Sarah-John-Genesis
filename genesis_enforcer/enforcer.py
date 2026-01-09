import re
import math

class GenesisEnforcer:
    def __init__(self, threshold=0.75):
        self.threshold = threshold

    def detect_ai_text(self, text):
        # Heuristic: AI text is often uniform, over-explains, and uses certain patterns
        ai_patterns = [
            r"As an AI[\w\s,]*", r"I'm an AI[\w\s,]*", r"In conclusion", r"delve|tapestry|landscape|foster|crucial|testament|realm|seamless"
        ]
        pattern_score = sum(bool(re.search(p, text, re.IGNORECASE)) for p in ai_patterns)
        avg_sentence_length = sum(len(s.split()) for s in text.split('.')) / max(1, len(text.split('.')))
        entropy = self._shannon_entropy(text)
        # AI text: high pattern_score, high avg_sentence_length, mid entropy
        score = 0
        if pattern_score:
            score += 0.5
        if avg_sentence_length > 18:
            score += 0.3
        if 3.5 < entropy < 4.2:
            score += 0.2
        return score >= self.threshold

    def _shannon_entropy(self, data):
        if not data:
            return 0
        freq = {c: data.count(c) for c in set(data)}
        probs = [f / len(data) for f in freq.values()]
        return -sum(p * math.log2(p) for p in probs if p > 0)
