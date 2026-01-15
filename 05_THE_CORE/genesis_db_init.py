import psycopg2
import os

def get_connection():
    conn_str = os.environ.get("GENESIS_DB_URI")
    if not conn_str:
        raise RuntimeError("GENESIS_DB_URI environment variable not set. Provide the PostgreSQL connection string.")
    return psycopg2.connect(conn_str)

def create_tables():
    schema = [
        '''CREATE TABLE IF NOT EXISTS genesis_users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''',
        '''CREATE TABLE IF NOT EXISTS genesis_memory (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES genesis_users(id),
            text TEXT NOT NULL,
            meta JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''
    ]
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for stmt in schema:
                cur.execute(stmt)
        conn.commit()
        print("[GENESIS CONSTRUCTOR] Tables created successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    create_tables()
