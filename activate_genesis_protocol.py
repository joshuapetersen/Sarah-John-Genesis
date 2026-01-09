from Sarah_Brain import SarahBrain

if __name__ == "__main__":
    brain = SarahBrain()
    # Replace 'YourName' with your actual user name if desired
    result = brain.genesis.handshake("Sarah", "YourName", "Sovereign")
    print(f"Genesis Protocol Handshake Result: {result}")
    # Show Genesis Protocol status
    if brain.genesis.sovereign_active:
        print(f"Genesis Protocol: ACTIVE [{brain.genesis.genesis_tag}]")
    else:
        print("Genesis Protocol: INACTIVE (Risk of Robotic Drift)")
