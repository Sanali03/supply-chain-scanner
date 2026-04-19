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
    
    return False

def evaluate_policy(application: Dict[str, Any], config: PolicyConfig) -> PolicyEvaluation:
    """Evaluate application against policy rules."""
    
    matched_rule = None
    for rule in config.rules:
        if rule.condition is None or matches_condition(application, rule.condition):
            matched_rule = rule
            break
    
    if matched_rule is None:
        return PolicyEvaluation(
            status=ApprovalDecision.APPROVED,
            message="No policy rules matched. Application approved by default."
        )
    
    if matched_rule.critical and matched_rule.action == PolicyAction.REJECT:
        return PolicyEvaluation(
            status=ApprovalDecision.BLOCKED,
            matched_rule=matched_rule,
            message=f'Blocked by critical policy rule "{matched_rule.name}".'
        )
    
    if matched_rule.action == PolicyAction.REVIEW:
        return PolicyEvaluation(
            status=ApprovalDecision.PENDING,
            matched_rule=matched_rule,
            message=f'Requires conditional approval due to policy rule "{matched_rule.name}".'
        )
    
    return PolicyEvaluation(
        status=ApprovalDecision.APPROVED,
        matched_rule=matched_rule,
        message=f'Approved by policy rule "{matched_rule.name}".'
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