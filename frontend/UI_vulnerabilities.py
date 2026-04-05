from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class VulnerabilityTable(QWidget):
    def __init__(self, vulnerabilities):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Vulnerabilities")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "CVE ID", "Severity", "Package", "Description"
        ])

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.update_data(vulnerabilities)

    def update_data(self, vulnerabilities):
        self.table.setRowCount(0)

        for vuln in vulnerabilities:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(vuln.get("cve", "N/A")))

            severity = vuln.get("severity", "UNKNOWN")
            sev_item = QTableWidgetItem(severity)

            if severity.upper() == "CRITICAL":
                sev_item.setForeground(Qt.GlobalColor.red)
            elif severity.upper() == "HIGH":
                sev_item.setForeground(Qt.GlobalColor.red)
            elif severity.upper() == "MEDIUM":
                sev_item.setForeground(Qt.GlobalColor.yellow)
            elif severity.upper() == "LOW":
                sev_item.setForeground(Qt.GlobalColor.green)

            self.table.setItem(row, 1, sev_item)
            self.table.setItem(row, 2, QTableWidgetItem(vuln.get("package", "")))
            self.table.setItem(row, 3, QTableWidgetItem(vuln.get("description", "")))

        self.table.resizeColumnsToContents()