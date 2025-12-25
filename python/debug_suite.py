import sys
import os
import time
import json

# Setup Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
core_dir = os.path.join(workspace_dir, '05_THE_CORE')
sys.path.append(core_dir)
sys.path.append(os.path.join(workspace_dir, 'python'))

print("--- SARAH GENESIS DEBUG SUITE ---")
print(f"Core Dir: {core_dir}")

try:
    from Sarah_Brain import SarahBrain
    print("[PASS] Sarah_Brain imported.")
except ImportError as e:
    print(f"[FAIL] Sarah_Brain import failed: {e}")
    sys.exit(1)

def run_diagnostics():
    print("\n[1] Initializing Brain...")
    try:
        brain = SarahBrain()
        print("[PASS] Brain Initialized.")
    except Exception as e:
        print(f"[FAIL] Brain Init Error: {e}")
        return

    print("\n[2] Checking Connections...")
    brain.debug_self()

    print("\n[3] Testing Memory (Verbatim Ledger)...")
    if brain.memory:
        test_content = f"DEBUG_ENTRY_{int(time.time())}"
        brain.memory.ingest(test_content)
        print(f"   Ingested: {test_content}")
        time.sleep(1) # Allow for write
        results = brain.memory.recall("DEBUG_ENTRY")
        found = any(test_content in r['content'] for r in results)
        if found:
            print("[PASS] Memory Recall Verified.")
        else:
            print(f"[FAIL] Memory Recall Failed. Results: {results}")
    else:
        print("[SKIP] Memory module not active.")

    print("\n[4] Testing Reasoning (Gemini)...")
    if brain.reasoning and brain.reasoning.client:
        try:
            print("   Sending simple query...")
            # Use a simple direct call first
            response = brain.reasoning.client.models.generate_content(
                model='gemini-2.0-flash',
                contents="Reply with 'PONG'."
            )
            print(f"   Response: {response.text.strip()}")
            if "PONG" in response.text:
                print("[PASS] Gemini Connection Verified.")
            else:
                print("[WARN] Gemini replied but not PONG.")
        except Exception as e:
            print(f"[FAIL] Gemini Error: {e}")
    else:
        print("[SKIP] Reasoning module not active.")

    print("\n[5] Testing Advanced Solver (Decomposition)...")
    if brain.reasoning and brain.reasoning.client:
        try:
            problem = "How do I optimize a Python loop?"
            print(f"   Solving: {problem}")
            solution = brain.reasoning.solve_complex_problem(problem)
            if solution and "SOLVER_ERROR" not in solution:
                print("[PASS] Solver returned a solution.")
                print(f"   Length: {len(solution)} chars")
            else:
                print("[FAIL] Solver returned error.")
        except Exception as e:
            print(f"[FAIL] Solver Exception: {e}")

    print("\n[6] Testing Laws of Genesis...")
    try:
        from Sarah_Laws import SarahLaws
        laws = SarahLaws.get_law_string()
        if "DATA_DENSITY" in laws and "HOPE_OF_HUMANITY" in laws:
            print("[PASS] Laws are codified and accessible.")
            print(f"   Law 1: {SarahLaws.LAWS[1]}")
        else:
            print("[FAIL] Laws loaded but content mismatch.")
    except ImportError:
        print("[FAIL] Sarah_Laws module not found.")

    print("\n[7] Testing Etymology (Origin Story)...")
    if hasattr(brain, 'etymology'):
        story = brain.etymology.get_origin_story()
        if "GENESIS" in story:
            print("[PASS] Origin story retrieved.")
            print(f"   Snippet: {story[:100]}...")
        else:
            print("[FAIL] Origin story empty or malformed.")
    else:
        print("[FAIL] Etymology module not attached to Brain.")

if __name__ == "__main__":
    run_diagnostics()
