def calculate_risk(vulnerabilities):
    """
    Calculate overall project risk based on vulnerability severities
    """

    if not vulnerabilities:
        return 0.0, "LOW"

    priority = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    max_level = 0

    for v in vulnerabilities:
        sev = v.get("severity", "LOW")

        # Normalize MODERATE → MEDIUM
        if sev == "MODERATE":
            sev = "MEDIUM"

        if sev in priority:
            level = priority.index(sev)
            max_level = max(max_level, level)

    final_severity = priority[max_level]

    # Optional numeric score mapping
    score_map = {
        "LOW": 3.0,
        "MEDIUM": 6.0,
        "HIGH": 8.0,
        "CRITICAL": 9.5
    }

    return score_map[final_severity], final_severity