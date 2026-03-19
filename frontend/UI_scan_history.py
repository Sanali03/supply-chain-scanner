from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class ScanHistoryTable(QWidget):
    def __init__(self, history):
        super().__init__()
        layout = QVBoxLayout()
        self.table = QTableWidget(len(history), 4)
        self.table.setHorizontalHeaderLabels(["Date", "SBOM File", "Dependencies", "Vulnerabilities"])

        for row, scan in enumerate(history):
            self.table.setItem(row, 0, QTableWidgetItem(scan["date"]))
            self.table.setItem(row, 1, QTableWidgetItem(scan["file"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(scan["deps"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(scan["vulns"])))

        layout.addWidget(self.table)
        self.setLayout(layout)
