from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class VulnerabilityTable(QWidget):
    def __init__(self, vulnerabilities):
        super().__init__()
        layout = QVBoxLayout()
        self.table = QTableWidget(len(vulnerabilities), 3)
        self.table.setHorizontalHeaderLabels(["CVE ID", "Severity", "Package"])

        for row, vul in enumerate(vulnerabilities):
            self.table.setItem(row, 0, QTableWidgetItem(vul["cve"]))
            self.table.setItem(row, 1, QTableWidgetItem(vul["severity"]))
            self.table.setItem(row, 2, QTableWidgetItem(vul["package"]))

        layout.addWidget(self.table)
        self.setLayout(layout)
