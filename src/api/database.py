import sqlite3
from config import DB_NAME

def add_record(material_id, formula, data):
    """
    Adds a new record to the database or updates an existing one.
    
    **Arguments**
        *material_id* (str)
            - The unique identifier for the material.
        *formula* (str)
            - The chemical formula of the material.
        *data* (str)
            - The JSON string representation of the material data.
    """
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
    """
    Retrieves all records matching a specific chemical formula.
    
    **Arguments**
        *formula* (str)
            - The chemical formula to search for.
            
    **Returns**
        *list*
            - A list of tuples containing (id, data) for matching records.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, data FROM records WHERE formula = ?", (formula,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def find_record(material_id):
    """
    Retrieves a specific record by its material ID.
    
    **Arguments**
        *material_id* (str)
            - The unique identifier of the material to retrieve.
            
    **Returns**
        *str* or *None*
            - The JSON data string if found, otherwise None.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM records WHERE id = ?", (material_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def remove_record(material_id):
    """
    Removes a record from the database by its material ID.
    
    **Arguments**
        *material_id* (str)
            - The unique identifier of the material to remove.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM records WHERE id = ?", (material_id,))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def add_dos_record(material_id, dos_data):
    """
    Adds a new DOS record to the database.
    
    **Arguments**
        *material_id* (str)
            - The unique identifier for the material.
        *dos_data* (str)
            - The JSON string representation of the DOS data.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dos_records (
                    id TEXT PRIMARY KEY,
                    data TEXT NOT NULL
                )
            """)
            
            # Only insert if it doesn't exist (IGNORE)
            cursor.execute("INSERT OR IGNORE INTO dos_records (id, data) VALUES (?, ?)", (material_id, dos_data))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def find_dos_record(material_id):
    """
    Retrieves a specific DOS record by its material ID.
    
    **Arguments**
        *material_id* (str)
            - The unique identifier of the material to retrieve.
            
    **Returns**
        *str* or *None*
            - The JSON data string if found, otherwise None.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM dos_records WHERE id = ?", (material_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")


