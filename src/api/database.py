import sqlite3
from config import DB_NAME

def add_record(material_id, formula, data):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    id TEXT PRIMARY KEY,
                    formula TEXT,
                    data TEXT NOT NULL
                )
            """)
            # Check if formula column exists (migration for existing db)
            cursor.execute("PRAGMA table_info(records)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'formula' not in columns:
                cursor.execute("ALTER TABLE records ADD COLUMN formula TEXT")
            
            cursor.execute("INSERT OR REPLACE INTO records (id, formula, data) VALUES (?, ?, ?)", (material_id, formula, data))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def find_by_formula(formula):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, data FROM records WHERE formula = ?", (formula,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def find_record(material_id):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM records WHERE id = ?", (material_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def remove_record(material_id):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM records WHERE id = ?", (material_id,))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

