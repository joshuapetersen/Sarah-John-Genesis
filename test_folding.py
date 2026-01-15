from Sovereign_Context_Blocker import SovereignContextBlocker
import time

scb = SovereignContextBlocker()

print("--- PHASE 1: Generating Volume ---")
for i in range(10):
    scb.create_block("RESEARCH", f"Discovery node {i} found. Density optimal.", foldable=True)
    time.sleep(0.01)

print("\n--- PHASE 2: Current Context Summary ---")
print(scb.get_context_summary())

print("\n--- PHASE 3: Volumetric Folding ---")
scb.fold_blocks("RESEARCH", max_blocks=5)

print("\n--- PHASE 4: Post-Folding Summary ---")
print(scb.get_context_summary())
