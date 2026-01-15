import os
import re

# Precise string the user wants
target = "1.09277703703703"

# Regex to match anything starting with 1.0927 or 1.0019 followed by digits
# We want to catch 1.092703..., 1.09277703, 1.00192703, etc.
pattern = re.compile(r"1\.[09]+[0-9]{4,}")

root_dir = r"c:\SarahCore"

for root, dirs, files in os.walk(root_dir):
    if ".venv" in dirs:
        dirs.remove(".venv")
    for file in files:
        if file.endswith((".py", ".json", ".md", ".txt")):
            path = os.path.join(root, file)
            # Skip the script itself
            if "global_regex_update" in file:
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Special cases for 0.5019... if needed, but the user didn't mention it.
                # The user said "all entries need to read 1.09277703703703"
                
                new_content = pattern.sub(target, content)
                
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Regex Updated: {path}")
            except Exception as e:
                pass # Binary files etc.
