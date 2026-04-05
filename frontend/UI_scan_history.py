from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem


class ScanHistoryTable(QWidget):
    def __init__(self, history):
        super().__init__()

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Date", "Project", "Dependencies", "Vulnerabilities"
        ])

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.update_data(history)

    def update_data(self, history):
        self.table.setRowCount(0)

        for scan in history:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(scan.get("date", "")))
            self.table.setItem(row, 1, QTableWidgetItem(scan.get("project", "")))
            self.table.setItem(row, 2, QTableWidgetItem(str(scan.get("deps", 0))))
            self.table.setItem(row, 3, QTableWidgetItem(str(scan.get("vulns", 0))))