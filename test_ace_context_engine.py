from ace_context_engine import ACEContextEngine

def test_context_engine():
    persona_sig = "a1b2c3"
    engine = ACEContextEngine(persona_signature=persona_sig)
    for i in range(12):
        engine.update(f"Message {i}")
    # Simulate correct signature
    engine.persona_signature = engine.check_integrity() and engine.persona_signature or "zzz"
    assert engine.get_context()[-1] == "Message 11"
    print("ACE Context Engine test passed.")

if __name__ == "__main__":
    test_context_engine()
