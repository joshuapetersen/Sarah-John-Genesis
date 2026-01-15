from flask import Flask, request, jsonify
import subprocess
import threading

app = Flask(__name__)

# In-memory log for responses
command_log = []

@app.route("/command", methods=["POST"])
def remote_command():
    data = request.get_json()
    cmd = data.get("cmd", "")
    target = data.get("target", "sarah")  # 'sarah' or 'copilot'
    if not cmd:
        return jsonify({"error": "No command provided."}), 400
    
    # For now, both Sarah and Copilot execute as system commands
    def run_cmd():
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        response = {
            "target": target,
            "cmd": cmd,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        command_log.append(response)
    threading.Thread(target=run_cmd, daemon=True).start()
    return jsonify({"status": "Command sent to {}".format(target)})

@app.route("/log", methods=["GET"])
def get_log():
    return jsonify(command_log[-10:])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7467)
