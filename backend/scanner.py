import subprocess
import json
import os
from datetime import datetime

from database import get_connection
from osv_service import check_vulnerability


# Generate SBOM using Syft

def generate_sbom(project_path):
    output_file = "sbom.json"

    syft_path = os.path.join(os.getcwd(), "syft.exe")
    project_full_path = os.path.abspath(project_path)

    command = [
        syft_path,
        project_full_path,
        "-o",
        "json"
    ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )

        if result.returncode != 0:
            print("Syft Error:")
            print(result.stderr)
            return None

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        print("SBOM generated successfully!")
        return output_file

    except Exception as e:
        print("Unexpected error:", e)
        return None


# Parse SBOM JSON

def parse_sbom(sbom_file):
    with open(sbom_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    dependencies = []
    artifacts = data.get("artifacts", [])

    for item in artifacts:
        name = item.get("name")
        version = item.get("version")

        if name and version:
            dependencies.append({
                "name": name,
                "version": version,
                "ecosystem": "PyPI"  # 🔥 For now we assume Python
            })

    print(f"Found {len(dependencies)} dependencies")
    return dependencies


# Save Project + Dependencies

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

    # Insert dependencies + Check OSV
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

        # Check OSV
        vulnerabilities = check_vulnerability(
            dep["name"],
            dep["version"],
            dep["ecosystem"]
        )

        for vuln in vulnerabilities:
            cursor.execute("""
                INSERT INTO vulnerabilities
                (dependency_id, osv_id, severity, description)
                VALUES (?, ?, ?, ?)
            """, (
                dependency_id,
                vuln["osv_id"],
                vuln["severity"],
                vuln["summary"]
            ))

            total_vulnerabilities += 1

    # Calculate risk
    risk_score, status = calculate_risk(total_vulnerabilities)

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

    print("Dependencies and vulnerabilities saved successfully!")
    print(f"Risk Score: {risk_score} | Status: {status}")


# Risk Scoring Logic

def calculate_risk(total_vulnerabilities):

    if total_vulnerabilities == 0:
        return 0.0, "LOW"

    elif total_vulnerabilities <= 3:
        return 5.0, "MEDIUM"

    else:
        return 8.5, "HIGH"


# Main Execution

if __name__ == "__main__":

    project_path = "../venv"   # Change this to target project
    project_name = "Test Project"

    sbom_file = generate_sbom(project_path)

    if sbom_file:
        dependencies = parse_sbom(sbom_file)
        save_project_and_dependencies(project_name, project_path, dependencies)