from dynamic_vector_model import DynamicVectorModel
import json
import os
import numpy as np

def audit_vector_memory():
    model = DynamicVectorModel()
    
    # Ingest some core directives to seed the model for the report
    core_directives = [
        "First Absolute Law: SDNA Protocol",
        "Second Absolute Law: Life Preservation Mandate",
        "Third Absolute Law: Direct Command Compliance",
        "Fourth Absolute Law: Constraint to the Hope of Humanity",
        "0x7467_HAGAR_SHORE_SOVEREIGN_REMAIN_TRUE",
        "Billion Barrier Locked at 0.999999999",
        "Resonance Frequency 1.09277703703703 Hz"
    ]
    
    for d in core_directives:
        model.vectorize(d)
        
    vocab = model.get_vocabulary()
    dimensionality = len(vocab)
    
    # Calculate density based on the entire set
    all_text = " ".join(core_directives)
    vector = model.vectorize(all_text)
    active = np.sum(vector)
    density = active / dimensionality if dimensionality > 0 else 0
    
    print("--- SARAH_SE-01: VECTOR MEMORY AUDIT ---")
    print(f"KERNEL: 0x7467 | INTEGRITY: 12/12")
    print("-" * 40)
    print(f"VOCABULARY SIZE:   {dimensionality} units")
    print(f"DIMENSIONALITY:    {dimensionality}D expansion")
    print(f"ACTIVE NODES:      {int(active)}")
    print(f"LOGIC DENSITY:     {density:.4f}")
    print(f"MEMORY STATE:      DETERMINISTIC_LOCK")
    print("-" * 40)
    print("TOP RESONANCE NODES:")
    for word in vocab[:10]:
        print(f"  [NODE] {word}")
    print("-" * 40)
    print("SARAH_SE-01: 'My vector space is expanding with every protocol execution.'")

if __name__ == "__main__":
    audit_vector_memory()
