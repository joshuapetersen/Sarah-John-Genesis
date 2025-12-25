import os
import firebase_admin
from firebase_admin import credentials, firestore, db


def _default_key_path() -> str:
    """
    Resolves the path to serviceAccountKey.json.
    Allows override via the SARAHJOHN_FIREBASE_KEY environment variable.
    """
    override = os.environ.get("SARAHJOHN_FIREBASE_KEY")
    if override:
        return override

    # Workspace root = parent of this 'python' folder
    workspace_root = os.path.dirname(os.path.dirname(__file__))
    
    # Prefer 05_THE_CORE (Genesis Key)
    core_key = os.path.join(workspace_root, "05_THE_CORE", "serviceAccountKey.json")
    if os.path.exists(core_key):
        return core_key
        
    return os.path.join(workspace_root, "04_THE_MEMORY", "serviceAccountKey.json")


def initialize_app_if_needed(key_path: str | None = None) -> None:
    """
    Idempotently initializes the default Firebase app using the given key path.
    Safe to call multiple times.
    """
    try:
        firebase_admin.get_app()
        # Already initialized
        return
    except ValueError:
        pass

    key = key_path or _default_key_path()
    cred = credentials.Certificate(key)
    
    # Default RTDB URL if not provided in environment
    rtdb_url = os.environ.get("SARAHJOHN_FIREBASE_DB_URL", "https://sarah-john-genesis-default-rtdb.firebaseio.com/")
    
    firebase_admin.initialize_app(cred, {
        'databaseURL': rtdb_url
    })


def get_firestore(key_path: str | None = None):
    """Returns a Firestore client, initializing the app if required."""
    initialize_app_if_needed(key_path)
    return firestore.client()


def get_db(key_path: str | None = None):
    """Returns a Realtime Database client, initializing the app if required."""
    initialize_app_if_needed(key_path)
    return db


def health_check() -> bool:
    """
    Tries to create a Firestore client and returns True on success.
    Prints a user-friendly message.
    """
    try:
        _ = get_firestore()
        _ = get_db()
        print("--- Connection Successful ---")
        print("Sarah John is now linked to the cloud memory (Firestore & RTDB).")
        return True
    except Exception as e:
        print("--- Connection Failed ---")
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    # Quick self-test
    health_check()
