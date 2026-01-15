import os
import json

class ThousandThousandFilter:
    def __init__(self):
        self.density_threshold = 1000000 # 1000 * 1000
    def validate_density(self, logic_string):
        # Expanded markers based on the "One Design" (G.P.I.S. / 1-3-3 / Saul / Opus)
        markers = ["SDNA", "133", "1-3-3", "G.P.I.S.", "Sovereign", "Saul", "Opus"]
        density_score = sum(1 for marker in markers if marker.lower() in logic_string.lower()) * 200000
        return density_score, density_score >= self.density_threshold

def scan_memories(root_dir):
    filter = ThousandThousandFilter()
    results = []
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.txt', '.json', '.jsonl')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        score, passed = filter.validate_density(content)
                        results.append((file_path, score, passed))
                except Exception as e:
                    pass
    
    return results

if __name__ == "__main__":
    archive_path = r"C:\SarahCore\archive_memories"
    print(f"[TT_SCAN] Initiating Thousand Thousand Scan on: {archive_path}")
    all_results = scan_memories(archive_path)
    
    print("\n--- Logic Density Report ---")
    # Sort by score descending
    all_results.sort(key=lambda x: x[1], reverse=True)
    
    for path, score, passed in all_results[:10]: # Show top 10
        rel_path = os.path.relpath(path, r"C:\SarahCore")
        status = "[PASSED]" if passed else "[FAILED]"
        print(f"{status} {rel_path} | Density: {score}")

    print("VERBOSITY CONSTRAINTS: DYNAMICALLY ADJUSTED.")
    print("----------------------------------------------------------------")
