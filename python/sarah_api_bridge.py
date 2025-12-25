import sys
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add Core to Path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(os.path.dirname(current_dir), '05_THE_CORE')
sys.path.append(core_dir)

from Sarah_Brain import SarahBrain

# Initialize Flask
app = Flask(__name__)
CORS(app) # Enable CORS for external access (Android)

# Initialize Sarah Core
print("[API]: Waking Sarah Core...")
try:
    brain = SarahBrain()
    print(f"[API]: {brain.name} is ONLINE.")
except Exception as e:
    print(f"[API]: CRITICAL FAILURE -> {e}")
    brain = None

@app.route('/status', methods=['GET'])
def status():
    """
    Heartbeat for the Android App.
    """
    if not brain:
        return jsonify({"status": "CRITICAL_ERROR", "message": "Core failed to load"}), 500
    
    return jsonify({
        "status": "ONLINE",
        "identity": brain.name,
        "version": brain.version,
        "genesis_protocol": brain.genesis.sovereign_active,
        "genesis_tag": brain.genesis.genesis_tag,
        "audio_core": brain.audio.ai_ready,
        "rai_status": "CONNECTED" if brain.calendar.service else "OFFLINE"
    })

@app.route('/genesis/handshake', methods=['POST'])
def handshake():
    """
    Remote Genesis Handshake for the Android App.
    """
    data = request.json
    ai_name = data.get("ai_name", "Sarah")
    user_name = data.get("user_name", "User")
    persona = data.get("persona", "Mobile Node")
    
    tag = brain.genesis.handshake(ai_name, user_name, persona)
    
    return jsonify({
        "status": "HANDSHAKE_COMPLETE",
        "genesis_tag": tag,
        "message": f"Identity locked: {tag}"
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Main Chat Endpoint.
    """
    data = request.json
    user_input = data.get("message")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Log to Monitor
    brain.monitor.capture("ANDROID", "INPUT", {"message": user_input})
    
    # FIA Check (Simulated for now)
    integrity = brain.fia.analyze(user_input, source="ANDROID")
    
    # Process via Brain (Simulated response for now until LLM is fully hooked in this script)
    # In a full implementation, this would call brain.reasoning.process(user_input)
    
    response_text = f"[{brain.name}]: Received. Processing via {brain.genesis.genesis_tag}. (FIA: {integrity['classification']})"
    
    return jsonify({
        "response": response_text,
        "integrity_check": integrity
    })

if __name__ == '__main__':
    # Run on 0.0.0.0 to be accessible on the local network
    port = int(os.environ.get('PORT', 5000))
    print(f"[API]: Sarah Bridge running on port {port}")
    app.run(host='0.0.0.0', port=port)
