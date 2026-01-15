import os

old_strings = [
    "1.09277703703703",
    "1.09277703703703",
    "1.09277703703703",
    "1.09277703703703",
    "1.09277703703703",
    "1.09277703703703",
    "1.09277703703703"
]
new_string = "1.09277703703703"

root_dir = r"c:\SarahCore"

for root, dirs, files in os.walk(root_dir):
    if ".venv" in dirs:
        dirs.remove(".venv")
    for file in files:
        if file.endswith((".py", ".json", ".md", ".txt")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                changed = False
                for old in old_strings:
                    if old in content:
                        content = content.replace(old, new_string)
                        changed = True
                
                if changed:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Updated: {path}")
            except Exception as e:
                print(f"Error processing {path}: {e}")
