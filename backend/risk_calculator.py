def calculate_risk(vulnerabilities):
    """
    Calculate overall project risk based on vulnerability severities

    Improvements:
    - Uses weighted scoring instead of max-only
    - Considers all vulnerabilities
    - Applies CRITICAL override
    - Normalizes score to 0–10 scale
    """

    if not vulnerabilities:
        return 0.0, "LOW"

    # Weight system (tuned for realistic impact)
    weights = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 4,
        "CRITICAL": 6
    }

    total_score = 0
    count = 0

    has_critical = False
    has_high = False

    for v in vulnerabilities:
        sev = v.get("severity", "LOW")

        # Normalize values
        if sev == "MODERATE":
            sev = "MEDIUM"

        sev = sev.upper()

        # Track high/critical presence
        if sev == "CRITICAL":
            has_critical = True
        elif sev == "HIGH":
            has_high = True

        weight = weights.get(sev, 1)

        total_score += weight
        count += 1

    # Average severity score
    avg_score = total_score / max(count, 1)

    # Normalize to 0–10 scale
    max_weight = max(weights.values())
    normalized_score = (avg_score / max_weight) * 10

    # ----------------------------
    # Severity Classification Logic
    # ----------------------------

    # 🔥 Hard override rules (important for realism)
    if has_critical:
        status = "CRITICAL"
        normalized_score = max(normalized_score, 9.0)

    elif has_high:
        if normalized_score < 6:
            normalized_score = 6.5
        status = "HIGH"

    else:
        if normalized_score >= 6:
            status = "HIGH"
        elif normalized_score >= 3:
            status = "MEDIUM"
        else:
            status = "LOW"

    return round(normalized_score, 2), status