from database import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        scan_date TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dependencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        name TEXT,
        version TEXT,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vulnerabilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dependency_id INTEGER,
        osv_id TEXT,
        severity TEXT,
        description TEXT,
        FOREIGN KEY (dependency_id) REFERENCES dependencies (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        risk_score REAL,
        status TEXT,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database and tables created successfully!")

if __name__ == "__main__":
    create_tables()