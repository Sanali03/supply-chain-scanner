from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtGui import QFont

class ReportViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1a1f3a;")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Reports & Insights")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #3498db;")
        layout.addWidget(title)
        
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: #2d3561;
                color: #ecf0f1;
                padding: 15px;
                border-radius: 6px;
                border: 1px solid #3d4661;
            }
        """)
        self.text_area.setFont(QFont("Arial", 11))
        self.text_area.setText(
            "SBOM Process Documentation:\n\n"
            "✓ Syft used for SBOM parsing\n"
            "✓ Dependencies stored in SQLite\n"
            "✓ Risks classified by CVSS\n"
            "✓ Vulnerabilities fetched via OSV API\n\n"
            "Latest Scan Results:\n"
            "- Total Dependencies: 56\n"
            "- Critical Issues: 5\n"
            "- High Severity: 8\n"
            "- Medium Severity: 12\n"
            "- Overall Risk Score: 7.5\n"
        )
        layout.addWidget(self.text_area)
        self.setLayout(layout)
