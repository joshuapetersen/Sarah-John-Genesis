from supabase import create_client, Client
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials not set. Set SUPABASE_URL and SUPABASE_KEY as environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def verify_user(email, password):
    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if not response or not response.get('user'):
        raise PermissionError("Authentication failed.")
    return response['user']

# Example: store and fetch memory

def store_memory(user_id, text, meta=None):
    data = {"user_id": user_id, "text": text, "meta": meta or {}}
    result = supabase.table("genesis_memory").insert(data).execute()
    return result

def fetch_memory(user_id, limit=10):
    result = supabase.table("genesis_memory").select("*").eq("user_id", user_id).limit(limit).execute()
    return result.data
