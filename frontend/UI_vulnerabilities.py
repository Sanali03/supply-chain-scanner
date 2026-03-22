from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class VulnerabilityTable(QWidget):
    def __init__(self, vulnerabilities):
        super().__init__()
        self.setStyleSheet("background-color: #1a1f3a;")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel(" Vulnerabilities")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #e74c3c;")
        layout.addWidget(title)
        
        self.table = QTableWidget(len(vulnerabilities), 3)
        self.table.setHorizontalHeaderLabels(["CVE ID", "Severity", "Package"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2d3561;
                gridline-color: #3d4661;
                border: none;
            }
            QTableWidget::item {
                color: #ecf0f1;
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #e74c3c;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        for row, vul in enumerate(vulnerabilities):
            self.table.setItem(row, 0, QTableWidgetItem(vul["cve"]))
            severity_item = QTableWidgetItem(vul["severity"])
            # Color code severity levels
            if vul["severity"] == "High":
                severity_item.setForeground(Qt.GlobalColor.red)
            elif vul["severity"] == "Medium":
                severity_item.setForeground(Qt.GlobalColor.yellow)
            else:
                severity_item.setForeground(Qt.GlobalColor.green)
            self.table.setItem(row, 1, severity_item)
            self.table.setItem(row, 2, QTableWidgetItem(vul["package"]))

        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)
        self.setLayout(layout)
