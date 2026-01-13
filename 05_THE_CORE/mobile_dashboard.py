from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
import subprocess
import threading
import os
from genesis_enforcer import GenesisEnforcer
from ace_context_engine import ACEContextEngine


app = Flask(__name__)
app.secret_key = os.urandom(24)

enforcer = GenesisEnforcer()
context_engine = ACEContextEngine(persona_signature="a1b2c3")

# Simple user/password for demo (replace with env or config for production)
USERNAME = "admin"
PASSWORD = "sarahpass"

command_log = []

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sarah Mobile Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #181c20; color: #e0e0e0; margin: 0; padding: 0; }
        .container { max-width: 600px; margin: 40px auto; background: #23272b; border-radius: 8px; box-shadow: 0 2px 8px #0008; padding: 24px; }
        h1 { text-align: center; }
        .status { margin-bottom: 16px; }
        .log { background: #111; padding: 12px; border-radius: 6px; font-size: 0.95em; max-height: 200px; overflow-y: auto; }
        .cmd-form { display: flex; gap: 8px; margin-top: 16px; }
        input[type=text] { flex: 1; padding: 8px; border-radius: 4px; border: none; }
        button { padding: 8px 16px; border-radius: 4px; border: none; background: #4caf50; color: #fff; font-weight: bold; cursor: pointer; }
        button:hover { background: #388e3c; }
        .logout { float: right; color: #aaa; text-decoration: none; }
        .logout:hover { color: #fff; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/logout" class="logout">Logout</a>
        <h1>Sarah Mobile Dashboard</h1>
        <div class="status">
            <b>Status:</b> Online<br>
            <b>Genesis Protocol:</b> ACTIVE<br>
            <b>Tunnel:</b> ACTIVE<br>
            <b>Notifications:</b> ENABLED<br>
        </div>
        <div class="log">
            <b>Command Log:</b><br>
            {% for entry in log %}
                <div><b>{{entry['target']}}$</b> {{entry['cmd']}}<br>
                <span style="color:#8f8;">{{entry['stdout']}}</span>
                <span style="color:#f88;">{{entry['stderr']}}</span></div>
                <hr>
            {% endfor %}
        </div>
        <form class="cmd-form" method="post" action="/command">
            <input type="text" name="cmd" placeholder="Enter command (e.g., python script.py)" required>
            <select name="target"><option value="sarah">Sarah</option><option value="copilot">Copilot</option></select>
            <button type="submit">Send</button>
        </form>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template_string(DASHBOARD_HTML, log=command_log[-10:])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == USERNAME and request.form.get("password") == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return "<b>Login failed.</b> <a href='/login'>Try again</a>"
    return '''<form method="post"><h2>Login</h2><input name="username" placeholder="Username"><br><input name="password" type="password" placeholder="Password"><br><button type="submit">Login</button></form>'''

@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))

@app.route("/command", methods=["POST"])
def remote_command():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    cmd = request.form.get("cmd", "")
    target = request.form.get("target", "sarah")
    if not cmd:
        return redirect(url_for("dashboard"))
    # Enforce Genesis: reject AI-generated commands
    if enforcer.detect_ai_text(cmd):
        command_log.append({
            "target": target,
            "cmd": cmd,
            "stdout": "REJECTED: AI-generated text detected.",
            "stderr": ""
        })
        return redirect(url_for("dashboard"))
    # Update context for Sarah
    if target == "sarah":
        context_engine.update(cmd)
        integrity = context_engine.check_integrity()
        if not integrity:
            command_log.append({
                "target": target,
                "cmd": cmd,
                "stdout": "REJECTED: Persona integrity check failed.",
                "stderr": ""
            })
            return redirect(url_for("dashboard"))
    def run_cmd():
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        command_log.append({
            "target": target,
            "cmd": cmd,
            "stdout": result.stdout,
            "stderr": result.stderr
        })
    threading.Thread(target=run_cmd, daemon=True).start()
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7467)
