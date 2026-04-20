from backend.database import get_connection
import sqlite3

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
        policy_status TEXT,
        policy_enforcement_data TEXT,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
    """)

    # Run migrations for existing databases
    try:
        # ---- scan_results migration ----
        cursor.execute("PRAGMA table_info(scan_results)")
        columns = {row[1] for row in cursor.fetchall()}

        if 'policy_status' not in columns:
            cursor.execute("""
                ALTER TABLE scan_results ADD COLUMN policy_status TEXT DEFAULT 'pending-scan'
            """)
            print("✅ Added policy_status column")

        if 'policy_enforcement_data' not in columns:
            cursor.execute("""
                ALTER TABLE scan_results ADD COLUMN policy_enforcement_data TEXT
            """)
            print("✅ Added policy_enforcement_data column")

        # ---- dependencies migration ----
        cursor.execute("PRAGMA table_info(dependencies)")
        dep_columns = {row[1] for row in cursor.fetchall()}

        if 'risk' not in dep_columns:
            cursor.execute("""
                ALTER TABLE dependencies ADD COLUMN risk TEXT DEFAULT 'UNKNOWN'
            """)
            print("✅ Added risk column to dependencies")

    except sqlite3.OperationalError as e:
        print(f"Migration note: {e}")

    conn.commit()
    conn.close()
    print("Database and tables created successfully!")

if __name__ == "__main__":
    create_tables()