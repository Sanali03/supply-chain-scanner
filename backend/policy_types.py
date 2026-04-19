from enum import Enum
from typing import Optional, Any
from dataclasses import dataclass

class ApprovalDecision(str, Enum):
    APPROVED = "approved"
    BLOCKED = "blocked"
    PENDING = "pending"

class PolicyAction(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    REVIEW = "review"

class ComparisonOperator(str, Enum):
    EQUALS = "equals"
    NOT_EQUALS = "notEquals"
    CONTAINS = "contains"
    IN = "in"
    GT = "gt"
    LT = "lt"

@dataclass
class PolicyCondition:
    field: str
    operator: ComparisonOperator
    value: Any

@dataclass
class PolicyRule:
    id: str
    name: str
    description: str
    critical: bool
    action: PolicyAction
    condition: Optional[PolicyCondition] = None

@dataclass
class PolicyConfig:
    rules: list[PolicyRule]

@dataclass
class PolicyEvaluation:
    status: ApprovalDecision
    matched_rule: Optional[PolicyRule] = None
    message: str = ""