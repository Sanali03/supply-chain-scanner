import requests

OSV_API_URL = "https://api.osv.dev/v1/query"


def check_vulnerability(name, version, ecosystem):
    """
    Query OSV API for a specific dependency
    Returns a list of vulnerabilities
    """

    payload = {
        "package": {
            "name": name,
            "ecosystem": ecosystem
        },
        "version": version
    }

    try:
        response = requests.post(OSV_API_URL, json=payload, timeout=10)

        if response.status_code != 200:
            print("OSV API request failed")
            return []

        data = response.json()

        if "vulns" not in data:
            return []

        vulnerabilities = []

        for vuln in data["vulns"]:

            osv_id = vuln.get("id")

            summary = vuln.get("summary", "")

            cve_id = extract_cve(vuln)

            cvss_score = extract_cvss_score(vuln)

            if cvss_score is not None:
                severity = map_score_to_level(cvss_score)
            else:
                severity = extract_fallback_severity(vuln)

            print(osv_id, cvss_score, severity)

            vulnerabilities.append({
                "osv_id": osv_id,
                "cve_id": cve_id,
                "summary": summary,
                "severity": severity,
                "cvss_score": cvss_score
            })

        return vulnerabilities

    except Exception as e:
        print(f"Error checking OSV: {e}")
        return []


def extract_cve(vuln):
    """
    Extract CVE ID from OSV aliases
    """

    aliases = vuln.get("aliases", [])

    for alias in aliases:
        if alias.startswith("CVE"):
            return alias

    return None


def extract_cvss_score(vuln):
    """
    Extract highest CVSS score from all available severity entries
    """

    scores = []

    if "severity" in vuln:
        for sev in vuln["severity"]:
            try:
                score = float(sev.get("score"))
                scores.append(score)
            except:
                pass

    return max(scores) if scores else None

def extract_fallback_severity(vuln):
    """
    Try to extract severity when CVSS is missing
    """

    # 1. Try database_specific field
    db = vuln.get("database_specific", {})
    sev = db.get("severity")

    if sev:
        return sev.upper()

    # 2. Try to infer from ID (quick heuristic)
    vuln_id = vuln.get("id", "").lower()

    if "critical" in vuln_id:
        return "CRITICAL"
    if "high" in vuln_id:
        return "HIGH"

    return "LOW"   # fallback default

def map_score_to_level(score):
    """
    Convert CVSS score to severity level
    """

    if score is None:
        return "UNKNOWN"

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
