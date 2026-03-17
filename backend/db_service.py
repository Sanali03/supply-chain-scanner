from datetime import datetime
from database import get_connection
from osv_service import check_vulnerability
from risk_calculator import calculate_risk


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

        cursor.execute("""
            INSERT INTO dependencies (project_id, name, version, ecosystem)
            VALUES (?, ?, ?, ?)
        """, (
            project_id,
            dep["name"],
            dep["version"],
            dep["ecosystem"]
        ))

        dependency_id = cursor.lastrowid

        vulnerabilities = check_vulnerability(
            dep["name"],
            dep["version"],
            dep["ecosystem"]
        )

        for vuln in vulnerabilities:

            cursor.execute("""
                INSERT INTO vulnerabilities
                (dependency_id, osv_id, cve_id, severity, cvss_score, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                dependency_id,
                vuln["osv_id"],
                vuln["cve_id"],
                vuln["severity"],
                vuln["cvss_score"],
                vuln["summary"]
            ))

            total_vulnerabilities += 1

            if vuln["cvss_score"] and vuln["cvss_score"] > highest_cvss:
                highest_cvss = vuln["cvss_score"]

    risk_score, status = calculate_risk(total_vulnerabilities, highest_cvss)

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

    print("Dependencies and vulnerabilities saved successfully!")
    print(f"Total vulnerabilities: {total_vulnerabilities}")
    print(f"Risk Score: {risk_score} | Status: {status}")