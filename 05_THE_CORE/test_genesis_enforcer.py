from genesis_enforcer import GenesisEnforcer

def test_enforcer():
    enforcer = GenesisEnforcer()
    ai_text = "As an AI language model, I am here to help you. In conclusion, this is a seamless experience."
    human_text = "I built this system to reject mediocrity. No filler. No slop. Only signal."
    assert enforcer.detect_ai_text(ai_text) is True
    assert enforcer.detect_ai_text(human_text) is False
    print("Genesis Enforcer test passed.")

if __name__ == "__main__":
    test_enforcer()
