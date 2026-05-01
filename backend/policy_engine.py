from backend.policy_types import (
    PolicyCondition, PolicyConfig, PolicyEvaluation,
    ApprovalDecision, ComparisonOperator, PolicyAction  
)
from typing import Any, Dict

def matches_condition(application: Dict[str, Any], condition: PolicyCondition) -> bool:
    """Check if application data matches a policy condition."""
    if condition is None:
        return True
    
    value = application.get(condition.field)
    
    if condition.operator == ComparisonOperator.EQUALS:
        return value == condition.value
    elif condition.operator == ComparisonOperator.NOT_EQUALS:
        return value != condition.value
    elif condition.operator == ComparisonOperator.CONTAINS:
        if isinstance(value, list):
            return condition.value in value
        return str(condition.value) in str(value)
    elif condition.operator == ComparisonOperator.IN:
        if isinstance(condition.value, list):
            return value in condition.value
        return False
    elif condition.operator == ComparisonOperator.GT:
        return isinstance(value, (int, float)) and value > condition.value
    elif condition.operator == ComparisonOperator.LT:
        return isinstance(value, (int, float)) and value < condition.value
    elif condition.operator == ComparisonOperator.GTE:
        return isinstance(value, (int, float)) and value >= condition.value
    elif condition.operator == ComparisonOperator.LTE:
        return isinstance(value, (int, float)) and value <= condition.value
    
    return False

def evaluate_policy(application: Dict[str, Any], config: PolicyConfig) -> PolicyEvaluation:
    """Evaluate application against ALL policy rules with priority."""

    matched_rules = []

    for rule in config.rules:
        if rule.condition is None or matches_condition(application, rule.condition):
            matched_rules.append(rule)

    # No rules matched
    if not matched_rules:
        return PolicyEvaluation(
            status=ApprovalDecision.APPROVED,
            message="No policy rules matched. Application approved by default."
        )

    # PRIORITY LOGIC

    # 1. Critical REJECT → BLOCKED
    for rule in matched_rules:
        if rule.critical and rule.action == PolicyAction.REJECT:
            return PolicyEvaluation(
                status=ApprovalDecision.BLOCKED,
                matched_rule=rule,
                message=f'Blocked by critical policy rule "{rule.name}".'
            )

    # 2. Any REVIEW → PENDING
    for rule in matched_rules:
        if rule.action == PolicyAction.REVIEW:
            return PolicyEvaluation(
                status=ApprovalDecision.PENDING,
                matched_rule=rule,
                message=f'Requires review due to policy rule "{rule.name}".'
            )

    # 3. Otherwise → APPROVED
    return PolicyEvaluation(
        status=ApprovalDecision.APPROVED,
        matched_rule=matched_rules[0],
        message=f'Approved by policy rules.'
    )

def apply_policy_to_scan(scan_data: Dict[str, Any], config: PolicyConfig) -> Dict[str, Any]:
    """Apply policy enforcement to scan results."""
    evaluation = evaluate_policy(scan_data, config)
    
    scan_data['policy_status'] = (
        'blocked' if evaluation.status == ApprovalDecision.BLOCKED
        else 'pending-review' if evaluation.status == ApprovalDecision.PENDING
        else 'approved'
    )
    
    scan_data['policy_enforcement'] = {
        'status': evaluation.status.value,
        'reason': evaluation.message,
        'rule_id': evaluation.matched_rule.id if evaluation.matched_rule else None
    }
    
    return scan_data 