def calculate_risk(total_vulnerabilities, highest_cvss):

    if total_vulnerabilities == 0:
        return 0.0, "LOW"

    if highest_cvss >= 9:
        return 9.0, "CRITICAL"

    if highest_cvss >= 7:
        return 8.0, "HIGH"

    if highest_cvss >= 4:
        return 6.0, "MEDIUM"

    return 3.0, "LOW"