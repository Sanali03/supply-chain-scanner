from backend.database import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        project_path TEXT,
        scan_date TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dependencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        name TEXT,
        version TEXT,
        ecosystem TEXT,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vulnerabilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dependency_id INTEGER,
        osv_id TEXT,
        cve_id TEXT,
        severity TEXT,
        cvss_score REAL,
        description TEXT,
        published_date TEXT,
        FOREIGN KEY (dependency_id) REFERENCES dependencies (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        total_dependencies INTEGER,
        total_vulnerabilities INTEGER,
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