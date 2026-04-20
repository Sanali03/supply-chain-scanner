from backend.policy_types import (
    PolicyRule, PolicyConfig, PolicyCondition,
    PolicyAction, ComparisonOperator
)
from typing import Dict


def get_default_policy_config() -> PolicyConfig:
    """Return default supply chain security policy."""
    
    rules = [

        # ================= CRITICAL RULE =================
        PolicyRule(
            id="critical_vuln_block",
            name="Block Critical Vulnerabilities",
            description="Automatically block projects containing any critical vulnerabilities",
            critical=True,
            action=PolicyAction.REJECT,
            condition=PolicyCondition(
                field="critical_count",
                operator=ComparisonOperator.GT,
                value=0
            )
        ),

        # ================= HIGH RULE (FIXED) =================
        PolicyRule(
            id="high_vuln_review",
            name="Review High Vulnerabilities",
            description="Require manual review if any high severity vulnerabilities are present",
            critical=False,
            action=PolicyAction.REVIEW,
            condition=PolicyCondition(
                field="high_count",
                operator=ComparisonOperator.GT,
                value=0   # 🔥 FIXED (was 2)
            )
        ),

        # ================= MEDIUM RULE (NEW - OPTIONAL BUT RECOMMENDED) =================
        PolicyRule(
            id="medium_vuln_review",
            name="Review Excessive Medium Vulnerabilities",
            description="Require review if too many medium severity vulnerabilities exist",
            critical=False,
            action=PolicyAction.REVIEW,
            condition=PolicyCondition(
                field="medium_count",
                operator=ComparisonOperator.GT,
                value=5   # threshold (you can tune this)
            )
        ),

        # ================= OUTDATED DEPENDENCIES =================
        PolicyRule(
            id="outdated_deps",
            name="Outdated Dependencies",
            description="Flag projects with a high number of outdated dependencies",
            critical=False,
            action=PolicyAction.REVIEW,
            condition=PolicyCondition(
                field="outdated_count",
                operator=ComparisonOperator.GT,
                value=5
            )
        ),
    ]

    return PolicyConfig(rules=rules)


def get_policy_summary() -> Dict:
    """Get human-readable policy summary."""
    
    config = get_default_policy_config()

    summary = {
        "total_rules": len(config.rules),
        "critical_rules": sum(1 for r in config.rules if r.critical),
        "rules": []
    }

    for rule in config.rules:
        summary["rules"].append({
            "id": rule.id,
            "name": rule.name,
            "description": rule.description,
            "critical": rule.critical,
            "action": rule.action.value
        })

    return summary