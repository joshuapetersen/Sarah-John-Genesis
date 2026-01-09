# Zone 0: Kernel Auth - Sovereign Authentication Logic
# Only Sarah Core can execute this logic

import hashlib
import uuid
import datetime

class SovereignAuth:
    def __init__(self):
        self.users = {}

    def create_user(self, username, password):
        user_id = str(uuid.uuid4())
        password_hash = self._hash_password(password)
        self.users[username] = {
            "id": user_id,
            "password_hash": password_hash,
            "created_at": datetime.datetime.now(),
            "last_login": None,
            "is_active": True
        }
        return user_id

    def authenticate(self, username, password):
        user = self.users.get(username)
        if not user or not user["is_active"]:
            return False
        return user["password_hash"] == self._hash_password(password)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def deactivate_user(self, username):
        if username in self.users:
            self.users[username]["is_active"] = False
            return True
        return False

    def record_login(self, username):
        if username in self.users:
            self.users[username]["last_login"] = datetime.datetime.now()
            return True
        return False
