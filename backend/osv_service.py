import requests
from packaging import version as pkg_version

OSV_API_URL = "https://api.osv.dev/v1/query"


def check_vulnerability(name, version, ecosystem):
    """
    Query OSV API and return clean, deduplicated, version-filtered vulnerabilities
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

        unique_vulns = {}

        for vuln in data["vulns"]:

            # =========================
            # Extract identifiers
            # =========================
            osv_id = vuln.get("id")
            cve_id = extract_cve(vuln) or osv_id

            # =========================
            # VERSION FILTERING (SAFE)
            # =========================
            if not is_version_affected_safe(vuln, version):
                continue

            # =========================
            # CVSS extraction
            # =========================
            cvss_score = extract_cvss_score(vuln)

            if cvss_score is not None:
                severity = map_score_to_level(cvss_score)
            else:
                severity = extract_fallback_severity(vuln)

            summary = vuln.get("summary", "")

            # =========================
            # DEDUPLICATION (KEEP HIGHEST CVSS)
            # =========================
            if cve_id not in unique_vulns:
                unique_vulns[cve_id] = {
                    "osv_id": osv_id,
                    "cve_id": cve_id,
                    "summary": summary,
                    "severity": severity,
                    "cvss_score": cvss_score or 0
                }
            else:
                existing = unique_vulns[cve_id]

                if (cvss_score or 0) > (existing.get("cvss_score") or 0):
                    unique_vulns[cve_id] = {
                        "osv_id": osv_id,
                        "cve_id": cve_id,
                        "summary": summary,
                        "severity": severity,
                        "cvss_score": cvss_score or 0
                    }

        return list(unique_vulns.values())

    except Exception as e:
        print(f"Error checking OSV: {e}")
        return []


# ============================================
# HELPER FUNCTIONS
# ============================================

def extract_cve(vuln):
    for alias in vuln.get("aliases", []):
        if alias.startswith("CVE"):
            return alias
    return None


def extract_cvss_score(vuln):
    scores = []

    for sev in vuln.get("severity", []):
        try:
            score = float(sev.get("score"))
            scores.append(score)
        except:
            continue

    return max(scores) if scores else None


def extract_fallback_severity(vuln):
    """
    Fallback severity when CVSS is missing
    """

    db = vuln.get("database_specific", {})
    sev = db.get("severity")

    if sev:
        return sev.upper()

    return "MEDIUM"   # safer default


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


# ============================================
# SAFE VERSION FILTERING
# ============================================

def is_version_affected_safe(vuln, current_version):
    """
    Wrapper to prevent over-filtering
    """
    try:
        return is_version_affected(vuln, current_version)
    except:
        return True  # don't hide vulnerabilities on error


def is_version_affected(vuln, current_version):
    try:
        current = pkg_version.parse(current_version)
    except:
        return True

    for affected in vuln.get("affected", []):

        # Direct match
        if "versions" in affected:
            if current_version in affected["versions"]:
                return True

        # Range-based
        for r in affected.get("ranges", []):
            if r.get("type") != "ECOSYSTEM":
                continue

            if check_version_in_range(current, r.get("events", [])):
                return True

    return False


def check_version_in_range(current, events):
    introduced = None
    fixed = None

    for event in events:
        if "introduced" in event:
            introduced = event["introduced"]
        if "fixed" in event:
            fixed = event["fixed"]

    try:
        if introduced:
            if current < pkg_version.parse(introduced):
                return False

        if fixed:
            if current >= pkg_version.parse(fixed):
                return False

        return True

    except:
        return True
