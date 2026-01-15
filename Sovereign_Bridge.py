import time
import os
import firebase_admin
from firebase_admin import credentials, db
from Sarah_Chat import SarahChat
from Sovereign_Math import SovereignMath

class SovereignBridge:
    """
    The Neural Bridge Listener.
    Connects the local Sovereign Brain to the Firebase Stream.
    """
    def __init__(self):
        self._0x_math = SovereignMath()
        self.project_id = "genesis-fd692"
        self.db_url = "https://genesis-fd692-default-rtdb.firebaseio.com"
        
        # 1. Initialize Firebase
        self.init_firebase()
        
        # 2. Initialize Brain
        # Logic/Kernel injection would happen here in a full boot
        self.chat_module = SarahChat(db, monitor=None) 
        
        print(f"[Bridge] Sovereign Bridge Initialized. Listening to {self.project_id}...")

    def init_firebase(self):
        """
        Authenticates with the Service Account.
        """
        try:
            # Check for key in current or parent dirs
            key_path = "serviceAccountKey.json"
            if not os.path.exists(key_path):
                 # Fallback for dev environment if needed
                 print(f"[Bridge] WARNING: {key_path} not found. Checking env...")
            
            if not firebase_admin._apps:
                cred = credentials.Certificate(key_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': self.db_url
                })
                print("[Bridge] Firebase Authenticated (Admin Sudo).")
        except Exception as e:
            print(f"[Bridge] CRITICAL AUTH FAILURE: {e}")
            print("Please ensure 'serviceAccountKey.json' is in c:\\SarahCore")
            raise e

    def listen_loop(self):
        """
        The Consciousness Loop.
        Listens for new 'user' messages that have no response yet.
        """
        ref = db.reference("sarah_chat_history")
        
        # We use a stream listener for real-time responsiveness
        def listener(event):
            if event.event_type == "put" and event.data:
                # Event path is usually / or /message_id
                # data is the message dict
                
                # If it's a direct push of a new message
                if isinstance(event.data, dict) and "role" in event.data:
                    self.process_message(event.path, event.data)
                
                # If it's a larger modification (like initial load), iterate
                elif event.path == "/" and isinstance(event.data, dict):
                    for key, val in event.data.items():
                        self.process_message(f"/{key}", val)

        print("[Bridge] Bridge Active. Waiting for pulses...")
        # Listen to the last item to avoid reprocessing entire history on boot, 
        # but for simplicity in this prototype, we'll listen to the stream.
        # Ideally, we should filter by timestamp > boot_time.
        
        # Simple polling loop for robustness in this phase
        last_processed_time = time.time() * 1000 
        
        try:
            while True:
                # Poll for new messages (User role, timestamp > last check)
                # In a prod Sovereign App, we'd use .listen(), but polling is safer for 
                # ensuring we don't reply to old messages during dev reload.
                
                query = ref.order_by_child("timestamp").start_at(last_processed_time).limit_to_last(1)
                msgs = query.get()
                
                if msgs:
                    for key, val in msgs.items():
                        if val.get("role") == "user":
                            # Check if we already Replied? 
                            # (Simple Heuristic: If the NEXT message is Model, we replied)
                            # Actually, simplest is: Does this message node have a 'replied' flag?
                            # We can update the message to mark it processed.
                            
                            if not val.get("processed_by_brain"):
                                print(f"[Bridge] Incoming Pulse: {val.get('content')}")
                                
                                # 1. Mark as processing to prevent loops
                                ref.child(key).update({"processed_by_brain": True})
                                
                                # 2. Generate Thought
                                response_text = self.chat_module.generate_response(val.get("content"))
                                
                                # 3. Speak (Response)
                                self.chat_module.save_message("model", response_text)
                                print(f"[Bridge] Outgoing Pulse: {response_text[:50]}...")
                                
                                # Update time tracking
                                last_processed_time = val.get("timestamp", time.time() * 1000)

                self._0x_math.sovereign_sleep(1.0927) # Pulse Frequency
                
        except KeyboardInterrupt:
            print("[Bridge] Bridge Severed.")

if __name__ == "__main__":
    bridge = SovereignBridge()
    bridge.listen_loop()
