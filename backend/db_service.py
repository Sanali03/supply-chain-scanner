from datetime import datetime
from backend.database import get_connection
from backend.osv_service import check_vulnerability
from backend.risk_calculator import calculate_risk


# ==============================
# SAVE SCAN DATA
# ==============================

def save_project_and_dependencies(project_name, project_path, dependencies):

    conn = get_connection()
    cursor = conn.cursor()

    scan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert project
    cursor.execute("""
        INSERT INTO projects (name, project_path, scan_date)
        VALUES (?, ?, ?)
    """, (project_name, project_path, scan_date))

    project_id = cursor.lastrowid

    total_vulnerabilities = 0
    highest_cvss = 0

    for dep in dependencies:

        # Insert dependency
        cursor.execute("""
            INSERT INTO dependencies (project_id, name, version, ecosystem)
            VALUES (?, ?, ?, ?)
        """, (
            project_id,
            dep.get("name"),
            dep.get("version"),
            dep.get("ecosystem")
        ))

        dependency_id = cursor.lastrowid

        # Fetch vulnerabilities
        vulnerabilities = check_vulnerability(
            dep.get("name"),
            dep.get("version"),
            dep.get("ecosystem")
        )

        for vuln in vulnerabilities:

            cursor.execute("""
                INSERT INTO vulnerabilities
                (dependency_id, osv_id, cve_id, severity, cvss_score, description, published_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                dependency_id,
                vuln.get("osv_id"),
                vuln.get("cve_id"),
                vuln.get("severity"),
                vuln.get("cvss_score"),
                vuln.get("summary"),
                None
            ))

            total_vulnerabilities += 1

            if vuln.get("cvss_score") and vuln["cvss_score"] > highest_cvss:
                highest_cvss = vuln["cvss_score"]

    # Calculate risk
    risk_score, status = calculate_risk(total_vulnerabilities, highest_cvss)

    # Insert scan result
    cursor.execute("""
        INSERT INTO scan_results
        (project_id, total_dependencies, total_vulnerabilities, risk_score, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        project_id,
        len(dependencies),
        total_vulnerabilities,
        risk_score,
        status
    ))

    conn.commit()
    conn.close()

    print("Scan saved successfully!")
    print(f"Project ID: {project_id}")
    print(f"Dependencies: {len(dependencies)}")
    print(f"Vulnerabilities: {total_vulnerabilities}")
    print(f"Risk Score: {risk_score} | Status: {status}")


# ==============================
# FETCH DEPENDENCIES (FILTERED)
# ==============================

def get_dependencies(project_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            d.id,
            d.name,
            d.version,
            d.ecosystem,
            sr.status
        FROM dependencies d
        JOIN scan_results sr ON d.project_id = sr.project_id
    """

    params = ()

    if project_id:
        query += " WHERE d.project_id = ?"
        params = (project_id,)

    query += " ORDER BY d.id DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "name": row["name"],
            "version": row["version"],
            "ecosystem": row["ecosystem"],
            "risk": row["status"] or "UNKNOWN"
        }
        for row in rows
    ]


# ==============================
# FETCH VULNERABILITIES (FILTERED)
# ==============================

def get_vulnerabilities(project_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            v.id,
            v.cve_id,
            v.severity,
            v.cvss_score,
            v.description,
            d.name AS package
        FROM vulnerabilities v
        JOIN dependencies d ON v.dependency_id = d.id
    """

    params = ()

    if project_id:
        query += " WHERE d.project_id = ?"
        params = (project_id,)

    query += " ORDER BY v.id DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "cve": row["cve_id"] or "N/A",
            "severity": row["severity"] or "UNKNOWN",
            "cvss": row["cvss_score"],
            "package": row["package"],
            "description": row["description"] or ""
        }
        for row in rows
    ]


# ==============================
# FETCH SCAN HISTORY
# ==============================

def get_scan_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.id AS project_id,
            p.scan_date,
            p.name,
            sr.total_dependencies,
            sr.total_vulnerabilities,
            sr.risk_score,
            sr.status
        FROM projects p
        JOIN scan_results sr ON p.id = sr.project_id
        ORDER BY p.id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row["project_id"],
            "date": row["scan_date"],
            "project": row["name"],
            "deps": row["total_dependencies"],
            "vulns": row["total_vulnerabilities"],
            "risk_score": row["risk_score"],
            "status": row["status"]
        }
        for row in rows
    ]


# ==============================
# CLEAR DATABASE
# ==============================

def clear_all_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM vulnerabilities")
    cursor.execute("DELETE FROM dependencies")
    cursor.execute("DELETE FROM scan_results")
    cursor.execute("DELETE FROM projects")

    conn.commit()
    conn.close()

    print("All data cleared!")