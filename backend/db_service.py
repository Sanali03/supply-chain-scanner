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

        # Get vulnerabilities from OSV
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
                None  # (Optional: you can extract published_date later)
            ))

            total_vulnerabilities += 1

            # Track highest CVSS
            if vuln.get("cvss_score") and vuln["cvss_score"] > highest_cvss:
                highest_cvss = vuln["cvss_score"]

    # Calculate overall risk
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
    print(f"Dependencies: {len(dependencies)}")
    print(f"Vulnerabilities: {total_vulnerabilities}")
    print(f"Risk Score: {risk_score} | Status: {status}")


# ==============================
# FETCH DATA FOR DASHBOARD
# ==============================

def get_dependencies():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, version, ecosystem
        FROM dependencies
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    dependencies = []

    for row in rows:
        dependencies.append({
            "name": row["name"],
            "version": row["version"],
            "ecosystem": row["ecosystem"],
            "risk": "N/A"  # Optional: enhance later
        })

    return dependencies


def get_vulnerabilities():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            v.cve_id,
            v.severity,
            v.cvss_score,
            d.name AS package
        FROM vulnerabilities v
        JOIN dependencies d ON v.dependency_id = d.id
        ORDER BY v.id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    vulnerabilities = []

    for row in rows:
        vulnerabilities.append({
            "cve": row["cve_id"] if row["cve_id"] else "N/A",
            "severity": row["severity"],
            "cvss": row["cvss_score"],
            "package": row["package"]
        })

    return vulnerabilities


def get_scan_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.scan_date AS date,
            p.name AS project,
            sr.total_dependencies AS deps,
            sr.total_vulnerabilities AS vulns,
            sr.risk_score,
            sr.status
        FROM projects p
        JOIN scan_results sr ON p.id = sr.project_id
        ORDER BY p.id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    history = []

    for row in rows:
        history.append({
            "date": row["date"],
            "project": row["project"],
            "deps": row["deps"],
            "vulns": row["vulns"],
            "risk_score": row["risk_score"],
            "status": row["status"]
        })

    return history


# ==============================
# OPTIONAL: CLEAR DATABASE
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