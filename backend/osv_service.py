import requests

OSV_API_URL = "https://api.osv.dev/v1/query"

def check_vulnerability(name, version, ecosystem):
    """
    Query OSV API for a specific dependency
    Returns list of vulnerabilities
    """

    payload = {
        "package": {
            "name": name,
            "ecosystem": ecosystem
        },
        "version": version
    }

    try:
        response = requests.post(OSV_API_URL, json=payload)
        data = response.json()

        if "vulns" not in data:
            return []

        vulnerabilities = []

        for vuln in data["vulns"]:
            vuln_data = {
                "osv_id": vuln.get("id"),
                "summary": vuln.get("summary", ""),
                "severity": extract_severity(vuln)
            }

            vulnerabilities.append(vuln_data)

        return vulnerabilities

    except Exception as e:
        print(f"Error checking OSV: {e}")
        return []


def extract_severity(vuln):
    """
    Extract severity level from OSV response
    """

    if "severity" not in vuln:
        return "UNKNOWN"

    for sev in vuln["severity"]:
        if sev["type"] == "CVSS_V3":
            score = float(sev["score"])
            return map_score_to_level(score)

    return "UNKNOWN"


def map_score_to_level(score):
    if score >= 9:
        return "CRITICAL"
    elif score >= 7:
        return "HIGH"
    elif score >= 4:
        return "MEDIUM"
    elif score > 0:
        return "LOW"
    else:
        return "NONE"