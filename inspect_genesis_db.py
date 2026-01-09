import sqlite3

def inspect_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Tables: {tables}")
        
        for table in tables:
            print(f"\n--- Schema for table: {table} ---")
            cursor.execute(f"PRAGMA table_info({table})")
            schema = cursor.fetchall()
            for col in schema:
                print(f"Column ID: {col[0]}, Name: {col[1]}, Type: {col[2]}, NotNull: {col[3]}, Default: {col[4]}, PK: {col[5]}")
            
            if 'memory' in table.lower() or 'history' in table.lower():
                print(f"\nFirst 5 rows of '{table}':")
                cursor.execute(f"SELECT * FROM {table} LIMIT 5")
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                    
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_db('c:/SarahCore/genesis_core.db')
