from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class PolicyStatusBadge(QWidget):
    """Display policy enforcement status badge."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.status_label = QLabel("Pending Scan")
        self.status_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.status_label)
        self.setMaximumWidth(150)
        self.set_status("pending-scan")
    
    def set_status(self, status: str):
        """Update badge based on policy status."""
        status_map = {
            "approved": ("✅ Approved", "#28a745", "white"),
            "pending-review": ("⚠️ Review", "#ffc107", "black"),
            "blocked": ("🚫 Blocked", "#dc3545", "white"),
            "pending-scan": ("⏳ Pending", "#6c757d", "white"),
        }
        
        label_text, bg_color, text_color = status_map.get(
            status, status_map["pending-scan"]
        )
        
        self.status_label.setText(label_text)
        self.status_label.setStyleSheet(
            f"""
            background-color: {bg_color};
            color: {text_color};
            padding: 8px 12px;
            border-radius: 5px;
            font-weight: bold;
            """
        )

class PolicyDetailsWidget(QWidget):
    """Display detailed policy enforcement information."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Policy Enforcement")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        self.status_badge = PolicyStatusBadge()
        layout.addWidget(self.status_badge)
        
        self.reason_label = QLabel("")
        self.reason_label.setWordWrap(True)
        self.reason_label.setStyleSheet("color: #555; font-size: 10px; padding: 5px;")
        layout.addWidget(self.reason_label)
        
        layout.addStretch()
    
    def update_policy_info(self, policy_enforcement: dict):
        """Update widget with policy enforcement data."""
        status = policy_enforcement.get("status", "pending-scan")
        reason = policy_enforcement.get("reason", "")
        
        self.status_badge.set_status(status)
        self.reason_label.setText(reason) 
        